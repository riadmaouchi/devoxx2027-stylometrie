# Corpus « temoin » — sous-paquet routing de pallets/werkzeug, lignes non vides.
# Licence BSD-3-Clause. Trois sous-paquets du MEME projet : si l ecart de la
# condition B venait de « fichiers entiers contre lignes concatenees », C monterait aussi.
"""When it comes to combining multiple controller or view functions
(however you want to call them) you need a dispatcher. A simple way
would be applying regular expression tests on the ``PATH_INFO`` and
calling registered callback functions that return the value then.
This module implements a much more powerful system than simple regular
expression matching because it can also convert values in the URLs and
build URLs.
Here a simple example that creates a URL map for an application with
two subdomains (www and kb) and some URL rules:
.. code-block:: python
    m = Map([
        # Static URLs
        Rule('/', endpoint='static/index'),
        Rule('/about', endpoint='static/about'),
        Rule('/help', endpoint='static/help'),
        # Knowledge Base
        Subdomain('kb', [
            Rule('/', endpoint='kb/index'),
            Rule('/browse/', endpoint='kb/browse'),
            Rule('/browse/<int:id>/', endpoint='kb/browse'),
            Rule('/browse/<int:id>/<int:page>', endpoint='kb/browse')
        ])
    ], default_subdomain='www')
If the application doesn't use subdomains it's perfectly fine to not set
the default subdomain and not use the `Subdomain` rule factory. The
endpoint in the rules can be anything, for example import paths or
unique identifiers. The WSGI application can use those endpoints to get the
handler for that URL.  It doesn't have to be a string at all but it's
recommended.
Now it's possible to create a URL adapter for one of the subdomains and
build URLs:
.. code-block:: python
    c = m.bind('example.com')
    c.build("kb/browse", dict(id=42))
    'http://kb.example.com/browse/42/'
    c.build("kb/browse", dict())
    'http://kb.example.com/browse/'
    c.build("kb/browse", dict(id=42, page=3))
    'http://kb.example.com/browse/42/3'
    c.build("static/about")
    '/about'
    c.build("static/index", force_external=True)
    'http://www.example.com/'
    c = m.bind('example.com', subdomain='kb')
    c.build("static/about")
    'http://www.example.com/about'
The first argument to bind is the server name *without* the subdomain.
Per default it will assume that the script is mounted on the root, but
often that's not the case so you can provide the real mount point as
second argument:
.. code-block:: python
    c = m.bind('example.com', '/applications/example')
The third argument can be the subdomain, if not given the default
subdomain is used.  For more details about binding have a look at the
documentation of the `MapAdapter`.
And here is how you can match URLs:
.. code-block:: python
    c = m.bind('example.com')
    c.match("/")
    ('static/index', {})
    c.match("/about")
    ('static/about', {})
    c = m.bind('example.com', '/', 'kb')
    c.match("/")
    ('kb/index', {})
    c.match("/browse/42/23")
    ('kb/browse', {'id': 42, 'page': 23})
If matching fails you get a ``NotFound`` exception, if the rule thinks
it's a good idea to redirect (for example because the URL was defined
to have a slash at the end but the request was missing that slash) it
will raise a ``RequestRedirect`` exception. Both are subclasses of
``HTTPException`` so you can use those errors as responses in the
application.
If matching succeeded but the URL rule was incompatible to the given
method (for example there were only rules for ``GET`` and ``HEAD`` but
routing tried to match a ``POST`` request) a ``MethodNotAllowed``
exception is raised.
"""
from .converters import AnyConverter as AnyConverter
from .converters import BaseConverter as BaseConverter
from .converters import FloatConverter as FloatConverter
from .converters import IntegerConverter as IntegerConverter
from .converters import PathConverter as PathConverter
from .converters import UnicodeConverter as UnicodeConverter
from .converters import UUIDConverter as UUIDConverter
from .converters import ValidationError as ValidationError
from .exceptions import BuildError as BuildError
from .exceptions import NoMatch as NoMatch
from .exceptions import RequestAliasRedirect as RequestAliasRedirect
from .exceptions import RequestPath as RequestPath
from .exceptions import RequestRedirect as RequestRedirect
from .exceptions import RoutingException as RoutingException
from .exceptions import WebsocketMismatch as WebsocketMismatch
from .map import Map as Map
from .map import MapAdapter as MapAdapter
from .matcher import StateMachineMatcher as StateMachineMatcher
from .rules import EndpointPrefix as EndpointPrefix
from .rules import parse_converter_args as parse_converter_args
from .rules import Rule as Rule
from .rules import RuleFactory as RuleFactory
from .rules import RuleTemplate as RuleTemplate
from .rules import RuleTemplateFactory as RuleTemplateFactory
from .rules import Subdomain as Subdomain
from .rules import Submount as Submount
from __future__ import annotations
import re
import typing as t
import uuid
from urllib.parse import quote
if t.TYPE_CHECKING:
    from .map import Map
class ValidationError(ValueError):
    """Validation error.  If a rule converter raises this exception the rule
    does not match the current URL and the next URL is tried.
    """
class BaseConverter:
    """Base class for all converters.
    .. versionchanged:: 2.3
        ``part_isolating`` defaults to ``False`` if ``regex`` contains a ``/``.
    """
    regex = "[^/]+"
    weight = 100
    part_isolating = True
    def __init_subclass__(cls, **kwargs: t.Any) -> None:
        super().__init_subclass__(**kwargs)
        # If the converter isn't inheriting its regex, disable part_isolating by default
        # if the regex contains a / character.
        if "regex" in cls.__dict__ and "part_isolating" not in cls.__dict__:
            cls.part_isolating = "/" not in cls.regex
    def __init__(self, map: Map, *args: t.Any, **kwargs: t.Any) -> None:
        self.map = map
    def to_python(self, value: str) -> t.Any:
        return value
    def to_url(self, value: t.Any) -> str:
        # safe = https://url.spec.whatwg.org/#url-path-segment-string
        return quote(str(value), safe="!$&'()*+,/:;=@")
class UnicodeConverter(BaseConverter):
    """This converter is the default converter and accepts any string but
    only one path segment.  Thus the string can not include a slash.
    This is the default validator.
    Example::
        Rule('/pages/<page>'),
        Rule('/<string(length=2):lang_code>')
    :param map: the :class:`Map`.
    :param minlength: the minimum length of the string.  Must be greater
                      or equal 1.
    :param maxlength: the maximum length of the string.
    :param length: the exact length of the string.
    """
    def __init__(
        self,
        map: Map,
        minlength: int = 1,
        maxlength: int | None = None,
        length: int | None = None,
    ) -> None:
        super().__init__(map)
        if length is not None:
            length_regex = f"{{{int(length)}}}"
        else:
            if maxlength is None:
                maxlength_value = ""
            else:
                maxlength_value = str(int(maxlength))
            length_regex = f"{{{int(minlength)},{maxlength_value}}}"
        self.regex = f"[^/]{length_regex}"
class AnyConverter(BaseConverter):
    """Matches one of the items provided.  Items can either be Python
    identifiers or strings::
        Rule('/<any(about, help, imprint, class, "foo,bar"):page_name>')
    :param map: the :class:`Map`.
    :param items: this function accepts the possible items as positional
                  arguments.
    .. versionchanged:: 2.2
        Value is validated when building a URL.
    """
    def __init__(self, map: Map, *items: str) -> None:
        super().__init__(map)
        self.items = set(items)
        self.regex = f"(?:{'|'.join([re.escape(x) for x in items])})"
    def to_url(self, value: t.Any) -> str:
        if value in self.items:
            return str(value)
        valid_values = ", ".join(f"'{item}'" for item in sorted(self.items))
        raise ValueError(f"'{value}' is not one of {valid_values}")
class PathConverter(BaseConverter):
    """Like the default :class:`UnicodeConverter`, but it also matches
    slashes.  This is useful for wikis and similar applications::
        Rule('/<path:wikipage>')
        Rule('/<path:wikipage>/edit')
    :param map: the :class:`Map`.
    """
    part_isolating = False
    regex = "[^/].*?"
    weight = 200
class NumberConverter(BaseConverter):
    """Baseclass for `IntegerConverter` and `FloatConverter`.
    :internal:
    """
    weight = 50
    num_convert: t.Callable[[t.Any], t.Any] = int
    def __init__(
        self,
        map: Map,
        fixed_digits: int = 0,
        min: int | None = None,
        max: int | None = None,
        signed: bool = False,
    ) -> None:
        if signed:
            self.regex = self.signed_regex
        super().__init__(map)
        self.fixed_digits = fixed_digits
        self.min = min
        self.max = max
        self.signed = signed
    def to_python(self, value: str) -> t.Any:
        if self.fixed_digits and len(value) != self.fixed_digits:
            raise ValidationError()
        value_num = self.num_convert(value)
        if (self.min is not None and value_num < self.min) or (
            self.max is not None and value_num > self.max
        ):
            raise ValidationError()
        return value_num
    def to_url(self, value: t.Any) -> str:
        value_str = str(self.num_convert(value))
        if self.fixed_digits:
            value_str = value_str.zfill(self.fixed_digits)
        return value_str
    @property
    def signed_regex(self) -> str:
        return f"-?{self.regex}"
class IntegerConverter(NumberConverter):
    """This converter only accepts integer values::
        Rule("/page/<int:page>")
    By default it only accepts unsigned, positive values. The ``signed``
    parameter will enable signed, negative values. ::
        Rule("/page/<int(signed=True):page>")
    :param map: The :class:`Map`.
    :param fixed_digits: The number of fixed digits in the URL. If you
        set this to ``4`` for example, the rule will only match if the
        URL looks like ``/0001/``. The default is variable length.
    :param min: The minimal value.
    :param max: The maximal value.
    :param signed: Allow signed (negative) values.
    .. versionadded:: 0.15
        The ``signed`` parameter.
    """
    regex = r"\d+"
