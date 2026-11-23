# Contributeur de github.com/pallets/flask (BSD-3-Clause), anonymise.
# Commits de plus de 300 lignes exclus (reformatages, deplacements).
# Periode : AVANT juin 2021
__version__ = "2.0.2.dev0"
__version__ = "2.0.1"
    generator_or_function: t.Union[
        t.Iterator[t.AnyStr], t.Callable[..., t.Iterator[t.AnyStr]]
    ]
) -> t.Iterator[t.AnyStr]:
        .. versionchanged:: 2.0.1
            Registering the same blueprint with the same name multiple
            times is deprecated and will become an error in Flask 2.1.
        first_registration = not any(bp is self for bp in app.blueprints.values())
        if name in app.blueprints:
            existing_at = f" '{name}'" if self_name != name else ""
            if app.blueprints[name] is not self:
                raise ValueError(
                    f"The name '{self_name}' is already registered for"
                    f" a different blueprint{existing_at}. Use 'name='"
                    " to provide a unique name."
                )
            else:
                import warnings
                warnings.warn(
                    f"The name '{self_name}' is already registered for"
                    f" this blueprint{existing_at}. Use 'name=' to"
                    " provide a unique name. This will become an error"
                    " in Flask 2.1.",
                    stacklevel=4,
                )
    app.register_blueprint(bp, name="test2", url_prefix="/2", url_defaults={"bar": 19})
    with pytest.warns(UserWarning):
        app.register_blueprint(bp)  # same bp, same name, warning
    app.register_blueprint(bp, name="again")  # same bp, different name, ok
        app.register_blueprint(bp2)  # different bp, same name, error
    app.register_blueprint(bp2, name="alt")  # different bp, different name, ok
        .. versionchanged:: 2.0.1
            The ``name`` option can be used to change the (pre-dotted)
            name the blueprint is registered with. This allows the same
            blueprint to be registered multiple times with unique names
            for ``url_for``.
        .. versionchanged:: 2.0.1
            The ``name`` option can be used to change the (pre-dotted)
            name the blueprint is registered with. This allows the same
            blueprint to be registered multiple times with unique names
            for ``url_for``.
        .. versionchanged:: 2.0.1
            Nested blueprints are registered with their dotted name.
            This allows different blueprints with the same name to be
            nested at different locations.
        .. versionchanged:: 2.0.1
            The ``name`` option can be used to change the (pre-dotted)
            name the blueprint is registered with. This allows the same
            blueprint to be registered multiple times with unique names
            for ``url_for``.
from .helpers import _split_blueprint_path
            # This is called by url_for, which can be called outside a
            # request, can't use request.blueprints.
            bps = _split_blueprint_path(endpoint.rpartition(".")[0])
            bp_funcs = chain.from_iterable(self.url_default_functions[bp] for bp in bps)
            funcs = chain(funcs, bp_funcs)
from functools import lru_cache
@lru_cache(maxsize=None)
def _split_blueprint_path(name: str) -> t.List[str]:
    out: t.List[str] = [name]
    if "." in name:
        out.extend(_split_blueprint_path(name.rpartition(".")[0]))
    return out
from .helpers import _split_blueprint_path
        This will be ``None`` if matching failed or has not been
        performed yet.
        This in combination with :attr:`view_args` can be used to
        reconstruct the same URL or a modified URL.
        return None
        This will be ``None`` if the endpoint is not part of a
        blueprint, or if URL matching failed or has not been performed
        yet.
        This does not necessarily match the name the blueprint was
        created with. It may have been nested, or registered with a
        different name.
        endpoint = self.endpoint
        if endpoint is not None and "." in endpoint:
            return endpoint.rpartition(".")[0]
        return None
    @property
    def blueprints(self) -> t.List[str]:
        parent blueprints.
        This will be an empty list if there is no current blueprint, or
        if URL matching failed.
        .. versionadded:: 2.0.1
        name = self.blueprint
        if name is None:
            return []
        return _split_blueprint_path(name)
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
    def from_json(self, filename: str, silent: bool = False) -> bool:
        data is passed to the :meth:`from_mapping` method.
        :param filename: The path to the JSON file. This can be an
            absolute path or relative to the config root path.
        :param silent: Ignore the file if it doesn't exist.
        .. deprecated:: 2.0.0
            Will be removed in Flask 2.1. Use :meth:`from_file` instead.
            This was removed early in 2.0.0, was added back in 2.0.1.
        .. versionadded:: 0.11
        import warnings
        from . import json
        warnings.warn(
            "'from_json' is deprecated and will be removed in Flask"
            " 2.1. Use 'from_file(path, json.load)' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.from_file(filename, json.load, silent=silent)
    from _typeshed.wsgi import WSGIApplication  # noqa: F401
        # Match the request URL after loading the session, so that the
        # session is available in custom URL converters.
        if self.url_adapter is not None:
            self.match_request()
from flask import request
from flask import session
            assert request is not None
            assert session is not None
    @app.get("/<ctx:name>")
def test_open_session_with_endpoint():
    while loading the session, RequestContext.match_request() can be
    called manually.
        def save_session(self, app, session, response):
        def open_session(self, app, request):
            flask._request_ctx_stack.top.match_request()
    @app.get("/")
    def index():
        return "Hello, World!"
    response = app.test_client().get("/")
__version__ = "1.1.4"
__version__ = "1.1.3"
        "Werkzeug >= 0.15, < 2.0",
        "Jinja2 >= 2.10.1, < 3.0",
        "itsdangerous >= 0.24, < 2.0",
        "click >= 5.1, < 8.0",
__version__ = "1.1.3.dev0"
        if "." in name:
            raise ValueError("'name' may not contain a dot '.' character.")
        if endpoint and "." in endpoint:
            raise ValueError("'endpoint' may not contain a dot '.' character.")
        if view_func and hasattr(view_func, "__name__") and "." in view_func.__name__:
            raise ValueError("'view_func' name may not contain a dot '.' character.")
    bp = flask.Blueprint("foo", __name__, template_folder="template")
    app.inject_url_defaults("foo.view", values)
        url = flask.url_for("foo.view")
def test_dotted_name_not_allowed(app, client):
    with pytest.raises(ValueError):
        flask.Blueprint("app.ui", __name__)
    with pytest.raises(ValueError):
        bp.route("/", endpoint="a.b")(lambda: "")
    with pytest.raises(ValueError):
        bp.add_url_rule("/", endpoint="a.b")
    def view():
        return ""
    view.__name__ = "a.b"
    with pytest.raises(ValueError):
        bp.add_url_rule("/", view_func=view)
    import typing_extensions as te
    def raise_routing_exception(self, request: Request) -> "te.NoReturn":
    import typing_extensions as te
    def _fail(self, *args: t.Any, **kwargs: t.Any) -> "te.NoReturn":
    import typing_extensions as te
    def on_json_loading_failed(self, e: Exception) -> "te.NoReturn":
    # Define attr methods to let mypy know this is a namespace object
    # that has arbitrary attributes.
    def __getattr__(self, name: str) -> t.Any:
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(name) from None
    def __setattr__(self, name: str, value: t.Any) -> None:
        self.__dict__[name] = value
    def __delattr__(self, name: str) -> None:
        try:
            del self.__dict__[name]
        except KeyError:
            raise AttributeError(name) from None
    def __contains__(self, item: str) -> bool:
    def __iter__(self) -> t.Iterator[str]:
    from .ctx import _AppCtxGlobals
session: "SessionMixin" = LocalProxy(  # type: ignore
    partial(_lookup_req_object, "session")
)
g: "_AppCtxGlobals" = LocalProxy(partial(_lookup_app_object, "g"))  # type: ignore
from werkzeug.exceptions import abort as abort
from werkzeug.utils import redirect as redirect
from . import json as json
from .app import Flask as Flask
from .app import Request as Request
from .app import Response as Response
from .blueprints import Blueprint as Blueprint
from .config import Config as Config
from .ctx import after_this_request as after_this_request
from .ctx import copy_current_request_context as copy_current_request_context
from .ctx import has_app_context as has_app_context
from .ctx import has_request_context as has_request_context
from .globals import _app_ctx_stack as _app_ctx_stack
from .globals import _request_ctx_stack as _request_ctx_stack
from .globals import current_app as current_app
from .globals import g as g
from .globals import request as request
from .globals import session as session
from .helpers import flash as flash
from .helpers import get_flashed_messages as get_flashed_messages
from .helpers import get_template_attribute as get_template_attribute
from .helpers import make_response as make_response
from .helpers import safe_join as safe_join
from .helpers import send_file as send_file
from .helpers import send_from_directory as send_from_directory
from .helpers import stream_with_context as stream_with_context
from .helpers import url_for as url_for
from .json import jsonify as jsonify
from .signals import appcontext_popped as appcontext_popped
from .signals import appcontext_pushed as appcontext_pushed
from .signals import appcontext_tearing_down as appcontext_tearing_down
from .signals import before_render_template as before_render_template
from .signals import got_request_exception as got_request_exception
from .signals import message_flashed as message_flashed
from .signals import request_finished as request_finished
from .signals import request_started as request_started
from .signals import request_tearing_down as request_tearing_down
from .signals import signals_available as signals_available
from .signals import template_rendered as template_rendered
from .templating import render_template as render_template
from .templating import render_template_string as render_template_string
        url = f"{base_url}main/{text}"
        "click>=8.0",
__version__ = "2.1.0.dev0"
__version__ = "2.0.1.dev0"
__version__ = "2.0.0"
        rv.policies["json.dumps_function"] = json.dumps
from jinja2.utils import htmlsafe_json_dumps as _jinja_htmlsafe_dumps
    def get_source(  # type: ignore
    ) -> t.Tuple[str, t.Optional[str], t.Optional[t.Callable]]:
    ) -> t.Tuple[str, t.Optional[str], t.Optional[t.Callable]]:
        rv: t.Optional[t.Tuple[str, t.Optional[str], t.Optional[t.Callable[[], bool]]]]
        trv: t.Optional[
            t.Tuple[str, t.Optional[str], t.Optional[t.Callable[[], bool]]]
        ] = None
    ) -> t.Tuple[str, t.Optional[str], t.Optional[t.Callable]]:
        "Werkzeug>=2.0",
        "Jinja2>=3.0",
        "itsdangerous>=2.0",
autodoc_typehints = "description"
__version__ = "2.0.0rc2"
__version__ = "2.0.0rc1"
        "Werkzeug>=2.0.0rc4",
        "Jinja2>=3.0.0rc1",
        "itsdangerous>=2.0.0rc2",
        "click>=8.0.0rc1",
    .. deprecated:: 2.0
        Will be removed in Flask 2.1. Use
        :meth:`timedelta.total_seconds` instead.
    warnings.warn(
        "'total_seconds' is deprecated and will be removed in Flask"
        " 2.1. Use 'timedelta.total_seconds' instead.",
        DeprecationWarning,
        stacklevel=2,
    )
        max_age = int(app.permanent_session_lifetime.total_seconds())
class locked_cached_property(werkzeug.utils.cached_property):
    :class:`werkzeug.utils.cached_property` except access uses a lock
    for thread safety.
    .. versionchanged:: 2.0
        Inherits from Werkzeug's ``cached_property`` (and ``property``).
    def __init__(self, fget, name=None, doc=None):
        super().__init__(fget, name=name, doc=doc)
        with self.lock:
            return super().__get__(obj, type=type)
    def __set__(self, obj, value):
        with self.lock:
            super().__set__(obj, value)
    def __delete__(self, obj):
            super().__delete__(obj)
            " passed to the app factory function in Flask 2.1.",
            " single argument to the app factory function in Flask"
            " 2.1.",
            "The 'attachment_filename' parameter has been renamed to"
            " 'download_name'. The old name will be removed in Flask"
            " 2.1.",
            "The 'cache_timeout' parameter has been renamed to"
            " 'max_age'. The old name will be removed in Flask 2.1.",
            "The 'add_etags' parameter has been renamed to 'etag'. The"
            " old name will be removed in Flask 2.1.",
    .. versionchanged:: 2.0
        " Flask 2.1. Use 'werkzeug.utils.safe_join' instead.",
        ``encoding`` is deprecated and will be removed in Flask 2.1.
            "'encoding' is deprecated and will be removed in Flask 2.1.",
        deprecated and will be removed in Flask 2.1.
            " deprecated and will be removed in Flask 2.1.",
        ``encoding`` is deprecated and will be removed in Flask 2.1. The
        data must be a string or UTF-8 bytes.
            "'encoding' is deprecated and will be removed in Flask 2.1."
            " The data must be a string or UTF-8 bytes.",
        ``encoding`` is deprecated and will be removed in Flask 2.1. The
        file must be text mode, or binary mode with UTF-8 bytes.
            "'encoding' is deprecated and will be removed in Flask 2.1."
            " The file must be text mode, or binary mode with UTF-8"
            " bytes.",
    .. versionadded:: 2.0
    # Site, customize, or startup script can set a hook to call when
    # entering interactive mode. The default one sets up readline with
    # tab and history completion.
    interactive_hook = getattr(sys, "__interactivehook__", None)
    if interactive_hook is not None:
        try:
            import readline
            from rlcompleter import Completer
        except ImportError:
            pass
        else:
            # rlcompleter uses __main__.__dict__ by default, which is
            # flask.__main__. Use the shell context instead.
            readline.set_completer(Completer(ctx).complete)
        interactive_hook()
        Plain ``def`` functions are returned as-is. ``async def``
        functions are wrapped to run and wait for the response.
        Override this method to change how the app runs async views.
        .. versionadded:: 2.0
        this blueprint. Otherwise the app's
        :meth:`~flask.Flask.ensure_sync` is used.
    # Check that Werkzeug isn't using its fallback ContextVar class.
            "Async cannot be used with this combination of Python & Greenlet versions."
            This is required as the function must be awaited within the
            context. Only calling ``func`` (as per the
            ``copy_current_xxx_context`` functions) doesn't work as the
pytest.importorskip("asgiref")
    :param root_path: By default, the blueprint will automatically set
        this based on ``import_name``. In certain situations this
        automatic detection can fail, so the path can be specified
        manually instead.
    .. versionchanged:: 1.1.0
        Blueprints have a ``cli`` group to register nested CLI commands.
        The ``cli_group`` parameter controls the name of the group under
        the ``flask`` command.
    .. versionadded:: 0.7
                    "The blueprint was already registered once but is"
                    " getting modified now. These changes will not show"
                    " up."
        views and callbacks registered on the blueprint with the
        application. Creates a :class:`.BlueprintSetupState` and calls
        each :meth:`record` callbackwith it.
        :param app: The application this blueprint is being registered
            with.
        # Merge blueprint data into parent.
        if first_registration:
            def extend(bp_dict, parent_dict):
                for key, values in bp_dict.items():
                    key = self.name if key is None else f"{self.name}.{key}"
                    parent_dict[key].extend(values)
            def update(bp_dict, parent_dict):
                for key, value in bp_dict.items():
                    key = self.name if key is None else f"{self.name}.{key}"
                    parent_dict[key] = value
            app.view_functions.update(self.view_functions)
            extend(self.before_request_funcs, app.before_request_funcs)
            extend(self.after_request_funcs, app.after_request_funcs)
            extend(self.teardown_request_funcs, app.teardown_request_funcs)
            extend(self.url_default_functions, app.url_default_functions)
            extend(self.url_value_preprocessors, app.url_value_preprocessors)
            extend(self.template_context_processors, app.template_context_processors)
            update(self.error_handler_spec, app.error_handler_spec)
        cli_resolved_group = options.get("cli_group", self.cli_group)
            self.register_error_handler(code_or_exception, f)
        self.error_handler_spec[None][code][exc_class] = f
        WSGI application. This calls :meth:`wsgi_app`, which can be
        wrapped to apply middleware.
    #: Blueprint local JSON encoder class to use. Set to ``None`` to use
    #: the app's :class:`~flask.Flask.json_encoder`.
    #: Blueprint local JSON decoder class to use. Set to ``None`` to use
    #: the app's :class:`~flask.Flask.json_decoder`.
import importlib.util
    :param import_name: The import name of the module where this object
        is defined. Usually :attr:`__name__` should be used.
    :param static_folder: Path to a folder of static files to serve.
        If this is set, a static route will be added.
    :param static_url_path: URL prefix for the static route.
    :param template_folder: Path to a folder containing template files.
        for rendering. If this is set, a Jinja loader will be added.
    :param root_path: The path that static, template, and resource files
        are relative to. Typically not set, it is discovered based on
        the ``import_name``.
    .. versionadded:: 2.0.0
    #: JSON encoder class used by :func:`flask.json.dumps`. If a
    #: blueprint sets this, it will be used instead of the app's value.
    #: JSON decoder class used by :func:`flask.json.loads`. If a
    #: blueprint sets this, it will be used instead of the app's value.
        static_folder=None,
        #: A dictionary mapping endpoint names to view functions.
        #:
        #:
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        #: A data structure of registered error handlers, in the format
        #: ``{scope: {code: {class: handler}}}```. The ``scope`` key is
        #: the name of a blueprint the handlers are active for, or
        #: ``None`` for all requests. The ``code`` key is the HTTP
        #: status code for ``HTTPException``, or ``None`` for
        #: other exceptions. The innermost dictionary maps exception
        #: classes to handler functions.
        #:
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        #: A data structure of functions to call at the beginning of
        #: each request, in the format ``{scope: [functions]}``. The
        #: ``scope`` key is the name of a blueprint the functions are
        #: active for, or ``None`` for all requests.
        #:
        #: To register a function, use the :meth:`before_request`
        #:
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        #: A data structure of functions to call at the end of each
        #: request, in the format ``{scope: [functions]}``. The
        #: ``scope`` key is the name of a blueprint the functions are
        #: active for, or ``None`` for all requests.
        #:
        #: To register a function, use the :meth:`after_request`
        #: decorator.
        #:
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        #: A data structure of functions to call at the end of each
        #: request even if an exception is raised, in the format
        #: ``{scope: [functions]}``. The ``scope`` key is the name of a
        #: blueprint the functions are active for, or ``None`` for all
        #: requests.
        #: To register a function, use the :meth:`teardown_request`
        #: decorator.
        #:
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        #: A data structure of functions to call to pass extra context
        #: values when rendering templates, in the format
        #: ``{scope: [functions]}``. The ``scope`` key is the name of a
        #: blueprint the functions are active for, or ``None`` for all
        #: requests.
        #:
        #: To register a function, use the :meth:`context_processor`
        #: decorator.
        #:
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        #: A data structure of functions to call to modify the keyword
        #: arguments passed to the view function, in the format
        #: ``{scope: [functions]}``. The ``scope`` key is the name of a
        #: blueprint the functions are active for, or ``None`` for all
        #: requests.
        #:
        #: To register a function, use the
        #: :meth:`url_value_preprocessor` decorator.
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        #: A data structure of functions to call to modify the keyword
        #: arguments when generating URLs, in the format
        #: ``{scope: [functions]}``. The ``scope`` key is the name of a
        #: blueprint the functions are active for, or ``None`` for all
        #: requests.
        #: To register a function, use the :meth:`url_defaults`
        #: decorator.
        #:
        #: This data structure is internal. It should not be modified
        #: directly and its format may change at any time.
        rule and options. Calls :meth:`add_url_rule`, which has more
        details about the implementation.
                return "Hello, World!"
        See :ref:`url-route-registrations`.
        The endpoint name for the route defaults to the name of the view
        function if the ``endpoint`` parameter isn't passed.
        The ``methods`` parameter defaults to ``["GET"]``. ``HEAD`` and
        ``OPTIONS`` are added automatically.
        :param rule: The URL rule string.
        :param options: Extra options passed to the
        URLs. The :meth:`route` decorator is a shortcut to call this
        with the ``view_func`` argument. These are equivalent:
        .. code-block:: python
            @app.route("/")
            def index():
                ...
        .. code-block:: python
            def index():
                ...
            app.add_url_rule("/", view_func=index)
        See :ref:`url-route-registrations`.
        The endpoint name for the route defaults to the name of the view
        function if the ``endpoint`` parameter isn't passed. An error
        will be raised if a function has already been registered for the
        endpoint.
        The ``methods`` parameter defaults to ``["GET"]``. ``HEAD`` is
        always added automatically, and ``OPTIONS`` is added
        automatically by default.
        ``view_func`` does not necessarily need to be passed, but if the
        rule should participate in routing an endpoint name must be
        associated with a view function at some point with the
        :meth:`endpoint` decorator.
        .. code-block:: python
            app.add_url_rule("/", endpoint="index")
            @app.endpoint("index")
            def index():
                ...
        If ``view_func`` has a ``required_methods`` attribute, those
        methods are added to the passed and automatic methods. If it
        has a ``provide_automatic_methods`` attribute, it is used as the
        default if the parameter is not passed.
        :param rule: The URL rule string.
        :param endpoint: The endpoint name to associate with the rule
            and view function. Used when routing and building URLs.
            Defaults to ``view_func.__name__``.
        :param view_func: The view function to associate with the
            endpoint name.
        :param provide_automatic_options: Add the ``OPTIONS`` method and
            respond to ``OPTIONS`` requests automatically.
        :param options: Extra options passed to the
            :class:`~werkzeug.routing.Rule` object.
        endpoint. Used if a rule is added without a ``view_func`` with
        :meth:`add_url_rule`.
        .. code-block:: python
            app.add_url_rule("/ex", endpoint="example")
            @app.endpoint("example")
                ...
        :param endpoint: The endpoint name to associate with the view
            function.
        For example, this can be used to open a database connection, or
        to load the logged in user from the session.
        .. code-block:: python
            @app.before_request
            def load_user():
                if "user_id" in session:
                    g.user = db.session.get(session["user_id"])
        The function will be called without any arguments. If it returns
        a non-``None`` value, the value is handled as if it was the
        return value from the view, and further request handling is
        stopped.
        The function is called with the response object, and must return
        a response object. This allows the functions to modify or
        replace the response before it is sent.
        If a function raises an exception, any remaining
        ``after_request`` functions will not be called. Therefore, this
        should not be used for actions that must execute, such as to
        close resources. Use :meth:`teardown_request` for that.
        Teardown functions must avoid raising exceptions, since they . If they
        execute code that might fail they
from .scaffold import find_package
import os
import pkgutil
import sys
from jinja2 import FileSystemLoader
from .cli import AppGroup
from .globals import current_app
from .helpers import locked_cached_property
from .helpers import send_from_directory
                "A setup function was called after the first request "
                "was handled. This usually indicates a bug in the"
                " application where a module was not imported and"
                " decorators or other functionality was called too"
                " late.\nTo fix this make sure to import all your view"
                " modules, database models, and everything related at a"
                " central place before the application starts serving"
                " requests."
class Scaffold:
    :class:`~flask.blueprints.Blueprint`.
    name: str
    _static_folder = None
    _static_url_path = None
        #: The name of the package or module that this object belongs
        #: to. Do not change this once it is set by the constructor.
        self.import_name = import_name
        #: The path to the templates folder, relative to
        #: :attr:`root_path`, to add to the template loader. ``None`` if
        #: templates should not be added.
        self.template_folder = template_folder
        if root_path is None:
            root_path = get_root_path(self.import_name)
        #: Absolute path to the package on the filesystem. Used to look
        #: up resources contained in the package.
        self.root_path = root_path
        #: The Click command group for registering CLI commands for this
        #: object. The commands are available from the ``flask`` command
        #: once the application has been discovered and blueprints have
        #: been registered.
        self.cli = AppGroup()
    def __repr__(self):
        return f"<{type(self).__name__} {self.name!r}>"
    @property
    def static_folder(self):
        if no static folder is set.
        if self._static_folder is not None:
            return os.path.join(self.root_path, self._static_folder)
    @static_folder.setter
    def static_folder(self, value):
        if value is not None:
            value = os.fspath(value).rstrip(r"\/")
        self._static_folder = value
    @property
    def has_static_folder(self):
        .. versionadded:: 0.5
        return self.static_folder is not None
    @property
    def static_url_path(self):
        If it was not configured during init, it is derived from
        :attr:`static_folder`.
        if self._static_url_path is not None:
            return self._static_url_path
        if self.static_folder is not None:
            basename = os.path.basename(self.static_folder)
            return f"/{basename}".rstrip("/")
    @static_url_path.setter
    def static_url_path(self, value):
        if value is not None:
            value = value.rstrip("/")
        self._static_url_path = value
    def get_send_file_max_age(self, filename):
        value for a given file path if it wasn't passed.
        By default, this returns :data:`SEND_FILE_MAX_AGE_DEFAULT` from
        the configuration of :data:`~flask.current_app`. This defaults
        to ``None``, which tells the browser to use conditional requests
        instead of a timed cache, which is usually preferable.
        .. versionchanged:: 2.0
            The default configuration is ``None`` instead of 12 hours.
        .. versionadded:: 0.9
        value = current_app.send_file_max_age_default
        if value is None:
            return None
        return int(value.total_seconds())
    def send_static_file(self, filename):
        :attr:`static_folder`. A route is automatically registered for
        this view at :attr:`static_url_path` if :attr:`static_folder` is
        set.
        .. versionadded:: 0.5
        if not self.has_static_folder:
            raise RuntimeError("'static_folder' must be set to serve static_files.")
        # send_file only knows to call get_send_file_max_age on the app,
        # call it here so it works for blueprints too.
        max_age = self.get_send_file_max_age(filename)
        return send_from_directory(self.static_folder, filename, max_age=max_age)
    @locked_cached_property
    def jinja_loader(self):
        is a class :class:`jinja2.loaders.FileSystemLoader` to
        :attr:`template_folder` if it is set.
        .. versionadded:: 0.5
        if self.template_folder is not None:
            return FileSystemLoader(os.path.join(self.root_path, self.template_folder))
    def open_resource(self, resource, mode="rb"):
        reading.
        For example, if the file ``schema.sql`` is next to the file
        ``app.py`` where the ``Flask`` app is defined, it can be opened
        with:
        .. code-block:: python
            with app.open_resource("schema.sql") as f:
                conn.executescript(f.read())
        :param resource: Path to the resource relative to
            :attr:`root_path`.
        :param mode: Open the file in this mode. Only reading is
            supported, valid values are "r" (or "rt") and "rb".
        if mode not in {"r", "rt", "rb"}:
            raise ValueError("Resources can only be opened for reading.")
        return open(os.path.join(self.root_path, resource), mode)
        given URL rule. This does the same thing as :meth:`add_url_rule`
        but is used as a decorator. See :meth:`add_url_rule` and
        :ref:`url-route-registrations` for more information.
        .. code-block:: python
            @app.route("/")
                return "Hello World"
        :param rule: The URL rule as a string.
        :param options: The options to be forwarded to the underlying
            :class:`~werkzeug.routing.Rule` object.
def get_root_path(import_name):
    module. If it cannot be found, returns the current working
    directory.
    Not to be confused with the value returned by :func:`find_package`.
    :meta private:
    # Module already imported and has a file attribute. Use that first.
    mod = sys.modules.get(import_name)
    if mod is not None and hasattr(mod, "__file__"):
        return os.path.dirname(os.path.abspath(mod.__file__))
    # Next attempt: check the loader.
    loader = pkgutil.get_loader(import_name)
    # Loader does not exist or we're referring to an unloaded main
    # module or a main module without path (interactive sessions), go
    # with the current working directory.
    if loader is None or import_name == "__main__":
        return os.getcwd()
    if hasattr(loader, "get_filename"):
        filepath = loader.get_filename(import_name)
    else:
        # Fall back to imports.
        __import__(import_name)
        mod = sys.modules[import_name]
        filepath = getattr(mod, "__file__", None)
        # If we don't have a file path it might be because it is a
        # namespace package. In this case pick the root path from the
        # first module that is contained in the package.
        if filepath is None:
            raise RuntimeError(
                "No root path can be found for the provided module"
                f" {import_name!r}. This can happen because the module"
                " came from an import hook that does not provide file"
                " name information or because it's a namespace package."
                " In this case the root path needs to be explicitly"
                " provided."
            )
    # filepath is import_name.py for a module, or __init__.py for a package.
    return os.path.dirname(os.path.abspath(filepath))
def _matching_loader_thinks_module_is_package(loader, mod_name):
    :param: loader: The loader that handled the name.
    :param mod_name: The name of the package or module.
    # Use loader.is_package if it's available.
    if hasattr(loader, "is_package"):
        return loader.is_package(mod_name)
    cls = type(loader)
    # NamespaceLoader doesn't implement is_package, but all names it
    # loads must be packages.
    if cls.__module__ == "_frozen_importlib" and cls.__name__ == "NamespaceLoader":
        return True
    # Otherwise we need to fail with an error that explains what went
    # wrong.
    raise AttributeError(
        f"'{cls.__name__}.is_package()' must be implemented for PEP 302"
        f" import hooks."
    )
def _find_package_path(root_mod_name):
    try:
        spec = importlib.util.find_spec(root_mod_name)
        if spec is None:
            raise ValueError("not found")
    # ImportError: the machinery told us it does not exist
    # ValueError:
    #    - the module name was invalid
    #    - the module name is __main__
    #    - *we* raised `ValueError` due to `spec` being `None`
    except (ImportError, ValueError):
        pass  # handled below
    else:
        # namespace package
        if spec.origin in {"namespace", None}:
            return os.path.dirname(next(iter(spec.submodule_search_locations)))
        # a package (with __init__.py)
        elif spec.submodule_search_locations:
            return os.path.dirname(os.path.dirname(spec.origin))
        # just a normal module
        else:
            return os.path.dirname(spec.origin)
    # we were unable to find the `package_path` using PEP 451 loaders
    loader = pkgutil.get_loader(root_mod_name)
    if loader is None or root_mod_name == "__main__":
        # import name is not found, or interactive/main module
        return os.getcwd()
    if hasattr(loader, "get_filename"):
        filename = loader.get_filename(root_mod_name)
    elif hasattr(loader, "archive"):
        # zipimporter's loader.archive points to the .egg or .zip file.
        filename = loader.archive
    else:
        # At least one loader is missing both get_filename and archive:
        # Google App Engine's HardenedModulesHook, use __file__.
        filename = importlib.import_module(root_mod_name).__file__
    package_path = os.path.abspath(os.path.dirname(filename))
    # If the imported name is a package, filename is currently pointing
    # to the root of the package, need to get the current directory.
    if _matching_loader_thinks_module_is_package(loader, root_mod_name):
        package_path = os.path.dirname(package_path)
    return package_path