class FloatConverter(NumberConverter):
    """This converter only accepts floating point values::
        Rule("/probability/<float:probability>")
    By default it only accepts unsigned, positive values. The ``signed``
    parameter will enable signed, negative values. ::
        Rule("/offset/<float(signed=True):offset>")
    :param map: The :class:`Map`.
    :param min: The minimal value.
    :param max: The maximal value.
    :param signed: Allow signed (negative) values.
    .. versionadded:: 0.15
        The ``signed`` parameter.
    """
    regex = r"\d+\.\d+"
    num_convert = float
    def __init__(
        self,
        map: Map,
        min: float | None = None,
        max: float | None = None,
        signed: bool = False,
    ) -> None:
        super().__init__(map, min=min, max=max, signed=signed)  # type: ignore
class UUIDConverter(BaseConverter):
    """This converter only accepts UUID strings::
        Rule('/object/<uuid:identifier>')
    .. versionadded:: 0.10
    :param map: the :class:`Map`.
    """
    regex = (
        r"[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-"
        r"[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}"
    )
    def to_python(self, value: str) -> uuid.UUID:
        return uuid.UUID(value)
    def to_url(self, value: uuid.UUID) -> str:
        return str(value)
#: the default converter mapping for the map.
DEFAULT_CONVERTERS: t.Mapping[str, type[BaseConverter]] = {
    "default": UnicodeConverter,
    "string": UnicodeConverter,
    "any": AnyConverter,
    "path": PathConverter,
    "int": IntegerConverter,
    "float": FloatConverter,
    "uuid": UUIDConverter,
}
from __future__ import annotations
import difflib
import typing as t
from ..exceptions import BadRequest
from ..exceptions import HTTPException
from ..utils import cached_property
from ..utils import redirect
if t.TYPE_CHECKING:
    from _typeshed.wsgi import WSGIEnvironment
    from ..wrappers.request import Request
    from ..wrappers.response import Response
    from .map import MapAdapter
    from .rules import Rule
class RoutingException(Exception):
    """Special exceptions that require the application to redirect, notifying
    about missing urls, etc.
    :internal:
    """
class RequestRedirect(HTTPException, RoutingException):
    """Raise if the map requests a redirect. This is for example the case if
    `strict_slashes` are activated and an url that requires a trailing slash.
    The attribute `new_url` contains the absolute destination url.
    """
    code = 308
    def __init__(self, new_url: str) -> None:
        super().__init__(new_url)
        self.new_url = new_url
    def get_response(
        self,
        environ: WSGIEnvironment | Request | None = None,
        scope: dict[str, t.Any] | None = None,
    ) -> Response:
        return redirect(self.new_url, self.code)
class RequestPath(RoutingException):
    """Internal exception."""
    __slots__ = ("path_info",)
    def __init__(self, path_info: str) -> None:
        super().__init__()
        self.path_info = path_info
class RequestAliasRedirect(RoutingException):  # noqa: B903
    """This rule is an alias and wants to redirect to the canonical URL."""
    def __init__(self, matched_values: t.Mapping[str, t.Any], endpoint: t.Any) -> None:
        super().__init__()
        self.matched_values = matched_values
        self.endpoint = endpoint
class BuildError(RoutingException, LookupError):
    """Raised if the build system cannot find a URL for an endpoint with the
    values provided.
    """
    def __init__(
        self,
        endpoint: t.Any,
        values: t.Mapping[str, t.Any],
        method: str | None,
        adapter: MapAdapter | None = None,
    ) -> None:
        super().__init__(endpoint, values, method)
        self.endpoint = endpoint
        self.values = values
        self.method = method
        self.adapter = adapter
    @cached_property
    def suggested(self) -> Rule | None:
        return self.closest_rule(self.adapter)
    def closest_rule(self, adapter: MapAdapter | None) -> Rule | None:
        def _score_rule(rule: Rule) -> float:
            return sum(
                [
                    0.98
                    * difflib.SequenceMatcher(
                        # endpoints can be any type, compare as strings
                        None,
                        str(rule.endpoint),
                        str(self.endpoint),
                    ).ratio(),
                    0.01 * bool(set(self.values or ()).issubset(rule.arguments)),
                    0.01 * bool(rule.methods and self.method in rule.methods),
                ]
            )
        if adapter and adapter.map._rules:
            return max(adapter.map._rules, key=_score_rule)
        return None
    def __str__(self) -> str:
        message = [f"Could not build url for endpoint {self.endpoint!r}"]
        if self.method:
            message.append(f" ({self.method!r})")
        if self.values:
            message.append(f" with values {sorted(self.values)!r}")
        message.append(".")
        if self.suggested:
            if self.endpoint == self.suggested.endpoint:
                if (
                    self.method
                    and self.suggested.methods is not None
                    and self.method not in self.suggested.methods
                ):
                    message.append(
                        " Did you mean to use methods"
                        f" {sorted(self.suggested.methods)!r}?"
                    )
                missing_values = self.suggested.arguments.union(
                    set(self.suggested.defaults or ())
                ) - set(self.values.keys())
                if missing_values:
                    message.append(
                        f" Did you forget to specify values {sorted(missing_values)!r}?"
                    )
            else:
                message.append(f" Did you mean {self.suggested.endpoint!r} instead?")
        return "".join(message)
class WebsocketMismatch(BadRequest):
    """The only matched rule is either a WebSocket and the request is
    HTTP, or the rule is HTTP and the request is a WebSocket.
    """
class NoMatch(Exception):
    __slots__ = ("have_match_for", "websocket_mismatch")
    def __init__(self, have_match_for: set[str], websocket_mismatch: bool) -> None:
        self.have_match_for = have_match_for
        self.websocket_mismatch = websocket_mismatch
from __future__ import annotations
import typing as t
import warnings
from pprint import pformat
from threading import Lock
from urllib.parse import quote
from urllib.parse import urljoin
from urllib.parse import urlunsplit
from .._internal import _get_environ
from .._internal import _wsgi_decoding_dance
from ..datastructures import ImmutableDict
from ..datastructures import MultiDict
from ..exceptions import BadHost
from ..exceptions import HTTPException
from ..exceptions import MethodNotAllowed
from ..exceptions import NotFound
from ..urls import _urlencode
from ..wsgi import get_host
from .converters import DEFAULT_CONVERTERS
from .exceptions import BuildError
from .exceptions import NoMatch
from .exceptions import RequestAliasRedirect
from .exceptions import RequestPath
from .exceptions import RequestRedirect
from .exceptions import WebsocketMismatch
from .matcher import StateMachineMatcher
from .rules import _simple_rule_re
from .rules import Rule
if t.TYPE_CHECKING:
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment
    from ..wrappers.request import Request
    from .converters import BaseConverter
    from .rules import RuleFactory
class Map:
    """The map class stores all the URL rules and some configuration
    parameters.  Some of the configuration values are only stored on the
    `Map` instance since those affect all rules, others are just defaults
    and can be overridden for each rule.  Note that you have to specify all
    arguments besides the `rules` as keyword arguments!
    :param rules: sequence of url rules for this map.
    :param default_subdomain: The default subdomain for rules without a
                              subdomain defined.
    :param strict_slashes: If a rule ends with a slash but the matched
        URL does not, redirect to the URL with a trailing slash.
    :param merge_slashes: Merge consecutive slashes when matching or
        building URLs. Matches will redirect to the normalized URL.
        Slashes in variable parts are not merged.
    :param redirect_defaults: This will redirect to the default rule if it
                              wasn't visited that way. This helps creating
                              unique URLs.
    :param converters: A dict of converters that adds additional converters
                       to the list of converters. If you redefine one
                       converter this will override the original one.
    :param sort_parameters: If set to `True` the url parameters are sorted.
                            See `url_encode` for more details.
    :param sort_key: The sort key function for `url_encode`.
    :param host_matching: if set to `True` it enables the host matching
                          feature and disables the subdomain one.  If
                          enabled the `host` parameter to rules is used
                          instead of the `subdomain` one.
    .. versionchanged:: 3.0
        The ``charset`` and ``encoding_errors`` parameters were removed.
    .. versionchanged:: 1.0
        If ``url_scheme`` is ``ws`` or ``wss``, only WebSocket rules will match.
    .. versionchanged:: 1.0
        The ``merge_slashes`` parameter was added.
    .. versionchanged:: 0.7
        The ``encoding_errors`` and ``host_matching`` parameters were added.
    .. versionchanged:: 0.5
        The ``sort_parameters`` and ``sort_key``  parameters were added.
    """
    #: A dict of default converters to be used.
    default_converters = ImmutableDict(DEFAULT_CONVERTERS)
    #: The type of lock to use when updating.
    #:
    #: .. versionadded:: 1.0
    lock_class = Lock
    def __init__(
        self,
        rules: t.Iterable[RuleFactory] | None = None,
        default_subdomain: str = "",
        strict_slashes: bool = True,
        merge_slashes: bool = True,
        redirect_defaults: bool = True,
        converters: t.Mapping[str, type[BaseConverter]] | None = None,
        sort_parameters: bool = False,
        sort_key: t.Callable[[t.Any], t.Any] | None = None,
        host_matching: bool = False,
    ) -> None:
        self._matcher = StateMachineMatcher(merge_slashes)
        self._rules_by_endpoint: dict[t.Any, list[Rule]] = {}
        self._remap = True
        self._remap_lock = self.lock_class()
        self.default_subdomain = default_subdomain
        self.strict_slashes = strict_slashes
        self.redirect_defaults = redirect_defaults
        self.host_matching = host_matching
        self.converters = self.default_converters.copy()
        if converters:
            self.converters.update(converters)
        self.sort_parameters = sort_parameters
        self.sort_key = sort_key
        for rulefactory in rules or ():
            self.add(rulefactory)
    @property
    def merge_slashes(self) -> bool:
        return self._matcher.merge_slashes
    @merge_slashes.setter
    def merge_slashes(self, value: bool) -> None:
        self._matcher.merge_slashes = value
    def is_endpoint_expecting(self, endpoint: t.Any, *arguments: str) -> bool:
        """Iterate over all rules and check if the endpoint expects
        the arguments provided.  This is for example useful if you have
        some URLs that expect a language code and others that do not and
        you want to wrap the builder a bit so that the current language
        code is automatically added if not provided but endpoints expect
        it.
        :param endpoint: the endpoint to check.
        :param arguments: this function accepts one or more arguments
                          as positional arguments.  Each one of them is
                          checked.
        """
        self.update()
        arguments_set = set(arguments)
        for rule in self._rules_by_endpoint[endpoint]:
            if arguments_set.issubset(rule.arguments):
                return True
        return False
    @property
    def _rules(self) -> list[Rule]:
        return [rule for rules in self._rules_by_endpoint.values() for rule in rules]
    def iter_rules(self, endpoint: t.Any | None = None) -> t.Iterator[Rule]:
        """Iterate over all rules or the rules of an endpoint.
        :param endpoint: if provided only the rules for that endpoint
                         are returned.
        :return: an iterator
        """
        self.update()
        if endpoint is not None:
            return iter(self._rules_by_endpoint[endpoint])
        return iter(self._rules)
    def add(self, rulefactory: RuleFactory) -> None:
        """Add a new rule or factory to the map and bind it.  Requires that the
        rule is not bound to another map.
        :param rulefactory: a :class:`Rule` or :class:`RuleFactory`
        """
        for rule in rulefactory.get_rules(self):
            rule.bind(self)
            if not rule.build_only:
                self._matcher.add(rule)
            self._rules_by_endpoint.setdefault(rule.endpoint, []).append(rule)
        self._remap = True
    def bind(
        self,
        server_name: str,
        script_name: str | None = None,
        subdomain: str | None = None,
        url_scheme: str = "http",
        default_method: str = "GET",
        path_info: str | None = None,
        query_args: t.Mapping[str, t.Any] | str | None = None,
    ) -> MapAdapter:
        """Return a new :class:`MapAdapter` with the details specified to the
        call.  Note that `script_name` will default to ``'/'`` if not further
        specified or `None`.  The `server_name` at least is a requirement
        because the HTTP RFC requires absolute URLs for redirects and so all
        redirect exceptions raised by Werkzeug will contain the full canonical
        URL.
        If no path_info is passed to :meth:`match` it will use the default path
        info passed to bind.  While this doesn't really make sense for
        manual bind calls, it's useful if you bind a map to a WSGI
        environment which already contains the path info.
        `subdomain` will default to the `default_subdomain` for this map if
        no defined. If there is no `default_subdomain` you cannot use the
        subdomain feature.
        .. versionchanged:: 1.0
            If ``url_scheme`` is ``ws`` or ``wss``, only WebSocket rules
            will match.
        .. versionchanged:: 0.15
            ``path_info`` defaults to ``'/'`` if ``None``.
        .. versionchanged:: 0.8
            ``query_args`` can be a string.
        .. versionchanged:: 0.7
            Added ``query_args``.
        """
        server_name = server_name.lower()
        if self.host_matching:
            if subdomain is not None:
                raise RuntimeError("host matching enabled and a subdomain was provided")
        elif subdomain is None:
            subdomain = self.default_subdomain
        if script_name is None:
            script_name = "/"
        if path_info is None:
            path_info = "/"
        # Port isn't part of IDNA, and might push a name over the 63 octet limit.
        server_name, port_sep, port = server_name.partition(":")
        try:
            server_name = server_name.encode("idna").decode("ascii")
        except UnicodeError as e:
            raise BadHost() from e
        return MapAdapter(
            self,
            f"{server_name}{port_sep}{port}",
            script_name,
            subdomain,
            url_scheme,
            path_info,
            default_method,
            query_args,
        )
    def bind_to_environ(
        self,
        environ: WSGIEnvironment | Request,
        server_name: str | None = None,
        subdomain: str | None = None,
    ) -> MapAdapter:
        """Like :meth:`bind` but you can pass it an WSGI environment and it
        will fetch the information from that dictionary.  Note that because of
        limitations in the protocol there is no way to get the current
        subdomain and real `server_name` from the environment.  If you don't
        provide it, Werkzeug will use `SERVER_NAME` and `SERVER_PORT` (or
        `HTTP_HOST` if provided) as used `server_name` with disabled subdomain
        feature.
        If `subdomain` is `None` but an environment and a server name is
        provided it will calculate the current subdomain automatically.
        Example: `server_name` is ``'example.com'`` and the `SERVER_NAME`
        in the wsgi `environ` is ``'staging.dev.example.com'`` the calculated
        subdomain will be ``'staging.dev'``.
        If the object passed as environ has an environ attribute, the value of
        this attribute is used instead.  This allows you to pass request
        objects.  Additionally `PATH_INFO` added as a default of the
        :class:`MapAdapter` so that you don't have to pass the path info to
        the match method.
        .. versionchanged:: 1.0.0
            If the passed server name specifies port 443, it will match
            if the incoming scheme is ``https`` without a port.
        .. versionchanged:: 1.0.0
            A warning is shown when the passed server name does not
            match the incoming WSGI server name.
        .. versionchanged:: 0.8
           This will no longer raise a ValueError when an unexpected server
           name was passed.
        .. versionchanged:: 0.5
            previously this method accepted a bogus `calculate_subdomain`
            parameter that did not have any effect.  It was removed because
            of that.
        :param environ: a WSGI environment.
        :param server_name: an optional server name hint (see above).
        :param subdomain: optionally the current subdomain (see above).
        """
        env = _get_environ(environ)
        wsgi_server_name = get_host(env).lower()
        scheme = env["wsgi.url_scheme"]
        upgrade = any(
            v.strip() == "upgrade"
            for v in env.get("HTTP_CONNECTION", "").lower().split(",")
        )
        if upgrade and env.get("HTTP_UPGRADE", "").lower() == "websocket":
            scheme = "wss" if scheme == "https" else "ws"
        if server_name is None:
            server_name = wsgi_server_name
        else:
            server_name = server_name.lower()
            # strip standard port to match get_host()
            if scheme in {"http", "ws"} and server_name.endswith(":80"):
                server_name = server_name[:-3]
            elif scheme in {"https", "wss"} and server_name.endswith(":443"):
                server_name = server_name[:-4]
        if subdomain is None and not self.host_matching:
            cur_server_name = wsgi_server_name.split(".")
            real_server_name = server_name.split(".")
            offset = -len(real_server_name)
            if cur_server_name[offset:] != real_server_name:
                # This can happen even with valid configs if the server was
                # accessed directly by IP address under some situations.
                # Instead of raising an exception like in Werkzeug 0.7 or
                # earlier we go by an invalid subdomain which will result
                # in a 404 error on matching.
                warnings.warn(
                    f"Current server name {wsgi_server_name!r} doesn't match configured"
                    f" server name {server_name!r}",
                    stacklevel=2,
                )
                subdomain = "<invalid>"
            else:
                subdomain = ".".join(filter(None, cur_server_name[:offset]))
        def _get_wsgi_string(name: str) -> str | None:
            val = env.get(name)
            if val is not None:
                return _wsgi_decoding_dance(val)
            return None
        script_name = _get_wsgi_string("SCRIPT_NAME")
        path_info = _get_wsgi_string("PATH_INFO")
        query_args = _get_wsgi_string("QUERY_STRING")
        return Map.bind(
            self,
            server_name,
            script_name,
            subdomain,
            scheme,
            env["REQUEST_METHOD"],
            path_info,
            query_args=query_args,
        )
    def update(self) -> None:
        """Called before matching and building to keep the compiled rules
        in the correct order after things changed.
        """
        if not self._remap:
            return
        with self._remap_lock:
            if not self._remap:
                return
            self._matcher.update()
            for rules in self._rules_by_endpoint.values():
                rules.sort(key=lambda x: x.build_compare_key())
            self._remap = False
    def __repr__(self) -> str:
        rules = self.iter_rules()
        return f"{type(self).__name__}({pformat(list(rules))})"