def find_package(import_name):
    that it would be imported from.
    The prefix is the directory containing the standard directory
    hierarchy (lib, bin, etc.). If the package is not installed to the
    system (:attr:`sys.prefix`) or a virtualenv (``site-packages``),
    ``None`` is returned.
    The path is the entry in :attr:`sys.path` that contains the package
    for import. If the package is not installed, it's assumed that the
    package was imported from the current working directory.
    root_mod_name, _, _ = import_name.partition(".")
    package_path = _find_package_path(root_mod_name)
    py_prefix = os.path.abspath(sys.prefix)
    # installed to the system
    if package_path.startswith(py_prefix):
        return py_prefix, package_path
    site_parent, site_folder = os.path.split(package_path)
    # installed to a virtualenv
    if site_folder.lower() == "site-packages":
        parent, folder = os.path.split(site_parent)
        # Windows (prefix/lib/site-packages)
        if folder.lower() == "lib":
            return parent, package_path
        # Unix (prefix/lib/pythonX.Y/site-packages)
        if os.path.basename(parent).lower() == "lib":
            return os.path.dirname(parent), package_path
        # something else (prefix/site-packages)
        return site_parent, package_path
    # not installed
    return None, package_path
        ProjectLink("Donate", "https://palletsprojects.com/donate"),
        ProjectLink("PyPI Releases", "https://pypi.org/project/Flask/"),
        ProjectLink("Website", "https://palletsprojects.com/p/flask/"),
        ProjectLink("Twitter", "https://twitter.com/PalletsTeam"),
        ProjectLink("Chat", "https://discord.gg/pallets"),
        rv.policies["json.dumps_function"] = json.dumps
from jinja2.utils import htmlsafe_json_dumps as _jinja_htmlsafe_dumps
    replace HTML-unsafe characters with Unicode escapes and mark the
    result safe with :class:`~markupsafe.Markup`.
    This is available in templates as the ``|tojson`` filter.
    .. versionchanged:: 2.0
        Uses :func:`jinja2.utils.htmlsafe_json_dumps`. The returned
        value is marked safe by wrapping in :class:`~markupsafe.Markup`.
    return _jinja_htmlsafe_dumps(obj, dumps=dumps, **kwargs)