class MapAdapter:
    """Returned by :meth:`Map.bind` or :meth:`Map.bind_to_environ` and does
    the URL matching and building based on runtime information.
    """
    def __init__(
        self,
        map: Map,
        server_name: str,
        script_name: str,
        subdomain: str | None,
        url_scheme: str,
        path_info: str,
        default_method: str,
        query_args: t.Mapping[str, t.Any] | str | None = None,
    ):
        self.map = map
        self.server_name = server_name
        if not script_name.endswith("/"):
            script_name += "/"
        self.script_name = script_name
        self.subdomain = subdomain
        self.url_scheme = url_scheme
        self.path_info = path_info
        self.default_method = default_method
        self.query_args = query_args
        self.websocket = self.url_scheme in {"ws", "wss"}
    def dispatch(
        self,
        view_func: t.Callable[[str, t.Mapping[str, t.Any]], WSGIApplication],
        path_info: str | None = None,
        method: str | None = None,
        catch_http_exceptions: bool = False,
    ) -> WSGIApplication:
        """Does the complete dispatching process.  `view_func` is called with
        the endpoint and a dict with the values for the view.  It should
        look up the view function, call it, and return a response object
        or WSGI application.  http exceptions are not caught by default
        so that applications can display nicer error messages by just
        catching them by hand.  If you want to stick with the default
        error messages you can pass it ``catch_http_exceptions=True`` and
        it will catch the http exceptions.
        Here a small example for the dispatch usage::
            from werkzeug.wrappers import Request, Response
            from werkzeug.wsgi import responder
            from werkzeug.routing import Map, Rule
            def on_index(request):
                return Response('Hello from the index')
            url_map = Map([Rule('/', endpoint='index')])
            views = {'index': on_index}
            @responder
            def application(environ, start_response):
                request = Request(environ)
                urls = url_map.bind_to_environ(environ)
                return urls.dispatch(lambda e, v: views[e](request, **v),
                                     catch_http_exceptions=True)
        Keep in mind that this method might return exception objects, too, so
        use :class:`Response.force_type` to get a response object.
        :param view_func: a function that is called with the endpoint as
                          first argument and the value dict as second.  Has
                          to dispatch to the actual view function with this
                          information.  (see above)
        :param path_info: the path info to use for matching.  Overrides the
                          path info specified on binding.
        :param method: the HTTP method used for matching.  Overrides the
                       method specified on binding.
        :param catch_http_exceptions: set to `True` to catch any of the
                                      werkzeug :class:`HTTPException`\\s.
        """
        try:
            try:
                endpoint, args = self.match(path_info, method)
            except RequestRedirect as e:
                return e
            return view_func(endpoint, args)
        except HTTPException as e:
            if catch_http_exceptions:
                return e
            raise
    @t.overload
    def match(
        self,
        path_info: str | None = None,
        method: str | None = None,
        return_rule: t.Literal[False] = False,
        query_args: t.Mapping[str, t.Any] | str | None = None,
        websocket: bool | None = None,
    ) -> tuple[t.Any, t.Mapping[str, t.Any]]: ...
    @t.overload
    def match(
        self,
        path_info: str | None = None,
        method: str | None = None,
        return_rule: t.Literal[True] = True,
        query_args: t.Mapping[str, t.Any] | str | None = None,
        websocket: bool | None = None,
    ) -> tuple[Rule, t.Mapping[str, t.Any]]: ...
    def match(
        self,
        path_info: str | None = None,
        method: str | None = None,
        return_rule: bool = False,
        query_args: t.Mapping[str, t.Any] | str | None = None,
        websocket: bool | None = None,
    ) -> tuple[t.Any | Rule, t.Mapping[str, t.Any]]:
        """The usage is simple: you just pass the match method the current
        path info as well as the method (which defaults to `GET`).  The
        following things can then happen:
        - you receive a `NotFound` exception that indicates that no URL is
          matching.  A `NotFound` exception is also a WSGI application you
          can call to get a default page not found page (happens to be the
          same object as `werkzeug.exceptions.NotFound`)
        - you receive a `MethodNotAllowed` exception that indicates that there
          is a match for this URL but not for the current request method.
          This is useful for RESTful applications.
        - you receive a `RequestRedirect` exception with a `new_url`
          attribute.  This exception is used to notify you about a request
          Werkzeug requests from your WSGI application.  This is for example the
          case if you request ``/foo`` although the correct URL is ``/foo/``
          You can use the `RequestRedirect` instance as response-like object
          similar to all other subclasses of `HTTPException`.
        - you receive a ``WebsocketMismatch`` exception if the only
          match is a WebSocket rule but the bind is an HTTP request, or
          if the match is an HTTP rule but the bind is a WebSocket
          request.
        - you get a tuple in the form ``(endpoint, arguments)`` if there is
          a match (unless `return_rule` is True, in which case you get a tuple
          in the form ``(rule, arguments)``)
        If the path info is not passed to the match method the default path
        info of the map is used (defaults to the root URL if not defined
        explicitly).
        All of the exceptions raised are subclasses of `HTTPException` so they
        can be used as WSGI responses. They will all render generic error or
        redirect pages.
        Here is a small example for matching:
        >>> m = Map([
        ...     Rule('/', endpoint='index'),
        ...     Rule('/downloads/', endpoint='downloads/index'),
        ...     Rule('/downloads/<int:id>', endpoint='downloads/show')
        ... ])
        >>> urls = m.bind("example.com", "/")
        >>> urls.match("/", "GET")
        ('index', {})
        >>> urls.match("/downloads/42")
        ('downloads/show', {'id': 42})
        And here is what happens on redirect and missing URLs:
        >>> urls.match("/downloads")
        Traceback (most recent call last):
          ...
        RequestRedirect: http://example.com/downloads/
        >>> urls.match("/missing")
        Traceback (most recent call last):
          ...
        NotFound: 404 Not Found
        :param path_info: the path info to use for matching.  Overrides the
                          path info specified on binding.
        :param method: the HTTP method used for matching.  Overrides the
                       method specified on binding.
        :param return_rule: return the rule that matched instead of just the
                            endpoint (defaults to `False`).
        :param query_args: optional query arguments that are used for
                           automatic redirects as string or dictionary.  It's
                           currently not possible to use the query arguments
                           for URL matching.
        :param websocket: Match WebSocket instead of HTTP requests. A
            websocket request has a ``ws`` or ``wss``
            :attr:`url_scheme`. This overrides that detection.
        .. versionadded:: 1.0
            Added ``websocket``.
        .. versionchanged:: 0.8
            ``query_args`` can be a string.
        .. versionadded:: 0.7
            Added ``query_args``.
        .. versionadded:: 0.6
            Added ``return_rule``.
        """
        self.map.update()
        if path_info is None:
            path_info = self.path_info
        if query_args is None:
            query_args = self.query_args or {}
        method = (method or self.default_method).upper()
        if websocket is None:
            websocket = self.websocket
        domain_part = self.server_name
        if not self.map.host_matching and self.subdomain is not None:
            domain_part = self.subdomain
        path_part = f"/{path_info.lstrip('/')}" if path_info else ""
        try:
            result = self.map._matcher.match(domain_part, path_part, method, websocket)
        except RequestPath as e:
            # safe = https://url.spec.whatwg.org/#url-path-segment-string
            new_path = quote(e.path_info, safe="!$&'()*+,/:;=@")
            raise RequestRedirect(
                self.make_redirect_url(new_path, query_args)
            ) from None
        except RequestAliasRedirect as e:
            raise RequestRedirect(
                self.make_alias_redirect_url(
                    f"{domain_part}|{path_part}",
                    e.endpoint,
                    e.matched_values,
                    method,
                    query_args,
                )
            ) from None
        except NoMatch as e:
            if e.have_match_for:
                raise MethodNotAllowed(valid_methods=list(e.have_match_for)) from None
            if e.websocket_mismatch:
                raise WebsocketMismatch() from None
            raise NotFound() from None
        else:
            rule, rv = result
            if self.map.redirect_defaults:
                redirect_url = self.get_default_redirect(rule, method, rv, query_args)
                if redirect_url is not None:
                    raise RequestRedirect(redirect_url)
            if rule.redirect_to is not None:
                if isinstance(rule.redirect_to, str):
                    def _handle_match(match: t.Match[str]) -> str:
                        value = rv[match.group(1)]
                        return rule._converters[match.group(1)].to_url(value)
                    redirect_url = _simple_rule_re.sub(_handle_match, rule.redirect_to)
                else:
                    redirect_url = rule.redirect_to(self, **rv)
                if self.subdomain:
                    netloc = f"{self.subdomain}.{self.server_name}"
                else:
                    netloc = self.server_name
                raise RequestRedirect(
                    urljoin(
                        f"{self.url_scheme or 'http'}://{netloc}{self.script_name}",
                        redirect_url,
                    )
                )
            if return_rule:
                return rule, rv
            else:
                return rule.endpoint, rv
    def test(self, path_info: str | None = None, method: str | None = None) -> bool:
        """Test if a rule would match.  Works like `match` but returns `True`
        if the URL matches, or `False` if it does not exist.
        :param path_info: the path info to use for matching.  Overrides the
                          path info specified on binding.
        :param method: the HTTP method used for matching.  Overrides the
                       method specified on binding.
        """
        try:
            self.match(path_info, method)
        except RequestRedirect:
            pass
        except HTTPException:
            return False
        return True
    def allowed_methods(self, path_info: str | None = None) -> t.Iterable[str]:
        """Returns the valid methods that match for a given path.
        .. versionadded:: 0.7
        """
        try:
            self.match(path_info, method="--")
        except MethodNotAllowed as e:
            return e.valid_methods  # type: ignore
        except HTTPException:
            pass
        return []
    def get_host(self, domain_part: str | None) -> str:
        """Figures out the full host name for the given domain part.  The
        domain part is a subdomain in case host matching is disabled or
        a full host name.
        """
        if self.map.host_matching:
            if domain_part is None:
                return self.server_name
            return domain_part
        if domain_part is None:
            subdomain = self.subdomain
        else:
            subdomain = domain_part
        if subdomain:
            return f"{subdomain}.{self.server_name}"
        else:
            return self.server_name
    def get_default_redirect(
        self,
        rule: Rule,
        method: str,
        values: t.MutableMapping[str, t.Any],
        query_args: t.Mapping[str, t.Any] | str,
    ) -> str | None:
        """A helper that returns the URL to redirect to if it finds one.
        This is used for default redirecting only.
        :internal:
        """
        assert self.map.redirect_defaults
        for r in self.map._rules_by_endpoint[rule.endpoint]:
            # every rule that comes after this one, including ourself
            # has a lower priority for the defaults.  We order the ones
            # with the highest priority up for building.
            if r is rule:
                break
            if r.provides_defaults_for(rule) and r.suitable_for(values, method):
                values.update(r.defaults)  # type: ignore
                domain_part, path = r.build(values)  # type: ignore
                return self.make_redirect_url(path, query_args, domain_part=domain_part)
        return None
    def encode_query_args(self, query_args: t.Mapping[str, t.Any] | str) -> str:
        if not isinstance(query_args, str):
            return _urlencode(query_args)
        return query_args
    def make_redirect_url(
        self,
        path_info: str,
        query_args: t.Mapping[str, t.Any] | str | None = None,
        domain_part: str | None = None,
    ) -> str:
        """Creates a redirect URL.
        :internal:
        """
        if query_args is None:
            query_args = self.query_args
        if query_args:
            query_str = self.encode_query_args(query_args)
        else:
            query_str = None
        scheme = self.url_scheme or "http"
        host = self.get_host(domain_part)
        path = "/".join((self.script_name.strip("/"), path_info.lstrip("/")))
        return urlunsplit((scheme, host, path, query_str, None))
    def make_alias_redirect_url(
        self,
        path: str,
        endpoint: t.Any,
        values: t.Mapping[str, t.Any],
        method: str,
        query_args: t.Mapping[str, t.Any] | str,
    ) -> str:
        """Internally called to make an alias redirect URL."""
        url = self.build(
            endpoint, values, method, append_unknown=False, force_external=True
        )
        if query_args:
            url += f"?{self.encode_query_args(query_args)}"
        assert url != path, "detected invalid alias setting. No canonical URL found"
        return url
    def _partial_build(
        self,
        endpoint: t.Any,
        values: t.Mapping[str, t.Any],
        method: str | None,
        append_unknown: bool,
    ) -> tuple[str, str, bool] | None:
        """Helper for :meth:`build`.  Returns subdomain and path for the
        rule that accepts this endpoint, values and method.
        :internal:
        """
        # in case the method is none, try with the default method first
        if method is None:
            rv = self._partial_build(
                endpoint, values, self.default_method, append_unknown
            )
            if rv is not None:
                return rv
        # Default method did not match or a specific method is passed.
        # Check all for first match with matching host. If no matching
        # host is found, go with first result.
        first_match = None
        for rule in self.map._rules_by_endpoint.get(endpoint, ()):
            if rule.suitable_for(values, method):
                build_rv = rule.build(values, append_unknown)
                if build_rv is not None:
                    rv = (build_rv[0], build_rv[1], rule.websocket)
                    if self.map.host_matching:
                        if rv[0] == self.server_name:
                            return rv
                        elif first_match is None:
                            first_match = rv
                    else:
                        return rv
        return first_match
    def build(
        self,
        endpoint: t.Any,
        values: t.Mapping[str, t.Any] | None = None,
        method: str | None = None,
        force_external: bool = False,
        append_unknown: bool = True,
        url_scheme: str | None = None,
    ) -> str:
        """Build a URL by filling in any variable slots in the endpoint's rule
        with the provided values.
        This produces relative URLs (path only, no host) by default, which is
        appropriate for most use cases. When using subdomain or host matching,
        the URL will be absolute if the endpoint is not on the same host as the
        current request. If you need an absolute URL no matter what, such as
        when adding a link to an email, pass ``force_external=True``.
        Characters that are not allowed directly in URLs will be percent-encoded
        using UTF-8.
        Additional values that don't match any rule parts are added to the query
        (``?key=value``) part of the URL.
        If a rule is not found, an :exc:`.BuildError` is raised. Converters may
        also raise exceptions when preparing a value.
        Unlike matching, building does not perform comprehensive validation of
        the values, it's assumed that they are trusted and correct. It's also
        possible to build a URL for one endpoint that will be matched by
        another, or will not match. This is very unlikely to happen or to matter
        in most applications, especially with testing. If you need a
        stronger guarantee, you can use a helper to verify that
        ``match(build(endpoint)) == endpoint``.
        :param endpoint: The endpoint for the rule to build.
        :param values: Values for the variable parts of the rule, which will be
            converted using the part's converter's
            :meth:`~.BaseConverter.to_url` method. Keys that don't match
            variable parts will be converted to a query string unless
            ``append_unknown`` is disabled.
        :param method: Further match the rule to build by this HTTP method, for
            when there are multiple rules for the same endpoint that vary based
            on method.
        :param force_external: Always produce an absolute URL, for external use.
            If ``scheme`` is not set, this produces a protocol-relative URL.
        :param append_unknown: Convert values that don't match any rule parts
            to a query string. Disable to ignore such values.
        :param url_scheme: Scheme to use for absolute URLs. Defaults to
            :attr:`url_scheme`.
        .. versionchanged:: 2.0
            Added the ``url_scheme`` parameter.
        .. versionadded:: 0.6
           Added the ``append_unknown`` parameter.
        """
        self.map.update()
        if values:
            if isinstance(values, MultiDict):
                values = {
                    k: (v[0] if len(v) == 1 else v)
                    for k, v in dict.items(values)
                    if len(v) != 0
                }
            else:  # plain dict
                values = {k: v for k, v in values.items() if v is not None}
        else:
            values = {}
        rv = self._partial_build(endpoint, values, method, append_unknown)
        if rv is None:
            raise BuildError(endpoint, values, method, self)
        domain_part, path, websocket = rv
        host = self.get_host(domain_part)
        if url_scheme is None:
            url_scheme = self.url_scheme
        # Always build WebSocket routes with the scheme (browsers
        # require full URLs). If bound to a WebSocket, ensure that HTTP
        # routes are built with an HTTP scheme.
        secure = url_scheme in {"https", "wss"}
        if websocket:
            force_external = True
            url_scheme = "wss" if secure else "ws"
        elif url_scheme:
            url_scheme = "https" if secure else "http"
        # shortcut this.
        if not force_external and (
            (self.map.host_matching and host == self.server_name)
            or (not self.map.host_matching and domain_part == self.subdomain)
        ):
            return f"{self.script_name.rstrip('/')}/{path.lstrip('/')}"
        scheme = f"{url_scheme}:" if url_scheme else ""
        return f"{scheme}//{host}{self.script_name[:-1]}/{path.lstrip('/')}"