def test_tojson_filter(app, req_ctx):
    # The tojson filter is tested in Jinja, this confirms that it's
    # using Flask's dumps.
    rv = flask.render_template_string(
        "const data = {{ data|tojson }};",
        data={"name": "</script>", "time": datetime.datetime(2021, 2, 1, 7, 15)},
    )
    assert rv == (
        'const data = {"name": "\\u003c/script\\u003e",'
        ' "time": "Mon, 01 Feb 2021 07:15:00 GMT"};'
    jinja_options = {}
main()
def main():
    cli.main(args=sys.argv[1:])
    main()
        server_error = InternalServerError(original_exception=e)
        if isinstance(e, BadRequestKeyError) and (
            self.debug or self.config["TRAP_BAD_REQUEST_ERRORS"]
        ):
            e.show_exception = True
    etag=None,
    add_etags=None,
    if add_etags is not None:
        warnings.warn(
            "The 'add_etags' parameter has been renamed to 'etag'. The old name will be"
            " removed in Flask 2.1.",
            DeprecationWarning,
            stacklevel=3,
        )
        etag = add_etags
        etag=etag,
    etag=True,
    add_etags=None,
    :param etag: Calculate an ETag for the file, which requires passing
        a file path. Can also be a string to use instead.
    .. versionchanged:: 2.0.0
        ``etag`` replaces the ``add_etags`` parameter. It can be a
        string to use instead of generating one.
            etag=etag,
from werkzeug.wrappers import Response as BaseResponse
from werkzeug.wrappers import Request as BaseRequest
        See :attr:`~werkzeug.wrappers.Response.max_cookie_size` in
class Request(RequestBase):
    json_module = json
    def on_json_loading_failed(self, e):
        if current_app and current_app.debug:
            raise BadRequest(f"Failed to decode JSON object: {e}")
        raise BadRequest()
class Response(ResponseBase):
    json_module = json
    if value is None or isinstance(value, timedelta):
        return value
    return timedelta(seconds=value)
    #: A :class:`~datetime.timedelta` or number of seconds which is used
    #: as the default ``max_age`` for :func:`send_file`. The default is
    #: ``None``, which tells the browser to use conditional requests
    #: instead of a timed cache.
    #: Configured with the :data:`SEND_FILE_MAX_AGE_DEFAULT`
    #: configuration key.
    #:
    #: .. versionchanged:: 2.0
    #:     Defaults to ``None`` instead of 12 hours.
            "SEND_FILE_MAX_AGE_DEFAULT": None,
import warnings
import werkzeug.utils
def _prepare_send_file_kwargs(
    download_name=None,
    attachment_filename=None,
    max_age=None,
    cache_timeout=None,
    **kwargs,
):
    if attachment_filename is not None:
        warnings.warn(
            "The 'attachment_filename' parameter has been renamed to 'download_name'."
            " The old name will be removed in Flask 2.1.",
            DeprecationWarning,
            stacklevel=3,
        )
        download_name = attachment_filename
    if cache_timeout is not None:
        warnings.warn(
            "The 'cache_timeout' parameter has been renamed to 'max_age'. The old name"
            " will be removed in Flask 2.1.",
            DeprecationWarning,
            stacklevel=3,
        )
        max_age = cache_timeout
    if max_age is None:
        max_age = current_app.get_send_file_max_age
    kwargs.update(
        environ=request.environ,
        download_name=download_name,
        max_age=max_age,
        use_x_sendfile=current_app.use_x_sendfile,
        response_class=current_app.response_class,
        _root_path=current_app.root_path,
    )
    return kwargs
    path_or_file,
    download_name=None,
    conditional=True,
    max_age=None,
    cache_timeout=None,
    The first argument can be a file path or a file-like object. Paths
    are preferred in most cases because Werkzeug can manage the file and
    get extra information from the path. Passing a file-like object
    requires that the file is opened in binary mode, and is mostly
    useful when building a file in memory with :class:`io.BytesIO`.
    Never pass file paths provided by a user. The path is assumed to be
    trusted, so a user could craft a path to access a file you didn't
    intend. Use :func:`send_from_directory` to safely serve
    user-requested paths from within a directory.
    If the WSGI server sets a ``file_wrapper`` in ``environ``, it is
    used, otherwise Werkzeug's built-in wrapper is used. Alternatively,
    if the HTTP server supports ``X-Sendfile``, configuring Flask with
    ``USE_X_SENDFILE = True`` will tell the server to send the given
    path, which is much more efficient than reading it in Python.
    :param path_or_file: The path to the file to send, relative to the
        current working directory if a relative path is given.
        Alternatively, a file-like object opened in binary mode. Make
        sure the file pointer is seeked to the start of the data.
    :param mimetype: The MIME type to send for the file. If not
        provided, it will try to detect it from the file name.
    :param as_attachment: Indicate to a browser that it should offer to
        save the file instead of displaying it.
    :param download_name: The default name browsers will use when saving
        the file. Defaults to the passed file name.
    :param conditional: Enable conditional and range responses based on
        request headers. Requires passing a file path and ``environ``.
    :param add_etags: Calculate an ETag for the file. Requires passing a
        file path.
    :param last_modified: The last modified time to send for the file,
        in seconds. If not provided, it will try to detect it from the
        file path.
    :param max_age: How long the client should cache the file, in
        seconds. If set, ``Cache-Control`` will be ``public``, otherwise
        it will be ``no-cache`` to prefer conditional caching.
    .. versionchanged:: 2.0
        ``download_name`` replaces the ``attachment_filename``
        parameter. If ``as_attachment=False``, it is passed with
        ``Content-Disposition: inline`` instead.
    .. versionchanged:: 2.0
        ``max_age`` replaces the ``cache_timeout`` parameter.
        ``conditional`` is enabled and ``max_age`` is not set by
        default.
    .. versionadded:: 2.0
        Moved the implementation to Werkzeug. This is now a wrapper to
        pass some Flask-specific arguments.
        UTF-8 filenames as specified in :rfc:`2231` are supported.
        The filename is no longer automatically inferred from file
        objects. If you want to use automatic MIME and etag support,
        pass a filename via ``filename_or_fp`` or
        ``attachment_filename``.
        ``attachment_filename`` is preferred over ``filename`` for MIME
        detection.
        ``cache_timeout`` defaults to
        :meth:`Flask.get_send_file_max_age`.
        MIME guessing and etag support for file-like objects was
        deprecated because it was unreliable. Pass a filename if you are
        able to, otherwise attach an etag yourself.
    .. versionchanged:: 0.5
        The ``add_etags``, ``cache_timeout`` and ``conditional``
        parameters were added. The default behavior is to add etags.
    return werkzeug.utils.send_file(
        **_prepare_send_file_kwargs(
            path_or_file=path_or_file,
            environ=request.environ,
            mimetype=mimetype,
            as_attachment=as_attachment,
            download_name=download_name,
            attachment_filename=attachment_filename,
            conditional=conditional,
            add_etags=add_etags,
            last_modified=last_modified,
            max_age=max_age,
            cache_timeout=cache_timeout,
        )
    directory to avoid escaping the base directory.
    :param directory: The trusted base directory.
    :param pathnames: The untrusted path components relative to the
        base directory.
    :return: A safe path, otherwise ``None``.
    warnings.warn(
        "'flask.helpers.safe_join' is deprecated and will be removed in"
        " 2.1. Use 'werkzeug.utils.safe_join' instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    path = werkzeug.utils.safe_join(directory, *pathnames)
    if path is None:
        raise NotFound()
    return path
def send_from_directory(directory, path, **kwargs):
    .. code-block:: python
        @app.route("/uploads/<path:name>")
        def download_file(name):
            return send_from_directory(
                app.config['UPLOAD_FOLDER'], name, as_attachment=True
            )
    This is a secure way to serve files from a folder, such as static
    files or uploads. Uses :func:`~werkzeug.security.safe_join` to
    ensure the path coming from the client is not maliciously crafted to
    point outside the specified directory.
    If the final path does not point to an existing regular file,
    raises a 404 :exc:`~werkzeug.exceptions.NotFound` error.
    :param directory: The directory that ``path`` must be located under.
    :param path: The path to the file to send, relative to
        ``directory``.
    :param kwargs: Arguments to pass to :func:`send_file`.
    .. versionadded:: 2.0
        Moved the implementation to Werkzeug. This is now a wrapper to
        pass some Flask-specific arguments.
    return werkzeug.utils.send_from_directory(
        directory, path, **_prepare_send_file_kwargs(**kwargs)
    )
        value for a given file path if it wasn't passed.
        By default, this returns :data:`SEND_FILE_MAX_AGE_DEFAULT` from
        the configuration of :data:`~flask.current_app`. This defaults
        to ``None``, which tells the browser to use conditional requests
        instead of a timed cache, which is usually preferable.
        .. versionchanged:: 2.0
            The default configuration is ``None`` instead of 12 hours.
        value = current_app.send_file_max_age_default
        if value is None:
            return None
        return total_seconds(value)
        # send_file only knows to call get_send_file_max_age on the app,
        # call it here so it works for blueprints too.
        max_age = self.get_send_file_max_age(filename)
        return send_from_directory(self.static_folder, filename, max_age=max_age)
def test_default_static_max_age(app):
    def test_send_file(self, app, req_ctx):
        # Default max_age is None.
        assert rv.cache_control.max_age is None
        # Test with direct use of send_file.
        assert rv.cache_control.max_age is None
        assert rv.cache_control.max_age == 3600
        # Test with direct use of send_file.
        assert rv.cache_control.max_age == 3600
        # Test with pathlib.Path.
        assert rv.cache_control.max_age == 3600
            assert rv.cache_control.max_age == 10
            # Test with direct use of send_file.
            assert rv.cache_control.max_age == 10
from copy import copy
from werkzeug.wrappers import BaseRequest
    def open(
        self, *args, as_tuple=False, buffered=False, follow_redirects=False, **kwargs
    ):
        # Same logic as super.open, but apply environ_base and preserve_context.
        request = None
        def copy_environ(other):
            return {
                **self.environ_base,
                **other,
                "flask._preserve_context": self.preserve_context,
            }
        if not kwargs and len(args) == 1:
            arg = args[0]
            if isinstance(arg, werkzeug.test.EnvironBuilder):
                builder = copy(arg)
                builder.environ_base = copy_environ(builder.environ_base or {})
                request = builder.get_request()
            elif isinstance(arg, dict):
                request = EnvironBuilder.from_environ(
                    arg, app=self.application, environ_base=copy_environ({})
                ).get_request()
            elif isinstance(arg, BaseRequest):
                request = copy(arg)
                request.environ = copy_environ(request.environ)
        if request is None:
            kwargs["environ_base"] = copy_environ(kwargs.get("environ_base", {}))
                request = builder.get_request()
        return super().open(
            request,
    rv = client.get("/", query_string={"foo": "정상처리"}, charset="euc-kr")
    assert rv.get_data(as_text=True) == "정상처리"
    python_implementation() != "CPython",
    reason="Requires CPython GC behavior",
from flask import json
def test_html_method():
    class ObjectWithHTML:
        def __html__(self):
            return "<p>test</p>"
    result = json.dumps(ObjectWithHTML())
    assert result == '"<p>test</p>"'
class Response(JSONMixin, ResponseBase):
        # Look up built-in and plugin commands, which should be
        # available even if the app fails to load.
        rv = super().get_command(ctx, name)
        # Look up commands provided by the app, showing an error and
        # continuing if the app couldn't be loaded.
            return info.load_app().cli.get_command(ctx, name)
        except NoAppException as e:
            click.secho(f"Error: {e.format_message()}\n", err=True, fg="red")
        # Start with the built-in and plugin commands.
        rv = set(super().list_commands(ctx))
        # Add commands provided by the app, showing an error and
        # continuing if the app couldn't be loaded.
        except NoAppException as e:
            # When an app couldn't be loaded, show the error message
            # without the traceback.
            click.secho(f"Error: {e.format_message()}\n", err=True, fg="red")
            # When any other errors occurred during loading, show the
            # full traceback.
            click.secho(f"{traceback.format_exc()}\n", err=True, fg="red")
    monkeypatch.syspath_prepend(os.path.join(os.path.dirname(__file__), "test_apps"))
    original_modules = set(sys.modules.keys())
    yield
    # Remove any imports cached during the test. Otherwise "import app"
    # will work in the next test even though it's no longer on the path.
    for key in sys.modules.keys() - original_modules:
        sys.modules.pop(key)
def test_locate_app_suppress_raise(test_apps):
def test_no_command_echo_loading_error():
    from flask.cli import cli
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["missing"])
    assert result.exit_code == 2
    assert "FLASK_APP" in result.stderr
    assert "Usage:" in result.stderr
def test_help_echo_loading_error():
    from flask.cli import cli
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "FLASK_APP" in result.stderr
    assert "Usage:" in result.stdout
def test_help_echo_exception():
    cli = FlaskGroup(create_app=create_app)
    runner = CliRunner(mix_stderr=False)
    assert "Exception: oh no" in result.stderr
    assert "Usage:" in result.stdout
    extras_require={"dotenv": ["python-dotenv"]},
def call_factory(script_info, app_factory, args=None, kwargs=None):
    sig = inspect.signature(app_factory)
    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    if "script_info" in sig.parameters:
        kwargs["script_info"] = script_info
    if (
        not args
        and len(sig.parameters) == 1
        and next(iter(sig.parameters.values())).default is inspect.Parameter.empty
    ):
            " single argument to the app factory function in 2.1.",
        args.append(script_info)
    return app_factory(*args, **kwargs)
def _called_with_wrong_args(f):
    :param f: The function that was called.
    :return: ``True`` if the call failed.
            if tb.tb_frame.f_code is f.__code__:
                # In the function, it was called successfully.
        # Didn't reach the function.
        # Delete tb to break a circular reference.
    # Parse app_name as a single expression to determine if it's a valid
    # attribute name or function call.
    try:
        expr = ast.parse(app_name.strip(), mode="eval").body
    except SyntaxError:
            f"Failed to parse {app_name!r} as an attribute name or function call."
    if isinstance(expr, ast.Name):
        name = expr.id
        args = kwargs = None
    elif isinstance(expr, ast.Call):
        # Ensure the function name is an attribute name only.
        if not isinstance(expr.func, ast.Name):
            raise NoAppException(
                f"Function reference must be a simple name: {app_name!r}."
            )
        name = expr.func.id
        # Parse the positional and keyword arguments as literals.
        try:
            args = [ast.literal_eval(arg) for arg in expr.args]
            kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in expr.keywords}
        except ValueError:
            # literal_eval gives cryptic error messages, show a generic
            # message with the full expression instead.
            raise NoAppException(
                f"Failed to parse arguments as literal values: {app_name!r}."
            )
    else:
        raise NoAppException(
            f"Failed to parse {app_name!r} as an attribute name or function call."
        )
    except AttributeError:
        raise NoAppException(
            f"Failed to find attribute {name!r} in {module.__name__!r}."
        )
    # If the attribute is a function, call it with any args and kwargs
    # to get the real application.
            app = call_factory(script_info, attr, args, kwargs)
        except TypeError:
                f"The factory {app_name!r} in module"
import warnings
    if "script_info" in args_spec.args:
        warnings.warn(
            "The 'script_info' argument is deprecated and will not be"
            " passed to the app factory function in 2.1.",
            DeprecationWarning,
        )
    elif not arguments and len(args_spec.args) == 1 and args_spec.defaults is None:
        warnings.warn(
            "Script info is deprecated and will not be passed as the"
            " first argument to the app factory function in 2.1.",
            DeprecationWarning,
        )
    a function to get the app instance, or return the variable directly.
    app = find_best_app(script_info, Module)
    assert isinstance(app, Flask)
    assert app.name == "appname"
    with pytest.deprecated_call(match="Script info"):
        app = find_best_app(script_info, Module)
    assert isinstance(app, Flask)
    assert app.name == "appname"
    with pytest.deprecated_call(match="script_info"):
        app = find_best_app(script_info, Module)
    assert isinstance(app, Flask)
    assert app.name == "appname"
    app = find_best_app(script_info, Module)
    assert isinstance(app, Flask)
    assert app.name == "appname"
    def create_app():
    obj = ScriptInfo(create_app=lambda: Flask("testapp"))
    obj = ScriptInfo(create_app=lambda: Flask("testappgroup"))
    def create_app():
    def create_app():
    def create_app():
        def create_app():
        def create_app():
    built-in :class:`json.JSONEncoder`.
    -   :class:`datetime.datetime` and :class:`datetime.date` are
        serialized to :rfc:`822` strings. This is the same as the HTTP
        date format.
    -   :class:`uuid.UUID` is serialized to a string.
    -   :class:`dataclasses.dataclass` is passed to
        :func:`dataclasses.asdict`.
    -   :class:`~markupsafe.Markup` (or any object with a ``__html__``
        method) will call the ``__html__`` method to get a string.
    Assign a subclass of this to :attr:`flask.Flask.json_encoder` or
    :attr:`flask.Blueprint.json_encoder` to override the default.
        :meth:`json.JSONEncoder.default`. Python does not support
        overriding how basic types like ``str`` or ``list`` are
        serialized, they are handled before this method.
    This does not change any behavior from the built-in
    :class:`json.JSONDecoder`.
    Assign a subclass of this to :attr:`flask.Flask.json_decoder` or
    :attr:`flask.Blueprint.json_decoder` to override the default.
    Takes the same arguments as the built-in :func:`json.dumps`, with
    some defaults from application configuration.
    :param app: Use this app's config instead of the active app context
        or defaults.
    :param kwargs: Extra arguments passed to func:`json.dumps`.
    .. versionchanged:: 2.0
        ``encoding`` is deprecated and will be removed in 2.1.
    .. versionchanged:: 1.0.3
    Takes the same arguments as the built-in :func:`json.dump`, with
    some defaults from application configuration.
    :param obj: Object to serialize to JSON.
    :param fp: File object to write JSON to.
    :param app: Use this app's config instead of the active app context
        or defaults.
    :param kwargs: Extra arguments passed to func:`json.dump`.
    .. versionchanged:: 2.0
        Writing to a binary file, and the ``encoding`` argument, is
        deprecated and will be removed in 2.1.
    Takes the same arguments as the built-in :func:`json.loads`, with
    some defaults from application configuration.
    :param app: Use this app's config instead of the active app context
        or defaults.
    :param kwargs: Extra arguments passed to func:`json.dump`.
    .. versionchanged:: 2.0
        ``encoding`` is deprecated and will be removed in 2.1. The data
        must be a string or UTF-8 bytes.
    .. versionchanged:: 1.0.3
    Takes the same arguments as the built-in :func:`json.load`, with
    some defaults from application configuration.
    :param fp: File object to read JSON from.
    :param app: Use this app's config instead of the active app context
        or defaults.
    :param kwargs: Extra arguments passed to func:`json.load`.
    .. versionchanged:: 2.0
        ``encoding`` is deprecated and will be removed in 2.1. The file
        must be text mode, or binary mode with UTF-8 bytes.
    characters with Unicode escapes. Otherwise behaves the same as
    :func:`dumps`.
    This is available in templates as the ``|tojson`` filter, which will
    also mark the result with ``|safe``.
    The returned string is safe to render in HTML documents and
    ``<script>`` tags. The exception is in HTML attributes that are
    double quoted; either use single quotes or the ``|forceescape``
    filter.
        Single quotes are escaped, making this safe to use in HTML,
        ``<script>`` tags, and single-quoted attributes without further
        escaping.
    HTML-unsafe characters with Unicode escapes. See
    :func:`htmlsafe_dumps` and :func:`dumps`.
    with the :mimetype:`application/json` mimetype.
    Uses :func:`dumps` to serialize the data, but ``args`` and
    ``kwargs`` are treated as data rather than arguments to
    :func:`json.dumps`.
    1.  Single argument: Treated as a single value.
    2.  Multiple arguments: Treated as a list of values.
        ``jsonify(1, 2, 3)`` is the same as ``jsonify([1, 2, 3])``.
    3.  Keyword arguments: Treated as a dict of values.
        ``jsonify(data=data, errors=errors)`` is the same as
        ``jsonify({"data": data, "errors": errors})``.
    4.  Passing both arguments and keyword arguments is not allowed as
        it's not clear what should happen.
    .. code-block:: python
        @app.route("/users/me")
            return jsonify(
                username=g.user.username,
                email=g.user.email,
                id=g.user.id,
            )
    Will return a JSON response like this:
    .. code-block:: javascript
          "username": "admin",
          "email": "admin@localhost",
          "id": 42
    The default output omits indents and spaces after separators. In
    debug mode or if :data:`JSONIFY_PRETTYPRINT_REGULAR` is ``True``,
    the output will be formatted to be easier to read.
        a security risk in ancient browsers. See :ref:`security-json`.
from markupsafe import Markup
    deserializes to an instance of :class:`~markupsafe.Markup`."""
    * :class:`~markupsafe.Markup`
import warnings
from markupsafe import Markup
        return super().default(self, o)
        cls = bp.json_encoder if bp and bp.json_encoder else app.json_encoder
        kwargs.setdefault("cls", cls)
        kwargs.setdefault("ensure_ascii", app.config["JSON_AS_ASCII"])
        cls = bp.json_decoder if bp and bp.json_decoder else app.json_decoder
        kwargs.setdefault("cls", cls)
    if encoding is not None:
        warnings.warn(
            "'encoding' is deprecated and will be removed in 2.1.",
            DeprecationWarning,
            stacklevel=2,
        )
        if isinstance(rv, str):
            return rv.encode(encoding)
    show_warning = encoding is not None
    try:
        fp.write("")
    except TypeError:
        show_warning = True
        fp = io.TextIOWrapper(fp, encoding or "utf-8")
    if show_warning:
        warnings.warn(
            "Writing to a binary file, and the 'encoding' argument, is"
            " deprecated and will be removed in 2.1.",
            DeprecationWarning,
            stacklevel=2,
        )
    if encoding is not None:
        warnings.warn(
            "'encoding' is deprecated and will be removed in 2.1. The"
            " data must be a string or UTF-8 bytes.",
            DeprecationWarning,
            stacklevel=2,
        )
        if isinstance(s, bytes):
            s = s.decode(encoding)
    if encoding is not None:
        warnings.warn(
            "'encoding' is deprecated and will be removed in 2.1. The"
            " file must be text mode, or binary mode with UTF-8 bytes.",
            DeprecationWarning,
            stacklevel=2,
        )
        if isinstance(fp.read(0), bytes):
            fp = io.TextIOWrapper(fp, encoding)
    fp.write(htmlsafe_dumps(obj, **kwargs))
import json as _json
    the default decoder.  Consult the :mod:`json` documentation
    does some extra configuration based on the application.
    does some extra configuration based on the application.
    encoding = kwargs.pop("encoding", None)
    if encoding is not None and isinstance(s, bytes):
    encoding = kwargs.pop("encoding", None)
    fp = _wrap_reader_for_text(fp, encoding or "utf-8")
_htmlsafe_map = str.maketrans(
    {"<": "\\u003c", ">": "\\u003e", "&": "\\u0026", "'": "\\u0027"}
)
    return dumps(obj, **kwargs).translate(_htmlsafe_map)
setup()
setup()
# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
from markupsafe import escape
from markupsafe import Markup
        Instead, see :doc:`/deploying/index` for WSGI server recommendations.
        about unit testing head over to :doc:`/testing`.
    See :doc:`/blueprints` for more information.
    instance of this. see :ref:`custom-scripts`.
    See :ref:`url-building`.
      :data:`PREFERRED_URL_SCHEME` if no request context is available.
      This also can be set to an empty string to build protocol-relative
      URLs.
    See :doc:`/patterns/flashing` for examples.
        Added support for serializing top-level arrays. This introduces
        a security risk in ancient browsers. See :ref:`security-json`
        for details.
    Basic usage is outlined in the :doc:`/testing` chapter.
from .cli import main
main(as_module=True)
A compact representation for lossless serialization of non-standard JSON
types. :class:`~flask.sessions.SecureCookieSessionInterface` uses this
to serialize the session data, but it may be useful in other places. It
can be extended to support other types.
Let's see an example that adds support for
:class:`~collections.OrderedDict`. Dicts don't have an order in JSON, so
to handle this we will dump the items as a list of ``[key, value]``
pairs. Subclass :class:`JSONTag` and give it the new key ``' od'`` to
identify the type. The session serializer processes dicts first, so
insert the new tag at the front of the order since ``OrderedDict`` must
be processed before ``dict``.
.. code-block:: python
                f"{self.static_url_path}/<path:filename>",
        return os.path.join(prefix, "var", f"{self.name}-instance")
                "A name collision occurred between blueprints"
                f" {blueprint!r} and {self.blueprints[blueprint.name]!r}."
                f" Both share the same name {blueprint.name!r}."
                f" Blueprints that are created on the fly need unique"
                f" names."
                    "View function mapping is overwriting an existing"
                    f" endpoint function: {endpoint}"
                "Tried to register a handler for an exception instance"
                f" {code_or_exception!r}. Handlers can only be"
                " registered for exception classes or HTTP error codes."
                f"'{code_or_exception}' is not a recognized HTTP error"
                " code. Use a subclass of HTTPException with that code"
                " instead."
                    e.description = f"KeyError: {e.args[0]!r}"
                f"The view function for {request.endpoint!r} did not"
                " return a valid response. The function either returned"
                " None or ended without a return statement."
                        f"{e}\nThe view function did not return a valid"
                        " response. The return type must be a string,"
                        " dict, tuple, Response instance, or WSGI"
                        f" callable, but it was a {type(rv).__name__}."
                    " response. The return type must be a string,"
                    " dict, tuple, Response instance, or WSGI"
                    f" callable, but it was a {type(rv).__name__}."
        return f"<{type(self).__name__} {self.name!r}>"
                f"{self.static_url_path}/<path:filename>",
            "Detected multiple Flask applications in module"
            f" {module.__name__!r}. Use 'FLASK_APP={module.__name__}:name'"
            f" to specify the correct one."
    for attr_name in {"create_app", "make_app"}:
                    f"Detected factory {attr_name!r} in module {module.__name__!r},"
                    " but could not call it without arguments. Use"
                    f" \"FLASK_APP='{module.__name__}:{attr_name}(args)'\""
                    " to specify arguments."
        "Failed to find Flask application or factory in module"
        f" {module.__name__!r}. Use 'FLASK_APP={module.__name__}:name'"
        " to specify one."
            f"{app_name!r} is not a valid variable name or function expression."
            except (ValueError, SyntaxError):
                raise NoAppException(f"Could not parse the arguments in {app_name!r}.")
                f"{e}\nThe factory {app_name!r} in module"
                f" {module.__name__!r} could not be called with the"
                " specified arguments."
        "A valid Flask application was not obtained from"
        f" '{module.__name__}:{app_name}'."
                f"While importing {module_name!r}, an ImportError was"
                f" raised:\n\n{traceback.format_exc()}"
            raise NoAppException(f"Could not import {module_name!r}.")
        f"Python {platform.python_version()}\n"
        f"Flask {__version__}\n"
        f"Werkzeug {werkzeug.__version__}",
        message = f" * Serving Flask app {app_import_path!r}"
            "   WARNING: This is a development server. Do not use it in"
            " a production deployment.",
        click.echo(f" * Debug mode: {'on' if debug else 'off'}")
        f" are separated by {os.path.pathsep!r}."
    banner = (
        f"Python {sys.version} on {sys.platform}\n"
        f"App: {app.import_name} [{app.env}]\n"
        f"Instance: {app.instance_path}"
                f"The environment variable {variable_name!r} is not set"
                " and as such configuration could not be loaded. Set"
                " this variable and make it point to a configuration"
                " file"
            e.strerror = f"Unable to load configuration file ({e.strerror})"
            e.strerror = f"Unable to load configuration file ({e.strerror})"
                f"expected at most 1 positional argument, got {len(mapping)}"
        return f"<{type(self).__name__} {dict.__repr__(self)}>"
            return f"<flask.g of {top.app.name!r}>"
        return (
            f"<{type(self).__name__} {self.request.url!r}"
            f" [{self.request.method}] of {self.app.name}>"
            f"You tried to access the file {key!r} in the request.files"
            " dictionary but it does not exist. The mimetype for the"
            f" request is {request.mimetype!r} instead of"
            " 'multipart/form-data' which means that no file contents"
            " were transmitted. To fix this error you should provide"
            ' enctype="multipart/form-data" in your form.'
            names = ", ".join(repr(x) for x in form_matches)
                f"This was submitted: {names}"
            f"A request was sent to this URL ({request.url}) but a"
            " redirect was issued automatically by the routing system"
            f" to {exc.new_url!r}."
        if f"{request.base_url}/" == exc.new_url.split("?")[0]:
                "  The URL was defined with a trailing slash so Flask"
                " will automatically redirect to the URL with the"
                " trailing slash if it was accessed without one."
            "  Make sure to directly send your"
            f" {request.method}-request to this URL since we can't make"
            " browsers or HTTP clients redirect with form data reliably"
            " or without user interaction."
    yield f"class: {type(loader).__module__}.{type(loader).__name__}"
            yield f"{key}:"
                yield f"  - {item}"
    info = [f"Locating template {template!r}:"]
            src_info = f"application {srcobj.import_name!r}"
            src_info = f"blueprint {srcobj.name!r} ({srcobj.import_name})"
        info.append(f"{idx + 1:5}: trying loader of {src_info}")
            info.append(f"       {line}")
            detail = f"found ({triple[1] or '<string>'!r})"
        info.append(f"       -> {detail}")
            "  The template was looked up from an endpoint that belongs"
            f" to the blueprint {blueprint!r}."
                "Silently ignoring app.run() because the application is"
                " run from the flask command line executable. Consider"
                ' putting app.run() behind an if __name__ == "__main__"'
                " guard to silence this warning."
                endpoint = f"{blueprint_name}{endpoint}"
        rv += f"#{url_quote(anchor)}"
            quoted = url_quote(attachment_filename, safe="")
                "filename*": f"UTF-8''{quoted}",
            check = (
                adler32(
                    filename.encode("utf-8") if isinstance(filename, str) else filename
                & 0xFFFFFFFF
            )
            rv.set_etag(
                f"{os.path.getmtime(filename)}-{os.path.getsize(filename)}-{check}"
                f"Access {filename} failed, maybe it does not exist, so"
                " ignore etags in headers",
                "No root path can be found for the provided module"
                f" {import_name!r}. This can happen because the module"
                " came from an import hook that does not provide file"
                " name information or because it's a namespace package."
                " In this case the root path needs to be explicitly"
                " provided."
    cls = type(loader)
    elif cls.__module__ == "_frozen_importlib" and cls.__name__ == "NamespaceLoader":
        f"{cls.__name__}.is_package() method is missing but is required"
        " for PEP 302 import hooks."
            return f"/{basename}".rstrip("/")
        f"{dumps(data, indent=indent, separators=separators)}\n",
        return {f"{key}__": self.serializer.tag(value[key])}
            # Chrome doesn't allow names without a '.'. This should only
            # come up with localhost. Hack around this by not setting
            # the name, and show a warning.
                f"{rv!r} is not a valid cookie domain, it must contain"
                " a '.'. Add an entry to your hosts file, for example"
                f" '{rv}.localdomain', and use that instead."
            rv = f".{rv}"
            base_url = (
                f"{url.scheme or url_scheme}://{url.netloc or http_host}"
                f"/{app_root.lstrip('/')}"
            "HTTP_USER_AGENT": f"werkzeug/{werkzeug.__version__}",
                return f"Hello {name}!"
        assert meth is not None, f"Unimplemented method {request.method!r}"
            if name in {"archive", "get_filename"}:
                raise AttributeError(f"Mocking a loader which does not have {name!r}.")
        .mkdir(f"python{sys.version_info.major}.{sys.version_info.minor}")
                f"""
                from setuptools import setup
                setup(
                    name="{name}",
                    version="1.0",
                    packages=["site_egg"],
                    zip_safe=True,
    assert "'localhost' is not a valid cookie domain" in str(w.message)
        assert "This was submitted: 'index.txt'" in str(e.value)
        return f"index for {user}"
        return f"index for {user}"
        return f"{bar}/{baz:d}"
    assert f"Python {python_version()}" in out
    assert f"Flask {flask_version}" in out
    assert f"Werkzeug {werkzeug_version}" in out
    obj = ScriptInfo(app_import_path=f"{cli_app_path}:testapp")
    assert result.output == f"{not set_debug_flag}\n"
    assert result.exit_code == 2, f"Unexpected success:\n\n{result.output}"
    app.config.from_pyfile(f"{__file__.rsplit('.', 1)[0]}.py")
        "os.environ", {"FOO_SETTINGS": f"{__file__.rsplit('.', 1)[0]}.py"}
            f"""
            # -*- coding: {encoding} -*-
            TEST_VALUE = "föö"
                    return f"<{o.val}>"
        class X:
            __slots__ = ("val",)
                    return f"<{o.val}>"
        assert f"filename={ascii}" in content_disposition
            assert f"filename*=UTF-8''{utf8}" in content_disposition
                return f"Get {id:d}"
        return f"Hello {flask.request.args['name']}!"
        return f"Hello {flask.request.args['name']}!"
            assert "1: trying loader of application 'blueprintapp'" in text
                "2: trying loader of blueprint 'admin' (blueprintapp.apps.admin)"
                "trying loader of blueprint 'frontend' (blueprintapp.apps.frontend)"
                "looked up from an endpoint that belongs to the blueprint 'frontend'"
    assert flask.g.user_agent == f"werkzeug/{werkzeug.__version__}"
        return f"Hello, {flask.request.json['name']}!"
            return f"wrapped {type(original).__name__}"
            return f"wrapped {type(original).__name__}"
        return f"direct {type(e).__name__}"
html_title = f"Flask Documentation ({version})"
latex_documents = [(master_doc, f"Flask-{version}.tex", html_title, author, "manual")]
        url = f"{base_url}master/{text}"
        url = f"{base_url}{release}/{text}"
from js_example import views  # noqa: F401
    return render_template(f"{js}.html", js=js)
with open("README.rst", encoding="utf8") as f:
            error = f"User {username} is already registered."
        abort(404, f"Post id {id} doesn't exist.")
with open("README.rst", encoding="utf8") as f:
class AuthActions:
    class Recorder:
with open("README.rst", encoding="utf8") as f:
with open("src/flask/__init__.py", encoding="utf8") as f:
        **options,
        methods = {item.upper() for item in methods}
                "Tried to register a handler for an exception instance {!r}."
                "'{}' is not a recognized HTTP error code. Use a subclass of"
            f"Exception on {request.path} [{request.method}]", exc_info=exc_info
        return f"<{self.__class__.__name__} {self.name!r}>"
class BlueprintSetupState:
            f"{self.blueprint.name}.{endpoint}",
            **options,
                args = ast.literal_eval(f"({args},)")
            raise NoAppException(f'Could not import "{module_name}".')
class DispatchingApp:
class ScriptInfo:
        **extra,
        return super().main(*args, **kwargs)
        message = f' * Serving Flask app "{app_import_path}"'
    click.echo(f" * Environment: {env}")
        click.echo(" * Debug mode: {}".format("on" if debug else "off"))
        super_convert = super().convert
    banner = "Python {} on {}\nApp: {} [{}]\nInstance: {}".format(
        sys.version, sys.platform, app.import_name, app.env, app.instance_path,
        with open(startup) as f:
class ConfigAttribute:
        except OSError as e:
        except OSError as e:
        return "<{} {}>".format(self.__class__.__name__, dict.__repr__(self))
class _AppCtxGlobals:
class AppContext:
        assert rv is self, f"Popped wrong app context.  ({rv!r} instead of {self!r})"
class RequestContext:
            assert (
                rv is self
            ), f"Popped wrong request context. ({rv!r} instead of {self!r})"
        return "<{} '{}' [{}] of {}>".format(
    yield "class: {}.{}".format(type(loader).__module__, type(loader).__name__)
        yield f"{key}: {value!r}"
            src_info = f'blueprint "{srcobj.name}" ({srcobj.import_name})'
                yield from gen
class locked_cached_property:
class _PackageBoundObject:
        except OSError:
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("'", "\\u0027")
class JSONTag:
        return {k: self.serializer.tag(v) for k, v in value.items()}
class TaggedJSONSerializer:
                raise KeyError(f"Tag '{key}' is already registered.")
        super().__init__(initial, on_update)
        return super().__getitem__(key)
        return super().get(key, default)
        return super().setdefault(key, default)
class SessionInterface:
    class Namespace:
    class _FakeSignal:
        **kwargs,
                http_host = f"{subdomain}.{http_host}"
        super().__init__(path, base_url, *args, **kwargs)
        super().__init__(*args, **kwargs)
        super().__init__(**kwargs)
        return super().invoke(cli, args, **kwargs)
class View:
        super().__init__(name, bases, d)
            raise BadRequest(f"Failed to decode JSON object: {e}")
        return super().max_cookie_size
    class LimitedLoader:
        setup(name='{}',
        (egg_path,) = modules_tmpdir.join("dist/").listdir()
    class CustomRequestGlobals:
        return ""
    class PrefixPathMiddleware:
        flask.flash("Hello World")
        flask.flash("Hello World", "error")
        flask.flash(flask.Markup("<em>Testing</em>"), "warning")
            "Hello World",
            "Hello World",
            flask.Markup("<em>Testing</em>"),
            ("message", "Hello World"),
            ("error", "Hello World"),
            ("warning", flask.Markup("<em>Testing</em>")),
        assert list(messages) == [("message", "Hello World")]
            ("message", "Hello World"),
            ("warning", flask.Markup("<em>Testing</em>")),
        assert messages[0] == "Hello World"
        assert messages[1] == flask.Markup("<em>Testing</em>")
        return "Hällo Wörld"
        return "Hällo Wörld".encode()
    assert client.get("/text").data == "Hällo Wörld".encode()
    assert client.get("/bytes").data == "Hällo Wörld".encode()
    @app.route("/киртест")
    rv = client.get("/киртест")
    class View:
        rv["result"] = f"running on {hostname}:{port} ..."
    assert rv["result"] == f"running on {hostname}:{port} ..."
    class MockCtx:
    class Base:
    # -*- coding: {} -*-
    assert value == "föö"
            base_to_url = super().to_url
class FakePath:
class TestJSON:
        "value", (1, "t", True, False, None, [], [1, 2, 3], {}, {"foo": "🐍"})
        "test_value,expected", [(True, '"\\u2603"'), (False, '"\u2603"')]
        rv = flask.json.dumps("\N{SNOWMAN}")
            url = f"/datetest{i}"
        assert rv == '"\\u003c/script\\u003e"'
        class X:  # noqa: B903, for Python2 compatibility
        class X:  # noqa: B903, for Python2 compatibility
        rv = client.get("/?foo=정상처리".encode("euc-kr"))
        assert rv.data == "정상처리".encode()
class PyBytesIO:
class TestSendfile:
            lambda app: io.StringIO("Test"),
                "Ñandú／pingüino.txt",
            ("Vögel.txt", "Vogel.txt", "V%C3%B6gel.txt"),
            ("те:/ст", '":/"', "%D1%82%D0%B5%3A%2F%D1%81%D1%82"),
class TestUrlFor:
class TestNoImports:
class TestStreaming:
        class Wrapper:
class TestSafeJoin:
class TestHelpers:
    class Foo:  # noqa: B903, for Python2 compatibility
class assert_no_leak:
class TestGreenletContextCopying:
                return super().get_cookie_name(app)
    environ["HTTP_HOST"] = "\x8a"
    environ["HTTP_HOST"] = "ąśźäüжŠßя.com"
                '2: trying loader of blueprint "admin" (blueprintapp.apps.admin)'
                'trying loader of blueprint "frontend" (blueprintapp.apps.frontend)'
                'looked up from an endpoint that belongs to the blueprint "frontend"'
    eb = EnvironBuilder(app, json="\u20ac")
    assert eb.input_stream.read().decode("utf8") == '"\u20ac"'
    class Namespace:
    class NS:
class TestGenericHandlers:
            if isinstance(obj, ssl.SSLContext):
                return obj
        clear_request = False
            fsize = file.getbuffer().nbytes
    import importlib.util
    try:
        spec = importlib.util.find_spec(root_mod_name)
        if spec is None:
            raise ValueError("not found")
    # ImportError: the machinery told us it does not exist
    # ValueError:
    #    - the module name was invalid
    #    - the module name is __main__
    #    - *we* raised `ValueError` due to `spec` being `None`
    except (ImportError, ValueError):
        pass  # handled below
    else:
        # namespace package
        if spec.origin in {"namespace", None}:
            return os.path.dirname(next(iter(spec.submodule_search_locations)))
        # a package (with __init__.py)
        elif spec.submodule_search_locations:
            return os.path.dirname(os.path.dirname(spec.origin))
        # just a normal module
            return os.path.dirname(spec.origin)
    rv = client.open("/", method="OPTIONS")
    rv = client.open("/more", method="OPTIONS")
    with pytest.raises(click.BadParameter):
        run_command.make_context("run", ["--cert", "flask"])
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
import platform
@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="CPython only")
    with assert_no_leak():
        for _x in range(10):
            fire()
        assert flask.session.get("data") == "foo"
        if isinstance(methods, str):
                "Allowed methods must be a list of strings, for"
                ' example: @app.route(..., methods=["POST"])'
        if isinstance(exc_class_or_code, int):
            raise
        exc_info = sys.exc_info()
            # Re-raise if called with an active exception, otherwise
            # raise the passed in exception.
            if exc_info[1] is e:
                raise
            raise e
        self.log_exception(exc_info)
            if isinstance(rv, (str, bytes, bytearray)):
                    raise TypeError(
                    ).with_traceback(sys.exc_info()[2])
            if isinstance(status, (str, bytes, bytearray)):
        :meth:`url_for`.
                # make error available outside except block
            else:
                if rv is not None:
                    return rv
        # Re-raise if called with an active exception, otherwise raise
        # the passed in exception.
        if error is sys.exc_info()[1]:
            raise
    matches = [v for v in module.__dict__.values() if isinstance(v, Flask)]
    args_spec = inspect.getfullargspec(app_factory)
        if sys.exc_info()[2].tb_next:
            raise exc_info
    is_context = ssl and isinstance(cert, ssl.SSLContext)
        if isinstance(obj, str):
        for k, v in self.items():
            if not all(isinstance(x, str) for x in value):
        elif not isinstance(value, (str, int, float, bool)):
        filename_or_fp = os.fspath(filename_or_fp)
    if isinstance(filename_or_fp, str):
        if not isinstance(attachment_filename, str):
                "filename*": "UTF-8''%s" % url_quote(attachment_filename, safe=""),
                        if isinstance(filename, str)
    filename = os.fspath(filename)
    directory = os.fspath(directory)
    # Python < 3.7
            return str(o.__html__())
    if encoding is not None and isinstance(rv, str):
    fp = _wrap_reader_for_text(fp, kwargs.pop("encoding", None) or "utf-8")
    fp.write(str(htmlsafe_dumps(obj, **kwargs)))
        return dict((k, self.serializer.tag(v)) for k, v in value.items())
        return str(value.__html__())
from collections.abc import MutableMapping
class SessionMixin(MutableMapping):
class MethodView(View, metaclass=MethodViewType):
        return str(flask.session.permanent)
        return str(bar)
            return flask.jsonify(foo=str(flask.request.get_json()))
        out = io.StringIO()
            return str(json["a"] + json["b"])
        assert type(rv) is str
class PyBytesIO(object):
            lambda app: PyBytesIO(b"Test"),
            lambda app: open(os.path.join(app.static_folder, "index.html")),
from io import StringIO
from io import StringIO
        return str(flask.session["foo"])
    python_requires=">=3.6",
__version__ = "2.0.0.dev"
@pytest.mark.xfail(reason="weird interaction with tox")
@pytest.mark.xfail(reason="weird interaction with tox")
@pytest.mark.xfail(reason="weird interaction with tox")
    :param root_path: The path to the root of the application files.
        This should only be set manually when it can't be detected
        automatically, such as for namespace packages.
            ``str``
            ``bytes``
        # rightmost part. This needs to go through a helper function
        # because of namespace packages.
__version__ = "1.1.2"
            Will be removed in 2.0. Use
            ``session_interface.open_session`` instead.
                '"open_session" is deprecated and will be removed in'
                ' 2.0. Use "session_interface.open_session" instead.'
            Will be removed in 2.0. Use
            ``session_interface.save_session`` instead.
                '"save_session" is deprecated and will be removed in'
                ' 2.0. Use "session_interface.save_session" instead.'
            Will be removed in 2.0. Use
            ``session_interface.make_null_session`` instead.
                '"make_null_session" is deprecated and will be removed'
                ' in 2.0. Use "session_interface.make_null_session"'
                " instead."
        Will be removed in 2.0. Construct
        ``flask.testing.EnvironBuilder`` directly instead.
            '"make_test_environ_builder()" is deprecated and will be'
            ' removed in 2.0. Construct "flask.testing.EnvironBuilder"'
            " directly instead."
                    import cryptography  # noqa: F401
                        "Using ad-hoc certificates requires the cryptography library.",
                        ctx,
                        param,
        is_context = ssl and isinstance(cert, ssl.SSLContext)
    monkeypatch.setitem(sys.modules, "cryptography", None)
    # cryptography not installed
    # cryptography installed
    monkeypatch.setitem(sys.modules, "cryptography", types.ModuleType("cryptography"))
@pytest.mark.xfail(reason="TODO: weird interaction with tox")
__version__ = "1.2.0.dev0"
    When passing a file-like object instead of a filename, only binary
    mode is supported (``open(filename, "rb")``, :class:`~io.BytesIO`,
    etc.). Text mode files and :class:`~io.StringIO` will raise a
    :exc:`ValueError`.
    .. versionchanged:: 2.0
        Passing a file-like object that inherits from
        :class:`~io.TextIOBase` will raise a :exc:`ValueError` rather
        than sending an empty file.
    .. versionchanged:: 1.1
        ``filename`` may be a :class:`~os.PathLike` object.
    .. versionchanged:: 1.1
        Passing a :class:`~io.BytesIO` object supports range requests.
    .. versionchanged:: 1.0.3
        Filenames are encoded with ASCII instead of Latin-1 for broader
        compatibility with WSGI servers.
    .. versionchanged:: 1.0
        UTF-8 filenames, as specified in `RFC 2231`_, are supported.
    .. _RFC 2231: https://tools.ietf.org/html/rfc2231#section-4
       The filename is no longer automatically inferred from file
       objects. If you want to use automatic MIME and etag support, pass
       a filename via ``filename_or_fp`` or ``attachment_filename``.
       ``attachment_filename`` is preferred over ``filename`` for MIME
    .. versionchanged:: 0.9
       ``cache_timeout`` defaults to
       :meth:`Flask.get_send_file_max_age`.
    .. versionchanged:: 0.7
       MIME guessing and etag support for file-like objects was
       deprecated because it was unreliable. Pass a filename if you are
       able to, otherwise attach an etag yourself. This functionality
       will be removed in Flask 1.0.
    .. versionadded:: 0.5
       The ``add_etags``, ``cache_timeout`` and ``conditional``
       parameters were added. The default behavior is to add etags.
    .. versionadded:: 0.2
    :param filename_or_fp: The filename of the file to send, relative to
        :attr:`~Flask.root_path` if a relative path is specified.
        Alternatively, a file-like object opened in binary mode. Make
        sure the file pointer is seeked to the start of the data.
        ``X-Sendfile`` will only be used with filenames.
        elif isinstance(file, io.TextIOBase):
            raise ValueError("Files must be opened in binary mode or use BytesIO.")
    if fsize is not None:
        headers["Content-Length"] = fsize
from flask._compat import PY2
class PyStringIO(object):
    def __init__(self, *args, **kwargs):
        self._io = io.BytesIO(*args, **kwargs)
    def __getattr__(self, name):
        return getattr(self._io, name)
                io.BytesIO(b"party like it's"),
            flask.send_file(io.BytesIO(b"LOL"))
        flask.send_file(io.BytesIO(b"LOL"), attachment_filename="filename")
    @pytest.mark.parametrize(
        "opener",
        [
            lambda app: open(os.path.join(app.static_folder, "index.html"), "rb"),
            lambda app: io.BytesIO(b"Test"),
            pytest.param(
                lambda app: StringIO("Test"),
                marks=pytest.mark.skipif(not PY2, reason="Python 2 only"),
            ),
            lambda app: PyStringIO(b"Test"),
        ],
    )
    @pytest.mark.usefixtures("req_ctx")
    def test_send_file_object(self, app, opener):
        file = opener(app)
        rv = flask.send_file(file, mimetype="text/plain")
        assert rv.data
        assert "x-sendfile" not in rv.headers
    @pytest.mark.parametrize(
        "opener",
        [
            lambda app: io.StringIO(u"Test"),
            pytest.param(
                lambda app: open(os.path.join(app.static_folder, "index.html")),
                marks=pytest.mark.skipif(PY2, reason="Python 3 only"),
            ),
        ],
    )
    @pytest.mark.usefixtures("req_ctx")
    def test_send_file_text_fails(self, app, opener):
        file = opener(app)
        with pytest.raises(ValueError):
            flask.send_file(file, mimetype="text/plain")
        file.close()
            with open(os.path.join(app.root_path, "static/index.html"), "rb") as f:
        with open(os.path.join(app.root_path, "static/index.html"), "rb") as f:
            io.BytesIO(b"Test"),
    "--eager-loading/--lazy-loading",
    def __init__(self, loader, use_eager_loading=None):
        if use_eager_loading is None:
            use_eager_loading = os.environ.get("WERKZEUG_RUN_MAIN") != "true"
        using the ``load`` parameter. The loaded data is passed to the
        :meth:`from_mapping` method.
        .. code-block:: python
            import toml
            app.config.from_file("config.toml", load=toml.load)
        :param filename: The path to the data file. This can be an
            absolute path or relative to the config root path.
        :param load: A callable that takes a file handle and returns a
            mapping of loaded data from the file.
        :type load: ``Callable[[Reader], Mapping]`` where ``Reader``
            implements a ``read`` method.
        :param silent: Ignore the file if it doesn't exist.
            with open(filename) as f:
                obj = load(f)
        data is passed to the :meth:`from_mapping` method.
        :param filename: The path to the JSON file. This can be an
            absolute path or relative to the config root path.
        :param silent: Ignore the file if it doesn't exist.
        .. deprecated:: 1.2
            Use :meth:`from_file` with :meth:`json.load` instead.
            "'from_json' is deprecated and will be removed in 2.0."
            " Use 'from_file(filename, load=json.load)' instead.",
            DeprecationWarning,
            stacklevel=2,
        from .json import load
        return self.from_file(filename, load, silent=silent)
import packaging.version
from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink
project = "Flask"
copyright = "2010 Pallets"
author = "Pallets"
release, version = get_version("Flask")
master_doc = "index"
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "pallets_sphinx_themes",
    "sphinx_issues",
    "python": ("https://docs.python.org/3/", None),
    "werkzeug": ("https://werkzeug.palletsprojects.com/", None),
    "click": ("https://click.palletsprojects.com/", None),
    "jinja": ("http://jinja.pocoo.org/docs/", None),
    "itsdangerous": ("https://itsdangerous.palletsprojects.com/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/", None),
    "wtforms": ("https://wtforms.readthedocs.io/en/stable/", None),
    "blinker": ("https://pythonhosted.org/blinker/", None),
issues_github_path = "pallets/flask"
html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
    "project_links": [
        ProjectLink("Donate to Pallets", "https://palletsprojects.com/donate"),
        ProjectLink("Flask Website", "https://palletsprojects.com/p/flask/"),
        ProjectLink("PyPI releases", "https://pypi.org/project/Flask/"),
        ProjectLink("Source Code", "https://github.com/pallets/flask/"),
        ProjectLink("Issue Tracker", "https://github.com/pallets/flask/issues/"),
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_static_path = ["_static"]
html_favicon = "_static/flask-icon.png"
html_logo = "_static/flask-icon.png"
html_title = "Flask Documentation ({})".format(version)
    (master_doc, "Flask-{}.tex".format(version), html_title, author, "manual")
def github_link(name, rawtext, text, lineno, inliner, options=None, content=None):
    base_url = "https://github.com/pallets/flask/tree/"
    if text.endswith(">"):
        words, text = text[:-1].rsplit("<", 1)
    if packaging.version.parse(release).is_devrelease:
        url = "{0}master/{1}".format(base_url, text)
        url = "{0}{1}/{2}".format(base_url, release, text)
    app.add_role("gh", github_link)
__version__ = "1.1.2.dev"
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    cli.main(args=sys.argv[1:], prog_name="python -m flask" if as_module else None)
__version__ = "1.1.2.dev"
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    cli.main(args=sys.argv[1:], prog_name="python -m flask" if as_module else None)
        "Documentation": "https://flask.palletsprojects.com/",
__version__ = "1.1.1"
from ._compat import json_available
__version__ = "1.1.1.dev"
class _DeprecatedBool(object):
    def __init__(self, name, version, value):
        self.message = "'{}' is deprecated and will be removed in version {}.".format(
            name, version
        )
        self.value = value
    def _warn(self):
        import warnings
        warnings.warn(self.message, DeprecationWarning, stacklevel=2)
    def __eq__(self, other):
        self._warn()
        return other == self.value
    def __ne__(self, other):
        self._warn()
        return other != self.value
    def __bool__(self):
        self._warn()
        return self.value
    __nonzero__ = __bool__
json_available = _DeprecatedBool("flask.json_available", "2.0.0", True)
import pytest
from flask import json_available
def test_json_available():
    with pytest.deprecated_call() as rec:
        assert json_available
        assert json_available == True  # noqa E712
        assert json_available != False  # noqa E712
    assert len(rec.list) == 3
__version__ = "1.1.0"
__version__ = '1.0.4'
        "Programming Language :: Python :: 3.7",
import warnings
def _has_config(logger):
    its properties against the defaults.
    :param logger: The :class:`~logging.Logger` to inspect.
    return (
        logger.level != logging.NOTSET
        or logger.handlers
        or logger.filters
        or not logger.propagate
    )
    # 1.1.0 changes name of logger, warn if config is detected for old
    # name and not new name
    for old_name in ("flask.app", "flask"):
        old_logger = logging.getLogger(old_name)
        if _has_config(old_logger) and not _has_config(logger):
            warnings.warn(
                "'app.logger' is named '{name}' for this application,"
                " but configuration was found for '{old_name}', which"
                " no longer has an effect. The logging configuration"
                " should be moved to '{name}'.".format(name=app.name, old_name=old_name)
            )
            break
    if app.debug and not logger.level:
def test_warn_old_config(app, request):
    old_logger = logging.getLogger("flask.app")
    old_logger.setLevel(logging.DEBUG)
    request.addfinalizer(lambda: old_logger.setLevel(logging.NOTSET))
    with pytest.warns(UserWarning):
        assert app.logger.getEffectiveLevel() == logging.WARNING
        the same name as :attr:`name`.
        In debug mode, the logger's :attr:`~logging.Logger.level` will
        be set to :data:`~logging.DEBUG`.
        If there are no handlers configured, a default handler will be
        added. See :doc:`/logging` for more information.
        .. versionchanged:: 1.1.0
            The logger takes the same name as :attr:`name` rather than
            hard-coding ``"flask.app"``.
        .. versionchanged:: 1.0.0
            ``"flask.app"``. The level is only set during configuration,
            it doesn't check ``app.debug`` each time. Only one format is
            used, not different ones depending on ``app.debug``. No
            handlers are removed, and a handler is only added if no
            handlers are already configured.
    The logger name will be the same as
    :attr:`app.import_name <flask.Flask.name>`.
    logger = logging.getLogger(app.name)
    logger = logging.getLogger("flask_test")
    assert app.logger.name == "flask_test"
        monkeypatch.setattr(
            logging.getLogger("blueprintapp"), "handlers", [_TestHandler()]
        )
                'filename*': "UTF-8''%s" % url_quote(attachment_filename, safe=b""),
        # ":/" are not safe in filename* value
        (u"те:/ст", '":/"', "%D1%82%D0%B5%3A%2F%D1%81%D1%82"),
__version__ = '1.0.4.dev'
                e.show_exception = True
                # TODO: clean up once Werkzeug >= 0.15.5 is required
                if e.args[0] not in e.get_description():
            elif not hasattr(BadRequestKeyError, "show_exception"):
from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink
copyright = "2010 Pallets"
author = "Pallets"
    "sphinx_issues",
    "werkzeug": ("https://werkzeug.palletsprojects.com/", None),
issues_github_path = "pallets/flask"
html_favicon = "_static/flask-icon.png"
html_logo = "_static/flask-icon.png"
    (master_doc, "Flask-{}.tex".format(version), html_title, author, "manual")
from setuptools import find_packages
with io.open("README.rst", "rt", encoding="utf8") as f:
with io.open("flask/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)
    name="Flask",
    url="https://palletsprojects.com/p/flask/",
    project_urls={
        "Documentation": "http://flask.palletsprojects.com/",
        "Code": "https://github.com/pallets/flask",
        "Issue tracker": "https://github.com/pallets/flask/issues",
    },
    license="BSD-3-Clause",
    author="Armin Ronacher",
    author_email="armin.ronacher@active-4.com",
    maintainer="Pallets",
    maintainer_email="contact@palletsprojects.com",
    description="A simple framework for building complex web applications.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
        "Werkzeug>=0.14",
        "Jinja2>=2.10",
        "itsdangerous>=0.24",
        "click>=5.1",
        "dotenv": ["python-dotenv"],
        "dev": [
            "pytest",
            "coverage",
            "tox",
            "sphinx",
            "pallets-sphinx-themes",
            "sphinxcontrib-log-cabinet",
            "sphinx-issues",
        "docs": [
            "sphinx",
            "pallets-sphinx-themes",
            "sphinxcontrib-log-cabinet",
            "sphinx-issues",
    entry_points={"console_scripts": ["flask = flask.cli:main"]},
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
:copyright: 2010 Pallets
:license: BSD-3-Clause
:copyright: 2010 Pallets
:license: BSD-3-Clause
:copyright: 2010 Pallets
:license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
:copyright: 2010 Pallets
:license: BSD-3-Clause
:copyright: 2010 Pallets
:license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
:copyright: 2010 Pallets
:license: BSD-3-Clause
    :copyright: 2010 Pallets
    :license: BSD-3-Clause
            always have an ``original_exception`` attribute. Use
        associated with it, or that was raised from an error handler.
        This always causes a 500 ``InternalServerError``.
        Always sends the :data:`got_request_exception` signal.
        If :attr:`propagate_exceptions` is ``True``, such as in debug
        mode, the error will be re-raised so that the debugger can
        display it. Otherwise, the original exception is logged, and
        an :exc:`~werkzeug.exceptions.InternalServerError` is returned.
        If an error handler is registered for ``InternalServerError`` or
        ``500``, it will be used. For consistency, the handler will
        always receive the ``InternalServerError``. The original
        unhandled exception is available as ``e.original_exception``.
        .. note::
            Prior to Werkzeug 1.0.0, ``InternalServerError`` will not
            always have a ``original_exception`` attribute. Use
            ``getattr(e, "original_exception", None)`` to simulate the
            behavior for compatibility.
        .. versionchanged:: 1.1.0
            Always passes the ``InternalServerError`` instance to the
            handler, setting ``original_exception`` to the unhandled
            error.
        .. versionchanged:: 1.1.0
            ``after_request`` functions and other finalization is done
            even for the default 500 response when there is no handler.
        server_error = InternalServerError()
        # TODO: pass as param when Werkzeug>=1.0.0 is required
        # TODO: also remove note about this from docstring and docs
        server_error.original_exception = e
        handler = self._find_error_handler(server_error)
        if handler is not None:
            server_error = handler(server_error)
        return self.finalize_request(server_error, from_error_handler=True)
import pytest
        assert isinstance(e, InternalServerError)
        original = getattr(e, "original_exception", None)
        if original is not None:
            return "wrapped " + type(original).__name__
        return "direct"
    @app.route("/abort")
    def do_abort():
        flask.abort(500)
    assert client.get("/keyerror").data == b"wrapped KeyError"
    assert client.get("/abort").data == b"direct"
class TestGenericHandlers(object):
    class Custom(Exception):
        pass
    @pytest.fixture()
    def app(self, app):
        @app.route("/custom")
        def do_custom():
            raise self.Custom()
        @app.route("/error")
        def do_error():
            raise KeyError()
        @app.route("/abort")
        def do_abort():
            flask.abort(500)
        @app.route("/raise")
        def do_raise():
            raise InternalServerError()
        app.config["PROPAGATE_EXCEPTIONS"] = False
        return app
    def report_error(self, e):
        original = getattr(e, "original_exception", None)
        if original is not None:
            return "wrapped " + type(original).__name__
        return "direct " + type(e).__name__
    @pytest.mark.parametrize("to_handle", (InternalServerError, 500))
    def test_handle_class_or_code(self, app, client, to_handle):
        have the same behavior. Both should only receive
        ``InternalServerError``, which might wrap another error.
        @app.errorhandler(to_handle)
        def handle_500(e):
            assert isinstance(e, InternalServerError)
            return self.report_error(e)
        assert client.get("/custom").data == b"wrapped Custom"
        assert client.get("/error").data == b"wrapped KeyError"
        assert client.get("/abort").data == b"direct InternalServerError"
        assert client.get("/raise").data == b"direct InternalServerError"
    def test_handle_generic_http(self, app, client):
        subclasses. It will receive ``404`` routing exceptions.
        @app.errorhandler(HTTPException)
        def handle_http(e):
            assert isinstance(e, HTTPException)
            return str(e.code)
        assert client.get("/error").data == b"500"
        assert client.get("/abort").data == b"500"
        assert client.get("/not-found").data == b"404"
    def test_handle_generic(self, app, client):
        including ``HTTPExceptions``.
        @app.errorhandler(Exception)
        def handle_exception(e):
            return self.report_error(e)
        assert client.get("/custom").data == b"direct Custom"
        assert client.get("/error").data == b"direct KeyError"
        assert client.get("/abort").data == b"direct InternalServerError"
        assert client.get("/not-found").data == b"direct NotFound"
            result = self.url_adapter.match(return_rule=True)
            self.request.url_rule, self.request.view_args = result
        if self.url_adapter is not None:
            self.match_request()
from werkzeug.routing import BaseConverter
from flask import has_request_context
from flask import url_for
def test_custom_converters(app, client):
    with app.test_request_context():
        assert url_for("index", args=[4, 5, 6]) == "/4,5,6"
def test_context_available(app, client):
    class ContextConverter(BaseConverter):
            assert has_request_context()
    app.url_map.converters["ctx"] = ContextConverter
    @app.route("/<ctx:name>")
    def index(name):
        return name
    assert client.get("/admin").data == b"admin"
    with ctx:
        assert ctx.request.blueprint == bp.name
        or ``HTTPException`` subclasses, return both the exception and
        status code.
        :param exc_class_or_code: Any exception class, or an HTTP status
            code as an integer.
    app-related functions that can be registered on a real application
    later.
    A blueprint is an object that allows defining application functions
    without requiring an application object ahead of time. It uses the
    same decorators as :class:`~flask.Flask`, but defers the need for an
    application by recording them for later registration.
    Decorating a function with a blueprint creates a deferred function
    that is called with :class:`~flask.blueprints.BlueprintSetupState`
    when the blueprint is registered on an application.
    See :ref:`blueprints` for more information.
    :param name: The name of the blueprint. Will be prepended to each
        endpoint name.
    :param import_name: The name of the blueprint package, usually
        ``__name__``. This helps locate the ``root_path`` for the
        blueprint.
    :param static_folder: A folder with static files that should be
        served by the blueprint's static route. The path is relative to
        the blueprint's root path. Blueprint static files are disabled
        by default.
    :param static_url_path: The url to serve static files from.
        Defaults to ``static_folder``. If the blueprint does not have
        a ``url_prefix``, the app's static route will take precedence,
        and the blueprint's static files won't be accessible.
    :param template_folder: A folder with templates that should be added
        to the app's template search path. The path is relative to the
        blueprint's root path. Blueprint templates are disabled by
        default. Blueprint templates have a lower precedence than those
        in the app's templates folder.
    :param url_prefix: A path to prepend to all of the blueprint's URLs,
        to make them distinct from the rest of the app's routes.
    :param subdomain: A subdomain that blueprint routes will match on by
        default.
    :param url_defaults: A dict of default values that blueprint routes
        will receive by default.
    :param root_path: By default, the blueprint will automatically this
        based on ``import_name``. In certain situations this automatic
        detection can fail, so the path can be specified manually
        instead.
def test_server_name_subdomain():
    @app.route("/")
        return "default"
    @app.route("/", subdomain="foo")
        return "subdomain"
    app.config["SERVER_NAME"] = "dev.local:5000"
    rv = client.get("/")
    assert rv.data == b"default"
    rv = client.get("/", "http://dev.local:5000")
    assert rv.data == b"default"
    rv = client.get("/", "https://dev.local:5000")
    assert rv.data == b"default"
    app.config["SERVER_NAME"] = "dev.local:443"
    rv = client.get("/", "https://dev.local")
    # Werkzeug 1.0 fixes matching https scheme with 443 port
    if rv.status_code != 404:
        assert rv.data == b"default"
    app.config["SERVER_NAME"] = "dev.local"
    rv = client.get("/", "https://dev.local")
    assert rv.data == b"default"
    # suppress Werkzeug 1.0 warning about name mismatch
    with pytest.warns(None):
        rv = client.get("/", "http://foo.localhost")
    rv = client.get("/", "http://foo.dev.local")
    assert rv.data == b"subdomain"
    # suppress Werkzeug 0.15 warning about name mismatch
    with pytest.warns(None):
        # ip address can't match name
        rv = client.get('/', 'http://127.0.0.1:3000/')
        assert rv.status_code == 404 if matching else 204
    def test_send_file_xsendfile(self, app, req_ctx):
    # suppress Werkzeug 0.15 warning about name mismatch
    with pytest.warns(None):
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                "Request finalizing failed with an error while handling an error"
    message = "Python %(python)s\nFlask %(flask)s\nWerkzeug %(werkzeug)s"
            assert rv is self, "Popped wrong request context. (%r instead of %r)" % (
                rv,
                self,
            )
    assert view_func is not None, "expected view func if endpoint is not provided."
            raise TypeError("filename unavailable, required for sending as attachment")
                "Session transactions only make sense with cookies enabled."
                    "Session backend did not open a session. Check the configuration"
        assert ("Make sure to directly send your POST-request to this URL") in str(e)
        "[Errno 2] Unable to load configuration file (No such file or directory):"
        "[Errno 2] Unable to load configuration file (No such file or directory):"
        "[Errno 2] Unable to load configuration file (No such file or directory):"
        "import flask\napp = flask.Flask(__name__)\n"
    rv = flask.render_template_string("Hello {{ config.WORLD_NAME }} {{ foo }}")
from flask import jsonify
from flask import render_template
from flask import request
from setuptools import find_packages
from setuptools import setup
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from flask import g
from setuptools import find_packages
from setuptools import setup
from flaskr.db import get_db
from flaskr.db import init_db
from flask import g
from flask import session
from datetime import date
from datetime import datetime
from subprocess import PIPE
from subprocess import Popen
from jinja2 import escape
from jinja2 import Markup
from .app import Flask
from .app import Request
from .app import Response
from .blueprints import Blueprint
from .config import Config
from .ctx import after_this_request
from .ctx import copy_current_request_context
from .ctx import has_app_context
from .ctx import has_request_context
from .globals import _app_ctx_stack
from .globals import _request_ctx_stack
from .globals import current_app
from .globals import g
from .globals import request
from .globals import session
from .helpers import flash
from .helpers import get_flashed_messages
from .helpers import get_template_attribute
from .helpers import make_response
from .helpers import safe_join
from .helpers import send_file
from .helpers import send_from_directory
from .helpers import stream_with_context
from .helpers import url_for
from .json import jsonify
from .signals import appcontext_popped
from .signals import appcontext_pushed
from .signals import appcontext_tearing_down
from .signals import before_render_template
from .signals import got_request_exception
from .signals import message_flashed
from .signals import request_finished
from .signals import request_started
from .signals import request_tearing_down
from .signals import signals_available
from .signals import template_rendered
from .templating import render_template
from .templating import render_template_string
__version__ = "1.1.dev"
from werkzeug.datastructures import Headers
from werkzeug.datastructures import ImmutableDict
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import BadRequestKeyError
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.routing import BuildError
from werkzeug.routing import Map
from werkzeug.routing import RequestRedirect
from werkzeug.routing import RoutingException
from werkzeug.routing import Rule
from . import cli
from . import json
from ._compat import integer_types
from ._compat import reraise
from ._compat import string_types
from ._compat import text_type
from .config import Config
from .config import ConfigAttribute
from .ctx import _AppCtxGlobals
from .ctx import AppContext
from .ctx import RequestContext
from .globals import _request_ctx_stack
from .globals import g
from .globals import request
from .globals import session
from .helpers import _endpoint_from_view_func
from .helpers import _PackageBoundObject
from .helpers import find_package
from .helpers import get_debug_flag
from .helpers import get_env
from .helpers import get_flashed_messages
from .helpers import get_load_dotenv
from .helpers import locked_cached_property
from .helpers import url_for
from .signals import appcontext_tearing_down
from .signals import got_request_exception
from .signals import request_finished
from .signals import request_started
from .signals import request_tearing_down
from .templating import _default_template_ctx_processor
from .templating import DispatchingJinjaLoader
from .templating import Environment
from .wrappers import Request
from .wrappers import Response
            from .testing import FlaskClient as cls
            from .testing import FlaskCliRunner as cls
        from .testing import EnvironBuilder
from .helpers import _endpoint_from_view_func
from .helpers import _PackageBoundObject
from threading import Lock
from threading import Thread
from ._compat import getargspec
from ._compat import itervalues
from ._compat import reraise
from ._compat import text_type
from .helpers import get_debug_flag
from .helpers import get_env
from .helpers import get_load_dotenv
    from . import Flask
    from . import __version__
    from .globals import _app_ctx_stack
import errno
from ._compat import iteritems
from ._compat import string_types
from ._compat import BROKEN_PYPY_CTXMGR_EXIT
from ._compat import reraise
from .globals import _app_ctx_stack
from .globals import _request_ctx_stack
from .signals import appcontext_popped
from .signals import appcontext_pushed
from ._compat import implements_to_string
from ._compat import text_type
from werkzeug.local import LocalProxy
from werkzeug.local import LocalStack
import mimetypes
import socket
import sys
from threading import RLock
from time import time
from zlib import adler32
from jinja2 import FileSystemLoader
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import RequestedRangeNotSatisfiable
from werkzeug.routing import BuildError
from werkzeug.urls import url_quote
from ._compat import fspath
from ._compat import PY2
from ._compat import string_types
from ._compat import text_type
from .globals import _app_ctx_stack
from .globals import _request_ctx_stack
from .globals import current_app
from .globals import request
from .globals import session
from datetime import date
from datetime import datetime
from itsdangerous import json as _json
from werkzeug.http import http_date
from .._compat import PY2
from .._compat import text_type
from ..globals import current_app
from ..globals import request
from base64 import b64decode
from base64 import b64encode
from werkzeug.http import http_date
from werkzeug.http import parse_date
from .._compat import iteritems
from .._compat import text_type
from ..json import dumps
from ..json import loads
from itsdangerous import BadSignature
from itsdangerous import URLSafeTimedSerializer
from ._compat import collections_abc
from .helpers import is_ip
from .helpers import total_seconds
from .json.tag import TaggedJSONSerializer
    signals_available = False
from jinja2 import BaseLoader
from jinja2 import Environment as BaseEnvironment
from jinja2 import TemplateNotFound
from .globals import _app_ctx_stack
from .globals import _request_ctx_stack
from .signals import before_render_template
from .signals import template_rendered
import werkzeug.test
from . import _request_ctx_stack
from .cli import ScriptInfo
from .json import dumps as json_dumps
from .globals import request
from werkzeug.wrappers import Request as RequestBase
from werkzeug.wrappers import Response as ResponseBase
from . import json
from .globals import current_app
from flask import Blueprint
from flask import render_template
from flask import Blueprint
from flask import render_template
from __future__ import absolute_import
from __future__ import print_function
from __future__ import absolute_import
from __future__ import print_function
from __future__ import absolute_import
from __future__ import print_function
from __future__ import absolute_import
from __future__ import print_function
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import NotFound
from jinja2 import TemplateNotFound
from werkzeug.http import parse_cache_control_header
from flask import Blueprint
from flask import current_app
from flask import Flask
from flask.cli import AppGroup
from flask.cli import dotenv
from flask.cli import find_best_app
from flask.cli import FlaskGroup
from flask.cli import get_version
from flask.cli import load_dotenv
from flask.cli import locate_app
from flask.cli import NoAppException
from flask.cli import prepare_import
from flask.cli import run_command
from flask.cli import ScriptInfo
from flask.cli import with_appcontext
from datetime import timedelta
import pytest
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound
from werkzeug.http import http_date
from werkzeug.http import parse_cache_control_header
from werkzeug.http import parse_options_header
from flask._compat import StringIO
from flask._compat import text_type
from flask.helpers import get_debug_flag
from flask.helpers import get_env
from flask.json.tag import JSONTag
from flask.json.tag import TaggedJSONSerializer
from flask.logging import default_handler
from flask.logging import has_level_handler
from flask.logging import wsgi_errors_stream
import logging
import werkzeug.serving
from jinja2 import TemplateNotFound
import flask
from flask.testing import EnvironBuilder
from flask.testing import FlaskCliRunner
from flask.testing import make_test_environ_builder
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import NotFound
from setuptools import find_packages
with io.open("src/flask/__init__.py", "rt", encoding="utf8") as f:
    packages=find_packages("src"),
    package_dir={"": "src"},
        self.static_url_path = static_url_path
        self.static_folder = static_folder
                self.static_url_path + "/<path:filename>",
                self.static_url_path + "/<path:filename>",
    @property
    def static_url_path(self):
        If it was not configured during init, it is derived from
        :attr:`static_folder`.
            return ("/" + basename).rstrip("/")
    @static_url_path.setter
    def static_url_path(self, value):
        if value is not None:
            value = value.rstrip("/")
        self._static_url_path = value
def test_static_url_empty_path(app):
def test_static_url_empty_path_default(app):
class SeparatedPathType(click.Path):
    OS's path separator (``:``, ``;`` on Windows). Each value is
    validated as a :class:`click.Path` type.
    def convert(self, value, param, ctx):
        items = self.split_envvar_value(value)
        super_convert = super(SeparatedPathType, self).convert
        return [super_convert(item, param, ctx) for item in items]
@click.option(
    "--extra-files",
    default=None,
    type=SeparatedPathType(),
    help=(
        "Extra files that trigger a reload on change. Multiple paths"
        " are separated by '{}'.".format(os.path.pathsep)
    ),
)
def run_command(
    info, host, port, reload, debugger, eager_loading, with_threads, cert, extra_files
):
        extra_files=extra_files,
    #: Options that are passed to the Jinja environment in
    #: :meth:`create_jinja_environment`. Changing these options after
    #: the environment is created (accessing :attr:`jinja_env`) will
    #: have no effect.
    #:
    #: .. versionchanged:: 1.1.0
    #:     This is a ``dict`` instead of an ``ImmutableDict`` to allow
    #:     easier configuration.
    #:
    jinja_options = {"extensions": ["jinja2.ext.autoescape", "jinja2.ext.with_"]}
        The environment is created the first time this property is
        accessed. Changing :attr:`jinja_options` after that will have no
        effect.
        and the various Jinja-related methods of the app. Changing
        :attr:`jinja_options` after this will have no effect. Also adds
        Flask-related globals and filters to the environment.
        .. versionadded:: 0.5
    "sphinx_issues",
issues_github_path = "pallets/flask"
        :param mode: Open file in this mode. Only reading is supported,
            valid values are "r" (or "rt") and "rb".
        if mode not in {"r", "rt", "rb"}:
    @pytest.mark.parametrize("mode", ("r", "rb", "rt"))
        with app.open_resource("static/index.html", mode) as f:
            assert "<h1>Hello World!</h1>" in str(f.read())
    @pytest.mark.parametrize("mode", ("w", "x", "a", "r+"))
        with pytest.raises(ValueError):
            app.open_resource("static/index.html", mode)
__version__ = '1.0.3'
def _dump_arg_defaults(kwargs, app=None):
    if app is None:
        app = current_app
    if app:
        bp = app.blueprints.get(request.blueprint) if request else None
            'cls', bp.json_encoder if bp and bp.json_encoder else app.json_encoder
        if not app.config['JSON_AS_ASCII']:
        kwargs.setdefault('sort_keys', app.config['JSON_SORT_KEYS'])
def _load_arg_defaults(kwargs, app=None):
    if app is None:
        app = current_app
    if app:
        bp = app.blueprints.get(request.blueprint) if request else None
                else app.json_decoder
def dumps(obj, app=None, **kwargs):
    app context pushed, use the current app's configured encoder
    (:attr:`~flask.Flask.json_encoder`), or fall back to the default
    :class:`JSONEncoder`.
    Takes the same arguments as the built-in :func:`json.dumps`, and
    does some extra configuration based on the application. If the
    simplejson package is installed, it is preferred.
    :param obj: Object to serialize to JSON.
    :param app: App instance to use to configure the JSON encoder.
        Uses ``current_app`` if not given, and falls back to the default
        encoder when not in an app context.
    :param kwargs: Extra arguments passed to :func:`json.dumps`.
    .. versionchanged:: 1.0.3
        ``app`` can be passed directly, rather than requiring an app
        context for configuration.
    _dump_arg_defaults(kwargs, app=app)
def dump(obj, fp, app=None, **kwargs):
    _dump_arg_defaults(kwargs, app=app)
def loads(s, app=None, **kwargs):
    there is an app context pushed, use the current app's configured
    decoder (:attr:`~flask.Flask.json_decoder`), or fall back to the
    default :class:`JSONDecoder`.
    Takes the same arguments as the built-in :func:`json.loads`, and
    does some extra configuration based on the application. If the
    simplejson package is installed, it is preferred.
    :param s: JSON string to deserialize.
    :param app: App instance to use to configure the JSON decoder.
        Uses ``current_app`` if not given, and falls back to the default
        encoder when not in an app context.
    :param kwargs: Extra arguments passed to :func:`json.dumps`.
    .. versionchanged:: 1.0.3
        ``app`` can be passed directly, rather than requiring an app
        context for configuration.
    _load_arg_defaults(kwargs, app=app)
def load(fp, app=None, **kwargs):
    _load_arg_defaults(kwargs, app=app)
    # TODO use EnvironBuilder.json_dumps once we require Werkzeug 0.15
        assert 'data' not in kwargs, "Client cannot provide both 'json' and 'data'."
        kwargs['data'] = json_dumps(kwargs.pop('json'), app=app)
from flask import appcontext_popped
try:
    import blinker
except ImportError:
    blinker = None
@pytest.mark.skipif(blinker is None, reason="blinker is not installed")
def test_client_json_no_app_context(app, client):
    @app.route("/hello", methods=["POST"])
    def hello():
        return "Hello, {}!".format(flask.request.json["name"])
    class Namespace(object):
        count = 0
        def add(self, app):
            self.count += 1
    ns = Namespace()
    with appcontext_popped.connected_to(ns.add, app):
        rv = client.post("/hello", json={"name": "Flask"})
    assert rv.get_data(as_text=True) == "Hello, Flask!"
    assert ns.count == 1
        .. versionchanged:: 1.0.3
            ``RoutingException``, used internally for actions such as
             slash redirects during routing, is not passed to error
             handlers.
        .. versionchanged:: 1.0
            Exceptions are looked up by code *and* by MRO, so
            ``HTTPExcpetion`` subclasses can be handled with a catch-all
            handler for the base ``HTTPException``.
        # RoutingExceptions are used internally to trigger routing
        # actions, such as slash redirects raising RequestRedirect. They
        # are not raised or handled in user code.
    @app.route("/slash/")
        return "slash"
    # Don't handle RequestRedirect raised when adding slash.
    assert c.get("/slash", follow_redirects=True).data == b"slash"
        Filename may be a :class:`~os.PathLike` object.
        Partial content supports :class:`~io.BytesIO`.
                # Python 2 doesn't have getbuffer
import platform
    import werkzeug
    message = (
        'Python %(python)s\n'
        'Flask %(flask)s\n'
        'Werkzeug %(werkzeug)s'
    )
        'python': platform.python_version(),
        'flask': __version__,
        'werkzeug': werkzeug.__version__,
    from flask import __version__ as flask_version
    from werkzeug import __version__ as werkzeug_version
    from platform import python_version
    assert "Python " + python_version() in out
    assert "Flask " + flask_version in out
    assert "Werkzeug " + werkzeug_version in out
from pallets_sphinx_themes import ProjectLink, get_version
project = "Flask"
copyright = "2010 Pallets Team"
author = "Pallets Team"
release, version = get_version("Flask")
master_doc = "index"
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "pallets_sphinx_themes",
    "python": ("https://docs.python.org/3/", None),
    "werkzeug": ("http://werkzeug.pocoo.org/docs/", None),
    "click": ("https://click.palletsprojects.com/", None),
    "jinja": ("http://jinja.pocoo.org/docs/", None),
    "itsdangerous": ("https://itsdangerous.palletsprojects.com/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/", None),
    "wtforms": ("https://wtforms.readthedocs.io/en/stable/", None),
    "blinker": ("https://pythonhosted.org/blinker/", None),
html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
    "project_links": [
        ProjectLink("Donate to Pallets", "https://palletsprojects.com/donate"),
        ProjectLink("Flask Website", "https://palletsprojects.com/p/flask/"),
        ProjectLink("PyPI releases", "https://pypi.org/project/Flask/"),
        ProjectLink("Source Code", "https://github.com/pallets/flask/"),
        ProjectLink("Issue Tracker", "https://github.com/pallets/flask/issues/"),
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_static_path = ["_static"]
html_favicon = "_static/flask-favicon.ico"
html_logo = "_static/flask.png"
html_title = "Flask Documentation ({})".format(version)
    (master_doc, "Flask.tex", "Flask Documentation", "Pallets Team", "manual")
    "papersize": "a4paper",
    "pointsize": "12pt",
    "fontpkg": r"\usepackage{mathpazo}",
    "preamble": r"\usepackage{flaskstyle}",
latex_additional_files = ["flaskstyle.sty", "logo.pdf"]
def github_link(name, rawtext, text, lineno, inliner, options=None, content=None):
    base_url = "https://github.com/pallets/flask/tree/"
    if text.endswith(">"):
        words, text = text[:-1].rsplit("<", 1)
    if release.endswith("dev"):
        url = "{0}master/{1}".format(base_url, text)
        url = "{0}{1}/{2}".format(base_url, release, text)
    app.add_role("gh", github_link)
        if isinstance(e, BadRequestKeyError):
            if self.debug or self.config["TRAP_BAD_REQUEST_ERRORS"]:
                # Werkzeug < 0.15 doesn't add the KeyError to the 400
                # message, add it in manually.
                description = e.get_description()
                if e.args[0] not in description:
                    e.description = "KeyError: '{}'".format(*e.args)
            else:
                # Werkzeug >= 0.15 does add it, remove it in production
                e.args = ()
    assert 'missing_key' in e.value.get_description()
from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink
project = "Flask"
copyright = "2010 Pallets Team"
author = "Pallets Team"
release, version = get_version("Flask")
master_doc = "index"
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "pallets_sphinx_themes",
    "python": ("https://docs.python.org/3/", None),
    "werkzeug": ("http://werkzeug.pocoo.org/docs/", None),
    "click": ("http://click.pocoo.org/", None),
    "jinja": ("http://jinja.pocoo.org/docs/", None),
    "itsdangerous": ("https://pythonhosted.org/itsdangerous", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/latest/", None),
    "wtforms": ("https://wtforms.readthedocs.io/en/latest/", None),
    "blinker": ("https://pythonhosted.org/blinker/", None),
html_theme = "flask"
    "project_links": [
        ProjectLink("Donate to Pallets", "https://palletsprojects.com/donate"),
        ProjectLink("Flask Website", "https://palletsprojects.com/p/flask/"),
        ProjectLink("PyPI releases", "https://pypi.org/project/Flask/"),
        ProjectLink("Source Code", "https://github.com/pallets/flask/"),
        ProjectLink("Issue Tracker", "https://github.com/pallets/flask/issues/"),
    ]
    "index": ["project.html", "localtoc.html", "versions.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "versions.html", "searchbox.html"],
html_static_path = ["_static"]
html_favicon = "_static/flask-icon.png"
html_logo = "_static/flask-logo-sidebar.png"
    (master_doc, "Flask-{}.tex".format(version), html_title, author, "manual")
    "papersize": "a4paper",
    "pointsize": "12pt",
    "fontpkg": r"\usepackage{mathpazo}",
    "preamble": r"\usepackage{flaskstyle}",
latex_additional_files = ["flaskstyle.sty", "logo.pdf"]
def github_link(name, rawtext, text, lineno, inliner, options=None, content=None):
    base_url = "https://github.com/pallets/flask/tree/"
    if text.endswith(">"):
        words, text = text[:-1].rsplit("<", 1)
    if release.endswith("dev"):
        url = "{0}master/{1}".format(base_url, text)
        url = "{0}{1}/{2}".format(base_url, release, text)
    app.add_role("gh", github_link)
html_theme_options = {"index_sidebar_logo": False}
        ProjectLink('Donate to Pallets', 'https://palletsprojects.com/donate'),
        ProjectLink('Issue Tracker', 'https://github.com/pallets/flask/issues/'),
    'index': ['project.html', "localtoc.html", 'versions.html', 'searchbox.html'],
    '**': ['localtoc.html', 'relations.html', 'versions.html', 'searchbox.html']
singlehtml_sidebars = {"index": ["project.html", "versions.html", "localtoc.html"]}
html_favicon = '_static/flask-icon.png'
html_logo = '_static/flask-logo-sidebar.png'
html_title = "Flask Documentation ({})".format(version)
html_domain_indices = False
    (master_doc, 'Flask-{}.tex'.format(version), html_title, author, 'manual'),
    .. versionchanged:: 1.0.3
        Filenames are encoded with ASCII instead of Latin-1 for broader
        compatibility with WSGI servers.
            attachment_filename = attachment_filename.encode('ascii')
                    'NFKD', attachment_filename).encode('ascii', 'ignore'),
    @pytest.mark.usefixtures('req_ctx')
    @pytest.mark.parametrize(('filename', 'ascii', 'utf8'), (
        ('index.html', 'index.html', False),
        (u'Ñandú／pingüino.txt', '"Nandu/pinguino.txt"',
        '%C3%91and%C3%BA%EF%BC%8Fping%C3%BCino.txt'),
        (u'Vögel.txt', 'Vogel.txt', 'V%C3%B6gel.txt'),
    ))
    def test_attachment_filename_encoding(self, filename, ascii, utf8):
        rv = flask.send_file('static/index.html', as_attachment=True, attachment_filename=filename)
        content_disposition = rv.headers['Content-Disposition']
        assert 'filename=%s' % ascii in content_disposition
        if utf8:
            assert "filename*=UTF-8''" + utf8 in content_disposition
        else:
            assert "filename*=UTF-8''" not in content_disposition
__version__ = '1.0.3.dev'
__version__ = '1.0.2'
from werkzeug.urls import url_join
                rule = '/'.join((
                    self.url_prefix.rstrip('/'), rule.lstrip('/')))
    ('', '/', '/'),
    ('/', '', '/'),
    ('/', '/', '/'),
    ('/foo/', '', '/foo/'),
    ('', '/bar', '/bar'),
        ('Code', 'https://github.com/pallets/flask'),
        ('Issue tracker', 'https://github.com/pallets/flask/issues'),
__version__ = '1.0.2.dev'
__version__ = '1.0.1'
from .helpers import (
    _PackageBoundObject,
    _endpoint_from_view_func, find_package, get_env, get_debug_flag,
    get_flashed_messages, locked_cached_property, url_for, get_load_dotenv
)
        if get_load_dotenv(load_dotenv):
__version__ = '0.12.5.dev'
__version__ = '0.12.4'
        if self.url_prefix is not None:
from .helpers import get_debug_flag, get_env, get_load_dotenv
        if get_load_dotenv(self.load_dotenv):
                ' Do "pip install python-dotenv" to use them.',
def get_load_dotenv(default=True):
    :envvar:`FLASK_SKIP_DOTENV`. The default is ``True``, load the
    files.
    :param default: What to return if the env var isn't set.
    val = os.environ.get('FLASK_SKIP_DOTENV')
    if not val:
        return default
    return val.lower() in ('0', 'false', 'no')
@need_dotenv
def test_disable_dotenv_from_env(monkeypatch, runner):
    monkeypatch.chdir(test_path)
    monkeypatch.setitem(os.environ, 'FLASK_SKIP_DOTENV', '1')
    runner.invoke(FlaskGroup())
    assert 'FOO' not in os.environ
        # if unset, trap key errors in debug mode
        if (
            trap_bad_request is None and self.debug
            and isinstance(e, BadRequestKeyError)
        ):
            return True
        if trap_bad_request:
    @app.route('/key')
    @app.route('/abort')
    def allow_abort():
        flask.abort(400)
    rv = client.get('/key')
    rv = client.get('/abort')
    assert rv.status_code == 400
    app.debug = True
        client.get("/key")
    rv = client.get('/abort')
    assert rv.status_code == 400
    app.debug = False
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    with pytest.raises(KeyError):
        client.get('/key')
    with pytest.raises(BadRequest):
        client.get('/abort')
        if url_prefix:
            url_prefix = url_prefix.rstrip('/')
            rule = '/'.join((self.url_prefix, rule.lstrip('/')))
@pytest.mark.parametrize(('prefix', 'rule', 'url'), (
    ('/foo/', '/bar', '/foo/bar'),
    ('/foo/', 'bar', '/foo/bar'),
    ('/foo', '/bar', '/foo/bar'),
    ('/foo/', '//bar', '/foo/bar'),
    ('/foo//', '/bar', '/foo/bar'),
))
def test_blueprint_prefix_slash(app, client, prefix, rule, url):
    bp = flask.Blueprint('test', __name__, url_prefix=prefix)
    @bp.route(rule)
    def index():
    assert client.get(url).status_code == 204
        'carbon_ads.html',
        'carbon_ads.html',
        'carbon_ads.html',
__version__ = '1.0.1.dev'
__version__ = '1.1.dev'
__version__ = '1.0'
        ('Code', 'https://github.com/pallets/flask'),
        ('Issue tracker', 'https://github.com/pallets/flask/issues'),
__version__ = '1.0'
__version__ = '0.12.4.dev'
__version__ = '0.12.3'
import sys
from datetime import date, datetime
from subprocess import PIPE, Popen
_date_strip_re = re.compile(r'(?<=\d)(st|nd|rd|th)')
            if next(lineiter).count('-') != len(match.group(0)):
                change_info = next(lineiter).strip()
            match = re.search(
                r'released on (\w+\s+\d+\w+\s+\d+)(?:, codename (.*))?',
                change_info,
                flags=re.IGNORECASE
            )
        parts = [int(i) for i in version.split('.')]
    string = _date_strip_re.sub('', string)
        contents = re.sub(
            r"^(\s*%s\s*=\s*')(.+?)(')" % pattern,
            inject_version, f.read(),
            flags=re.DOTALL | re.MULTILINE
        )
def build():
    cmd = [sys.executable, 'setup.py', 'sdist', 'bdist_wheel']
    Popen(cmd).wait()
    return set(
        Popen(['git', 'tag'], stdout=PIPE).communicate()[0].splitlines()
    )
    dev_version = bump_version(version) + '.dev'
    info(
        'Releasing %s (codename %s, release date %s)',
        version, codename, release_date.strftime('%d/%m/%Y')
    )
        fail(
            'Release date is not today (%s != %s)',
            release_date.date(), date.today()
        )
    try:
        import wheel  # noqa: F401
    except ImportError:
        fail('You need to install the wheel package.')
    build()
from collections import OrderedDict
    project_urls=OrderedDict((
        ('Documentation', 'http://flask.pocoo.org/docs/'),
        ('Code', 'https://github.com/pallets/pallets-sphinx-themes'),
        ('Issue tracker', 'https://github.com/pallets/pallets-sphinx-themes/issues'),
    )),
        ProjectLink('Donate to Pallets', 'https://psfmember.org/civicrm/contribute/transact?reset=1&id=20'),
        ProjectLink('Donate to Pallets', 'https://psfmember.org/civicrm/contribute/transact?reset=1&id=20'),
        ProjectLink('Donate to Pallets', 'https://psfmember.org/civicrm/contribute/transact?id=20'),
        ProjectLink('Donate to Pallets', 'https://psfmember.org/civicrm/contribute/transact?id=20'),
        cli.show_server_banner(self.env, self.debug, self.name, False)
def show_server_banner(env, debug, app_import_path, eager_loading):
        click.echo(message)
    click.echo(' * Environment: {0}'.format(env))
        click.echo(' * Debug mode: {0}'.format('on' if debug else 'off'))
__version__ = '1.0-dev'
    'python': ('https://docs.python.org/3/', None),
    'werkzeug': ('http://werkzeug.pocoo.org/docs/', None),
    'click': ('http://click.pocoo.org/', None),
    'jinja': ('http://jinja.pocoo.org/docs/', None),
    'itsdangerous': ('https://pythonhosted.org/itsdangerous', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/latest/', None),
    'wtforms': ('https://wtforms.readthedocs.io/en/latest/', None),
    'blinker': ('https://pythonhosted.org/blinker/', None),
import inspect
import re
from pallets_sphinx_themes import ProjectLink, get_version
# Project --------------------------------------------------------------
project = 'Flask'
copyright = '2010 Pallets Team'
author = 'Pallets Team'
release, version = get_version('Flask')
# General --------------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.log_cabinet',
]
intersphinx_mapping = {
    # 'python': ('https://docs.python.org/3/', None),
    # 'werkzeug': ('http://werkzeug.pocoo.org/docs/', None),
    # 'click': ('http://click.pocoo.org/', None),
    # 'jinja': ('http://jinja.pocoo.org/docs/', None),
    # 'itsdangerous': ('https://pythonhosted.org/itsdangerous', None),
    # 'sqlalchemy': ('https://docs.sqlalchemy.org/en/latest/', None),
    # 'wtforms': ('https://wtforms.readthedocs.io/en/latest/', None),
    # 'blinker': ('https://pythonhosted.org/blinker/', None),
}
# HTML -----------------------------------------------------------------
html_theme = 'flask'
html_context = {
    'project_links': [
        ProjectLink('Flask Website', 'https://palletsprojects.com/p/flask/'),
        ProjectLink('PyPI releases', 'https://pypi.org/project/Flask/'),
        ProjectLink('Source Code', 'https://github.com/pallets/flask/'),
        ProjectLink(
            'Issue Tracker', 'https://github.com/pallets/flask/issues/'),
    ],
    'canonical_url': 'http://flask.pocoo.org/docs/{}/'.format(version),
    'carbon_ads_args': 'zoneid=1673&serve=C6AILKT&placement=pocooorg',
}
        'project.html',
        'versions.html',
        'searchbox.html',
        'versions.html',
        'carbon_ads.html',
        'searchbox.html',
html_static_path = ['_static']
html_favicon = '_static/flask-favicon.ico'
html_logo = '_static/flask.png'
html_additional_pages = {
    '404': '404.html',
}
html_show_sourcelink = False
# LaTeX ----------------------------------------------------------------
    (master_doc, 'Flask.tex', 'Flask Documentation', 'Pallets Team', 'manual'),
    'fontpkg': r'\usepackage{mathpazo}',
    'preamble': r'\usepackage{flaskstyle}',
# linkcheck ------------------------------------------------------------
linkcheck_anchors = False
# Local Extensions -----------------------------------------------------
_internal_mark_re = re.compile(r'^\s*:internal:\s*$(?m)', re.M)
def skip_internal(app, what, name, obj, skip, options):
    docstring = inspect.getdoc(obj) or ''
    if skip or _internal_mark_re.search(docstring) is not None:
        return True
def cut_module_meta(app, what, name, obj, options, lines):
    if what != 'module':
        return
    lines[:] = [
        line for line in lines
        if not line.startswith((':copyright:', ':license:'))
    ]
def github_link(
    name, rawtext, text, lineno, inliner, options=None, content=None
):
    app = inliner.document.settings.env.app
    release = app.config.release
    base_url = 'https://github.com/pallets/flask/tree/'
    if text.endswith('>'):
        words, text = text[:-1].rsplit('<', 1)
        words = words.strip()
    else:
        words = None
    if release.endswith('dev'):
        url = '{0}master/{1}'.format(base_url, text)
    else:
        url = '{0}{1}/{2}'.format(base_url, release, text)
    if words is None:
        words = url
    from docutils.nodes import reference
    from docutils.parsers.rst.roles import set_classes
    options = options or {}
    set_classes(options)
    node = reference(rawtext, words, refuri=url, **options)
    return [node], []
def setup(app):
    app.connect('autodoc-skip-member', skip_internal)
    app.connect('autodoc-process-docstring', cut_module_meta)
    app.add_role('gh', github_link)
import inspect
import re
from pallets_sphinx_themes import DocVersion, ProjectLink, get_version
# Project --------------------------------------------------------------
project = 'Flask'
copyright = '2010 Pallets Team'
author = 'Pallets Team'
release, version = get_version('Flask')
# General --------------------------------------------------------------
master_doc = 'index'
    'sphinxcontrib.log_cabinet',
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'werkzeug': ('http://werkzeug.pocoo.org/docs/', None),
    'click': ('http://click.pocoo.org/', None),
    'jinja': ('http://jinja.pocoo.org/docs/', None),
    'itsdangerous': ('https://pythonhosted.org/itsdangerous', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/latest/', None),
    'wtforms': ('https://wtforms.readthedocs.io/en/latest/', None),
    'blinker': ('https://pythonhosted.org/blinker/', None),
}
# HTML -----------------------------------------------------------------
html_theme = 'flask'
html_context = {
    'project_links': [
        ProjectLink('Flask Website', 'https://palletsprojects.com/p/flask/'),
        ProjectLink('PyPI releases', 'https://pypi.org/project/Flask/'),
        ProjectLink('Source Code', 'https://github.com/pallets/flask/'),
        ProjectLink(
            'Issue Tracker', 'https://github.com/pallets/flask/issues/'),
    ],
    'versions': [
        DocVersion('dev', 'Development', 'unstable'),
        DocVersion('1.0', 'Flask 1.0', 'stable'),
        DocVersion('0.12', 'Flask 0.12'),
    ],
    'canonical_url': 'http://flask.pocoo.org/docs/{}/'.format(version),
    'carbon_ads_args': 'zoneid=1673&serve=C6AILKT&placement=pocooorg',
}
        'project.html',
        'versions.html',
        'searchbox.html',
        'versions.html',
        'carbon_ads.html',
        'searchbox.html',
html_static_path = ['_static']
html_favicon = '_static/flask-favicon.ico'
html_logo = '_static/flask.png'
html_additional_pages = {
    '404': '404.html',
}
html_show_sourcelink = False
# LaTeX ----------------------------------------------------------------
    (master_doc, 'Flask.tex', 'Flask Documentation', 'Pallets Team', 'manual'),
    'fontpkg': r'\usepackage{mathpazo}',
    'preamble': r'\usepackage{flaskstyle}',
# linkcheck ------------------------------------------------------------
linkcheck_anchors = False
# Local Extensions -----------------------------------------------------
_internal_mark_re = re.compile(r'^\s*:internal:\s*$(?m)', re.M)
def skip_internal(app, what, name, obj, skip, options):
    docstring = inspect.getdoc(obj) or ''
    if skip or _internal_mark_re.search(docstring) is not None:
        return True
def cut_module_meta(app, what, name, obj, options, lines):
    if what != 'module':
        return
    lines[:] = [
        line for line in lines
        if not line.startswith((':copyright:', ':license:'))
    ]
def github_link(
    name, rawtext, text, lineno, inliner, options=None, content=None
):
    app = inliner.document.settings.env.app
    release = app.config.release
    base_url = 'https://github.com/pallets/flask/tree/'
    if text.endswith('>'):
        words, text = text[:-1].rsplit('<', 1)
        words = words.strip()
    else:
        words = None
    if release.endswith('dev'):
        url = '{0}master/{1}'.format(base_url, text)
    else:
        url = '{0}{1}/{2}'.format(base_url, release, text)
    if words is None:
        words = url
    from docutils.nodes import reference
    from docutils.parsers.rst.roles import set_classes
    options = options or {}
    set_classes(options)
    node = reference(rawtext, words, refuri=url, **options)
    return [node], []
def setup(app):
    app.connect('autodoc-skip-member', skip_internal)
    app.connect('autodoc-process-docstring', cut_module_meta)
                'Could not import "{name}".'.format(name=module_name)
    .. versionchanged:: 1.0
            'pallets-sphinx-themes',
            'sphinxcontrib-log-cabinet',
        'docs': [
            'sphinx',
            'pallets-sphinx-themes',
            'sphinxcontrib-log-cabinet',
        ]
from flask import Flask
app = Flask(__name__)
from js_example import views
from flask import jsonify, render_template, request
from js_example import app
@app.route('/', defaults={'js': 'plain'})
@app.route('/<any(plain, jquery, fetch):js>')
def index(js):
    return render_template('{0}.html'.format(js), js=js)
@app.route('/add', methods=['POST'])
def add():
    a = request.form.get('a', 0, type=float)
    b = request.form.get('b', 0, type=float)
    return jsonify(result=a + b)
import io
from setuptools import find_packages, setup
with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()
setup(
    name='js_example',
    version='1.0.0',
    url='http://flask.pocoo.org/docs/patterns/jquery/',
    license='BSD',
    maintainer='Pallets team',
    maintainer_email='contact@palletsprojects.com',
    description='Demonstrates making Ajax requests to Flask.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
            'blinker',
        ],
    },
)
import pytest
from js_example import app
@pytest.fixture(name='app')
def fixture_app():
    app.testing = True
    yield app
    app.testing = False
@pytest.fixture
def client(app):
    return app.test_client()
import pytest
from flask import template_rendered
@pytest.mark.parametrize(('path', 'template_name'), (
    ('/', 'plain.html'),
    ('/plain', 'plain.html'),
    ('/fetch', 'fetch.html'),
    ('/jquery', 'jquery.html'),
))
def test_index(app, client, path, template_name):
    def check(sender, template, context):
        assert template.name == template_name
    with template_rendered.connected_to(check, app):
        client.get(path)
@pytest.mark.parametrize(('a', 'b', 'result'), (
    (2, 3, 5),
    (2.5, 3, 5.5),
    (2, None, 2),
    (2, 'b', 2),
))
def test_add(client, a, b, result):
    response = client.post('/add', data={'a': a, 'b': b})
    assert response.get_json()['result'] == result
            error = 'User {0} is already registered.'.format(username)
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
import codecs
def detect_encoding(data):
    The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
    accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
    or little endian. Some editors or libraries may prepend a BOM.
    :param data: Bytes in unknown UTF encoding.
    :return: UTF encoding name
    head = data[:4]
    if head[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'
    if b'\x00' not in head:
        return 'utf-8'
    if head in (codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE):
        return 'utf-32'
    if head[:2] in (codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE):
        return 'utf-16'
    if len(head) == 4:
        if head[:3] == b'\x00\x00\x00':
            return 'utf-32-be'
        if head[::2] == b'\x00\x00':
            return 'utf-16-be'
        if head[1:] == b'\x00\x00\x00':
            return 'utf-32-le'
        if head[1::2] == b'\x00\x00':
            return 'utf-16-le'
    if len(head) == 2:
        return 'utf-16-be' if head.startswith(b'\x00') else 'utf-16-le'
    return 'utf-8'
        encoding = kwargs.pop('encoding', None)
        if encoding is None:
            encoding = detect_encoding(s)
        s = s.decode(encoding)
        data = _get_data(self, cache)
            rv = json.loads(data)
from flask import json
    @pytest.mark.parametrize('value', (
        1, 't', True, False, None,
        [], [1, 2, 3],
        {}, {'foo': u'🐍'},
    ))
    @pytest.mark.parametrize('encoding', (
        'utf-8', 'utf-8-sig',
        'utf-16-le', 'utf-16-be', 'utf-16',
        'utf-32-le', 'utf-32-be', 'utf-32',
    ))
    def test_detect_encoding(self, value, encoding):
        data = json.dumps(value).encode(encoding)
        assert json.detect_encoding(data) == encoding
        assert json.loads(data) == value
        this_module = 'flask'
        if sys.version_info < (2, 7):
            this_module += '.cli'
        name = 'python -m ' + this_module
        # Python rewrites "python -m flask" to the path to the file in argv.
        # Restore the original command so that the reloader works.
        sys.argv = ['-m', this_module] + args
        'MAX_COOKIE_SIZE': 4093,
    .. versionchanged:: 1.0
        Added :attr:`max_cookie_size`.
    @property
    def max_cookie_size(self):
        See :attr:`~werkzeug.wrappers.BaseResponse.max_cookie_size` in
        Werkzeug's docs.
        if current_app:
            return current_app.config['MAX_COOKIE_SIZE']
        # return Werkzeug's default when not in an app context
        return super(Response, self).max_cookie_size
def test_max_cookie_size(app, client, recwarn):
    app.config['MAX_COOKIE_SIZE'] = 100
    # outside app context, default to Werkzeug static value,
    # which is also the default config
    response = flask.Response()
    default = flask.Flask.default_config['MAX_COOKIE_SIZE']
    assert response.max_cookie_size == default
    # inside app context, use app config
    with app.app_context():
        assert flask.Response().max_cookie_size == 100
    @app.route('/')
    def index():
        r = flask.Response('', status=204)
        r.set_cookie('foo', 'bar' * 100)
        return r
    client.get('/')
    assert len(recwarn) == 1
    w = recwarn.pop()
    assert 'cookie is too large' in str(w.message)
    app.config['MAX_COOKIE_SIZE'] = 0
    client.get('/')
    assert len(recwarn) == 0
import codecs
def detect_encoding(data):
    The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
    accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
    or little endian. Some editors or libraries may prepend a BOM.
    :param data: Bytes in unknown UTF encoding.
    :return: UTF encoding name
    head = data[:4]
    if head[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'
    if b'\x00' not in head:
        return 'utf-8'
    if head in (codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE):
        return 'utf-32'
    if head[:2] in (codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE):
        return 'utf-16'
    if len(head) == 4:
        if head[:3] == b'\x00\x00\x00':
            return 'utf-32-be'
        if head[::2] == b'\x00\x00':
            return 'utf-16-be'
        if head[1:] == b'\x00\x00\x00':
            return 'utf-32-le'
        if head[1::2] == b'\x00\x00':
            return 'utf-16-le'
    if len(head) == 2:
        return 'utf-16-be' if head.startswith(b'\x00') else 'utf-16-le'
    return 'utf-8'
        encoding = kwargs.pop('encoding', None)
        if encoding is None:
            encoding = detect_encoding(s)
        s = s.decode(encoding)
        indicate JSON (:mimetype:`application/json`, see
        :meth:`is_json`), this returns ``None`` unless ``force`` is
        true. If parsing fails, :meth:`on_json_loading_failed` is called
        and its return value is used as the return value.
        :param silent: Silence parsing errors and return ``None``
            instead.
        :param cache: Store the parsed JSON to return for subsequent
            calls.
        data = self._get_data_for_json(cache=cache)
            rv = json.loads(data)
from werkzeug.http import (
    http_date, parse_cache_control_header,
)
from flask import json
    @pytest.mark.parametrize('value', (
        1, 't', True, False, None,
        [], [1, 2, 3],
        {}, {'foo': u'🐍'},
    ))
    @pytest.mark.parametrize('encoding', (
        'utf-8', 'utf-8-sig',
        'utf-16-le', 'utf-16-be', 'utf-16',
        'utf-32-le', 'utf-32-be', 'utf-32',
    ))
    def test_detect_encoding(self, value, encoding):
        data = json.dumps(value).encode(encoding)
        assert json.detect_encoding(data) == encoding
        assert json.loads(data) == value
        returned, right before the request context is popped.
        This calls all functions decorated with
        :meth:`teardown_request`, and :meth:`Blueprint.teardown_request`
        if a blueprint handled the request. Finally, the
        :data:`request_tearing_down` signal is sent.
        This is called by
        :meth:`RequestContext.pop() <flask.ctx.RequestContext.pop>`,
        which may be delayed during testing to maintain access to
        resources.
        :param exc: An unhandled exception raised while dispatching the
            request. Detected from the current exception information if
            not passed. Passed to each teardown function.
            Added the ``exc`` argument.
        When handling a request, the application context is popped
        after the request context. See :meth:`do_teardown_request`.
        This calls all functions decorated with
        :meth:`teardown_appcontext`. Then the
        :data:`appcontext_tearing_down` signal is sent.
        This is called by
        :meth:`AppContext.pop() <flask.ctx.AppContext.pop>`.
        block to push the context, which will make :data:`current_app`
        point at this application.
        An application context is automatically pushed by
        :meth:`RequestContext.push() <flask.ctx.RequestContext.push>`
        when handling a request, and when running a CLI command. Use
        this to manually create a context outside of these situations.
        ::
                init_db()
        See :doc:`/appcontext`.
        WSGI environment. Use a ``with`` block to push the context,
        which will make :data:`request` point at this request.
        See :doc:`/reqcontext`.
        Typically you should not call this from your own code. A request
        context is automatically pushed by the :meth:`wsgi_app` when
        handling a request. Use :meth:`test_request_context` to create
        an environment and context instead of this method.
        environment created from the given values. This is mostly useful
        during testing, where you may want to run a function that uses
        request data without dispatching a full request.
        See :doc:`/reqcontext`.
        Use a ``with`` block to push the context, which will make
        :data:`request` point at the request for the created
        environment. ::
            with test_request_context(...):
                generate_report()
        When using the shell, it may be easier to push and pop the
        context manually to avoid indentation. ::
            ctx = app.test_request_context(...)
            ctx.push()
            ...
            ctx.pop()
        Takes the same arguments as Werkzeug's
        :class:`~werkzeug.test.EnvironBuilder`, with some defaults from
        the application. See the linked Werkzeug docs for most of the
        available arguments. Flask-specific behavior is listed here.
        :param path: URL path being requested.
        :param base_url: Base URL where the app is being served, which
            ``path`` is relative to. If not given, built from
            :data:`PREFERRED_URL_SCHEME`, ``subdomain``,
            :data:`SERVER_NAME`, and :data:`APPLICATION_ROOT`.
        :param subdomain: Subdomain name to append to
            :data:`SERVER_NAME`.
        :param url_scheme: Scheme to use instead of
            :data:`PREFERRED_URL_SCHEME`.
        :param data: The request body, either as a string or a dict of
            form keys and values.
        :param json: If given, this is serialized as JSON and passed as
            ``data``. Also defaults ``content_type`` to
            ``application/json``.
        :param args: other positional arguments passed to
            :class:`~werkzeug.test.EnvironBuilder`.
        :param kwargs: other keyword arguments passed to
            :class:`~werkzeug.test.EnvironBuilder`.
        :meth:`__call__` so that middlewares can be applied without
        losing a reference to the app object. Instead of doing this::
            Teardown events for the request and app contexts are called
            even if an unhandled error occurs. Other events may not be
            called depending on when an error occurs during dispatch.
            See :ref:`callbacks-and-errors`.
        :param environ: A WSGI environment.
        :param start_response: A callable accepting a status code,
            a list of headers, and an optional exception context to
            start the response.
        WSGI application. This calls :meth:`wsgi_app` which can be
        wrapped to applying middleware."""
    application context.
    Creating an app context automatically creates this object, which is
    made available as the :data:`g` proxy.
    .. describe:: 'key' in g
        Check whether an attribute is present.
        .. versionadded:: 0.10
    .. describe:: iter(g)
        Return an iterator over the attribute names.
        .. versionadded:: 0.10
        :meth:`dict.get`.
        :param name: Name of attribute to get.
        :param default: Value to return if the attribute is not present.
        .. versionadded:: 0.10
        :param name: Name of attribute to pop.
        :param default: Value to return if the attribute is not present,
            instead of raise a ``KeyError``.
        .. versionadded:: 0.11
        set and return a default value. Like :meth:`dict.setdefault`.
        :param name: Name of attribute to get.
        :param: default: Value to set and return if the attribute is not
            present.
        .. versionadded:: 0.11
to interface with the current application object in some way. To solve
this, set up an application context with app.app_context().  See the
    defaults from the application.
    :param app: The Flask application to configure the environment from.
    :param path: URL path being requested.
    :param base_url: Base URL where the app is being served, which
        ``path`` is relative to. If not given, built from
        :data:`PREFERRED_URL_SCHEME`, ``subdomain``,
        :data:`SERVER_NAME`, and :data:`APPLICATION_ROOT`.
    :param subdomain: Subdomain name to append to :data:`SERVER_NAME`.
    :param url_scheme: Scheme to use instead of
        :data:`PREFERRED_URL_SCHEME`.
    :param json: If given, this is serialized as JSON and passed as
        ``data``. Also defaults ``content_type`` to
        ``application/json``.
    :param args: other positional arguments passed to
        :class:`~werkzeug.test.EnvironBuilder`.
    :param kwargs: other keyword arguments passed to
        :class:`~werkzeug.test.EnvironBuilder`.
    app = Flask('flask_test', root_path=os.path.dirname(__file__))
    assert called == ['flask_test', 'TEARDOWN']
        if url_prefix and url_prefix[-1] == '/':
            url_prefix = url_prefix[:-1]
def test_blueprint_prefix_slash(app, client):
    bp = flask.Blueprint('test', __name__, url_prefix='/bar/')
    @bp.route('/foo')
    def foo():
        return '', 204
    app.register_blueprint(bp)
    app.register_blueprint(bp, url_prefix='/spam/')
    assert client.get('/bar/foo').status_code == 204
    assert client.get('/spam/foo').status_code == 204
def test_blueprint_url_defaults(app, client):
    .. versionadded:: 1.0
       The ``host_matching`` and ``static_host`` parameters were added.
       The ``subdomain_matching`` parameter was added. Subdomain
       matching needs to be enabled manually now. Setting
       :data:`SERVER_NAME` does not implicitly enable it.
    :param static_host: the host to use when adding the static route.
        Defaults to None. Required when using ``host_matching=True``
        with a ``static_folder`` configured.
    :param host_matching: set ``url_map.host_matching`` attribute.
        Defaults to False.
    :param subdomain_matching: consider the subdomain relative to
        :data:`SERVER_NAME` when matching routes. Defaults to False.
        is created at a point where the request context is not yet set
        up so the request is passed explicitly.
        .. versionchanged:: 1.0
            :data:`SERVER_NAME` no longer implicitly enables subdomain
            matching. Use :attr:`subdomain_matching` instead.
            # If subdomain matching is disabled (the default), use the
            # default subdomain in all cases. This should be the default
            # in Werkzeug but it currently does not have that feature.
            subdomain = ((self.url_map.default_subdomain or None)
                         if not self.subdomain_matching else None)
            return self.url_map.bind_to_environ(
                request.environ,
                server_name=self.config['SERVER_NAME'],
                subdomain=subdomain)
@pytest.mark.parametrize('matching', (False, True))
def test_subdomain_matching_other_name(matching):
    app = flask.Flask(__name__, subdomain_matching=matching)
    app.config['SERVER_NAME'] = 'localhost.localdomain:3000'
    client = app.test_client()
    @app.route('/')
    def index():
        return '', 204
    # ip address can't match name
    rv = client.get('/', 'http://127.0.0.1:3000/')
    assert rv.status_code == 404 if matching else 204
    # allow all subdomains if matching is disabled
    rv = client.get('/', 'http://www.localhost.localdomain:3000/')
    assert rv.status_code == 404 if matching else 204
    #: The :class:`~click.testing.CliRunner` subclass, by default
    #: :class:`~flask.testing.FlaskCliRunner` that is used by
    #: :meth:`test_cli_runner`. Its ``__init__`` method should take a
    #: Flask app object as the first argument.
    #:
    #: .. versionadded:: 1.0
    test_cli_runner_class = None
    def test_cli_runner(self, **kwargs):
        See :ref:`testing-cli`.
        Returns an instance of :attr:`test_cli_runner_class`, by default
        :class:`~flask.testing.FlaskCliRunner`. The Flask app object is
        passed as the first argument.
        .. versionadded:: 1.0
        cls = self.test_cli_runner_class
        if cls is None:
            from flask.testing import FlaskCliRunner as cls
        return cls(self, **kwargs)
from click.testing import CliRunner
from flask.cli import ScriptInfo
class FlaskCliRunner(CliRunner):
    CLI commands. Typically created using
    :meth:`~flask.Flask.test_cli_runner`. See :ref:`testing-cli`.
    def __init__(self, app, **kwargs):
        self.app = app
        super(FlaskCliRunner, self).__init__(**kwargs)
    def invoke(self, cli=None, args=None, **kwargs):
        :meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
        full method documentation. See :ref:`testing-cli` for examples.
        If the ``obj`` argument is not given, passes an instance of
        :class:`~flask.cli.ScriptInfo` that knows how to load the Flask
        app being tested.
        :param cli: Command object to invoke. Default is the app's
            :attr:`~flask.app.Flask.cli` group.
        :param args: List of strings to invoke the command with.
        :return: a :class:`~click.testing.Result` object.
        if cli is None:
            cli = self.app.cli
        if 'obj' not in kwargs:
            kwargs['obj'] = ScriptInfo(create_app=lambda: self.app)
        return super(FlaskCliRunner, self).invoke(cli, args, **kwargs)
import click
from flask.cli import ScriptInfo
from flask.testing import make_test_environ_builder, FlaskCliRunner
def test_cli_runner_class(app):
    runner = app.test_cli_runner()
    assert isinstance(runner, FlaskCliRunner)
    class SubRunner(FlaskCliRunner):
        pass
    app.test_cli_runner_class = SubRunner
    runner = app.test_cli_runner()
    assert isinstance(runner, SubRunner)
def test_cli_invoke(app):
    @app.cli.command('hello')
    def hello_command():
        click.echo('Hello, World!')
    runner = app.test_cli_runner()
    # invoke with command name
    result = runner.invoke(args=['hello'])
    assert 'Hello' in result.output
    # invoke with command object
    result = runner.invoke(hello_command)
    assert 'Hello' in result.output
def test_cli_custom_obj(app):
    class NS(object):
        called = False
    def create_app():
        NS.called = True
        return app
    @app.cli.command('hello')
    def hello_command():
        click.echo('Hello, World!')
    script_info = ScriptInfo(create_app=create_app)
    runner = app.test_cli_runner()
    runner.invoke(hello_command, obj=script_info)
    assert NS.called
from sphinx.application import Sphinx
def setup(app: Sphinx):
    def cut_module_meta(app, what, name, obj, options, lines):
        if what != 'module':
            return
        lines[:] = [
            line for line in lines
            if not line.startswith((':copyright:', ':license:'))
        ]
    app.connect('autodoc-process-docstring', cut_module_meta)
# -*- coding: utf-8 -*-
Blueprint Example
~~~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
Blueprint Example Tests
~~~~~~~~~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
# -*- coding: utf-8 -*-
Larger App Tests
~~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
    assert b"Hello World!" in rv.data
# -*- coding: utf-8 -*-
yourapplication
~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
# -*- coding: utf-8 -*-
yourapplication.views
~~~~~~~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
    return 'Hello World!'
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
flask.json
~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
# -*- coding: utf-8 -*-
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
# -*- coding: utf-8 -*-
flask.logging
~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    #: because the request was never internally bound.
# -*- coding: utf-8 -*-
    maintainer='Pallets team',
    maintainer_email='contact@palletsprojects.com',
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
# This file was part of Flask-CLI and was modified under the terms of
# its Revised BSD License. Copyright © 2015 CERN.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
# -*- coding: utf-8 -*-
tests.test_json_tag
~~~~~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
# -*- coding: utf-8 -*-
tests.test_logging
~~~~~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
    :copyright: © 2010 by the Pallets team.
tests.test_user_error_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: © 2010 by the Pallets team.
:license: BSD, see LICENSE for more details.
    :copyright: © 2010 by the Pallets team.
import sys
from datetime import date, datetime
from subprocess import PIPE, Popen
_date_strip_re = re.compile(r'(?<=\d)(st|nd|rd|th)')
            if next(lineiter).count('-') != len(match.group(0)):
                change_info = next(lineiter).strip()
            match = re.search(
                r'released on (\w+\s+\d+\w+\s+\d+)(?:, codename (.*))?',
                change_info,
                flags=re.IGNORECASE
            )
        parts = [int(i) for i in version.split('.')]
    string = _date_strip_re.sub('', string)
        contents = re.sub(
            r"^(\s*%s\s*=\s*')(.+?)(')" % pattern,
            inject_version, f.read(),
            flags=re.DOTALL | re.MULTILINE
        )
def build():
    cmd = [sys.executable, 'setup.py', 'sdist', 'bdist_wheel']
    Popen(cmd).wait()
    return set(
        Popen(['git', 'tag'], stdout=PIPE).communicate()[0].splitlines()
    )
    dev_version = bump_version(version) + '.dev'
    info(
        'Releasing %s (codename %s, release date %s)',
        version, codename, release_date.strftime('%d/%m/%Y')
    )
        fail(
            'Release date is not today (%s != %s)',
            release_date.date(), date.today()
        )
    try:
        import wheel  # noqa: F401
    except ImportError:
        fail('You need to install the wheel package.')
    build()
#!/usr/bin/env python
import io
with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()
with io.open('flask/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
    url='https://www.palletsprojects.com/p/flask/',
    description='A simple framework for building complex web applications.',
    long_description=readme,
        try:
            rv = rv.make_conditional(request, accept_ranges=True,
                                     complete_length=fsize)
        except RequestedRangeNotSatisfiable:
            if file is not None:
                file.close()
            raise
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
        'Werkzeug>=0.14',
        'Jinja2>=2.10',
        'itsdangerous>=0.24',
        'click>=5.1',
        'Development Status :: 5 - Production/Stable',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    entry_points={
        'console_scripts': [
            'flask = flask.cli:main',
        ],
    },
                if not _called_with_wrong_args(app_factory):
def _called_with_wrong_args(factory):
    the call failed or because something in the factory raised the
    error.
    :param factory: the factory function that was called
    :return: true if the call failed
    tb = sys.exc_info()[2]
    try:
        while tb is not None:
            if tb.tb_frame.f_code is factory.__code__:
                # in the factory, it was called successfully
                return False
            tb = tb.tb_next
        # didn't reach the factory
        return True
    finally:
        del tb
            if not _called_with_wrong_args(attr):
    with open('CHANGES.rst') as f:
        ``SameSite`` attribute. This currently just returns the value of
        the :data:`SESSION_COOKIE_SAMESITE` setting.
        SESSION_COOKIE_SAMESITE='Lax',
    app.config.update(SESSION_COOKIE_SAMESITE='invalid')
        client.get('/')
    rv = client.get('/')
    rv = client.get('/')
    rv = client.get('/')
import ssl
from werkzeug.utils import import_string
from ._compat import getargspec, iteritems, reraise, text_type
class CertParamType(click.ParamType):
    existing file, the string ``'adhoc'``, or an import for a
    :class:`~ssl.SSLContext` object.
    name = 'path'
    def __init__(self):
        self.path_type = click.Path(
            exists=True, dir_okay=False, resolve_path=True)
    def convert(self, value, param, ctx):
        try:
            return self.path_type(value, param, ctx)
        except click.BadParameter:
            value = click.STRING(value, param, ctx).lower()
            if value == 'adhoc':
                try:
                    import OpenSSL
                except ImportError:
                    raise click.BadParameter(
                        'Using ad-hoc certificates requires pyOpenSSL.',
                        ctx, param)
                return value
            obj = import_string(value, silent=True)
            if sys.version_info < (2, 7):
                if obj:
                    return obj
            else:
                if isinstance(obj, ssl.SSLContext):
                    return obj
            raise
def _validate_key(ctx, param, value):
    Modifies the ``cert`` param to be a ``(cert, key)`` pair if needed.
    cert = ctx.params.get('cert')
    is_adhoc = cert == 'adhoc'
    if sys.version_info < (2, 7):
        is_context = cert and not isinstance(cert, (text_type, bytes))
    else:
        is_context = isinstance(cert, ssl.SSLContext)
    if value is not None:
        if is_adhoc:
            raise click.BadParameter(
                'When "--cert" is "adhoc", "--key" is not used.',
                ctx, param)
        if is_context:
            raise click.BadParameter(
                'When "--cert" is an SSLContext object, "--key is not used.',
                ctx, param)
        if not cert:
            raise click.BadParameter(
                '"--cert" must also be specified.',
                ctx, param)
        ctx.params['cert'] = cert, value
    else:
        if cert and not (is_adhoc or is_context):
            raise click.BadParameter(
                'Required when using "--cert".',
                ctx, param)
    return value
@click.option('--cert', type=CertParamType(),
              help='Specify a certificate file to use HTTPS.')
@click.option('--key',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              callback=_validate_key, expose_value=False,
              help='The key file to use when specifying a certificate.')
              help='Enable or disable the reloader. By default the reloader '
              help='Enable or disable the debugger. By default the debugger '
              help='Enable or disable eager loading. By default eager '
                with_threads, cert):
               threaded=with_threads, ssl_context=cert)
import ssl
import types
    AppGroup, FlaskGroup, NoAppException, ScriptInfo, dotenv, find_best_app,
    get_version, load_dotenv, locate_app, prepare_import, run_command,
def test_run_cert_path():
    # no key
    with pytest.raises(click.BadParameter):
        run_command.make_context('run', ['--cert', __file__])
    # no cert
    with pytest.raises(click.BadParameter):
        run_command.make_context('run', ['--key', __file__])
    ctx = run_command.make_context(
        'run', ['--cert', __file__, '--key', __file__])
    assert ctx.params['cert'] == (__file__, __file__)
def test_run_cert_adhoc(monkeypatch):
    monkeypatch.setitem(sys.modules, 'OpenSSL', None)
    # pyOpenSSL not installed
    with pytest.raises(click.BadParameter):
        run_command.make_context('run', ['--cert', 'adhoc'])
    # pyOpenSSL installed
    monkeypatch.setitem(sys.modules, 'OpenSSL', types.ModuleType('OpenSSL'))
    ctx = run_command.make_context('run', ['--cert', 'adhoc'])
    assert ctx.params['cert'] == 'adhoc'
    # no key with adhoc
    with pytest.raises(click.BadParameter):
        run_command.make_context('run', ['--cert', 'adhoc', '--key', __file__])
def test_run_cert_import(monkeypatch):
    monkeypatch.setitem(sys.modules, 'not_here', None)
    # ImportError
    with pytest.raises(click.BadParameter):
        run_command.make_context('run', ['--cert', 'not_here'])
    # not an SSLContext
    if sys.version_info >= (2, 7):
        with pytest.raises(click.BadParameter):
            run_command.make_context('run', ['--cert', 'flask'])
    # SSLContext
    if sys.version_info < (2, 7):
        ssl_context = object()
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    monkeypatch.setitem(sys.modules, 'ssl_context', ssl_context)
    ctx = run_command.make_context('run', ['--cert', 'ssl_context'])
    assert ctx.params['cert'] is ssl_context
    # no --key with SSLContext
    with pytest.raises(click.BadParameter):
        run_command.make_context(
            'run', ['--cert', 'ssl_context', '--key', __file__])
    #: What environment the app is running in. Flask and extensions may
    #: enable behaviors based on the environment, such as enabling debug
    #: mode. This maps to the :data:`ENV` config key. This is set by the
    #: :envvar:`FLASK_ENV` environment variable and may not behave as
    #: expected if set in code.
    #:
    #: **Do not enable development when deploying in production.**
    #:
    #: Default: ``'production'``
        self.config['DEBUG'] = value
        self.jinja_env.auto_reload = self.templates_auto_reload
    #: Whether debug mode is enabled. When using ``flask run`` to start
    #: the development server, an interactive debugger will be shown for
    #: unhandled exceptions, and the server will be reloaded when code
    #: changes. This maps to the :data:`DEBUG` config key. This is
    #: enabled when :attr:`env` is ``'development'`` and is overridden
    #: by the ``FLASK_DEBUG`` environment variable. It may not behave as
    #: expected if set in code.
    #: **Do not enable debug mode when deploying in production.**
    #:
    #: Default: ``True`` if :attr:`env` is ``'development'``, or
    #: ``False`` otherwise.
    :envvar:`FLASK_ENV` environment variable. The default is
    ``'production'``.
    return os.environ.get('FLASK_ENV') or 'production'
    by the :envvar:`FLASK_DEBUG` environment variable. The default is
    ``True`` if :func:`.get_env` returns ``'development'``, or ``False``
    otherwise.
        return get_env() == 'development'
import sys
import pytest
from _pytest import monkeypatch
import flask
@pytest.fixture(scope='session', autouse=True)
def _standard_os_environ():
    standard values. Returns a list of operations that is used by
    :func:`._reset_os_environ` after each test.
    mp = monkeypatch.MonkeyPatch()
    out = (
        (os.environ, 'FLASK_APP', monkeypatch.notset),
        (os.environ, 'FLASK_ENV', monkeypatch.notset),
        (os.environ, 'FLASK_DEBUG', monkeypatch.notset),
        (os.environ, 'FLASK_RUN_FROM_CLI', monkeypatch.notset),
        (os.environ, 'WERKZEUG_RUN_MAIN', monkeypatch.notset),
    )
    for _, key, value in out:
        if value is monkeypatch.notset:
            mp.delenv(key, False)
        else:
            mp.setenv(key, value)
    yield out
    mp.undo()
@pytest.fixture(autouse=True)
def _reset_os_environ(monkeypatch, _standard_os_environ):
    in case a test changed something without cleaning up.
    monkeypatch._setitem.extend(_standard_os_environ)
from flask.cli import (
    AppGroup, FlaskGroup, NoAppException, ScriptInfo, dotenv,
    find_best_app, get_version, load_dotenv, locate_app, prepare_import,
)
            If set, the :envvar:`FLASK_ENV` and :envvar:`FLASK_DEBUG`
            environment variables will override :attr:`env` and
            :attr:`debug`.
            Threaded mode is enabled by default.
        .. versionchanged:: 0.10
            The default port is now picked from the ``SERVER_NAME``
            variable.
        # command line. Have a look at cli.py for more information.
            cli.load_dotenv()
            # if set, let env vars override previous values
            if 'FLASK_ENV' in os.environ:
                self.env = get_env()
                self.debug = get_debug_flag()
            elif 'FLASK_DEBUG' in os.environ:
                self.debug = get_debug_flag()
        # debug passed to method overrides all other sources
        options.setdefault('threaded', True)
        cli.show_server_banner(self.env, self.debug, self.name)
def show_server_banner(env, debug, app_import_path):
    ignoring the reloader.
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        return
    if app_import_path is not None:
        print(' * Serving Flask app "{0}"'.format(app_import_path))
    print(' * Environment: {0}'.format(env))
    if env == 'production':
        click.secho(
            '   WARNING: Do not use the development server in a production'
            ' environment.', fg='red')
        click.secho('   Use a production WSGI server instead.', dim=True)
    if debug is not None:
        print(' * Debug mode: {0}'.format('on' if debug else 'off'))
    This server is for development purposes only. It does not provide
    the stability, security, or performance of production WSGI servers.
    The reloader and debugger are enabled by default if
    FLASK_ENV=development or FLASK_DEBUG=1.
        reload = debug
        debugger = debug
    show_server_banner(get_env(), debug, info.app_import_path)
    from werkzeug.serving import run_simple
    run_simple(host, port, app, use_reloader=reload, use_debugger=debugger,
               threaded=with_threads)
from ._compat import string_types, text_type, PY2
    Python 2 on Windows doesn't provide ``inet_pton``, so this only
    checks IPv4 addresses in that environment.
    if PY2 and os.name == 'nt':
        try:
            socket.inet_aton(value)
            return True
        except socket.error:
            return False
def app():
    db_fd, db_path = tempfile.mkstemp()
        'DATABASE': db_path,
    os.close(db_fd)
    os.unlink(db_path)
@pytest.fixture
def client(app):
    return app.test_client()
            if silent and e.errno in (
                errno.ENOENT, errno.EISDIR, errno.ENOTDIR
            ):
from collections import MutableMapping
class SessionMixin(MutableMapping):
    @property
    def permanent(self):
    @permanent.setter
    def permanent(self, value):
    #: Some implementations can detect whether a session is newly
    #: created, but that is not guaranteed. Use with caution. The mixin
    # default is hard-coded ``False``.
    #: Some implementations can detect changes to the session and set
    #: this when that happens. The mixin default is hard coded to
    #: ``True``.
    #: Some implementations can detect when session data is read or
    #: written and set this when that happens. The mixin default is hard
    #: coded to ``True``.
    This session backend will set the :attr:`modified` and
    :attr:`accessed` attributes. It cannot reliably track whether a
    session is new (vs. empty), so :attr:`new` remains hard coded to
    ``False``.
    #: When data is changed, this is set to ``True``. Only the session
    #: dictionary itself is tracked; if the session contains mutable
    #: data (for example a nested dict) then this must be set to
    #: ``True`` manually when modifying that data. The session cookie
    #: will only be written to the response if this is ``True``.
    modified = False
    #: When data is read or written, this is set to ``True``. Used by
    # :class:`.SecureCookieSessionInterface` to add a ``Vary: Cookie``
    #: header, which allows caching proxies to cache different pages for
    #: different users.
    accessed = False
        assert not flask.session.accessed
        assert not flask.session.modified
        assert flask.session.accessed
        assert flask.session.modified
        assert not flask.session.accessed
        assert not flask.session.modified
        v = flask.session.get('value', 'None')
        assert flask.session.accessed
        assert not flask.session.modified
        return v
        dumps(data, indent=indent, separators=separators) + '\n',
def reset_logging(pytestconfig):
    logging.root.handlers = []
    logging_plugin = pytestconfig.pluginmanager.unregister(
        name='logging-plugin')
        pytestconfig.pluginmanager.register(logging_plugin, 'logging-plugin')
version_option = click.Option(
    ['--version'],
    help='Show the flask version',
    expose_value=False,
    callback=get_version,
    is_flag=True,
    is_eager=True
)
A general utility script for Flask applications.
Provides commands from Flask, extensions, and the application. Loads the
application defined in the FLASK_APP environment variable, or from a wsgi.py
file. Debug mode can be controlled with the FLASK_DEBUG
environment variable.
  {prefix}{cmd} FLASK_APP=hello.py
  {prefix}{cmd} FLASK_DEBUG=1
  {prefix}flask run
    cmd='export' if os.name == 'posix' else 'set',
    prefix='$ ' if os.name == 'posix' else '> '
))
            'Detected multiple Flask applications in module "{module}". Use '
            '"FLASK_APP={module}:name" to specify the correct '
            'one.'.format(module=module.__name__)
                app = call_factory(script_info, app_factory)
                    'Detected factory "{factory}" in module "{module}", but '
                    'could not call it without arguments. Use '
                    '"FLASK_APP=\'{module}:{factory}(args)\'" to specify '
                    'arguments.'.format(
                        factory=attr_name, module=module.__name__
        'Failed to find Flask application or factory in module "{module}". '
        'Use "FLASK_APP={module}:name to specify one.'.format(
            module=module.__name__
        )
def call_factory(script_info, app_factory, arguments=()):
def find_app_by_string(script_info, module, app_name):
    function, it checks for specified arguments and whether it takes a
    ``script_info`` argument and calls the function with the appropriate
    arguments.
    from flask import Flask
    match = re.match(r'^ *([^ ()]+) *(?:\((.*?) *,? *\))? *$', app_name)
    if not match:
        raise NoAppException(
            '"{name}" is not a valid variable name or function '
            'expression.'.format(name=app_name)
        )
    name, args = match.groups()
    try:
        attr = getattr(module, name)
    except AttributeError as e:
        raise NoAppException(e.args[0])
    if inspect.isfunction(attr):
        if args:
            try:
                args = ast.literal_eval('({args},)'.format(args=args))
            except (ValueError, SyntaxError)as e:
                raise NoAppException(
                    'Could not parse the arguments in '
                    '"{app_name}".'.format(e=e, app_name=app_name)
                )
        else:
            args = ()
            app = call_factory(script_info, attr, args)
            raise NoAppException(
                '{e}\nThe factory "{app_name}" in module "{module}" could not '
                'be called with the specified arguments.'.format(
                    e=e, app_name=app_name, module=module.__name__
                )
            )
        app = attr
    if isinstance(app, Flask):
        return app
    raise NoAppException(
        'A valid Flask application was not obtained from '
        '"{module}:{app_name}".'.format(
            module=module.__name__, app_name=app_name
        )
    )
        return find_app_by_string(script_info, module, app_name)
            app = call_factory(self, self.create_app)
def no_app():
    pass
    # strip whitespace
    ('cliapp.factory', ' create_app () ', 'app'),
    # invalid identifier
    ('cliapp.factory', 'create_app('),
    # no app returned
    ('cliapp.factory', 'no_app'),
    'itsdangerous': ('https://pythonhosted.org/itsdangerous', None),
    'blinker': ('https://pythonhosted.org/blinker/', None),
from werkzeug.datastructures import Headers, ImmutableDict
from werkzeug.exceptions import BadRequest, BadRequestKeyError, HTTPException, \
    InternalServerError, MethodNotAllowed, default_exceptions
from .logging import create_logger
    @locked_cached_property
        :class:`~logging.Logger`.
        In debug mode, the logger's :attr:`~logging.Logger.level` will be set
        to :data:`~logging.DEBUG`.
        If there are no handlers configured, a default handler will be added.
        See :ref:`logging` for more information.
        .. versionchanged:: 1.0
            Behavior was simplified. The logger is always named
            ``flask.app``. The level is only set during configuration, it
            doesn't check ``app.debug`` each time. Only one format is used,
            not different ones depending on ``app.debug``. No handlers are
            removed, and a handler is only added if no handlers are already
            configured.
        return create_logger(self)
import logging
from .globals import request
def wsgi_errors_stream():
    is active, log to ``wsgi.errors``, otherwise use ``sys.stderr``.
    If you configure your own :class:`logging.StreamHandler`, you may want to
    use this for the stream. If you are using file or dict configuration and
    can't import this directly, you can refer to it as
    ``ext://flask.logging.wsgi_errors_stream``.
    return request.environ['wsgi.errors'] if request else sys.stderr
def has_level_handler(logger):
    given logger's :meth:`effective level <~logging.Logger.getEffectiveLevel>`.
    level = logger.getEffectiveLevel()
    current = logger
    while current:
        if any(handler.level <= level for handler in current.handlers):
            return True
        if not current.propagate:
            break
        current = current.parent
#: Log messages to :func:`~flask.logging.wsgi_errors_stream` with the format
#: ``[%(asctime)s] %(levelname)s in %(module)s: %(message)s``.
default_handler = logging.StreamHandler(wsgi_errors_stream)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
    When :attr:`~flask.Flask.debug` is enabled, set the logger level to
    :data:`logging.DEBUG` if it is not set.
    If there is no handler for the logger's effective level, add a
    :class:`~logging.StreamHandler` for
    :func:`~flask.logging.wsgi_errors_stream` with a basic format.
    logger = logging.getLogger('flask.app')
    if app.debug and logger.level == logging.NOTSET:
        logger.setLevel(logging.DEBUG)
    if not has_level_handler(logger):
        logger.addHandler(default_handler)
def test_error_handler_after_processor_error(app, client):
    app.testing = False
    @app.before_request
    def before_request():
        if trigger == 'before':
            1 // 0
    @app.after_request
    def after_request(response):
        if trigger == 'after':
            1 // 0
        return response
    @app.route('/')
    def index():
        return 'Foo'
    @app.errorhandler(500)
    def internal_server_error(e):
        return 'Hello Server Error', 500
    for trigger in 'before', 'after':
        rv = client.get('/')
        assert rv.status_code == 500
        assert rv.data == b'Hello Server Error'
import datetime
import pytest
from werkzeug.http import http_date, parse_cache_control_header, \
    parse_options_header
import flask
from flask.helpers import get_debug_flag
class TestUrlFor(object):
import logging
import sys
import pytest
from flask._compat import StringIO
from flask.logging import default_handler, has_level_handler, \
    wsgi_errors_stream
@pytest.fixture(autouse=True)
def reset_logging(monkeypatch):
    root_handlers = logging.root.handlers[:]
    root_level = logging.root.level
    logger = logging.getLogger('flask.app')
    logger.handlers = []
    logger.setLevel(logging.NOTSET)
    yield
    logging.root.handlers[:] = root_handlers
    logging.root.setLevel(root_level)
    logger.handlers = []
    logger.setLevel(logging.NOTSET)
def test_logger(app):
    assert app.logger.name == 'flask.app'
    assert app.logger.level == logging.NOTSET
    assert app.logger.handlers == [default_handler]
def test_logger_debug(app):
    app.debug = True
    assert app.logger.level == logging.DEBUG
    assert app.logger.handlers == [default_handler]
def test_existing_handler(app):
    logging.root.addHandler(logging.StreamHandler())
    assert app.logger.level == logging.NOTSET
    assert not app.logger.handlers
def test_wsgi_errors_stream(app, client):
    @app.route('/')
    def index():
        app.logger.error('test')
        return ''
    stream = StringIO()
    client.get('/', errors_stream=stream)
    assert 'ERROR in test_logging: test' in stream.getvalue()
    assert wsgi_errors_stream._get_current_object() is sys.stderr
    with app.test_request_context(errors_stream=stream):
        assert wsgi_errors_stream._get_current_object() is stream
def test_has_level_handler():
    logger = logging.getLogger('flask.app')
    assert not has_level_handler(logger)
    handler = logging.StreamHandler()
    logging.root.addHandler(handler)
    assert has_level_handler(logger)
    logger.propagate = False
    assert not has_level_handler(logger)
    logger.propagate = True
    handler.setLevel(logging.ERROR)
    assert not has_level_handler(logger)
def test_log_view_exception(app, client):
    @app.route('/')
    def index():
        raise Exception('test')
    app.testing = False
    stream = StringIO()
    rv = client.get('/', errors_stream=stream)
    assert rv.status_code == 500
    assert rv.data
    err = stream.getvalue()
    assert 'Exception on / [GET]' in err
    assert 'Exception: test' in err
        raise Exception('test')
    rv = app.test_client().get('/', errors_stream=out)
    assert not out.getvalue()
def test_template_loader_debugging(test_apps, monkeypatch):
        monkeypatch.setitem(app.config, 'EXPLAIN_TEMPLATE_LOADING', True)
        monkeypatch.setattr(
            logging.getLogger('flask'), 'handlers', [_TestHandler()]
        )
        with pytest.raises(TemplateNotFound) as excinfo:
            c.get('/missing')
        assert 'missing_template.html' in str(excinfo.value)
            url_scheme = app.config['PREFERRED_URL_SCHEME']
        url = url_parse(path)
        base_url = '{scheme}://{netloc}/{path}'.format(
            scheme=url.scheme or url_scheme,
            netloc=url.netloc or http_host,
            path=app_root.lstrip('/')
def test_path_is_url(app):
    eb = make_test_environ_builder(app, 'https://example.com/')
    assert eb.url_scheme == 'https'
    assert eb.host == 'example.com'
    assert eb.script_root == ''
    assert eb.path == '/'
    def run(
        self, host=None, port=None, debug=None, load_dotenv=True, **options
    ):
        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
            have the server available externally as well. Defaults to
            ``'127.0.0.1'`` or the host in the ``SERVER_NAME`` config variable
            if present.
        :param port: the port of the webserver. Defaults to ``5000`` or the
            port defined in the ``SERVER_NAME`` config variable if present.
        :param debug: if given, enable or disable debug mode. See
            :attr:`debug`.
        :param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
            files to set environment variables. Will also change the working
            directory to the directory containing the first file found.
        :param options: the options to be forwarded to the underlying Werkzeug
            server. See :func:`werkzeug.serving.run_simple` for more
            information.
        .. versionchanged:: 1.0
            If installed, python-dotenv will be used to load environment
            variables from :file:`.env` and :file:`.flaskenv` files.
        if os.environ.get('FLASK_RUN_FROM_CLI') == 'true':
        if load_dotenv:
            from flask.cli import load_dotenv
            load_dotenv()
from __future__ import print_function
from ._compat import getargspec, iteritems, reraise
try:
    import dotenv
except ImportError:
    dotenv = None
        shell commands wil be added.
    :param create_app: an optional callback that is passed the script info and
        returns the loaded app.
    :param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
        files to set environment variables. Will also change the working
        directory to the directory containing the first file found.
    .. versionchanged:: 1.0
        If installed, python-dotenv will be used to load environment variables
        from :file:`.env` and :file:`.flaskenv` files.
    def __init__(
        self, add_default_commands=True, create_app=None,
        add_version_option=True, load_dotenv=True, **extra
    ):
        self.load_dotenv = load_dotenv
        # Set a global flag that indicates that we were invoked from the
        # command line interface. This is detected by Flask.run to make the
        # call into a no-op. This is necessary to avoid ugly errors when the
        # script that is loaded here also attempts to start a server.
        os.environ['FLASK_RUN_FROM_CLI'] = 'true'
        if self.load_dotenv:
            load_dotenv()
        return super(FlaskGroup, self).main(*args, **kwargs)
def _path_is_ancestor(path, other):
    to ``path``. If it is the original value, ``path`` is an ancestor of
    ``other``."""
    return os.path.join(path, other[len(path):].lstrip(os.sep)) == other
def load_dotenv(path=None):
    If an env var is already set it is not overwritten, so earlier files in the
    list are preferred over later files.
    Changes the current working directory to the location of the first file
    found, with the assumption that it is in the top level project directory
    and will be where the Python path should import local packages from.
    This is a no-op if `python-dotenv`_ is not installed.
    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme
    :param path: Load the file at this location instead of searching.
    :return: ``True`` if a file was loaded.
    .. versionadded:: 1.0
    if dotenv is None:
        return
    if path is not None:
        return dotenv.load_dotenv(path)
    new_dir = None
    for name in ('.env', '.flaskenv'):
        path = dotenv.find_dotenv(name, usecwd=True)
        if not path:
            continue
        if new_dir is None:
            new_dir = os.path.dirname(path)
        dotenv.load_dotenv(path)
    if new_dir and os.getcwd() != new_dir:
        os.chdir(new_dir)
    return new_dir is not None  # at least one file was located and loaded
        'dotenv': ['python-dotenv'],
            'python-dotenv',
from _pytest.monkeypatch import notset
from flask.cli import AppGroup, FlaskGroup, NoAppException, ScriptInfo, dotenv, \
    find_best_app, get_version, load_dotenv, locate_app, prepare_import, \
    with_appcontext
cwd = os.getcwd()
test_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'test_apps'
))
@pytest.fixture(autouse=True)
def manage_os_environ(monkeypatch):
    # can't use monkeypatch.delitem since we don't want to restore a value
    os.environ.pop('FLASK_APP', None)
    os.environ.pop('FLASK_DEBUG', None)
    # use monkeypatch internals to force-delete environ keys
    monkeypatch._setitem.extend((
        (os.environ, 'FLASK_APP', notset),
        (os.environ, 'FLASK_DEBUG', notset),
        (os.environ, 'FLASK_RUN_FROM_CLI', notset),
    ))
need_dotenv = pytest.mark.skipif(
    dotenv is None, reason='dotenv is not installed'
)
@need_dotenv
def test_load_dotenv(monkeypatch):
    # can't use monkeypatch.delitem since the keys don't exist yet
    for item in ('FOO', 'BAR', 'SPAM'):
        monkeypatch._setitem.append((os.environ, item, notset))
    monkeypatch.setenv('EGGS', '3')
    monkeypatch.chdir(os.path.join(test_path, 'cliapp', 'inner1'))
    load_dotenv()
    assert os.getcwd() == test_path
    # .flaskenv doesn't overwrite .env
    assert os.environ['FOO'] == 'env'
    # set only in .flaskenv
    assert os.environ['BAR'] == 'bar'
    # set only in .env
    assert os.environ['SPAM'] == '1'
    # set manually, files don't overwrite
    assert os.environ['EGGS'] == '3'
@need_dotenv
def test_dotenv_path(monkeypatch):
    for item in ('FOO', 'BAR', 'EGGS'):
        monkeypatch._setitem.append((os.environ, item, notset))
    cwd = os.getcwd()
    load_dotenv(os.path.join(test_path, '.flaskenv'))
    assert os.getcwd() == cwd
    assert 'FOO' in os.environ
def test_dotenv_optional(monkeypatch):
    monkeypatch.setattr('flask.cli.dotenv', None)
    monkeypatch.chdir(test_path)
    load_dotenv()
    assert 'FOO' not in os.environ
                raise NoAppException('Failed to find application in module '
def prepare_import(path):
    path = os.path.realpath(path)
    if os.path.splitext(path)[1] == '.py':
        path = os.path.splitext(path)[0]
    if os.path.basename(path) == '__init__':
        path = os.path.dirname(path)
    module_name = []
    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)
        if not os.path.exists(os.path.join(path, '__init__.py')):
    if sys.path[0] != path:
        sys.path.insert(0, path)
    return '.'.join(module_name[::-1])
def locate_app(script_info, module_name, app_name, raise_if_not_found=True):
        __import__(module_name)
                'While importing "{name}", an ImportError was raised:'
                '\n\n{tb}'.format(name=module_name, tb=traceback.format_exc())
                'Could not import "{name}"."'.format(name=module_name)
    module = sys.modules[module_name]
    if app_name is None:
        return find_best_app(script_info, module)
        return find_app_by_string(app_name, script_info, module)
        self.app_import_path = app_import_path or os.environ.get('FLASK_APP')
        app = None
            app = call_factory(self.create_app, self)
                path, name = (self.app_import_path.split(':', 1) + [None])[:2]
                import_name = prepare_import(path)
                app = locate_app(self, import_name, name)
                for path in ('wsgi.py', 'app.py'):
                    import_name = prepare_import(path)
                    app = locate_app(
                        self, import_name, None, raise_if_not_found=False
                    if app:
        if not app:
            raise NoAppException(
                'Could not locate a Flask application. You did not provide '
                'the "FLASK_APP" environment variable, and a "wsgi.py" or '
                '"app.py" module was not found in the current directory.'
            )
            app._reconfigure_for_run_debug(debug)
        self._loaded_app = app
        return app
    return Flask('app')
    return Flask('_'.join(['app2', foo, bar]))
def create_app3(foo, script_info):
    return Flask('_'.join(['app3', foo, script_info.data['test']]))
from flask import Flask
application = Flask(__name__)
from flask import Flask
app = Flask(__name__)
from __future__ import absolute_import
from flask import Flask, current_app
from flask.cli import AppGroup, FlaskGroup, NoAppException, ScriptInfo, \
    find_best_app, get_version, locate_app, prepare_import, with_appcontext
cwd = os.getcwd()
test_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'test_apps'
))
@pytest.mark.parametrize('value,path,result', (
    ('test', cwd, 'test'),
    ('test.py', cwd, 'test'),
    ('a/test', os.path.join(cwd, 'a'), 'test'),
    ('test/__init__.py', cwd, 'test'),
    ('test/__init__', cwd, 'test'),
    # nested package
    (
        os.path.join(test_path, 'cliapp', 'inner1', '__init__'),
        test_path, 'cliapp.inner1'
    ),
    (
        os.path.join(test_path, 'cliapp', 'inner1', 'inner2'),
        test_path, 'cliapp.inner1.inner2'
    ),
    # dotted name
    ('test.a.b', cwd, 'test.a.b'),
    (os.path.join(test_path, 'cliapp.app'), test_path, 'cliapp.app'),
    # not a Python file, will be caught during import
    (
        os.path.join(test_path, 'cliapp', 'message.txt'),
        test_path, 'cliapp.message.txt'
    ),
))
def test_prepare_import(request, value, path, result):
    to be returned.
    :func:`prepare_exec_for_file` has a side effect where the parent directory
    of the given import is added to :data:`sys.path`. This is reset after the
    test runs.
    original_path = sys.path[:]
    def reset_path():
        sys.path[:] = original_path
    request.addfinalizer(reset_path)
    assert prepare_import(value) == result
    assert sys.path[0] == path
@pytest.mark.parametrize('iname,aname,result', (
    ('cliapp.app', None, 'testapp'),
    ('cliapp.app', 'testapp', 'testapp'),
    ('cliapp.factory', None, 'app'),
    ('cliapp.factory', 'create_app', 'app'),
    ('cliapp.factory', 'create_app()', 'app'),
    # no script_info
    ('cliapp.factory', 'create_app2("foo", "bar")', 'app2_foo_bar'),
    # trailing comma space
    ('cliapp.factory', 'create_app2("foo", "bar", )', 'app2_foo_bar'),
    # takes script_info
    ('cliapp.factory', 'create_app3("foo")', 'app3_foo_spam'),
))
def test_locate_app(test_apps, iname, aname, result):
    info = ScriptInfo()
    info.data['test'] = 'spam'
    assert locate_app(info, iname, aname).name == result
@pytest.mark.parametrize('iname,aname', (
    ('notanapp.py', None),
    ('cliapp/app', None),
    ('cliapp.app', 'notanapp'),
    # not enough arguments
    ('cliapp.factory', 'create_app2("foo")'),
    # nested import error
    ('cliapp.importerrorapp', None),
    # not a Python file
    ('cliapp.message.txt', None),
    # space before arg list
    ('cliapp.factory', 'create_app ()'),
))
def test_locate_app_raises(test_apps, iname, aname):
    info = ScriptInfo()
        locate_app(info, iname, aname)
def test_locate_app_suppress_raise():
    info = ScriptInfo()
    app = locate_app(info, 'notanapp.py', None, raise_if_not_found=False)
    assert app is None
    # only direct import error is suppressed
    with pytest.raises(NoAppException):
        locate_app(
            info, 'cliapp.importerrorapp', None, raise_if_not_found=False
        )
        if (
            not kwargs and len(args) == 1
            and isinstance(args[0], (EnvironBuilder, dict))
        ):
            environ = self.environ_base.copy()
            if isinstance(args[0], EnvironBuilder):
                environ.update(args[0].get_environ())
            else:
                environ.update(args[0])
            environ['flask._preserve_context'] = self.preserve_context
        else:
            kwargs.setdefault('environ_overrides', {}) \
                ['flask._preserve_context'] = self.preserve_context
            kwargs.setdefault('environ_base', self.environ_base)
            builder = make_test_environ_builder(
                self.application, *args, **kwargs
            )
            try:
                environ = builder.get_environ()
            finally:
                builder.close()
        return Client.open(
            self, environ,
            as_tuple=as_tuple,
            buffered=buffered,
            follow_redirects=follow_redirects
        )
from flask.testing import make_test_environ_builder
def test_client_open_environ(app, client, request):
    @app.route('/index')
    def index():
        return flask.request.remote_addr
    builder = make_test_environ_builder(app, path='/index', method='GET')
    request.addfinalizer(builder.close)
    rv = client.open(builder)
    assert rv.data == b'127.0.0.1'
    environ = builder.get_environ()
    client.environ_base['REMOTE_ADDR'] = '127.0.0.2'
    rv = client.open(environ)
    assert rv.data == b'127.0.0.2'
        it will be passed an error object. If an :meth:`errorhandler` is
        registered, it will handle the exception and the teardown will not
def test_app_tearing_down_with_handled_exception_by_app_handler(app, client):
    app.config['PROPAGATE_EXCEPTIONS'] = True
        client.get('/')
def test_app_tearing_down_with_unhandled_exception(app, client):
    app.config['PROPAGATE_EXCEPTIONS'] = True
            client.get('/')
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    #: sign cookies and other things. Set this to a complex random value
    #: :data:`SECRET_KEY` configuration key. Defaults to ``None``.
    secret_key = 'test key'
def test_missing_session(app):
    app.secret_key = None
SECRET_KEY = 'config'
    assert app.secret_key == 'config'
        'SECRET_KEY': 'config',
        ('SECRET_KEY', 'config'),
        SECRET_KEY='config',
        SECRET_KEY = 'config'
def test_flash_signal(app):
    packages=['flask', 'flask.json'],
        raise RuntimeError(
            'Attempted to generate a URL without the application context being'
            ' pushed. This has to be executed when application context is'
            ' available.'
        )
        if endpoint[:1] == '.':
            if blueprint_name is not None:
                endpoint = blueprint_name + endpoint
            else:
            raise RuntimeError(
                'Application was not able to create a URL adapter for request'
                ' independent URL generation. You might be able to fix this by'
                ' setting the SERVER_NAME config variable.'
            )
    def __init__(
        self,
        import_name,
        static_url_path=None,
        static_folder='static',
        static_host=None,
        host_matching=False,
        template_folder='templates',
        instance_path=None,
        instance_relative_config=False,
        root_path=None
    ):
        _PackageBoundObject.__init__(
            self,
            import_name,
            template_folder=template_folder,
            root_path=root_path
        )
            raise ValueError(
                'If an instance path is provided it must be absolute.'
                ' A relative path was given instead.'
            )
            self.add_url_rule(
                self.static_url_path + '/<path:filename>',
                endpoint='static',
                host=static_host,
                view_func=self.send_static_file
            )
        self.error_handler_spec = {}
            raise NoAppException(
                'There was an error trying to import the app ({module}):\n'
                '{stack_trace}'.format(
                    module=module, stack_trace=stack_trace
                )
            )
            raise NoAppException(
                'The file/path provided (%s) does not appear to exist. Please'
                ' verify the path is correct. If app is not on PYTHONPATH,'
                ' ensure the extension is .py.'.format(module=module)
            )
                    rv = locate_app(
                        self, import_path, raise_if_not_found=False
                    )
                    'http://flask.pocoo.org/docs/latest/quickstart/'
                )
    assert locate_app(
        script_info, "notanpp.py", raise_if_not_found=False
    ) is None
    pytest.raises(NoAppException, obj.load_app)
    monkeypatch.chdir(os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'test_apps', 'helloworld'
    )))
    monkeypatch.chdir(os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'test_apps', 'cliapp'
    )))
def test_templates_auto_reload_debug_run(app, monkeypatch):
    app.run()
    assert app.templates_auto_reload == False
    assert app.jinja_env.auto_reload == False
    assert app.templates_auto_reload == True
    assert app.jinja_env.auto_reload == True
    def _get_templates_auto_reload(self):
        :meth:`create_jinja_environment`.
        This attribute can be configured with :data:`TEMPLATES_AUTO_RELOAD`. If
        not set, it will be enabled in debug mode.
        .. versionadded:: 1.0
            This property was added but the underlying config and behavior
            already existed.
        rv = self.config['TEMPLATES_AUTO_RELOAD']
        return rv if rv is not None else self.debug
    def _set_templates_auto_reload(self, value):
        self.config['TEMPLATES_AUTO_RELOAD'] = value
    templates_auto_reload = property(
        _get_templates_auto_reload, _set_templates_auto_reload
    )
    del _get_templates_auto_reload, _set_templates_auto_reload
            options['auto_reload'] = self.templates_auto_reload
    def _reconfigure_for_run_debug(self, debug):
        application configuration may already be calculated based on the
        previous debug value. This method will recalculate affected values.
        Called by the :func:`flask.cli.run` command or :meth:`Flask.run`
        method if the debug flag is set explicitly in the call.
        :param debug: the new value of the debug flag
        .. versionadded:: 1.0
            Reconfigures ``app.jinja_env.auto_reload``.
        self.debug = debug
        self.jinja_env.auto_reload = self.templates_auto_reload
        if debug is not None:
            self._reconfigure_for_run_debug(bool(debug))
        from werkzeug.serving import run_simple
            rv._reconfigure_for_run_debug(debug)
    def register_blueprint(self, blueprint, **options):
        :param blueprint: The blueprint to register.
    def register_blueprint(
        self, blueprint, **options
    ):
        arguments passed to this method will override the defaults set on the
        blueprint.
        Calls the blueprint's :meth:`~flask.Blueprint.register` method after
        recording the blueprint in the application's :attr:`blueprints`.
        :param url_prefix: Blueprint routes will be prefixed with this.
        :param subdomain: Blueprint routes will match on this subdomain.
        :param url_defaults: Blueprint routes will use these default values for
            view arguments.
        :param options: Additional keyword arguments are passed to
            :class:`~flask.blueprints.BlueprintSetupState`. They can be
            accessed in :meth:`~flask.Blueprint.record` callbacks.
            assert self.blueprints[blueprint.name] is blueprint, (
                'A name collision occurred between blueprints %r and %r. Both'
                ' share the same name "%s". Blueprints that are created on the'
                ' fly need unique names.' % (
                    blueprint, self.blueprints[blueprint.name], blueprint.name
                )
            )
        and callbacks registered on the blueprint with the application. Creates
        a :class:`.BlueprintSetupState` and calls each :meth:`record` callback
        with it.
        :param app: The application this blueprint is being registered with.
        :param options: Keyword arguments forwarded from
            :meth:`~Flask.register_blueprint`.
        :param first_registration: Whether this is the first time this
            blueprint has been registered on the application.
            state.add_url_rule(
                self.static_url_path + '/<path:filename>',
                view_func=self.send_static_file, endpoint='static'
            )
    # TODO remove the next three attrs when Sphinx :inherited-members: works
    # https://github.com/sphinx-doc/sphinx/issues/741
    #: The name of the package or module that this app belongs to. Do not
    #: change this once it is set by the constructor.
    import_name = None
    #: Location of the template files to be added to the template lookup.
    #: ``None`` if templates should not be added.
    template_folder = None
    #: Absolute path to the package on the filesystem. Used to look up
    #: resources contained in the package.
    root_path = None
    # TODO remove the next three attrs when Sphinx :inherited-members: works
    # https://github.com/sphinx-doc/sphinx/issues/741
    #: The name of the package or module that this app belongs to. Do not
    #: change this once it is set by the constructor.
    import_name = None
    #: Location of the template files to be added to the template lookup.
    #: ``None`` if templates should not be added.
    template_folder = None
    #: Absolute path to the package on the filesystem. Used to look up
    #: resources contained in the package.
    root_path = None
    #: The name of the package or module that this app belongs to. Do not
    #: change this once it is set by the constructor.
    import_name = None
    #: Location of the template files to be added to the template lookup.
    #: ``None`` if templates should not be added.
    template_folder = None
    #: Absolute path to the package on the filesystem. Used to look up
    #: resources contained in the package.
    root_path = None
    static_folder = property(
        _get_static_folder, _set_static_folder,
        doc='The absolute path to the configured static folder.'
    )
    static_url_path = property(
        _get_static_url_path, _set_static_url_path,
        doc='The URL prefix that the static route will be registered for.'
    )
        blueprint handler for an exception class, app handler for an exception
        class, or ``None`` if a suitable handler is not found.
        for name, c in (
            (request.blueprint, code), (None, code),
            (request.blueprint, None), (None, None)
        ):
            handler_map = self.error_handler_spec.setdefault(name, {}).get(c)
                continue
def test_errorhandler_precedence(app, client):
    class E1(Exception):
        pass
    class E2(Exception):
        pass
    class E3(E1, E2):
        pass
    @app.errorhandler(E2)
    def handle_e2(e):
        return 'E2'
    @app.errorhandler(Exception)
    def handle_exception(e):
        return 'Exception'
    @app.route('/E1')
    def raise_e1():
        raise E1
    @app.route('/E3')
    def raise_e3():
        raise E3
    rv = client.get('/E1')
    assert rv.data == b'Exception'
    rv = client.get('/E3')
    assert rv.data == b'E2'
from ._compat import iteritems, reraise
from ._compat import iteritems, reraise, PY2
        this_module = 'flask'
        if sys.version_info < (2, 7):
            this_module += '.cli'
        name = 'python -m ' + this_module
        # Python rewrites "python -m flask" to the path to the file in argv.
        # Restore the original command so that the reloader works.
        sys.argv = ['-m', this_module] + args
    app, path='/', base_url=None, subdomain=None, url_scheme=None,
        assert 'data' not in kwargs, (
            "Client cannot provide both 'json' and 'data'."
        )
        # push a context so flask.json can use app's json attributes
        with app.app_context():
            kwargs['data'] = json_dumps(kwargs.pop('json'))
from warnings import warn
from werkzeug.wrappers import Request as RequestBase, Response as ResponseBase
from flask import json
from flask.globals import current_app
    .. versionadded:: 1.0
    _cached_json = Ellipsis
        .. versionadded:: 0.11
        return (
            mt == 'application/json'
            or (mt.startswith('application/')) and mt.endswith('+json')
        )
        JSON (:mimetype:`application/json`, see :meth:`is_json`), otherwise it
        will be ``None``.
        .. deprecated:: 1.0
            Use :meth:`get_json` instead.
            "'json' is deprecated. Use 'get_json()' instead."
        ), stacklevel=2)
        return self.get_data(cache=cache)
        JSON (:mimetype:`application/json`, see :meth:`is_json`), this returns
        ``None`` unless ``force`` is true. If parsing fails,
        :meth:`on_json_loading_failed` is called and its return value is used
        as the return value.
        :param force: Ignore the mimetype and always try to parse JSON.
        :param silent: Silence parsing errors and return ``None`` instead.
        :param cache: Store the parsed JSON to return for subsequent calls.
        if cache and self._cached_json is not Ellipsis:
            return self._cached_json
        # We accept MIME charset against the specification as certain clients
        # have used this in the past. For responses, we assume that if the
        # charset is set then the data has been encoded correctly as well.
            data = self._get_data_for_json(cache=cache)
            rv = json.loads(data, encoding=charset)
        this method returns a value, it is used as the return value for
        :meth:`get_json`. The default implementation raises a
        :class:`BadRequest` exception.
           Raise a :exc:`BadRequest` error instead of returning an error
           message as JSON. If you want that behavior you can add it by
           subclassing.
        if current_app is not None and current_app.debug:
        if current_app:
            return current_app.config['MAX_CONTENT_LENGTH']
        if (
            current_app
            and current_app.debug
            and self.mimetype != 'multipart/form-data'
            and not self.files
        ):
    .. versionchanged:: 1.0
        JSON support is added to the response, like the request. This is useful
        when testing to get the test client response data as JSON.
    def _get_data_for_json(self, cache):
        return self.get_data()
        return jsonify(flask.request.get_json())
        # Open the session at the moment that the request context is available.
        # This allows a custom open_session method to use the request context.
        # Only open a new session if this is the first time the request was
        # pushed, otherwise stream_with_context loses the session.
            session_interface = self.app.session_interface
            self.session = session_interface.open_session(
                self.app, self.request
            )
            if self.session is None:
                self.session = session_interface.make_null_session(self.app)
    def test_stream_keeps_session(self, app, client):
        @app.route('/')
        def index():
            flask.session['test'] = 'flask'
            @flask.stream_with_context
            def gen():
                yield flask.session['test']
            return flask.Response(gen())
        rv = client.get('/')
        assert rv.data == b'flask'
        (see :meth:`is_json`), this will contain the parsed JSON data.
        Otherwise this will be ``None``.
        this function will return ``None`` if the request does not use a JSON
        mimetype like :mimetype:`application/json`. See :meth:`is_json`. This
        can be overridden by the ``force`` parameter. If parsing fails,
        the :meth:`on_json_loading_failed` method on the request object will be
        invoked.
            and return ``None``.
            on the request.
        flask.session['t'] = (1, 2, 3)
        flask.session['b'] = b'\xff'
        flask.session['m'] = flask.Markup('<html>')
        flask.session['u'] = the_uuid
        flask.session['d'] = now
        flask.session['t_tag'] = {' t': 'not-a-tuple'}
        flask.session['di_t_tag'] = {' t__': 'not-a-tuple'}
        flask.session['di_tag'] = {' di': 'not-a-dict'}
        return '', 204
    with client:
        client.get('/')
        s = flask.session
        assert s['t'] == (1, 2, 3)
        assert type(s['b']) == bytes
        assert s['b'] == b'\xff'
        assert type(s['m']) == flask.Markup
        assert s['m'] == flask.Markup('<html>')
        assert s['u'] == the_uuid
        assert s['d'] == now
        assert s['t_tag'] == {' t': 'not-a-tuple'}
        assert s['di_t_tag'] == {' t__': 'not-a-tuple'}
        assert s['di_tag'] == {' di': 'not-a-dict'}
from datetime import datetime
from uuid import uuid4
import pytest
from flask import Markup
from flask.json.tag import TaggedJSONSerializer, JSONTag
@pytest.mark.parametrize("data", (
    {' t': (1, 2, 3)},
    {' t__': b'a'},
    {' di': ' di'},
    {'x': (1, 2, 3), 'y': 4},
    (1, 2, 3),
    [(1, 2, 3)],
    b'\xff',
    Markup('<html>'),
    uuid4(),
    datetime.utcnow().replace(microsecond=0),
))
def test_dump_load_unchanged(data):
    s = TaggedJSONSerializer()
    assert s.loads(s.dumps(data)) == data
def test_duplicate_tag():
    class TagDict(JSONTag):
        key = ' d'
    s = TaggedJSONSerializer()
    pytest.raises(KeyError, s.register, TagDict)
    s.register(TagDict, force=True, index=0)
    assert isinstance(s.tags[' d'], TagDict)
    assert isinstance(s.order[0], TagDict)
def test_custom_tag():
    class Foo(object):
        def __init__(self, data):
            self.data = data
    class TagFoo(JSONTag):
        __slots__ = ()
        key = ' f'
        def check(self, value):
            return isinstance(value, Foo)
        def to_json(self, value):
            return self.serializer.tag(value.data)
        def to_python(self, value):
            return Foo(value)
    s = TaggedJSONSerializer()
    s.register(TagFoo)
    assert s.loads(s.dumps(Foo('bar'))).data == 'bar'
def test_tag_interface():
    t = JSONTag(None)
    pytest.raises(NotImplementedError, t.check, None)
    pytest.raises(NotImplementedError, t.to_json, None)
    pytest.raises(NotImplementedError, t.to_python, None)
Tagged JSON
~~~~~~~~~~~
A compact representation for lossless serialization of non-standard JSON types.
:class:`~flask.sessions.SecureCookieSessionInterface` uses this to serialize
the session data, but it may be useful in other places. It can be extended to
support other types.
.. autoclass:: TaggedJSONSerializer
    :members:
.. autoclass:: JSONTag
    :members:
Let's seen an example that adds support for :class:`~collections.OrderedDict`.
Dicts don't have an order in Python or JSON, so to handle this we will dump
the items as a list of ``[key, value]`` pairs. Subclass :class:`JSONTag` and
give it the new key ``' od'`` to identify the type. The session serializer
processes dicts first, so insert the new tag at the front of the order since
``OrderedDict`` must be processed before ``dict``. ::
    from flask.json.tag import JSONTag
    class TagOrderedDict(JSONTag):
        __slots__ = ('serializer',)
        key = ' od'
        def check(self, value):
            return isinstance(value, OrderedDict)
        def to_json(self, value):
            return [[k, self.serializer.tag(v)] for k, v in iteritems(value)]
        def to_python(self, value):
            return OrderedDict(value)
    app.session_interface.serializer.register(TagOrderedDict, 0)
    __slots__ = ()
    __slots__ = ()
    __slots__ = ()
    __slots__ = ()
    __slots__ = ()
    __slots__ = ()
    __slots__ = ()
    __slots__ = ()
    #: The tag to mark the serialized object with. If ``None``, this tag is
    #: only used as an intermediate step during tagging.
    deserializes to an instance of :class:`~flask.Markup`."""
    :class:`itsdangerous.Serializer`.
    The following extra types are supported:
    * :class:`dict`
    * :class:`tuple`
    * :class:`bytes`
    * :class:`~flask.Markup`
    * :class:`~uuid.UUID`
    * :class:`~datetime.datetime`
    #: Tag classes to bind when creating the serializer. Other tags can be
    #: added later using :meth:`~register`.
    __slots__ = ('serializer',)
    only used as an intermediate step during tagging."""
    def __init__(self, serializer):
        self.serializer = serializer
    def check(self, value):
    def to_json(self, value):
        The tag will be added later."""
    def to_python(self, value):
        will already be removed."""
    def tag(self, value):
        around it."""
        return {self.key: self.to_json(value)}
    Internally, the dict key is suffixed with `__`, and the suffix is removed
    when deserializing.
    __slots__ = ('serializer',)
    key = ' di'
    def check(self, value):
        return (
            isinstance(value, dict)
            and len(value) == 1
            and next(iter(value)) in self.serializer.tags
        )
    def to_json(self, value):
        key = next(iter(value))
        return {key + '__': self.serializer.tag(value[key])}
    def to_python(self, value):
class PassDict(JSONTag):
    __slots__ = ('serializer',)
    def check(self, value):
        return isinstance(value, dict)
    def to_json(self, value):
        # JSON objects may only have string keys, so don't bother tagging the
        # key here.
        return dict((k, self.serializer.tag(v)) for k, v in iteritems(value))
    tag = to_json
    __slots__ = ('serializer',)
    def check(self, value):
    def to_json(self, value):
        return [self.serializer.tag(item) for item in value]
    def to_python(self, value):
    __slots__ = ('serializer',)
    def check(self, value):
    def to_json(self, value):
        return [self.serializer.tag(item) for item in value]
    __slots__ = ('serializer',)
    def check(self, value):
    def to_json(self, value):
    def to_python(self, value):
    having a ``__html__`` method to the result of that method. Always
    deserializes to an instance of :class:`~markupsafe.Markup`."""
    __slots__ = ('serializer',)
    def check(self, value):
    def to_json(self, value):
    def to_python(self, value):
    __slots__ = ('serializer',)
    def check(self, value):
    def to_json(self, value):
    def to_python(self, value):
    __slots__ = ('serializer',)
    def check(self, value):
    def to_json(self, value):
    def to_python(self, value):
    are not JSON types. Passed as the intermediate serializer to
    :class:`itsdangerous.Serializer`."""
    __slots__ = ('tags', 'order')
    default_tags = [
        TagDict, PassDict, TagTuple, PassList, TagBytes, TagMarkup, TagUUID,
        TagDateTime,
    added later using :meth:`~register`."""
        self.tags = {}
        self.order = []
        for cls in self.default_tags:
            self.register(cls)
    def register(self, tag_class, force=False, index=-1):
        :param tag_class: tag class to register. Will be instantiated with this
            serializer instance.
        :param force: overwrite an existing tag. If false (default), a
            :exc:`KeyError` is raised.
        :param index: index to insert the new tag in the tag order. Useful when
            the new tag is a special case of an existing tag. If -1 (default),
            the tag is appended to the end of the order.
        :raise KeyError: if the tag key is already registered and ``force`` is
            not true.
        tag = tag_class(self)
            if not force and key in self.tags:
            self.tags[key] = tag
            self.order.append(tag)
            self.order.insert(index, tag)
    def tag(self, value):
        for tag in self.order:
            if tag.check(value):
                return tag.tag(value)
    def untag(self, value):
        if key not in self.tags:
        return self.tags[key].to_python(value[key])
        return dumps(self.tag(value), separators=(',', ':'))
        return loads(value, object_hook=self.untag)
from flask.globals import current_app, request
from flask._compat import text_type, PY2
from base64 import b64decode, b64encode
from datetime import datetime
from uuid import UUID
from jinja2 import Markup
from werkzeug.http import http_date, parse_date
from flask._compat import iteritems, text_type
from flask.json import dumps, loads
class JSONTag(object):
    __slots__ = ()
    key = None
    def check(self, serializer, value):
        raise NotImplementedError
    def to_json(self, serializer, value):
        raise NotImplementedError
    def to_python(self, serializer, value):
        raise NotImplementedError
    def tag(self, serializer, value):
        return {self.key: self.to_json(serializer, value)}
class TagDict(JSONTag):
    __slots__ = ()
    key = ' di'
    def check(self, serializer, value):
        return isinstance(value, dict)
    def to_json(self, serializer, value, key=None):
        if key is not None:
            return {key + '__': serializer._tag(value[key])}
        return dict((k, serializer._tag(v)) for k, v in iteritems(value))
    def to_python(self, serializer, value):
        key = next(iter(value))
        return {key[:-2]: value[key]}
    def tag(self, serializer, value):
        if len(value) == 1:
            key = next(iter(value))
            if key in serializer._tags:
                return {self.key: self.to_json(serializer, value, key=key)}
        return self.to_json(serializer, value)
class TagTuple(JSONTag):
    __slots__ = ()
    key = ' t'
    def check(self, serializer, value):
        return isinstance(value, tuple)
    def to_json(self, serializer, value):
        return [serializer._tag(item) for item in value]
    def to_python(self, serializer, value):
        return tuple(value)
class PassList(JSONTag):
    __slots__ = ()
    def check(self, serializer, value):
        return isinstance(value, list)
    def to_json(self, serializer, value):
        return [serializer._tag(item) for item in value]
    tag = to_json
class TagBytes(JSONTag):
    __slots__ = ()
    key = ' b'
    def check(self, serializer, value):
        return isinstance(value, bytes)
    def to_json(self, serializer, value):
        return b64encode(value).decode('ascii')
    def to_python(self, serializer, value):
        return b64decode(value)
class TagMarkup(JSONTag):
    __slots__ = ()
    key = ' m'
    def check(self, serializer, value):
        return callable(getattr(value, '__html__', None))
    def to_json(self, serializer, value):
        return text_type(value.__html__())
    def to_python(self, serializer, value):
        return Markup(value)
class TagUUID(JSONTag):
    __slots__ = ()
    key = ' u'
    def check(self, serializer, value):
        return isinstance(value, UUID)
    def to_json(self, serializer, value):
        return value.hex
    def to_python(self, serializer, value):
        return UUID(value)
class TagDateTime(JSONTag):
    __slots__ = ()
    key = ' d'
    def check(self, serializer, value):
        return isinstance(value, datetime)
    def to_json(self, serializer, value):
        return http_date(value)
    def to_python(self, serializer, value):
        return parse_date(value)
class TaggedJSONSerializer(object):
    __slots__ = ('_tags', '_order')
    _default_tags = [
        TagDict(), TagTuple(), PassList(), TagBytes(), TagMarkup(), TagUUID(),
        TagDateTime(),
    ]
    def __init__(self):
        self._tags = {}
        self._order = []
        for tag in self._default_tags:
            self.register(tag)
    def register(self, tag, force=False, index=-1):
        key = tag.key
        if key is not None:
            if not force and key in self._tags:
                raise KeyError("Tag '{0}' is already registered.".format(key))
            self._tags[key] = tag
        if index == -1:
            self._order.append(tag)
        else:
            self._order.insert(index, tag)
    def _tag(self, value):
        for tag in self._order:
            if tag.check(self, value):
                return tag.tag(self, value)
        return value
    def _untag(self, value):
        if len(value) != 1:
            return value
        key = next(iter(value))
        if key not in self._tags:
            return value
        return self._tags[key].to_python(self, value[key])
    def dumps(self, value):
        return dumps(self._tag(value), separators=(',', ':'))
    def loads(self, value):
        return loads(value, object_hook=self._untag)
from flask.helpers import is_ip, total_seconds
from flask.json.tag import TaggedJSONSerializer
session_json_serializer = TaggedJSONSerializer()
        A decorator that is used to register a function given an
    @setupmethod
                'Tried to register a handler for an exception instance {0!r}.'
                ' Handlers can only be registered for exception classes or'
                ' HTTP error codes.'.format(code_or_exception)
            )
        try:
            exc_class, code = self._get_exc_class_and_code(code_or_exception)
        except KeyError:
            raise KeyError(
                "'{0}' is not a recognized HTTP error code. Use a subclass of"
                " HTTPException with that code instead.".format(code_or_exception)
            )
def test_error_handler_unknown_code(app):
    with pytest.raises(KeyError) as exc_info:
        app.register_error_handler(999, lambda e: ('999', 999))
    assert 'Use a subclass' in exc_info.value.args[0]
            (self.debug or self.config['TRAP_BAD_REQUEST_ERRORS'])
        # description for key errors in debug mode or when trapping errors.
            self.debug or self.config['TRAP_BAD_REQUEST_ERRORS']
    rv = client.get('/fail')
    assert rv.status_code == 400
    assert b'missing_key' not in rv.data
    assert 'missing_key' in e.value.description
    InternalServerError, MethodNotAllowed, default_exceptions, \
    BadRequestKeyError
        'TRAP_BAD_REQUEST_ERRORS':              None,
        .. versionchanged:: 1.0
            Bad request errors are not trapped by default in debug mode.
        trap_bad_request = self.config['TRAP_BAD_REQUEST_ERRORS']
        # if unset, trap based on debug mode
        if (trap_bad_request is None and self.debug) or trap_bad_request:
        .. versionchanged:: 1.0
            Key errors raised from request data like ``form`` show the the bad
            key in debug mode rather than a generic bad request message.
        # MultiDict passes the key to the exception, but that's ignored
        # when generating the response message. Set an informative
        # description for key errors in debug mode.
        if (
            self.debug
            and isinstance(e, BadRequestKeyError)
            # only set it if it's still the default description
            and e.description is BadRequestKeyError.description
        ):
            e.description = "KeyError: '{0}'".format(*e.args)
        app.config['TRAP_BAD_REQUEST_ERRORS'] = False
        app.config['TRAP_BAD_REQUEST_ERRORS'] = False
import warnings
        .. deprecated: 1.0
            Will be removed in 1.1. Use ``session_interface.open_session``
            instead.
        warnings.warn(DeprecationWarning(
            '"open_session" is deprecated and will be removed in 1.1. Use'
            ' "session_interface.open_session" instead.'
        ))
        .. deprecated: 1.0
            Will be removed in 1.1. Use ``session_interface.save_session``
            instead.
        warnings.warn(DeprecationWarning(
            '"save_session" is deprecated and will be removed in 1.1. Use'
            ' "session_interface.save_session" instead.'
        ))
        .. deprecated: 1.0
            Will be removed in 1.1. Use ``session_interface.make_null_session``
            instead.
        warnings.warn(DeprecationWarning(
            '"make_null_session" is deprecated and will be removed in 1.1. Use'
            ' "session_interface.make_null_session" instead.'
        ))
            self.session_interface.save_session(self, ctx.session, response)
        session_interface = self.app.session_interface
        self.session = session_interface.open_session(self.app, self.request)
            self.session = session_interface.make_null_session(self.app)
            session_interface = app.session_interface
            sess = session_interface.open_session(app, c.request)
            if not session_interface.is_null_session(sess):
                session_interface.save_session(app, sess, resp)
            response.vary.add('Cookie')
import pickle
import uuid
import pytest
import werkzeug.serving
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
import flask
from flask._compat import text_type
        response.vary.add('Cookie')
        response.vary.update(('Accept-Encoding', 'Accept-Language'))
        'APPLICATION_ROOT':                     '/',
                script_name=self.config['APPLICATION_ROOT'],
        return app.config['SESSION_COOKIE_PATH'] \
               or app.config['APPLICATION_ROOT']
        app_root = app.config['APPLICATION_ROOT']
            url_scheme = app.config['PREFERRED_URL_SCHEME']
        'Programming Language :: Python :: 3.6',
    extras_require={
        'dev': [
            'blinker',
            'greenlet',
            'pytest>=3',
            'coverage',
            'tox',
            'sphinx',
            'sphinxcontrib-log-cabinet'
        ],
    },
    app = Flask('flaskr')
app = Flask('minitwit')
app = Flask('yourapplication')
import yourapplication.views
    app = Flask(__name__.split('.')[0])
            g.sqlite_db.close()
def patch_vary_header(response, value):
    header = response.headers.get('Vary', '')
    headers = [h for h in (h.strip() for h in header.split(',')) if h]
    lower_value = value.lower()
    if not any(h.lower() == lower_value for h in headers):
        headers.append(value)
    updated_header = ', '.join(headers)
    response.headers['Vary'] = updated_header
import uuid
from base64 import b64decode, b64encode
from itsdangerous import BadSignature, URLSafeTimedSerializer
from werkzeug.http import http_date, parse_date
from flask.helpers import patch_vary_header
from .helpers import is_ip, total_seconds
            patch_vary_header(response, 'Cookie')
        'Werkzeug>=0.9',
                app = call_factory(app_factory, script_info)
def call_factory(func, script_info):
    ``script_info`` or just a single argument and calls the function passing 
    ``script_info`` if so. Otherwise, calls the function without any arguments
    and returns the result.
        return func(script_info=script_info)
        return func(script_info)
    return func()
            rv = call_factory(self.create_app, self)
    for attr_name in ('app', 'application'):
    for attr_name in ('create_app', 'make_app'):
    matches = [
        v for k, v in iteritems(module.__dict__) if isinstance(v, Flask)
    ]
    elif len(matches) > 1:
        raise NoAppException(
            'Auto-detected multiple Flask applications in module "{module}".'
            ' Use "FLASK_APP={module}:name" to specify the correct'
            ' one.'.format(module=module.__name__)
        )
                    'could not call it without specifying arguments.'.format(
                        callable=attr_name, module=module.__name__
                    )
                )
        'Failed to find application in module "{module}". Are you sure '
        'it contains a Flask application? Maybe you wrapped it in a WSGI '
        'middleware.'.format(module=module.__name__)
    )
    def setdefault(self, key, default=None):
        self.accessed = True
        return super(SecureCookieSession, self).setdefault(key, default)
    @app.route('/set')
    @app.route('/get')
    def get():
        return flask.session.get('test')
    @app.route('/getitem')
    def getitem():
        return flask.session['test']
    @app.route('/setdefault')
    def setdefault():
        return flask.session.setdefault('test', 'default')
    def expect(path, header=True):
        rv = c.get(path)
        if header:
            assert rv.headers['Vary'] == 'Cookie'
        else:
            assert 'Vary' not in rv.headers
    expect('/set')
    expect('/get')
    expect('/getitem')
    expect('/setdefault')
    expect('/no-vary-header', False)
        super(SecureCookieSession, self).__init__(initial, on_update)
        should be set for this session cookie for this response. If the session
        has been modified, the cookie is set. If the session is permanent and
        the ``SESSION_REFRESH_EACH_REQUEST`` config is true, the cookie is
        always set.
        This check is usually skipped if the session was deleted.
        return session.modified or (
            session.permanent and app.config['SESSION_REFRESH_EACH_REQUEST']
        )
        # If the session is modified to be empty, remove the cookie.
        # If the session is empty, return without setting the cookie.
        if not session:
            if session.modified:
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain,
                    path=path
                )
            return
        # Add a "Vary: Cookie" header if the session was accessed at all.
        if session.accessed:
        if not self.should_set_cookie(app, session):
            return
        response.set_cookie(
            app.session_cookie_name,
            val,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure
        )
    parts = [directory]
        if (
            any(sep in filename for sep in _os_alt_seps)
            or os.path.isabs(filename)
            or filename == '..'
            or filename.startswith('../')
        ):
        parts.append(filename)
    return posixpath.join(*parts)
            (('a/b/c',), 'a/b/c'),
            (('/', 'a/', 'b/', 'c/'), '/a/b/c'),
            (('a', 'b', 'c'), 'a/b/c'),
            (('/a', 'b/c'), '/a/b/c'),
            (('a/b', 'X/../c'), 'a/b/c'),
            (('/a/b', 'c/X/..'), '/a/b/c'),
            (('/a/b/c', ''), '/a/b/c/'),
            (('/a/b/c', './'), '/a/b/c/.'),
            (('a/b/c', 'X/..'), 'a/b/c/.'),
            ('/a', '../b/c'),
            ('/a', 'b/../b/../../c'),
            ('/a', 'b/../../c'),
    parts = [directory]
        if (
            any(sep in filename for sep in _os_alt_seps)
            or os.path.isabs(filename)
            or filename == '..'
            or filename.startswith('../')
        ):
        parts.append(filename)
    return posixpath.join(*parts)
            (('a/b/c',), 'a/b/c'),
            (('/', 'a/', 'b/', 'c/'), '/a/b/c'),
            (('a', 'b', 'c'), 'a/b/c'),
            (('/a', 'b/c'), '/a/b/c'),
            (('a/b', 'X/../c'), 'a/b/c'),
            (('/a/b', 'c/X/..'), '/a/b/c'),
            (('/a/b/c', ''), '/a/b/c/'),
            (('/a/b/c', './'), '/a/b/c/.'),
            (('a/b/c', 'X/..'), 'a/b/c/.'),
            ('/a', '../b/c'),
            ('/a', 'b/../b/../../c'),
            ('/a', 'b/../../c'),
import socket
def is_ip(value):
    :param value: value to check
    :type value: str
    :return: True if string is an IP address
    :rtype: bool
            socket.inet_pton(family, value)
import warnings
        Uses ``SESSION_COOKIE_DOMAIN`` if it is configured, otherwise
        falls back to detecting the domain based on ``SERVER_NAME``.
        Once detected (or if not set at all), ``SESSION_COOKIE_DOMAIN`` is
        updated to avoid re-running the logic.
        rv = app.config['SESSION_COOKIE_DOMAIN']
        # set explicitly, or cached from SERVER_NAME detection
        # if False, return None
        if rv is not None:
            return rv if rv else None
        rv = app.config['SERVER_NAME']
        # server name not set, cache False to return none next time
        if not rv:
            app.config['SESSION_COOKIE_DOMAIN'] = False
            return None
        # chop off the port which is usually not supported by browsers
        # remove any leading '.' since we'll add that later
        rv = rv.rsplit(':', 1)[0].lstrip('.')
        if '.' not in rv:
            # Chrome doesn't allow names without a '.'
            # this should only come up with localhost
            # hack around this by not setting the name, and show a warning
            warnings.warn(
                '"{rv}" is not a valid cookie domain, it must contain a ".".'
                ' Add an entry to your hosts file, for example'
                ' "{rv}.localdomain", and use that instead.'.format(rv=rv)
            )
            app.config['SESSION_COOKIE_DOMAIN'] = False
            return None
        ip = is_ip(rv)
        if ip:
            warnings.warn(
                'The session cookie domain is an IP address. This may not work'
                ' as intended in some browsers. Add an entry to your hosts'
                ' file, for example "localhost.localdomain", and use that'
                ' instead.'
            )
        # if this is not an ip and app is mounted at the root, allow subdomain
        # matching by adding a '.' prefix
        if self.get_cookie_path(app) == '/' and not ip:
            rv = '.' + rv
        app.config['SESSION_COOKIE_DOMAIN'] = rv
        return rv
def test_session_localhost_warning(recwarn):
    app = flask.Flask(__name__)
    app.config.update(
        SECRET_KEY='testing',
        SERVER_NAME='localhost:5000',
    )
    @app.route('/')
    def index():
        flask.session['testing'] = 42
        return 'testing'
    rv = app.test_client().get('/', 'http://localhost:5000/')
    assert 'domain' not in rv.headers['set-cookie'].lower()
    w = recwarn.pop(UserWarning)
    assert '"localhost" is not a valid cookie domain' in str(w.message)
def test_session_ip_warning(recwarn):
    app = flask.Flask(__name__)
    app.config.update(
        SECRET_KEY='testing',
        SERVER_NAME='127.0.0.1:5000',
    )
    @app.route('/')
    def index():
        flask.session['testing'] = 42
        return 'testing'
    rv = app.test_client().get('/', 'http://127.0.0.1:5000/')
    assert 'domain=127.0.0.1' in rv.headers['set-cookie'].lower()
    w = recwarn.pop(UserWarning)
    assert 'cookie domain is an IP' in str(w.message)
try:
    __import__('sphinxcontrib.log_cabinet')
except ImportError:
    print('sphinxcontrib-log-cabinet is not installed.')
    print('Changelog directives will not be re-organized.')
else:
    extensions.append('sphinxcontrib.log_cabinet')
from operator import attrgetter
from threading import Lock, Thread
from . import __version__
from .globals import current_app
@click.command('routes', short_help='Show the routes for the app.')
@click.option(
    '--sort', '-s',
    type=click.Choice(('endpoint', 'methods', 'rule', 'match')),
    default='endpoint',
    help=(
        'Method to sort routes by. "match" is the order that Flask will match '
        'routes when dispatching a request.'
    )
)
@click.option(
    '--all-methods',
    is_flag=True,
    help="Show HEAD and OPTIONS methods."
)
def routes_command(sort, all_methods):
    rules = list(current_app.url_map.iter_rules())
    ignored_methods = set(() if all_methods else ('HEAD', 'OPTIONS'))
    if sort in ('endpoint', 'rule'):
        rules = sorted(rules, key=attrgetter(sort))
    elif sort == 'methods':
        rules = sorted(rules, key=lambda rule: sorted(rule.methods))
    rule_methods = [
        ', '.join(sorted(rule.methods - ignored_methods)) for rule in rules
    ]
    headers = ('Endpoint', 'Methods', 'Rule')
    widths = (
        max(len(rule.endpoint) for rule in rules),
        max(len(methods) for methods in rule_methods),
        max(len(rule.rule) for rule in rules),
    )
    widths = [max(len(h), w) for h, w in zip(headers, widths)]
    row = '{{0:<{0}}}  {{1:<{1}}}  {{2:<{2}}}'.format(*widths)
    click.echo(row.format(*headers).strip())
    click.echo(row.format(*('-' * width for width in widths)))
    for rule, methods in zip(rules, rule_methods):
        click.echo(row.format(rule.endpoint, methods, rule.rule).rstrip())
from functools import partial
def test_print_exceptions(runner):
    @pytest.fixture
    def invoke(self, runner):
        def create_app(info):
            app = Flask(__name__)
            app.testing = True
            @app.route('/get_post/<int:x>/<int:y>', methods=['GET', 'POST'])
            def yyy_get_post(x, y):
                pass
            @app.route('/zzz_post', methods=['POST'])
            def aaa_post():
                pass
            return app
        cli = FlaskGroup(create_app=create_app)
        return partial(runner.invoke, cli)
    def expect_order(self, order, output):
        # skip the header and match the start of each row
        for expect, line in zip(order, output.splitlines()[2:]):
            # do this instead of startswith for nicer pytest output
            assert line[:len(expect)] == expect
    def test_simple(self, invoke):
        result = invoke(['routes'])
        self.expect_order(
            ['aaa_post', 'static', 'yyy_get_post'],
            result.output
        )
    def test_sort(self, invoke):
        default_output = invoke(['routes']).output
        endpoint_output = invoke(['routes', '-s', 'endpoint']).output
        assert default_output == endpoint_output
        self.expect_order(
            ['static', 'yyy_get_post', 'aaa_post'],
            invoke(['routes', '-s', 'methods']).output
        )
        self.expect_order(
            ['yyy_get_post', 'static', 'aaa_post'],
            invoke(['routes', '-s', 'rule']).output
        )
        self.expect_order(
            ['aaa_post', 'yyy_get_post', 'static'],
            invoke(['routes', '-s', 'match']).output
        )
    def test_all_methods(self, invoke):
        output = invoke(['routes']).output
        assert 'GET, HEAD, OPTIONS, POST' not in output
        output = invoke(['routes', '--all-methods']).output
        assert 'GET, HEAD, OPTIONS, POST' in output
        #: A dictionary with lists of functions that will be called at the
        #: beginning of each request. The key of the dictionary is the name of
        #: the blueprint this function is active for, or ``None`` for all
        #: requests. To register a function, use the :meth:`before_request`
        #: decorator.
        #: A list of functions that will be called at the beginning of the
        #: first request to this instance. To register a function, use the
        #: :meth:`before_first_request` decorator.
        #: A dictionary with lists of functions that are called before the
        #: :attr:`before_request_funcs` functions. The key of the dictionary is
        #: the name of the blueprint this function is active for, or ``None``
        #: for all requests. To register a function, use
        #: :meth:`url_value_preprocessor`.
        For example, this can be used to open a database connection, or to load
        the logged in user from the session.
        The function will be called without any arguments. If it returns a
        non-None value, the value is handled as if it was the return value from
        the view, and further request handling is stopped.
        functions in the application. These functions will be called before the
        :meth:`before_request` functions.
        The function can modify the values captured from the matched url before
        they are passed to the view. For example, this can be used to pop a
        common language code value and place it in ``g`` rather than pass it to
        every view.
        The function is passed the endpoint name and values dict. The return
        value is ignored.
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.
        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
from itertools import chain
from threading import Lock
from werkzeug.datastructures import ImmutableDict, Headers
from werkzeug.exceptions import BadRequest, HTTPException, \
    InternalServerError, MethodNotAllowed, default_exceptions
from werkzeug.routing import BuildError, Map, RequestRedirect, Rule
from . import cli, json
from ._compat import integer_types, reraise, string_types, text_type
from .config import Config, ConfigAttribute
from .ctx import AppContext, RequestContext, _AppCtxGlobals
from .globals import _request_ctx_stack, g, request, session
from .helpers import _PackageBoundObject, \
    _endpoint_from_view_func, find_package, get_debug_flag, \
    get_flashed_messages, locked_cached_property, url_for
from .signals import appcontext_tearing_down, got_request_exception, \
    request_finished, request_started, request_tearing_down
    _default_template_ctx_processor
from .wrappers import Request, Response
        :attr:`response_class`.
        :param rv: the return value from the view function. The view function
            must return a response. Returning ``None``, or the view ending
            without returning, is not allowed. The following types are allowed
            for ``view_rv``:
            ``str`` (``unicode`` in Python 2)
                A response object is created with the string encoded to UTF-8
                as the body.
            ``bytes`` (``str`` in Python 2)
                A response object is created with the bytes as the body.
            ``tuple``
                Either ``(body, status, headers)``, ``(body, status)``, or
                ``(body, headers)``, where ``body`` is any of the other types
                allowed here, ``status`` is a string or an integer, and
                ``headers`` is a dictionary or a list of ``(key, value)``
                tuples. If ``body`` is a :attr:`response_class` instance,
                ``status`` overwrites the exiting value and ``headers`` are
                extended.
            :attr:`response_class`
                The object is returned unchanged.
            other :class:`~werkzeug.wrappers.Response` class
                The object is coerced to :attr:`response_class`.
            :func:`callable`
                The function is called as a WSGI application. The result is
                used to create a response object.
        status = headers = None
        # unpack tuple returns
        if isinstance(rv, (tuple, list)):
            len_rv = len(rv)
            # a 3-tuple is unpacked directly
            if len_rv == 3:
                rv, status, headers = rv
            # decide if a 2-tuple has status or headers
            elif len_rv == 2:
                if isinstance(rv[1], (Headers, dict, tuple, list)):
                    rv, headers = rv
                else:
                    rv, status = rv
            # other sized tuples are not allowed
            else:
                raise TypeError(
                    'The view function did not return a valid response tuple.'
                    ' The tuple must have the form (body, status, headers),'
                    ' (body, status), or (body, headers).'
                )
        # the body must not be None
        if rv is None:
            raise TypeError(
                'The view function did not return a valid response. The'
                ' function either returned None or ended without a return'
                ' statement.'
            )
        # make sure the body is an instance of the response class
                # let the response class set the status and headers instead of
                # waiting to do it manually, so that the class can handle any
                # special logic
                rv = self.response_class(rv, status=status, headers=headers)
                status = headers = None
                # evaluate a WSGI callable, or coerce a different response
                # class to the correct type
                try:
                    rv = self.response_class.force_type(rv, request.environ)
                except TypeError as e:
                    new_error = TypeError(
                        '{e}\nThe view function did not return a valid'
                        ' response. The return type must be a string, tuple,'
                        ' Response instance, or WSGI callable, but it was a'
                        ' {rv.__class__.__name__}.'.format(e=e, rv=rv)
                    )
                    reraise(TypeError, new_error, sys.exc_info()[2])
        # prefer the status if it was provided
        if status is not None:
            if isinstance(status, (text_type, bytes, bytearray)):
                rv.status = status
                rv.status_code = status
        # extend existing headers with provided headers
def test_response_types():
    app.testing = True
    @app.route('/text')
    def from_text():
    @app.route('/bytes')
    def from_bytes():
    @app.route('/full_tuple')
    def from_full_tuple():
    @app.route('/text_headers')
    def from_text_headers():
    @app.route('/text_status')
    def from_text_status():
    @app.route('/response_headers')
    def from_response_headers():
        return flask.Response('Hello world', 404, {'X-Foo': 'Baz'}), {
    @app.route('/response_status')
    def from_response_status():
        return app.response_class('Hello world', 400), 500
    @app.route('/wsgi')
    def from_wsgi():
        return NotFound()
    assert c.get('/text').data == u'Hällo Wörld'.encode('utf-8')
    assert c.get('/bytes').data == u'Hällo Wörld'.encode('utf-8')
    rv = c.get('/full_tuple')
    rv = c.get('/text_headers')
    assert rv.data == b'Hello'
    assert rv.headers['X-Foo'] == 'Test'
    assert rv.status_code == 200
    assert rv.mimetype == 'text/plain'
    rv = c.get('/text_status')
    assert rv.data == b'Hi, status!'
    assert rv.status_code == 400
    assert rv.mimetype == 'text/html'
    rv = c.get('/response_headers')
    assert rv.data == b'Hello world'
    assert rv.headers.getlist('X-Foo') == ['Baz', 'Bar']
    assert rv.headers['X-Bar'] == 'Foo'
    assert rv.status_code == 404
    rv = c.get('/response_status')
    assert rv.data == b'Hello world'
    assert rv.status_code == 500
    rv = c.get('/wsgi')
    assert b'Not Found' in rv.data
    assert rv.status_code == 404
def test_response_type_errors():
    app = flask.Flask(__name__)
    app.testing = True
    @app.route('/none')
    def from_none():
        pass
    @app.route('/small_tuple')
    def from_small_tuple():
        return 'Hello',
    @app.route('/large_tuple')
    def from_large_tuple():
        return 'Hello', 234, {'X-Foo': 'Bar'}, '???'
    @app.route('/bad_type')
    def from_bad_type():
        return True
    @app.route('/bad_wsgi')
    def from_bad_wsgi():
        return lambda: None
    c = app.test_client()
    with pytest.raises(TypeError) as e:
        c.get('/none')
        assert 'returned None' in str(e)
    with pytest.raises(TypeError) as e:
        c.get('/small_tuple')
        assert 'tuple must have the form' in str(e)
    pytest.raises(TypeError, c.get, '/large_tuple')
    with pytest.raises(TypeError) as e:
        c.get('/bad_type')
        assert 'it was a bool' in str(e)
    pytest.raises(TypeError, c.get, '/bad_wsgi')
    #: Set to ``None`` to use the app's :class:`~flask.app.Flask.json_encoder`.
    #: Set to ``None`` to use the app's :class:`~flask.app.Flask.json_decoder`.
        bp = current_app.blueprints.get(request.blueprint) if request else None
        kwargs.setdefault(
            'cls',
            bp.json_encoder if bp and bp.json_encoder
                else current_app.json_encoder
        )
        bp = current_app.blueprints.get(request.blueprint) if request else None
        kwargs.setdefault(
            'cls',
            bp.json_decoder if bp and bp.json_decoder
                else current_app.json_decoder
        )
        bp = flask.Blueprint('bp', __name__)
        bp.json_encoder = MyEncoder
        bp.json_decoder = MyDecoder
        @bp.route('/bp', methods=['POST'])
        app.register_blueprint(bp)
                ctx.push()
from flask.sessions import SessionInterface
def test_session_error_pops_context():
    class SessionError(Exception):
        pass
    class FailingSessionInterface(SessionInterface):
        def open_session(self, app, request):
            raise SessionError()
    class CustomFlask(flask.Flask):
        session_interface = FailingSessionInterface()
    app = CustomFlask(__name__)
    @app.route('/')
    def index():
        # shouldn't get here
        assert False
    response = app.test_client().get('/')
    assert response.status_code == 500
    assert not flask.request
    assert not flask.current_app
    defines.
    def __init__(cls, name, bases, d):
        super(MethodViewType, cls).__init__(name, bases, d)
            methods = set()
            for key in http_method_funcs:
                if hasattr(cls, key):
            # If we have no method at all in there we don't want to add a
            # method list. This is for instance the case for the base class
            # or another subclass of a base method view that does not introduce
            # new methods.
                cls.methods = methods
    class methods. For example, if you implement a ``get`` method, it will be
    used to handle ``GET`` requests. ::
    def add_url_rule(self, rule, endpoint=None, view_func=None, provide_automatic_options=None, **options):
        :param provide_automatic_options: controls whether the ``OPTIONS``
            method should be added automatically. This can also be controlled
            by setting the ``view_func.provide_automatic_options = False``
            before adding the rule.
def test_provide_automatic_options_attr():
def test_provide_automatic_options_kwarg():
    app = flask.Flask(__name__)
    def index():
        return flask.request.method
    def more():
        return flask.request.method
    app.add_url_rule('/', view_func=index, provide_automatic_options=False)
    app.add_url_rule(
        '/more', view_func=more, methods=['GET', 'POST'],
        provide_automatic_options=False
    )
    c = app.test_client()
    assert c.get('/').data == b'GET'
    rv = c.post('/')
    assert rv.status_code == 405
    assert sorted(rv.allow) == ['GET', 'HEAD']
    # Older versions of Werkzeug.test.Client don't have an options method
    if hasattr(c, 'options'):
        rv = c.options('/')
    else:
        rv = c.open('/', method='OPTIONS')
    assert rv.status_code == 405
    rv = c.head('/')
    assert rv.status_code == 200
    assert not rv.data  # head truncates
    assert c.post('/more').data == b'POST'
    assert c.get('/more').data == b'GET'
    rv = c.delete('/more')
    assert rv.status_code == 405
    assert sorted(rv.allow) == ['GET', 'HEAD', 'POST']
    if hasattr(c, 'options'):
        rv = c.options('/more')
    else:
        rv = c.open('/more', method='OPTIONS')
    assert rv.status_code == 405
def test_url_for_passes_special_values_to_build_error_handler():
    app = flask.Flask(__name__)
    @app.url_build_error_handlers.append
    def handler(error, endpoint, values):
        assert values == {
            '_external': False,
            '_anchor': None,
            '_method': None,
            '_scheme': None,
        }
        return 'handled'
    with app.test_request_context():
        flask.url_for('/')
        last_modified = datetime.datetime.utcfromtimestamp(os.path.getmtime(
        last_modified = datetime.datetime.utcfromtimestamp(os.path.getmtime(
    :param filename_or_fp: the filename of the file to send.
            attachment_filename = attachment_filename.encode('latin-1')
                'filename': unicodedata.normalize(
                    'NFKD', attachment_filename).encode('latin-1', 'ignore'),
                assert 'filename*' not in rv.headers['Content-Disposition']
            rv = flask.send_file('static/index.html', as_attachment=True, attachment_filename=u'Ñandú／pingüino.txt')
            content_disposition = set(rv.headers['Content-Disposition'].split('; '))
            assert content_disposition == set((
                'attachment',
                'filename="Nandu/pinguino.txt"',
                "filename*=UTF-8''%C3%91and%C3%BA%EF%BC%8Fping%C3%BCino.txt"
            ))
import unicodedata
    .. versionchanged:: 0.13
        UTF-8 filenames, as specified in `RFC 2231`_, are supported.
    .. _RFC 2231: https://tools.ietf.org/html/rfc2231#section-4
        normalized = unicodedata.normalize(
            'NFKD', text_type(attachment_filename)
        )
            filenames = {'filename': attachment_filename}
        headers.add('Content-Disposition', 'attachment', **filenames)
                assert options['filename'] == 'index.html'
                assert 'filename*' not in options
            rv = flask.send_file(
                'static/index.html', as_attachment=True,
                attachment_filename=u'Ñandú／pingüino.txt'
            )
            value, options = parse_options_header(
                rv.headers['Content-Disposition']
            )
            rv.close()
        assert value == 'attachment'
        assert sorted(options.keys()) == ('filename', 'filename*')
        assert options['filename'] == 'Nandu/pinguino.txt'
        assert options['filename*'] == 'UTF-8''%C3%91and%C3%BA%EF%BC%8Fping%C3%BCino.txt'
@pytest.mark.parametrize('host,port,expect_host,expect_port', (
    (None, None, 'pocoo.org', 8080),
    ('localhost', None, 'localhost', 8080),
    (None, 80, 'pocoo.org', 80),
    ('localhost', 80, 'localhost', 80),
))
def test_run_from_config(monkeypatch, host, port, expect_host, expect_port):
    def run_simple_mock(hostname, port, *args, **kwargs):
        assert hostname == expect_host
        assert port == expect_port
    monkeypatch.setattr(werkzeug.serving, 'run_simple', run_simple_mock)
    app = flask.Flask(__name__)
    app.config['SERVER_NAME'] = 'pocoo.org:8080'
    app.run(host, port)
# html_theme_path = ['_themes']
    __import__('flask_sphinx_themes')
    print('Flask theme unavailable; using the default theme.')
    print('Install using `pip install Flask-Sphinx-Themes`.')
from flask._compat import StringIO, text_type
        test_data = {'name': 'Flask'}
        out = StringIO()
            flask.json.dump(test_data, out)
            out.seek(0)
            rv = flask.json.load(out)
        app.add_url_rule(url, url, lambda: flask.jsonify(x=test_uuid))
        c = app.test_client()
        rv_x = flask.json.loads(rv.data)['x']
        assert rv_x == str(test_uuid)
        rv_uuid = uuid.UUID(rv_x)
        assert rv_uuid == test_uuid
from datetime import datetime
import os
import sys
import pkg_resources
sys.path.append(os.path.join(os.path.dirname(__file__), '_themes'))
sys.path.append(os.path.dirname(__file__))
copyright = u'2010 - {0}, Armin Ronacher'.format(datetime.utcnow().year)
    release = ''.join(release.partition('dev')[:2])
# html_theme = 'default'
# html_theme_options = {}
html_favicon = '_static/flask-favicon.ico'
    'index': [
        'sidebarintro.html',
        'sourcelink.html',
        'searchbox.html'
    ],
    '**': [
        'sidebarlogo.html',
        'localtoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html'
    ]
  ('latexindex', 'Flask.tex', u'Flask Documentation', u'Armin Ronacher', 'manual'),
    'fontpkg': r'\usepackage{mathpazo}',
    'papersize': 'a4paper',
    'pointsize': '12pt',
    'preamble': r'\usepackage{flaskstyle}'
    'python': ('https://docs.python.org/3/', None),
    'werkzeug': ('http://werkzeug.pocoo.org/docs/', None),
    'click': ('http://click.pocoo.org/', None),
    'jinja': ('http://jinja.pocoo.org/docs/', None),
    'sqlalchemy': ('http://docs.sqlalchemy.org/en/latest/', None),
    'wtforms': ('https://wtforms.readthedocs.io/en/latest/', None),
    'blinker': ('https://pythonhosted.org/blinker/', None)
    pygments_style = 'flask_theme_support.FlaskyStyle'
    html_theme = 'flask'
    html_theme_options = {
        'touch_icon': 'touch-icon.png'
    }
except ImportError:
    :param add_version_option: adds the ``--version`` option.
    # Extra startup messages.  This depends a bit on Werkzeug internals to
               use_debugger=debugger, threaded=with_threads,
               passthrough_errors=True)
    :param last_modified: set the ``Last-Modified`` header to this value,
        a :class:`~datetime.datetime` or timestamp.
        If a file was passed, this overrides its mtime.
        rv.last_modified = last_modified
        rv.last_modified = mtime
        last_modified = datetime.datetime(1999, 1, 1)
        @app.route('/')
        def index():
            return flask.send_file(StringIO("party like it's"), last_modified=last_modified)
        c = app.test_client()
        rv = c.get('/')
        assert rv.last_modified == last_modified
from __future__ import print_function
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'flaskdocext'
]
    print('Flask must be installed to build the documentation.')
    print('Install from source using `pip install -e .` in a virtualenv.')
except ImportError as e:
    print('-' * 74)
    print('Warning: Flask themes unavailable.  Building with default theme')
    print('If you want the Flask themes, run this command and build again:')
    print()
    print('  git submodule update --init')
    print('-' * 74)
    fp.write(text_type(htmlsafe_dumps(obj, **kwargs)))
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] and not request.is_xhr:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    return current_app.response_class(
        mimetype='application/json'
    )