from __future__ import annotations
import re
import typing as t
from dataclasses import dataclass
from dataclasses import field
from .converters import ValidationError
from .exceptions import NoMatch
from .exceptions import RequestAliasRedirect
from .exceptions import RequestPath
from .rules import Rule
from .rules import RulePart
class SlashRequired(Exception):
    pass
@dataclass
class State:
    """A representation of a rule state.
    This includes the *rules* that correspond to the state and the
    possible *static* and *dynamic* transitions to the next state.
    """
    dynamic: list[tuple[RulePart, State]] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
    static: dict[str, State] = field(default_factory=dict)
class StateMachineMatcher:
    def __init__(self, merge_slashes: bool) -> None:
        self._root = State()
        self.merge_slashes = merge_slashes
    def add(self, rule: Rule) -> None:
        state = self._root
        for part in rule._parts:
            if part.static:
                state.static.setdefault(part.content, State())
                state = state.static[part.content]
            else:
                for test_part, new_state in state.dynamic:
                    if test_part == part:
                        state = new_state
                        break
                else:
                    new_state = State()
                    state.dynamic.append((part, new_state))
                    state = new_state
        state.rules.append(rule)
    def update(self) -> None:
        # For every state the dynamic transitions should be sorted by
        # the weight of the transition
        state = self._root
        def _update_state(state: State) -> None:
            state.dynamic.sort(key=lambda entry: entry[0].weight)
            for new_state in state.static.values():
                _update_state(new_state)
            for _, new_state in state.dynamic:
                _update_state(new_state)
        _update_state(state)
    def match(
        self, domain: str, path: str, method: str, websocket: bool
    ) -> tuple[Rule, t.MutableMapping[str, t.Any]]:
        # To match to a rule we need to start at the root state and
        # try to follow the transitions until we find a match, or find
        # there is no transition to follow.
        have_match_for = set()
        websocket_mismatch = False
        def _match(
            state: State, parts: list[str], values: list[str]
        ) -> tuple[Rule, list[str]] | None:
            # This function is meant to be called recursively, and will attempt
            # to match the head part to the state's transitions.
            nonlocal have_match_for, websocket_mismatch
            # The base case is when all parts have been matched via
            # transitions. Hence if there is a rule with methods &
            # websocket that work return it and the dynamic values
            # extracted.
            if parts == []:
                for rule in state.rules:
                    if rule.methods is not None and method not in rule.methods:
                        have_match_for.update(rule.methods)
                    elif rule.websocket != websocket:
                        websocket_mismatch = True
                    else:
                        return rule, values
                # Test if there is a match with this path with a
                # trailing slash, if so raise an exception to report
                # that matching is possible with an additional slash
                if "" in state.static:
                    for rule in state.static[""].rules:
                        if websocket == rule.websocket and (
                            rule.methods is None or method in rule.methods
                        ):
                            if rule.strict_slashes:
                                raise SlashRequired()
                            else:
                                return rule, values
                return None
            part = parts[0]
            # To match this part try the static transitions first
            if part in state.static:
                rv = _match(state.static[part], parts[1:], values)
                if rv is not None:
                    return rv
            # No match via the static transitions, so try the dynamic
            # ones.
            for test_part, new_state in state.dynamic:
                target = part
                remaining = parts[1:]
                # A final part indicates a transition that always
                # consumes the remaining parts i.e. transitions to a
                # final state.
                if test_part.final:
                    target = "/".join(parts)
                    remaining = []
                match = re.compile(test_part.content).match(target)
                if match is not None:
                    if test_part.suffixed:
                        # If a part_isolating=False part has a slash suffix, remove the
                        # suffix from the match and check for the slash redirect next.
                        suffix = match.groups()[-1]
                        if suffix == "/":
                            remaining = [""]
                    converter_groups = sorted(
                        match.groupdict().items(), key=lambda entry: entry[0]
                    )
                    groups = [
                        value
                        for key, value in converter_groups
                        if key[:11] == "__werkzeug_"
                    ]
                    rv = _match(new_state, remaining, values + groups)
                    if rv is not None:
                        return rv
            # If there is no match and the only part left is a
            # trailing slash ("") consider rules that aren't
            # strict-slashes as these should match if there is a final
            # slash part.
            if parts == [""]:
                for rule in state.rules:
                    if rule.strict_slashes:
                        continue
                    if rule.methods is not None and method not in rule.methods:
                        have_match_for.update(rule.methods)
                    elif rule.websocket != websocket:
                        websocket_mismatch = True
                    else:
                        return rule, values
            return None
        try:
            rv = _match(self._root, [domain, *path.split("/")], [])
        except SlashRequired:
            raise RequestPath(f"{path}/") from None
        if self.merge_slashes and rv is None:
            # Try to match again, but with slashes merged
            path = re.sub("/{2,}", "/", path)
            try:
                rv = _match(self._root, [domain, *path.split("/")], [])
            except SlashRequired:
                raise RequestPath(f"{path}/") from None
            if rv is None or rv[0].merge_slashes is False:
                raise NoMatch(have_match_for, websocket_mismatch)
            else:
                raise RequestPath(f"{path}")
        elif rv is not None:
            rule, values = rv
            result = {}
            for name, value in zip(rule._converters.keys(), values):
                try:
                    value = rule._converters[name].to_python(value)
                except ValidationError:
                    raise NoMatch(have_match_for, websocket_mismatch) from None
                result[str(name)] = value
            if rule.defaults:
                result.update(rule.defaults)
            if rule.alias and rule.map.redirect_defaults:
                raise RequestAliasRedirect(result, rule.endpoint)
            return rule, result
        raise NoMatch(have_match_for, websocket_mismatch)
from __future__ import annotations
import ast
import re
import typing as t
from dataclasses import dataclass
from string import Template
from types import CodeType
from urllib.parse import quote
from ..datastructures import iter_multi_items
from ..urls import _urlencode
from .converters import ValidationError
if t.TYPE_CHECKING:
    from .converters import BaseConverter
    from .map import Map
class Weighting(t.NamedTuple):
    number_static_weights: int
    static_weights: list[tuple[int, int]]
    number_argument_weights: int
    argument_weights: list[int]
@dataclass
class RulePart:
    """A part of a rule.
    Rules can be represented by parts as delimited by `/` with
    instances of this class representing those parts. The *content* is
    either the raw content if *static* or a regex string to match
    against. The *weight* can be used to order parts when matching.
    """
    content: str
    final: bool
    static: bool
    suffixed: bool
    weight: Weighting
_part_re = re.compile(
    r"""
    (?:
        (?P<slash>/)                                 # a slash
      |
        (?P<static>[^</]+)                           # static rule data
      |
        (?:
          <
            (?:
              (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)   # converter name
              (?:\((?P<arguments>.*?)\))?             # converter arguments
              :                                       # variable delimiter
            )?
            (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)      # variable name
           >
        )
    )
    """,
    re.VERBOSE,
)
_simple_rule_re = re.compile(r"<([^>]+)>")
_converter_args_re = re.compile(
    r"""
    \s*
    ((?P<name>\w+)\s*=\s*)?
    (?P<value>
        True|False|
        \d+.\d+|
        \d+.|
        \d+|
        [\w\d_.]+|
        [urUR]?(?P<stringval>"[^"]*?"|'[^']*')
    )\s*,
    """,
    re.VERBOSE,
)
_PYTHON_CONSTANTS = {"None": None, "True": True, "False": False}
def _find(value: str, target: str, pos: int) -> int:
    """Find the *target* in *value* after *pos*.
    Returns the *value* length if *target* isn't found.
    """
    try:
        return value.index(target, pos)
    except ValueError:
        return len(value)
def _pythonize(value: str) -> None | bool | int | float | str:
    if value in _PYTHON_CONSTANTS:
        return _PYTHON_CONSTANTS[value]
    for convert in int, float:
        try:
            return convert(value)
        except ValueError:
            pass
    if value[:1] == value[-1:] and value[0] in "\"'":
        value = value[1:-1]
    return str(value)
def parse_converter_args(argstr: str) -> tuple[tuple[t.Any, ...], dict[str, t.Any]]:
    argstr += ","
    args = []
    kwargs = {}
    position = 0
    for item in _converter_args_re.finditer(argstr):
        if item.start() != position:
            raise ValueError(
                f"Cannot parse converter argument '{argstr[position : item.start()]}'"
            )
        value = item.group("stringval")
        if value is None:
            value = item.group("value")
        value = _pythonize(value)
        if not item.group("name"):
            args.append(value)
        else:
            name = item.group("name")
            kwargs[name] = value
        position = item.end()
    return tuple(args), kwargs
class RuleFactory:
    """As soon as you have more complex URL setups it's a good idea to use rule
    factories to avoid repetitive tasks.  Some of them are builtin, others can
    be added by subclassing `RuleFactory` and overriding `get_rules`.
    """
    def get_rules(self, map: Map) -> t.Iterable[Rule]:
        """Subclasses of `RuleFactory` have to override this method and return
        an iterable of rules."""
        raise NotImplementedError()
class Subdomain(RuleFactory):
    """All URLs provided by this factory have the subdomain set to a
    specific domain. For example if you want to use the subdomain for
    the current language this can be a good setup::
        url_map = Map([
            Rule('/', endpoint='#select_language'),
            Subdomain('<string(length=2):lang_code>', [
                Rule('/', endpoint='index'),
                Rule('/about', endpoint='about'),
                Rule('/help', endpoint='help')
            ])
        ])
    All the rules except for the ``'#select_language'`` endpoint will now
    listen on a two letter long subdomain that holds the language code
    for the current request.
    """
    def __init__(self, subdomain: str, rules: t.Iterable[RuleFactory]) -> None:
        self.subdomain = subdomain
        self.rules = rules
    def get_rules(self, map: Map) -> t.Iterator[Rule]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                rule = rule.empty()
                rule.subdomain = self.subdomain
                yield rule
class Submount(RuleFactory):
    """Like `Subdomain` but prefixes the URL rule with a given string::
        url_map = Map([
            Rule('/', endpoint='index'),
            Submount('/blog', [
                Rule('/', endpoint='blog/index'),
                Rule('/entry/<entry_slug>', endpoint='blog/show')
            ])
        ])
    Now the rule ``'blog/show'`` matches ``/blog/entry/<entry_slug>``.
    """
    def __init__(self, path: str, rules: t.Iterable[RuleFactory]) -> None:
        self.path = path.rstrip("/")
        self.rules = rules
    def get_rules(self, map: Map) -> t.Iterator[Rule]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                rule = rule.empty()
                rule.rule = self.path + rule.rule
                yield rule
class EndpointPrefix(RuleFactory):
    """Prefixes all endpoints (which must be strings for this factory) with
    another string. This can be useful for sub applications::
        url_map = Map([
            Rule('/', endpoint='index'),
            EndpointPrefix('blog/', [Submount('/blog', [
                Rule('/', endpoint='index'),
                Rule('/entry/<entry_slug>', endpoint='show')
            ])])
        ])
    """
    def __init__(self, prefix: str, rules: t.Iterable[RuleFactory]) -> None:
        self.prefix = prefix
        self.rules = rules
    def get_rules(self, map: Map) -> t.Iterator[Rule]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                rule = rule.empty()
                rule.endpoint = self.prefix + rule.endpoint
                yield rule
class RuleTemplate:
    """Returns copies of the rules wrapped and expands string templates in
    the endpoint, rule, defaults or subdomain sections.
    Here a small example for such a rule template::
        from werkzeug.routing import Map, Rule, RuleTemplate
        resource = RuleTemplate([
            Rule('/$name/', endpoint='$name.list'),
            Rule('/$name/<int:id>', endpoint='$name.show')
        ])
        url_map = Map([resource(name='user'), resource(name='page')])
    When a rule template is called the keyword arguments are used to
    replace the placeholders in all the string parameters.
    """
    def __init__(self, rules: t.Iterable[Rule]) -> None:
        self.rules = list(rules)
    def __call__(self, *args: t.Any, **kwargs: t.Any) -> RuleTemplateFactory:
        return RuleTemplateFactory(self.rules, dict(*args, **kwargs))
class RuleTemplateFactory(RuleFactory):
    """A factory that fills in template variables into rules.  Used by
    `RuleTemplate` internally.
    :internal:
    """
    def __init__(
        self, rules: t.Iterable[RuleFactory], context: dict[str, t.Any]
    ) -> None:
        self.rules = rules
        self.context = context
    def get_rules(self, map: Map) -> t.Iterator[Rule]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                new_defaults = subdomain = None
                if rule.defaults:
                    new_defaults = {}
                    for key, value in rule.defaults.items():
                        if isinstance(value, str):
                            value = Template(value).substitute(self.context)
                        new_defaults[key] = value
                if rule.subdomain is not None:
                    subdomain = Template(rule.subdomain).substitute(self.context)
                new_endpoint = rule.endpoint
                if isinstance(new_endpoint, str):
                    new_endpoint = Template(new_endpoint).substitute(self.context)
                yield Rule(
                    Template(rule.rule).substitute(self.context),
                    new_defaults,
                    subdomain,
                    rule.methods,
                    rule.build_only,
                    new_endpoint,
                    rule.strict_slashes,
                )
_ASTT = t.TypeVar("_ASTT", bound=ast.AST)
def _prefix_names(src: str, expected_type: type[_ASTT]) -> _ASTT:
    """ast parse and prefix names with `.` to avoid collision with user vars"""
    tree: ast.AST = ast.parse(src).body[0]
    if isinstance(tree, ast.Expr):
        tree = tree.value
    if not isinstance(tree, expected_type):
        raise TypeError(
            f"AST node is of type {type(tree).__name__}, not {expected_type.__name__}"
        )
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            node.id = f".{node.id}"
    return tree
_CALL_CONVERTER_CODE_FMT = "self._converters[{elem!r}].to_url()"
_IF_KWARGS_URL_ENCODE_CODE = """\
if kwargs:
    params = self._encode_query_vars(kwargs)
    q = "?" if params else ""
else:
    q = params = ""
"""
_IF_KWARGS_URL_ENCODE_AST = _prefix_names(_IF_KWARGS_URL_ENCODE_CODE, ast.If)
_URL_ENCODE_AST_NAMES = (
    _prefix_names("q", ast.Name),
    _prefix_names("params", ast.Name),
)
class Rule(RuleFactory):
    """A Rule represents one URL pattern.  There are some options for `Rule`
    that change the way it behaves and are passed to the `Rule` constructor.
    Note that besides the rule-string all arguments *must* be keyword arguments
    in order to not break the application on Werkzeug upgrades.
    `string`
        Rule strings basically are just normal URL paths with placeholders in
        the format ``<converter(arguments):name>`` where the converter and the
        arguments are optional.  If no converter is defined the `default`
        converter is used which means `string` in the normal configuration.
        URL rules that end with a slash are branch URLs, others are leaves.
        If you have `strict_slashes` enabled (which is the default), all
        branch URLs that are matched without a trailing slash will trigger a
        redirect to the same URL with the missing slash appended.
        The converters are defined on the `Map`.
    `endpoint`
        The endpoint for this rule. This can be anything. A reference to a
        function, a string, a number etc.  The preferred way is using a string
        because the endpoint is used for URL generation.
    `defaults`
        An optional dict with defaults for other rules with the same endpoint.
        This is a bit tricky but useful if you want to have unique URLs::
            url_map = Map([
                Rule('/all/', defaults={'page': 1}, endpoint='all_entries'),
                Rule('/all/page/<int:page>', endpoint='all_entries')
            ])
        If a user now visits ``http://example.com/all/page/1`` they will be
        redirected to ``http://example.com/all/``.  If `redirect_defaults` is
        disabled on the `Map` instance this will only affect the URL
        generation.
    `subdomain`
        The subdomain rule string for this rule. If not specified the rule
        only matches for the `default_subdomain` of the map.  If the map is
        not bound to a subdomain this feature is disabled.
        Can be useful if you want to have user profiles on different subdomains
        and all subdomains are forwarded to your application::
            url_map = Map([
                Rule('/', subdomain='<username>', endpoint='user/homepage'),
                Rule('/stats', subdomain='<username>', endpoint='user/stats')
            ])
    `methods`
        A sequence of http methods this rule applies to.  If not specified, all
        methods are allowed. For example this can be useful if you want different
        endpoints for `POST` and `GET`.  If methods are defined and the path
        matches but the method matched against is not in this list or in the
        list of another rule for that path the error raised is of the type
        `MethodNotAllowed` rather than `NotFound`.  If `GET` is present in the
        list of methods and `HEAD` is not, `HEAD` is added automatically.
    `strict_slashes`
        Override the `Map` setting for `strict_slashes` only for this rule. If
        not specified the `Map` setting is used.
    `merge_slashes`
        Override :attr:`Map.merge_slashes` for this rule.
    `build_only`
        Set this to True and the rule will never match but will create a URL
        that can be build. This is useful if you have resources on a subdomain
        or folder that are not handled by the WSGI application (like static data)
    `redirect_to`
        If given this must be either a string or callable.  In case of a
        callable it's called with the url adapter that triggered the match and
        the values of the URL as keyword arguments and has to return the target
        for the redirect, otherwise it has to be a string with placeholders in
        rule syntax::
            def foo_with_slug(adapter, id):
                # ask the database for the slug for the old id.  this of
                # course has nothing to do with werkzeug.
                return f'foo/{Foo.get_slug_for_id(id)}'
            url_map = Map([
                Rule('/foo/<slug>', endpoint='foo'),
                Rule('/some/old/url/<slug>', redirect_to='foo/<slug>'),
                Rule('/other/old/url/<int:id>', redirect_to=foo_with_slug)
            ])
        When the rule is matched the routing system will raise a
        `RequestRedirect` exception with the target for the redirect.
        Keep in mind that the URL will be joined against the URL root of the
        script so don't use a leading slash on the target URL unless you
        really mean root of that domain.
    `alias`
        If enabled this rule serves as an alias for another rule with the same
        endpoint and arguments.
    `host`
        If provided and the URL map has host matching enabled this can be
        used to provide a match rule for the whole host.  This also means
        that the subdomain feature is disabled.
    `websocket`
        If ``True``, this rule is only matches for WebSocket (``ws://``,
        ``wss://``) requests. By default, rules will only match for HTTP
        requests.
    .. versionchanged:: 2.1
        Percent-encoded newlines (``%0a``), which are decoded by WSGI
        servers, are considered when routing instead of terminating the
        match early.
    .. versionadded:: 1.0
        Added ``websocket``.
    .. versionadded:: 1.0
        Added ``merge_slashes``.
    .. versionadded:: 0.7
        Added ``alias`` and ``host``.
    .. versionchanged:: 0.6.1
       ``HEAD`` is added to ``methods`` if ``GET`` is present.
    """
    def __init__(
        self,
        string: str,
        defaults: t.Mapping[str, t.Any] | None = None,
        subdomain: str | None = None,
        methods: t.Iterable[str] | None = None,
        build_only: bool = False,
        endpoint: t.Any | None = None,
        strict_slashes: bool | None = None,
        merge_slashes: bool | None = None,
        redirect_to: str | t.Callable[..., str] | None = None,
        alias: bool = False,
        host: str | None = None,
        websocket: bool = False,
    ) -> None:
        if not string.startswith("/"):
            raise ValueError(f"URL rule '{string}' must start with a slash.")
        self.rule = string
        self.is_leaf = not string.endswith("/")
        self.is_branch = string.endswith("/")
        self.map: Map = None  # type: ignore
        self.strict_slashes = strict_slashes
        self.merge_slashes = merge_slashes
        self.subdomain = subdomain
        self.host = host
        self.defaults = defaults
        self.build_only = build_only
        self.alias = alias
        self.websocket = websocket
        if methods is not None:
            if isinstance(methods, str):
                raise TypeError("'methods' should be a list of strings.")
            methods = {x.upper() for x in methods}
            if "HEAD" not in methods and "GET" in methods:
                methods.add("HEAD")
            if websocket and methods - {"GET", "HEAD", "OPTIONS"}:
                raise ValueError(
                    "WebSocket rules can only use 'GET', 'HEAD', and 'OPTIONS' methods."
                )
        self.methods = methods
        self.endpoint: t.Any = endpoint
        self.redirect_to = redirect_to
        if defaults:
            self.arguments = set(map(str, defaults))
        else:
            self.arguments = set()
        self._converters: dict[str, BaseConverter] = {}
        self._trace: list[tuple[bool, str]] = []
        self._parts: list[RulePart] = []
    def empty(self) -> Rule:
        """
        Return an unbound copy of this rule.
        This can be useful if want to reuse an already bound URL for another
        map.  See ``get_empty_kwargs`` to override what keyword arguments are
        provided to the new copy.
        """
        return type(self)(self.rule, **self.get_empty_kwargs())
    def get_empty_kwargs(self) -> t.Mapping[str, t.Any]:
        """
        Provides kwargs for instantiating empty copy with empty()
        Use this method to provide custom keyword arguments to the subclass of
        ``Rule`` when calling ``some_rule.empty()``.  Helpful when the subclass
        has custom keyword arguments that are needed at instantiation.
        Must return a ``dict`` that will be provided as kwargs to the new
        instance of ``Rule``, following the initial ``self.rule`` value which
        is always provided as the first, required positional argument.
        """
        defaults = None
        if self.defaults:
            defaults = dict(self.defaults)
        return dict(
            defaults=defaults,
            subdomain=self.subdomain,
            methods=self.methods,
            build_only=self.build_only,
            endpoint=self.endpoint,
            strict_slashes=self.strict_slashes,
            redirect_to=self.redirect_to,
            alias=self.alias,
            host=self.host,
        )
    def get_rules(self, map: Map) -> t.Iterator[Rule]:
        yield self
    def refresh(self) -> None:
        """Rebinds and refreshes the URL.  Call this if you modified the
        rule in place.
        :internal:
        """
        self.bind(self.map, rebind=True)
    def bind(self, map: Map, rebind: bool = False) -> None:
        """Bind the url to a map and create a regular expression based on
        the information from the rule itself and the defaults from the map.
        :internal:
        """
        if self.map is not None and not rebind:
            raise RuntimeError(f"url rule {self!r} already bound to map {self.map!r}")
        self.map = map
        if self.strict_slashes is None:
            self.strict_slashes = map.strict_slashes
        if self.merge_slashes is None:
            self.merge_slashes = map.merge_slashes
        if self.subdomain is None:
            self.subdomain = map.default_subdomain
        self.compile()
    def get_converter(
        self,
        variable_name: str,
        converter_name: str,
        args: tuple[t.Any, ...],
        kwargs: t.Mapping[str, t.Any],
    ) -> BaseConverter:
        """Looks up the converter for the given parameter.
        .. versionadded:: 0.9
        """
        if converter_name not in self.map.converters:
            raise LookupError(f"the converter {converter_name!r} does not exist")
        return self.map.converters[converter_name](self.map, *args, **kwargs)
    def _encode_query_vars(self, query_vars: t.Mapping[str, t.Any]) -> str:
        items: t.Iterable[tuple[str, str]] = iter_multi_items(query_vars)
        if self.map.sort_parameters:
            items = sorted(items, key=self.map.sort_key)
        return _urlencode(items)
    def _parse_rule(self, rule: str) -> t.Iterable[RulePart]:
        content = ""
        static = True
        argument_weights = []
        static_weights: list[tuple[int, int]] = []
        final = False
        convertor_number = 0
        pos = 0
        while pos < len(rule):
            match = _part_re.match(rule, pos)
            if match is None:
                raise ValueError(f"malformed url rule: {rule!r}")
            data = match.groupdict()
            if data["static"] is not None:
                static_weights.append((len(static_weights), -len(data["static"])))
                self._trace.append((False, data["static"]))
                content += data["static"] if static else re.escape(data["static"])
            if data["variable"] is not None:
                if static:
                    # Switching content to represent regex, hence the need to escape
                    content = re.escape(content)
                static = False
                c_args, c_kwargs = parse_converter_args(data["arguments"] or "")
                convobj = self.get_converter(
                    data["variable"], data["converter"] or "default", c_args, c_kwargs
                )
                self._converters[data["variable"]] = convobj
                self.arguments.add(data["variable"])
                if not convobj.part_isolating:
                    final = True
                content += f"(?P<__werkzeug_{convertor_number}>{convobj.regex})"
                convertor_number += 1
                argument_weights.append(convobj.weight)
                self._trace.append((True, data["variable"]))
            if data["slash"] is not None:
                self._trace.append((False, "/"))
                if final:
                    content += "/"
                else:
                    if not static:
                        content += r"\Z"
                    weight = Weighting(
                        -len(static_weights),
                        static_weights,
                        -len(argument_weights),
                        argument_weights,
                    )
                    yield RulePart(
                        content=content,
                        final=final,
                        static=static,
                        suffixed=False,
                        weight=weight,
                    )
                    content = ""
                    static = True
                    argument_weights = []
                    static_weights = []
                    final = False
                    convertor_number = 0
            pos = match.end()
        suffixed = False
        if final and content[-1] == "/":
            # If a converter is part_isolating=False (matches slashes) and ends with a
            # slash, augment the regex to support slash redirects.
            suffixed = True
            content = content[:-1] + "(?<!/)(/?)"
        if not static:
            content += r"\Z"
        weight = Weighting(
            -len(static_weights),
            static_weights,
            -len(argument_weights),
            argument_weights,
        )
        yield RulePart(
            content=content,
            final=final,
            static=static,
            suffixed=suffixed,
            weight=weight,
        )
        if suffixed:
            yield RulePart(
                content="", final=False, static=True, suffixed=False, weight=weight
            )
    def compile(self) -> None:
        """Compiles the regular expression and stores it."""
        assert self.map is not None, "rule not bound"
        if self.map.host_matching:
            domain_rule = self.host or ""
        else:
            domain_rule = self.subdomain or ""
        self._parts = []
        self._trace = []
        self._converters = {}
        if domain_rule == "":
            self._parts = [
                RulePart(
                    content="",
                    final=False,
                    static=True,
                    suffixed=False,
                    weight=Weighting(0, [], 0, []),
                )
            ]
        else:
            self._parts.extend(self._parse_rule(domain_rule))
        self._trace.append((False, "|"))
        rule = self.rule
        if self.merge_slashes:
            rule = re.sub("/{2,}", "/", self.rule)
        self._parts.extend(self._parse_rule(rule))
        self._build: t.Callable[..., tuple[str, str]]
        self._build = self._compile_builder(False).__get__(self, None)
        self._build_unknown: t.Callable[..., tuple[str, str]]
        self._build_unknown = self._compile_builder(True).__get__(self, None)
    @staticmethod
    def _get_func_code(code: CodeType, name: str) -> t.Callable[..., tuple[str, str]]:
        globs: dict[str, t.Any] = {}
        locs: dict[str, t.Any] = {}
        exec(code, globs, locs)
        return locs[name]  # type: ignore
    def _compile_builder(
        self, append_unknown: bool = True
    ) -> t.Callable[..., tuple[str, str]]:
        defaults = self.defaults or {}
        dom_ops: list[tuple[bool, str]] = []
        url_ops: list[tuple[bool, str]] = []
        opl = dom_ops
        for is_dynamic, data in self._trace:
            if data == "|" and opl is dom_ops:
                opl = url_ops
                continue
            # this seems like a silly case to ever come up but:
            # if a default is given for a value that appears in the rule,
            # resolve it to a constant ahead of time
            if is_dynamic and data in defaults:
                data = self._converters[data].to_url(defaults[data])
                opl.append((False, data))
            elif not is_dynamic:
                # safe = https://url.spec.whatwg.org/#url-path-segment-string
                opl.append((False, quote(data, safe="!$&'()*+,/:;=@")))
            else:
                opl.append((True, data))
        def _convert(elem: str) -> ast.Call:
            ret = _prefix_names(_CALL_CONVERTER_CODE_FMT.format(elem=elem), ast.Call)
            ret.args = [ast.Name(elem, ast.Load())]
            return ret
        def _parts(ops: list[tuple[bool, str]]) -> list[ast.expr]:
            parts: list[ast.expr] = [
                _convert(elem) if is_dynamic else ast.Constant(elem)
                for is_dynamic, elem in ops
            ]
            parts = parts or [ast.Constant("")]
            # constant fold
            ret = [parts[0]]
            for p in parts[1:]:
                if isinstance(p, ast.Constant) and isinstance(ret[-1], ast.Constant):
                    ret[-1] = ast.Constant(ret[-1].value + p.value)  # type: ignore[operator]
                else:
                    ret.append(p)
            return ret
        dom_parts = _parts(dom_ops)
        url_parts = _parts(url_ops)
        body: list[ast.stmt]
        if not append_unknown:
            body = []
        else:
            body = [_IF_KWARGS_URL_ENCODE_AST]
            url_parts.extend(_URL_ENCODE_AST_NAMES)
        def _join(parts: list[ast.expr]) -> ast.expr:
            if len(parts) == 1:  # shortcut
                return parts[0]
            return ast.JoinedStr(parts)
        body.append(
            ast.Return(ast.Tuple([_join(dom_parts), _join(url_parts)], ast.Load()))
        )
        pargs = [
            elem
            for is_dynamic, elem in dom_ops + url_ops
            if is_dynamic and elem not in defaults
        ]
        kargs = [str(k) for k in defaults]
        func_ast = _prefix_names("def _(): pass", ast.FunctionDef)
        func_ast.name = f"<builder:{self.rule!r}>"
        func_ast.args.args.append(ast.arg(".self", None))
        for arg in pargs + kargs:
            func_ast.args.args.append(ast.arg(arg, None))
        func_ast.args.kwarg = ast.arg(".kwargs", None)
        for _ in kargs:
            func_ast.args.defaults.append(ast.Constant(""))
        func_ast.body = body
        # Use `ast.parse` instead of `ast.Module` for better portability, since the
        # signature of `ast.Module` can change.
        module = ast.parse("")
        module.body = [func_ast]
        # mark everything as on line 1, offset 0
        # less error-prone than `ast.fix_missing_locations`
        # bad line numbers cause an assert to fail in debug builds
        for node in ast.walk(module):
            if "lineno" in node._attributes:
                node.lineno = 1  # type: ignore[attr-defined]
            if "end_lineno" in node._attributes:
                node.end_lineno = node.lineno  # type: ignore[attr-defined]
            if "col_offset" in node._attributes:
                node.col_offset = 0  # type: ignore[attr-defined]
            if "end_col_offset" in node._attributes:
                node.end_col_offset = node.col_offset  # type: ignore[attr-defined]
        code = compile(module, "<werkzeug routing>", "exec")
        return self._get_func_code(code, func_ast.name)
    def build(
        self, values: t.Mapping[str, t.Any], append_unknown: bool = True
    ) -> tuple[str, str] | None:
        """Assembles the relative url for that rule and the subdomain.
        If building doesn't work for some reasons `None` is returned.
        :internal:
        """
        try:
            if append_unknown:
                return self._build_unknown(**values)
            else:
                return self._build(**values)
        except ValidationError:
            return None
    def provides_defaults_for(self, rule: Rule) -> bool:
        """Check if this rule has defaults for a given rule.
        :internal:
        """
        return bool(
            not self.build_only
            and self.defaults
            and self.endpoint == rule.endpoint
            and self != rule
            and self.arguments == rule.arguments
        )
    def suitable_for(
        self, values: t.Mapping[str, t.Any], method: str | None = None
    ) -> bool:
        """Check if the dict of values has enough data for url generation.
        :internal:
        """
        # if a method was given explicitly and that method is not supported
        # by this rule, this rule is not suitable.
        if (
            method is not None
            and self.methods is not None
            and method not in self.methods
        ):
            return False
        defaults = self.defaults or ()
        # all arguments required must be either in the defaults dict or
        # the value dictionary otherwise it's not suitable
        for key in self.arguments:
            if key not in defaults and key not in values:
                return False
        # in case defaults are given we ensure that either the value was
        # skipped or the value is the same as the default value.
        if defaults:
            for key, value in defaults.items():
                if key in values and value != values[key]:
                    return False
        return True
    def build_compare_key(self) -> tuple[int, int, int]:
        """The build compare key for sorting.
        :internal:
        """
        return (1 if self.alias else 0, -len(self.arguments), -len(self.defaults or ()))
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self._trace == other._trace
    __hash__ = None  # type: ignore
    def __str__(self) -> str:
        return self.rule
    def __repr__(self) -> str:
        if self.map is None:
            return f"<{type(self).__name__} (unbound)>"
        parts = []
        for is_dynamic, data in self._trace:
            if is_dynamic:
                parts.append(f"<{data}>")
            else:
                parts.append(data)
        parts_str = "".join(parts).lstrip("|")
        methods = f" ({', '.join(self.methods)})" if self.methods is not None else ""
        return f"<{type(self).__name__} {parts_str!r}{methods} -> {self.endpoint}>"
