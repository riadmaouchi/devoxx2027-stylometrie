# Corpus « temoin » — sous-paquet sansio de pallets/werkzeug, lignes non vides.
# Licence BSD-3-Clause. Trois sous-paquets du MEME projet : si l ecart de la
# condition B venait de « fichiers entiers contre lignes concatenees », C monterait aussi.
from __future__ import annotations
import re
import typing as t
from datetime import datetime
from .._internal import _dt_as_utc
from ..http import generate_etag
from ..http import parse_date
from ..http import parse_etags
from ..http import parse_if_range_header
from ..http import unquote_etag
_etag_re = re.compile(r'([Ww]/)?(?:"(.*?)"|(.*?))(?:\s*,\s*|$)')
def is_resource_modified(
    http_range: str | None = None,
    http_if_range: str | None = None,
    http_if_modified_since: str | None = None,
    http_if_none_match: str | None = None,
    http_if_match: str | None = None,
    etag: str | None = None,
    data: bytes | None = None,
    last_modified: datetime | str | None = None,
    ignore_if_range: bool = True,
) -> bool:
    """Convenience method for conditional requests.
    :param http_range: Range HTTP header
    :param http_if_range: If-Range HTTP header
    :param http_if_modified_since: If-Modified-Since HTTP header
    :param http_if_none_match: If-None-Match HTTP header
    :param http_if_match: If-Match HTTP header
    :param etag: the etag for the response for comparison.
    :param data: or alternatively the data of the response to automatically
                 generate an etag using :func:`generate_etag`.
    :param last_modified: an optional date of the last modification.
    :param ignore_if_range: If `False`, `If-Range` header will be taken into
                            account.
    :return: `True` if the resource was modified, otherwise `False`.
    .. versionadded:: 2.2
    """
    if etag is None and data is not None:
        etag = generate_etag(data)
    elif data is not None:
        raise TypeError("both data and etag given")
    unmodified = False
    if isinstance(last_modified, str):
        last_modified = parse_date(last_modified)
    # HTTP doesn't use microsecond, remove it to avoid false positive
    # comparisons. Mark naive datetimes as UTC.
    if last_modified is not None:
        last_modified = _dt_as_utc(last_modified.replace(microsecond=0))
    if_range = None
    if not ignore_if_range and http_range is not None:
        # https://tools.ietf.org/html/rfc7233#section-3.2
        # A server MUST ignore an If-Range header field received in a request
        # that does not contain a Range header field.
        if_range = parse_if_range_header(http_if_range)
    if if_range is not None and if_range.date is not None:
        modified_since: datetime | None = if_range.date
    else:
        modified_since = parse_date(http_if_modified_since)
    if modified_since and last_modified and last_modified <= modified_since:
        unmodified = True
    if etag:
        etag, _ = unquote_etag(etag)
        if if_range is not None and if_range.etag is not None:
            unmodified = parse_etags(if_range.etag).contains(etag)
        else:
            if_none_match = parse_etags(http_if_none_match)
            if if_none_match:
                # https://tools.ietf.org/html/rfc7232#section-3.2
                # "A recipient MUST use the weak comparison function when comparing
                # entity-tags for If-None-Match"
                unmodified = if_none_match.contains_weak(etag)
            # https://tools.ietf.org/html/rfc7232#section-3.1
            # "Origin server MUST use the strong comparison function when
            # comparing entity-tags for If-Match"
            if_match = parse_etags(http_if_match)
            if if_match:
                unmodified = not if_match.is_strong(etag)
    return not unmodified
_cookie_re = re.compile(
    r"""
    ([^=;]*)
    (?:\s*=\s*
      (
        "(?:[^\\"]|\\.)*"
      |
        .*?
      )
    )?
    \s*;\s*
    """,
    flags=re.ASCII | re.VERBOSE,
)
_cookie_unslash_re = re.compile(rb"\\([0-3][0-7]{2}|.)")
def _cookie_unslash_replace(m: t.Match[bytes]) -> bytes:
    v = m.group(1)
    if len(v) == 1:
        return v
    return int(v, 8).to_bytes(1, "big")
def parse_cookie(
    cookie: str | None = None,
    cls: type[ds.MultiDict[str, str]] | None = None,
) -> ds.MultiDict[str, str]:
    """Parse a cookie from a string.
    The same key can be provided multiple times, the values are stored
    in-order. The default :class:`MultiDict` will have the first value
    first, and all values can be retrieved with
    :meth:`MultiDict.getlist`.
    :param cookie: The cookie header as a string.
    :param cls: A dict-like class to store the parsed cookies in.
        Defaults to :class:`MultiDict`.
    .. versionchanged:: 3.0
        Passing bytes, and the ``charset`` and ``errors`` parameters, were removed.
    .. versionadded:: 2.2
    """
    if cls is None:
        cls = t.cast("type[ds.MultiDict[str, str]]", ds.MultiDict)
    if not cookie:
        return cls()
    cookie = f"{cookie};"
    out = []
    for ck, cv in _cookie_re.findall(cookie):
        ck = ck.strip()
        cv = cv.strip()
        if not ck:
            continue
        if len(cv) >= 2 and cv[0] == cv[-1] == '"':
            # Work with bytes here, since a UTF-8 character could be multiple bytes.
            cv = _cookie_unslash_re.sub(
                _cookie_unslash_replace, cv[1:-1].encode()
            ).decode(errors="replace")
        out.append((ck, cv))
    return cls(out)
# circular dependencies
from .. import datastructures as ds  # noqa: E402
from __future__ import annotations
import re
import typing as t
from dataclasses import dataclass
from enum import auto
from enum import Enum
from ..datastructures import Headers
from ..exceptions import RequestEntityTooLarge
from ..http import parse_options_header
class Event:
    pass
@dataclass(frozen=True)
class Preamble(Event):
    data: bytes
@dataclass(frozen=True)
class Field(Event):
    name: str
    headers: Headers
@dataclass(frozen=True)
class File(Event):
    name: str
    filename: str
    headers: Headers
@dataclass(frozen=True)
class Data(Event):
    data: bytes
    more_data: bool
@dataclass(frozen=True)
class Epilogue(Event):
    data: bytes
class NeedData(Event):
    pass
NEED_DATA = NeedData()
class State(Enum):
    PREAMBLE = auto()
    PART = auto()
    DATA = auto()
    DATA_START = auto()
    EPILOGUE = auto()
    COMPLETE = auto()
# Multipart line breaks MUST be CRLF (\r\n) by RFC-7578, except that
# many implementations break this and either use CR or LF alone.
LINE_BREAK = b"(?:\r\n|\n|\r)"
BLANK_LINE_RE = re.compile(b"(?:\r\n\r\n|\r\r|\n\n)", re.MULTILINE)
LINE_BREAK_RE = re.compile(LINE_BREAK, re.MULTILINE)
# Header values can be continued via a space or tab after the linebreak, as
# per RFC2231
HEADER_CONTINUATION_RE = re.compile(b"%s[ \t]" % LINE_BREAK, re.MULTILINE)
# This must be long enough to contain any line breaks plus any
# additional boundary markers (--) such that they will be found in a
# subsequent search
SEARCH_EXTRA_LENGTH = 8
class MultipartDecoder:
    """Decodes a multipart message as bytes into Python events.
    The part data is returned as available to allow the caller to save
    the data from memory to disk, if desired.
    .. versionchanged:: 3.1.4
        Handle chunks that split a``\r\n`` sequence.
    """
    def __init__(
        self,
        boundary: bytes,
        max_form_memory_size: int | None = None,
        *,
        max_parts: int | None = None,
    ) -> None:
        self.buffer = bytearray()
        self.complete = False
        self.max_form_memory_size = max_form_memory_size
        self.max_parts = max_parts
        self.state = State.PREAMBLE
        self.boundary = boundary
        # Note in the below \h i.e. horizontal whitespace is used
        # as [^\S\n\r] as \h isn't supported in python.
        # The preamble must end with a boundary where the boundary is
        # prefixed by a line break, RFC2046. Except that many
        # implementations including Werkzeug's tests omit the line
        # break prefix. In addition the first boundary could be the
        # epilogue boundary (for empty form-data) hence the matching
        # group to understand if it is an epilogue boundary.
        self.preamble_re = re.compile(
            rb"%s?--%s(--[^\S\n\r]*%s?|[^\S\n\r]*%s)"
            % (LINE_BREAK, re.escape(boundary), LINE_BREAK, LINE_BREAK),
            re.MULTILINE,
        )
        # A boundary must include a line break prefix and suffix, and
        # may include trailing whitespace. In addition the boundary
        # could be the epilogue boundary hence the matching group to
        # understand if it is an epilogue boundary.
        self.boundary_re = re.compile(
            rb"%s--%s(--[^\S\n\r]*%s?|[^\S\n\r]*%s)"
            % (LINE_BREAK, re.escape(boundary), LINE_BREAK, LINE_BREAK),
            re.MULTILINE,
        )
        self._search_position = 0
        self._parts_decoded = 0
    def receive_data(self, data: bytes | None) -> None:
        if data is None:
            self.complete = True
        elif (
            self.max_form_memory_size is not None
            and len(self.buffer) + len(data) > self.max_form_memory_size
        ):
            # Ensure that data within single event does not exceed limit.
            # Also checked across accumulated events in MultiPartParser.
            raise RequestEntityTooLarge()
        else:
            self.buffer.extend(data)
    def next_event(self) -> Event:
        event: Event = NEED_DATA
        if self.state == State.PREAMBLE:
            match = self.preamble_re.search(self.buffer, self._search_position)
            if match is not None:
                if match.group(1).startswith(b"--"):
                    self.state = State.EPILOGUE
                else:
                    self.state = State.PART
                data = bytes(self.buffer[: match.start()])
                del self.buffer[: match.end()]
                event = Preamble(data=data)
                self._search_position = 0
            else:
                # Update the search start position to be equal to the
                # current buffer length (already searched) minus a
                # safe buffer for part of the search target.
                self._search_position = max(
                    0, len(self.buffer) - len(self.boundary) - SEARCH_EXTRA_LENGTH
                )
        elif self.state == State.PART:
            match = BLANK_LINE_RE.search(self.buffer, self._search_position)
            if match is not None:
                headers = self._parse_headers(self.buffer[: match.start()])
                # The final header ends with a single CRLF, however a
                # blank line indicates the start of the
                # body. Therefore the end is after the first CRLF.
                headers_end = (match.start() + match.end()) // 2
                del self.buffer[:headers_end]
                if "content-disposition" not in headers:
                    raise ValueError("Missing Content-Disposition header")
                disposition, extra = parse_options_header(
                    headers["content-disposition"]
                )
                name = t.cast(str, extra.get("name"))
                filename = extra.get("filename")
                if filename is not None:
                    event = File(
                        filename=filename,
                        headers=headers,
                        name=name,
                    )
                else:
                    event = Field(
                        headers=headers,
                        name=name,
                    )
                self.state = State.DATA_START
                self._search_position = 0
                self._parts_decoded += 1
                if self.max_parts is not None and self._parts_decoded > self.max_parts:
                    raise RequestEntityTooLarge()
            else:
                # Update the search start position to be equal to the
                # current buffer length (already searched) minus a
                # safe buffer for part of the search target.
                self._search_position = max(0, len(self.buffer) - SEARCH_EXTRA_LENGTH)
        elif self.state == State.DATA_START:
            data, del_index, more_data = self._parse_data(self.buffer, start=True)
            del self.buffer[:del_index]
            event = Data(data=data, more_data=more_data)
            if more_data:
                self.state = State.DATA
        elif self.state == State.DATA:
            data, del_index, more_data = self._parse_data(self.buffer, start=False)
            del self.buffer[:del_index]
            if data or not more_data:
                event = Data(data=data, more_data=more_data)
        elif self.state == State.EPILOGUE and self.complete:
            event = Epilogue(data=bytes(self.buffer))
            del self.buffer[:]
            self.state = State.COMPLETE
        if self.complete and isinstance(event, NeedData):
            raise ValueError(f"Invalid form-data cannot parse beyond {self.state}")
        return event
    def _parse_headers(self, data: bytes | bytearray) -> Headers:
        headers: list[tuple[str, str]] = []
        # Merge the continued headers into one line
        data = HEADER_CONTINUATION_RE.sub(b" ", data)
        # Now there is one header per line
        for line in data.splitlines():
            line = line.strip()
            if line != b"":
                name, _, value = line.decode().partition(":")
                headers.append((name.strip(), value.strip()))
        return Headers(headers)
    def _parse_data(
        self, data: bytes | bytearray, *, start: bool
    ) -> tuple[bytes, int, bool]:
        # Body parts must start with CRLF (or CR or LF)
        if start:
            match = LINE_BREAK_RE.match(data)
            data_start = t.cast(t.Match[bytes], match).end()
        else:
            data_start = 0
        if self.buffer.find(b"--" + self.boundary) == -1:
            # No complete boundary in the buffer, but there may be
            # a partial boundary at the end.
            data_end = del_index = (
                self._last_partial_boundary_index(data[data_start:]) + data_start
            )
            more_data = True
        else:
            match = self.boundary_re.search(data)
            if match is not None:
                if match.group(1).startswith(b"--"):
                    self.state = State.EPILOGUE
                else:
                    self.state = State.PART
                data_end = match.start()
                del_index = match.end()
            else:
                data_end = del_index = (
                    self._last_partial_boundary_index(data[data_start:]) + data_start
                )
            more_data = match is None
        return bytes(data[data_start:data_end]), del_index, more_data
    def _last_partial_boundary_index(self, data: bytes | bytearray) -> int:
        # Find the last index following which a partial boundary
        # could be present in the data. This will be the earliest
        # position of a LF or a CR, unless that position is more
        # than a complete boundary from the end in which case there
        # is no partial boundary.
        complete_boundary_index = len(data) - len(b"\r\n--" + self.boundary)
        try:
            last_nl = data.rindex(b"\n")
        except ValueError:
            last_nl = len(data)
        else:
            if last_nl < complete_boundary_index:
                last_nl = len(data)
        try:
            last_cr = data.rindex(b"\r")
        except ValueError:
            last_cr = len(data)
        else:
            if last_cr < complete_boundary_index:
                last_cr = len(data)
        return min(last_nl, last_cr)
class MultipartEncoder:
    def __init__(self, boundary: bytes) -> None:
        self.boundary = boundary
        self.state = State.PREAMBLE
    def send_event(self, event: Event) -> bytes:
        if isinstance(event, Preamble) and self.state == State.PREAMBLE:
            self.state = State.PART
            return event.data
        elif isinstance(event, (Field, File)) and self.state in {
            State.PREAMBLE,
            State.PART,
            State.DATA,
        }:
            data = b"\r\n--" + self.boundary + b"\r\n"
            data += b'Content-Disposition: form-data; name="%s"' % event.name.encode()
            if isinstance(event, File):
                data += b'; filename="%s"' % event.filename.encode()
            data += b"\r\n"
            for name, value in t.cast(Field, event).headers:
                if name.lower() != "content-disposition":
                    data += f"{name}: {value}\r\n".encode()
            self.state = State.DATA_START
            return data
        elif isinstance(event, Data) and self.state == State.DATA_START:
            self.state = State.DATA
            if len(event.data) > 0:
                return b"\r\n" + event.data
            else:
                return event.data
        elif isinstance(event, Data) and self.state == State.DATA:
            return event.data
        elif isinstance(event, Epilogue):
            self.state = State.COMPLETE
            return b"\r\n--" + self.boundary + b"--\r\n" + event.data
        else:
            raise ValueError(f"Cannot generate {event} in state: {self.state}")
from __future__ import annotations
import typing as t
from datetime import datetime
from urllib.parse import parse_qsl
from ..datastructures import Accept
from ..datastructures import Authorization
from ..datastructures import CharsetAccept
from ..datastructures import ETags
from ..datastructures import Headers
from ..datastructures import HeaderSet
from ..datastructures import IfRange
from ..datastructures import ImmutableList
from ..datastructures import ImmutableMultiDict
from ..datastructures import LanguageAccept
from ..datastructures import MIMEAccept
from ..datastructures import MultiDict
from ..datastructures import Range
from ..datastructures import RequestCacheControl
from ..http import parse_accept_header
from ..http import parse_cache_control_header
from ..http import parse_date
from ..http import parse_etags
from ..http import parse_if_range_header
from ..http import parse_list_header
from ..http import parse_options_header
from ..http import parse_range_header
from ..http import parse_set_header
from ..user_agent import UserAgent
from ..utils import cached_property
from ..utils import header_property
from .http import parse_cookie
from .utils import get_content_length
from .utils import get_current_url
from .utils import get_host
class Request:
    """Represents the non-IO parts of a HTTP request, including the
    method, URL info, and headers.
    This class is not meant for general use. It should only be used when
    implementing WSGI, ASGI, or another HTTP application spec. Werkzeug
    provides a WSGI implementation at :cls:`werkzeug.wrappers.Request`.
    :param method: The method the request was made with, such as
        ``GET``.
    :param scheme: The URL scheme of the protocol the request used, such
        as ``https`` or ``wss``.
    :param server: The address of the server. ``(host, port)``,
        ``(path, None)`` for unix sockets, or ``None`` if not known.
    :param root_path: The prefix that the application is mounted under.
        This is prepended to generated URLs, but is not part of route
        matching.
    :param path: The path part of the URL after ``root_path``.
    :param query_string: The part of the URL after the "?".
    :param headers: The headers received with the request.
    :param remote_addr: The address of the client sending the request.
    .. versionchanged:: 3.0
        The ``charset``, ``url_charset``, and ``encoding_errors`` attributes
        were removed.
    .. versionadded:: 2.0
    """
    #: the class to use for `args` and `form`.  The default is an
    #: :class:`~werkzeug.datastructures.ImmutableMultiDict` which supports
    #: multiple values per key. A :class:`~werkzeug.datastructures.ImmutableDict`
    #: is faster but only remembers the last key. It is also
    #: possible to use mutable structures, but this is not recommended.
    #:
    #: .. versionadded:: 0.6
    parameter_storage_class: type[MultiDict[str, t.Any]] = ImmutableMultiDict
    #: The type to be used for dict values from the incoming WSGI
    #: environment. (For example for :attr:`cookies`.) By default an
    #: :class:`~werkzeug.datastructures.ImmutableMultiDict` is used.
    #:
    #: .. versionchanged:: 1.0.0
    #:     Changed to ``ImmutableMultiDict`` to support multiple values.
    #:
    #: .. versionadded:: 0.6
    dict_storage_class: type[MultiDict[str, t.Any]] = ImmutableMultiDict
    #: the type to be used for list values from the incoming WSGI environment.
    #: By default an :class:`~werkzeug.datastructures.ImmutableList` is used
    #: (for example for :attr:`access_list`).
    #:
    #: .. versionadded:: 0.6
    list_storage_class: type[list[t.Any]] = ImmutableList
    user_agent_class: type[UserAgent] = UserAgent
    """The class used and returned by the :attr:`user_agent` property to
    parse the header. Defaults to
    :class:`~werkzeug.user_agent.UserAgent`, which does no parsing. An
    extension can provide a subclass that uses a parser to provide other
    data.
    .. versionadded:: 2.0
    """
    #: Valid host names when handling requests. By default all hosts are
    #: trusted, which means that whatever the client says the host is
    #: will be accepted.
    #:
    #: Because ``Host`` and ``X-Forwarded-Host`` headers can be set to
    #: any value by a malicious client, it is recommended to either set
    #: this property or implement similar validation in the proxy (if
    #: the application is being run behind one).
    #:
    #: .. versionadded:: 0.9
    trusted_hosts: list[str] | None = None
    def __init__(
        self,
        method: str,
        scheme: str,
        server: tuple[str, int | None] | None,
        root_path: str,
        path: str,
        query_string: bytes,
        headers: Headers,
        remote_addr: str | None,
    ) -> None:
        #: The method the request was made with, such as ``GET``.
        self.method = method.upper()
        #: The URL scheme of the protocol the request used, such as
        #: ``https`` or ``wss``.
        self.scheme = scheme
        #: The address of the server. ``(host, port)``, ``(path, None)``
        #: for unix sockets, or ``None`` if not known.
        self.server = server
        #: The prefix that the application is mounted under, without a
        #: trailing slash. :attr:`path` comes after this.
        self.root_path = root_path.rstrip("/")
        #: The path part of the URL after :attr:`root_path`. This is the
        #: path used for routing within the application.
        self.path = "/" + path.lstrip("/")
        #: The part of the URL after the "?". This is the raw value, use
        #: :attr:`args` for the parsed values.
        self.query_string = query_string
        #: The headers received with the request.
        self.headers = headers
        #: The address of the client sending the request.
        self.remote_addr = remote_addr
    def __repr__(self) -> str:
        try:
            url = self.url
        except Exception as e:
            url = f"(invalid URL: {e})"
        return f"<{type(self).__name__} {url!r} [{self.method}]>"
    @cached_property
    def args(self) -> MultiDict[str, str]:
        """The parsed URL parameters (the part in the URL after the question
        mark).
        By default an
        :class:`~werkzeug.datastructures.ImmutableMultiDict`
        is returned from this function.  This can be changed by setting
        :attr:`parameter_storage_class` to a different type.  This might
        be necessary if the order of the form data is important.
        .. versionchanged:: 2.3
            Invalid bytes remain percent encoded.
        """
        return self.parameter_storage_class(
            parse_qsl(
                self.query_string.decode(),
                keep_blank_values=True,
                errors="werkzeug.url_quote",
            )
        )
    @cached_property
    def access_route(self) -> list[str]:
        """If a forwarded header exists this is a list of all ip addresses
        from the client ip to the last proxy server.
        """
        if "X-Forwarded-For" in self.headers:
            return self.list_storage_class(
                parse_list_header(self.headers["X-Forwarded-For"])
            )
        elif self.remote_addr is not None:
            return self.list_storage_class([self.remote_addr])
        return self.list_storage_class()
    @cached_property
    def full_path(self) -> str:
        """Requested path, including the query string."""
        return f"{self.path}?{self.query_string.decode()}"
    @property
    def is_secure(self) -> bool:
        """``True`` if the request was made with a secure protocol
        (HTTPS or WSS).
        """
        return self.scheme in {"https", "wss"}
    @cached_property
    def url(self) -> str:
        """The full request URL with the scheme, host, root path, path,
        and query string."""
        return get_current_url(
            self.scheme, self.host, self.root_path, self.path, self.query_string
        )
    @cached_property
    def base_url(self) -> str:
        """Like :attr:`url` but without the query string."""
        return get_current_url(self.scheme, self.host, self.root_path, self.path)
    @cached_property
    def root_url(self) -> str:
        """The request URL scheme, host, and root path. This is the root
        that the application is accessed from.
        """
        return get_current_url(self.scheme, self.host, self.root_path)
    @cached_property
    def host_url(self) -> str:
        """The request URL scheme and host only."""
        return get_current_url(self.scheme, self.host)
    @cached_property
    def host(self) -> str:
        """The host name the request was made to, including the port if
        it's non-standard. Validated with :attr:`trusted_hosts`.
        See :func:`.get_host` for a detailed explanation.
        """
        return get_host(
            self.scheme, self.headers.get("host"), self.server, self.trusted_hosts
        )
    @cached_property
    def cookies(self) -> ImmutableMultiDict[str, str]:
        """A :class:`dict` with the contents of all cookies transmitted with
        the request."""
        wsgi_combined_cookie = ";".join(self.headers.getlist("Cookie"))
        return parse_cookie(  # type: ignore
            wsgi_combined_cookie, cls=self.dict_storage_class
        )
    # Common Descriptors
    content_type = header_property[str](
        "Content-Type",
        doc="""The Content-Type entity-header field indicates the media
        type of the entity-body sent to the recipient or, in the case of
        the HEAD method, the media type that would have been sent had
        the request been a GET.""",
        read_only=True,
    )
    @cached_property
    def content_length(self) -> int | None:
        """The Content-Length entity-header field indicates the size of the
        entity-body in bytes or, in the case of the HEAD method, the size of
        the entity-body that would have been sent had the request been a
        GET.
        """
        return get_content_length(
            http_content_length=self.headers.get("Content-Length"),
            http_transfer_encoding=self.headers.get("Transfer-Encoding"),
        )
    content_encoding = header_property[str](
        "Content-Encoding",
        doc="""The Content-Encoding entity-header field is used as a
        modifier to the media-type. When present, its value indicates
        what additional content codings have been applied to the
        entity-body, and thus what decoding mechanisms must be applied
        in order to obtain the media-type referenced by the Content-Type
        header field.
        .. versionadded:: 0.9""",
        read_only=True,
    )
    content_md5 = header_property[str](
        "Content-MD5",
        doc="""The Content-MD5 entity-header field, as defined in
        RFC 1864, is an MD5 digest of the entity-body for the purpose of
        providing an end-to-end message integrity check (MIC) of the
        entity-body. (Note: a MIC is good for detecting accidental
        modification of the entity-body in transit, but is not proof
        against malicious attacks.)
        .. versionadded:: 0.9""",
        read_only=True,
    )
    referrer = header_property[str](
        "Referer",
        doc="""The Referer[sic] request-header field allows the client
        to specify, for the server's benefit, the address (URI) of the
        resource from which the Request-URI was obtained (the
        "referrer", although the header field is misspelled).""",
        read_only=True,
    )
    date = header_property(
        "Date",
        None,
        parse_date,
        doc="""The Date general-header field represents the date and
        time at which the message was originated, having the same
        semantics as orig-date in RFC 822.
        .. versionchanged:: 2.0
            The datetime object is timezone-aware.
        """,
        read_only=True,
    )
    max_forwards = header_property(
        "Max-Forwards",
        None,
        int,
        doc="""The Max-Forwards request-header field provides a
        mechanism with the TRACE and OPTIONS methods to limit the number
        of proxies or gateways that can forward the request to the next
        inbound server.""",
        read_only=True,
    )
    def _parse_content_type(self) -> None:
        if not hasattr(self, "_parsed_content_type"):
            self._parsed_content_type = parse_options_header(
                self.headers.get("Content-Type", "")
            )
    @property
    def mimetype(self) -> str:
        """Like :attr:`content_type`, but without parameters (eg, without
        charset, type etc.) and always lowercase.  For example if the content
        type is ``text/HTML; charset=utf-8`` the mimetype would be
        ``'text/html'``.
        """
        self._parse_content_type()
        return self._parsed_content_type[0].lower()
    @property
    def mimetype_params(self) -> dict[str, str]:
        """The mimetype parameters as dict.  For example if the content
        type is ``text/html; charset=utf-8`` the params would be
        ``{'charset': 'utf-8'}``.
        """
        self._parse_content_type()
        return self._parsed_content_type[1]
    @cached_property
    def pragma(self) -> HeaderSet:
        """The Pragma general-header field is used to include
        implementation-specific directives that might apply to any recipient
        along the request/response chain.  All pragma directives specify
        optional behavior from the viewpoint of the protocol; however, some
        systems MAY require that behavior be consistent with the directives.
        """
        return parse_set_header(self.headers.get("Pragma", ""))
    # Accept
    @cached_property
    def accept_mimetypes(self) -> MIMEAccept:
        """List of mimetypes this client supports as
        :class:`~werkzeug.datastructures.MIMEAccept` object.
        """
        return parse_accept_header(self.headers.get("Accept"), MIMEAccept)
    @cached_property
    def accept_charsets(self) -> CharsetAccept:
        """List of charsets this client supports as
        :class:`~werkzeug.datastructures.CharsetAccept` object.
        """
        return parse_accept_header(self.headers.get("Accept-Charset"), CharsetAccept)
    @cached_property
    def accept_encodings(self) -> Accept:
        """List of encodings this client accepts.  Encodings in a HTTP term
        are compression encodings such as gzip.  For charsets have a look at
        :attr:`accept_charset`.
        """
        return parse_accept_header(self.headers.get("Accept-Encoding"))
    @cached_property
    def accept_languages(self) -> LanguageAccept:
        """List of languages this client accepts as
        :class:`~werkzeug.datastructures.LanguageAccept` object.
        .. versionchanged 0.5
           In previous versions this was a regular
           :class:`~werkzeug.datastructures.Accept` object.
        """
        return parse_accept_header(self.headers.get("Accept-Language"), LanguageAccept)
    # ETag
    @cached_property
    def cache_control(self) -> RequestCacheControl:
        """A :class:`~werkzeug.datastructures.RequestCacheControl` object
        for the incoming cache control headers.
        """
        cache_control = self.headers.get("Cache-Control")
        return parse_cache_control_header(cache_control, None, RequestCacheControl)
    @cached_property
    def if_match(self) -> ETags:
        """An object containing all the etags in the `If-Match` header.
        :rtype: :class:`~werkzeug.datastructures.ETags`
        """
        return parse_etags(self.headers.get("If-Match"))
    @cached_property
    def if_none_match(self) -> ETags:
        """An object containing all the etags in the `If-None-Match` header.
        :rtype: :class:`~werkzeug.datastructures.ETags`
        """
        return parse_etags(self.headers.get("If-None-Match"))
    @cached_property
    def if_modified_since(self) -> datetime | None:
        """The parsed `If-Modified-Since` header as a datetime object.
        .. versionchanged:: 2.0
            The datetime object is timezone-aware.
        """
        return parse_date(self.headers.get("If-Modified-Since"))
    @cached_property
    def if_unmodified_since(self) -> datetime | None:
        """The parsed `If-Unmodified-Since` header as a datetime object.
        .. versionchanged:: 2.0
            The datetime object is timezone-aware.
        """
        return parse_date(self.headers.get("If-Unmodified-Since"))
    @cached_property
    def if_range(self) -> IfRange:
        """The parsed ``If-Range`` header.
        .. versionchanged:: 2.0
            ``IfRange.date`` is timezone-aware.
        .. versionadded:: 0.7
        """
        return parse_if_range_header(self.headers.get("If-Range"))
    @cached_property
    def range(self) -> Range | None:
        """The parsed `Range` header.
        .. versionadded:: 0.7
        :rtype: :class:`~werkzeug.datastructures.Range`
        """
        return parse_range_header(self.headers.get("Range"))
    # User Agent
    @cached_property
    def user_agent(self) -> UserAgent:
        """The user agent. Use ``user_agent.string`` to get the header
        value. Set :attr:`user_agent_class` to a subclass of
        :class:`~werkzeug.user_agent.UserAgent` to provide parsing for
        the other properties or other extended data.
        .. versionchanged:: 2.1
            The built-in parser was removed. Set ``user_agent_class`` to a ``UserAgent``
            subclass to parse data from the string.
        """
        return self.user_agent_class(self.headers.get("User-Agent", ""))
    # Authorization
    @cached_property
    def authorization(self) -> Authorization | None:
        """The ``Authorization`` header parsed into an :class:`.Authorization` object.
        ``None`` if the header is not present.
        .. versionchanged:: 2.3
            :class:`Authorization` is no longer a ``dict``. The ``token`` attribute
            was added for auth schemes that use a token instead of parameters.
        """
        return Authorization.from_header(self.headers.get("Authorization"))
    # CORS
    origin = header_property[str](
        "Origin",
        doc=(
            "The host that the request originated from. Set"
            " :attr:`~CORSResponseMixin.access_control_allow_origin` on"
            " the response to indicate which origins are allowed."
        ),
        read_only=True,
    )
    access_control_request_headers = header_property(
        "Access-Control-Request-Headers",
        load_func=parse_set_header,
        doc=(
            "Sent with a preflight request to indicate which headers"
            " will be sent with the cross origin request. Set"
            " :attr:`~CORSResponseMixin.access_control_allow_headers`"
            " on the response to indicate which headers are allowed."
        ),
        read_only=True,
    )
    access_control_request_method = header_property[str](
        "Access-Control-Request-Method",
        doc=(
            "Sent with a preflight request to indicate which method"
            " will be used for the cross origin request. Set"
            " :attr:`~CORSResponseMixin.access_control_allow_methods`"
            " on the response to indicate which methods are allowed."
        ),
        read_only=True,
    )
    @property
    def is_json(self) -> bool:
        """Check if the mimetype indicates JSON data, either
        :mimetype:`application/json` or :mimetype:`application/*+json`.
        """
        mt = self.mimetype
        return (
            mt == "application/json"
            or mt.startswith("application/")
            and mt.endswith("+json")
        )
from __future__ import annotations
import typing as t
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from http import HTTPStatus
from ..datastructures import CallbackDict
from ..datastructures import ContentRange
from ..datastructures import ContentSecurityPolicy
from ..datastructures import Headers
from ..datastructures import HeaderSet
from ..datastructures import ResponseCacheControl
from ..datastructures import WWWAuthenticate
from ..http import COEP
from ..http import COOP
from ..http import dump_age
from ..http import dump_cookie
from ..http import dump_header
from ..http import dump_options_header
from ..http import http_date
from ..http import HTTP_STATUS_CODES
from ..http import parse_age
from ..http import parse_cache_control_header
from ..http import parse_content_range_header
from ..http import parse_csp_header
from ..http import parse_date
from ..http import parse_options_header
from ..http import parse_set_header
from ..http import quote_etag
from ..http import unquote_etag
from ..utils import get_content_type
from ..utils import header_property
if t.TYPE_CHECKING:
    from ..datastructures.cache_control import _CacheControl
def _set_property(name: str, doc: str | None = None) -> property:
    def fget(self: Response) -> HeaderSet:
        def on_update(header_set: HeaderSet) -> None:
            if not header_set and name in self.headers:
                del self.headers[name]
            elif header_set:
                self.headers[name] = header_set.to_header()
        return parse_set_header(self.headers.get(name), on_update)
    def fset(
        self: Response,
        value: None | (str | dict[str, str | int] | t.Iterable[str]),
    ) -> None:
        if not value:
            del self.headers[name]
        elif isinstance(value, str):
            self.headers[name] = value
        else:
            self.headers[name] = dump_header(value)
    return property(fget, fset, doc=doc)
class Response:
    """Represents the non-IO parts of an HTTP response, specifically the
    status and headers but not the body.
    This class is not meant for general use. It should only be used when
    implementing WSGI, ASGI, or another HTTP application spec. Werkzeug
    provides a WSGI implementation at :cls:`werkzeug.wrappers.Response`.
    :param status: The status code for the response. Either an int, in
        which case the default status message is added, or a string in
        the form ``{code} {message}``, like ``404 Not Found``. Defaults
        to 200.
    :param headers: A :class:`~werkzeug.datastructures.Headers` object,
        or a list of ``(key, value)`` tuples that will be converted to a
        ``Headers`` object.
    :param mimetype: The mime type (content type without charset or
        other parameters) of the response. If the value starts with
        ``text/`` (or matches some other special cases), the charset
        will be added to create the ``content_type``.
    :param content_type: The full content type of the response.
        Overrides building the value from ``mimetype``.
    .. versionchanged:: 3.0
        The ``charset`` attribute was removed.
    .. versionadded:: 2.0
    """
    #: the default status if none is provided.
    default_status = 200
    #: the default mimetype if none is provided.
    default_mimetype: str | None = "text/plain"
    #: Warn if a cookie header exceeds this size. The default, 4093, should be
    #: safely `supported by most browsers <cookie_>`_. A cookie larger than
    #: this size will still be sent, but it may be ignored or handled
    #: incorrectly by some browsers. Set to 0 to disable this check.
    #:
    #: .. versionadded:: 0.13
    #:
    #: .. _`cookie`: http://browsercookielimits.squawky.net/
    max_cookie_size = 4093
    # A :class:`Headers` object representing the response headers.
    headers: Headers
    def __init__(
        self,
        status: int | str | HTTPStatus | None = None,
        headers: t.Mapping[str, str | t.Iterable[str]]
        | t.Iterable[tuple[str, str]]
        | None = None,
        mimetype: str | None = None,
        content_type: str | None = None,
    ) -> None:
        if isinstance(headers, Headers):
            self.headers = headers
        elif not headers:
            self.headers = Headers()
        else:
            self.headers = Headers(headers)
        if content_type is None:
            if mimetype is None and "content-type" not in self.headers:
                mimetype = self.default_mimetype
            if mimetype is not None:
                mimetype = get_content_type(mimetype, "utf-8")
            content_type = mimetype
        if content_type is not None:
            self.headers["Content-Type"] = content_type
        if status is None:
            status = self.default_status
        self.status = status
    def __repr__(self) -> str:
        return f"<{type(self).__name__} [{self.status}]>"
    @property
    def status_code(self) -> int:
        """The HTTP status code as a number."""
        return self._status_code
    @status_code.setter
    def status_code(self, code: int) -> None:
        self.status = code
    @property
    def status(self) -> str:
        """The HTTP status code as a string."""
        return self._status
    @status.setter
    def status(self, value: str | int | HTTPStatus) -> None:
        self._status, self._status_code = self._clean_status(value)
    def _clean_status(self, value: str | int | HTTPStatus) -> tuple[str, int]:
        if isinstance(value, (int, HTTPStatus)):
            status_code = int(value)
        else:
            value = value.strip()
            if not value:
                raise ValueError("Empty status argument")
            code_str, sep, _ = value.partition(" ")
            try:
                status_code = int(code_str)
            except ValueError:
                # only message
                return f"0 {value}", 0
            if sep:
                # code and message
                return value, status_code
        # only code, look up message
        try:
            status = f"{status_code} {HTTP_STATUS_CODES[status_code].upper()}"
        except KeyError:
            status = f"{status_code} UNKNOWN"
        return status, status_code
    def set_cookie(
        self,
        key: str,
        value: str = "",
        max_age: timedelta | int | None = None,
        expires: str | datetime | int | float | None = None,
        path: str | None = "/",
        domain: str | None = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: str | None = None,
        partitioned: bool = False,
    ) -> None:
        """Sets a cookie.
        A warning is raised if the size of the cookie header exceeds
        :attr:`max_cookie_size`, but the header will still be set.
        :param key: the key (name) of the cookie to be set.
        :param value: the value of the cookie.
        :param max_age: should be a number of seconds, or `None` (default) if
                        the cookie should last only as long as the client's
                        browser session.
        :param expires: should be a `datetime` object or UNIX timestamp.
        :param path: limits the cookie to a given path, per default it will
                     span the whole domain.
        :param domain: if you want to set a cross-domain cookie.  For example,
                       ``domain="example.com"`` will set a cookie that is
                       readable by the domain ``www.example.com``,
                       ``foo.example.com`` etc.  Otherwise, a cookie will only
                       be readable by the domain that set it.
        :param secure: If ``True``, the cookie will only be available
            via HTTPS.
        :param httponly: Disallow JavaScript access to the cookie.
        :param samesite: Limit the scope of the cookie to only be
            attached to requests that are "same-site".
        :param partitioned: If ``True``, the cookie will be partitioned.
        .. versionchanged:: 3.1
            The ``partitioned`` parameter was added.
        """
        self.headers.add(
            "Set-Cookie",
            dump_cookie(
                key,
                value=value,
                max_age=max_age,
                expires=expires,
                path=path,
                domain=domain,
                secure=secure,
                httponly=httponly,
                max_size=self.max_cookie_size,
                samesite=samesite,
                partitioned=partitioned,
            ),
        )
    def delete_cookie(
        self,
        key: str,
        path: str | None = "/",
        domain: str | None = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: str | None = None,
        partitioned: bool = False,
    ) -> None:
        """Delete a cookie.  Fails silently if key doesn't exist.
        :param key: the key (name) of the cookie to be deleted.
        :param path: if the cookie that should be deleted was limited to a
                     path, the path has to be defined here.
        :param domain: if the cookie that should be deleted was limited to a
                       domain, that domain has to be defined here.
        :param secure: If ``True``, the cookie will only be available
            via HTTPS.
        :param httponly: Disallow JavaScript access to the cookie.
        :param samesite: Limit the scope of the cookie to only be
            attached to requests that are "same-site".
        :param partitioned: If ``True``, the cookie will be partitioned.
        """
        self.set_cookie(
            key,
            expires=0,
            max_age=0,
            path=path,
            domain=domain,
            secure=secure,
            httponly=httponly,
            samesite=samesite,
            partitioned=partitioned,
        )
    @property
    def is_json(self) -> bool:
        """Check if the mimetype indicates JSON data, either
        :mimetype:`application/json` or :mimetype:`application/*+json`.
        """
        mt = self.mimetype
        return mt is not None and (
            mt == "application/json"
            or mt.startswith("application/")
            and mt.endswith("+json")
        )
    # Common Descriptors
    @property
    def mimetype(self) -> str | None:
        """The mimetype (content type without charset etc.)"""
        ct = self.headers.get("content-type")
        if ct:
            return ct.split(";")[0].strip()
        else:
            return None
    @mimetype.setter
    def mimetype(self, value: str) -> None:
        self.headers["Content-Type"] = get_content_type(value, "utf-8")
    @property
    def mimetype_params(self) -> dict[str, str]:
        """The mimetype parameters as dict. For example if the
        content type is ``text/html; charset=utf-8`` the params would be
        ``{'charset': 'utf-8'}``.
        .. versionadded:: 0.5
        """
        def on_update(d: CallbackDict[str, str]) -> None:
            self.headers["Content-Type"] = dump_options_header(self.mimetype, d)
        d = parse_options_header(self.headers.get("content-type", ""))[1]
        return CallbackDict(d, on_update)
    location = header_property[str](
        "Location",
        doc="""The Location response-header field is used to redirect
        the recipient to a location other than the Request-URI for
        completion of the request or identification of a new
        resource.""",
    )
    age = header_property(
        "Age",
        None,
        parse_age,
        dump_age,  # type: ignore
        doc="""The Age response-header field conveys the sender's
        estimate of the amount of time since the response (or its
        revalidation) was generated at the origin server.
        Age values are non-negative decimal integers, representing time
        in seconds.""",
    )
    content_type = header_property[str](
        "Content-Type",
        doc="""The Content-Type entity-header field indicates the media
        type of the entity-body sent to the recipient or, in the case of
        the HEAD method, the media type that would have been sent had
        the request been a GET.""",
    )
    content_length = header_property(
        "Content-Length",
        None,
        int,
        str,
        doc="""The Content-Length entity-header field indicates the size
        of the entity-body, in decimal number of OCTETs, sent to the
        recipient or, in the case of the HEAD method, the size of the
        entity-body that would have been sent had the request been a
        GET.""",
    )
    content_location = header_property[str](
        "Content-Location",
        doc="""The Content-Location entity-header field MAY be used to
        supply the resource location for the entity enclosed in the
        message when that entity is accessible from a location separate
        from the requested resource's URI.""",
    )
    content_encoding = header_property[str](
        "Content-Encoding",
        doc="""The Content-Encoding entity-header field is used as a
        modifier to the media-type. When present, its value indicates
        what additional content codings have been applied to the
        entity-body, and thus what decoding mechanisms must be applied
        in order to obtain the media-type referenced by the Content-Type
        header field.""",
    )
    content_md5 = header_property[str](
        "Content-MD5",
        doc="""The Content-MD5 entity-header field, as defined in
        RFC 1864, is an MD5 digest of the entity-body for the purpose of
        providing an end-to-end message integrity check (MIC) of the
        entity-body. (Note: a MIC is good for detecting accidental
        modification of the entity-body in transit, but is not proof
        against malicious attacks.)""",
    )
    date = header_property(
        "Date",
        None,
        parse_date,
        http_date,
        doc="""The Date general-header field represents the date and
        time at which the message was originated, having the same
        semantics as orig-date in RFC 822.
        .. versionchanged:: 2.0
            The datetime object is timezone-aware.
        """,
    )
    expires = header_property(
        "Expires",
        None,
        parse_date,
        http_date,
        doc="""The Expires entity-header field gives the date/time after
        which the response is considered stale. A stale cache entry may
        not normally be returned by a cache.
        .. versionchanged:: 2.0
            The datetime object is timezone-aware.
        """,
    )
    last_modified = header_property(
        "Last-Modified",
        None,
        parse_date,
        http_date,
        doc="""The Last-Modified entity-header field indicates the date
        and time at which the origin server believes the variant was
        last modified.
        .. versionchanged:: 2.0
            The datetime object is timezone-aware.
        """,
    )
    @property
    def retry_after(self) -> datetime | None:
        """The Retry-After response-header field can be used with a
        503 (Service Unavailable) response to indicate how long the
        service is expected to be unavailable to the requesting client.
        Time in seconds until expiration or date.
        .. versionchanged:: 2.0
            The datetime object is timezone-aware.
        """
        value = self.headers.get("retry-after")
        if value is None:
            return None
        try:
            seconds = int(value)
        except ValueError:
            return parse_date(value)
        return datetime.now(timezone.utc) + timedelta(seconds=seconds)
    @retry_after.setter
    def retry_after(self, value: datetime | int | str | None) -> None:
        if value is None:
            if "retry-after" in self.headers:
                del self.headers["retry-after"]
            return
        elif isinstance(value, datetime):
            value = http_date(value)
        else:
            value = str(value)
        self.headers["Retry-After"] = value
    vary = _set_property(
        "Vary",
        doc="""The Vary field value indicates the set of request-header
        fields that fully determines, while the response is fresh,
        whether a cache is permitted to use the response to reply to a
        subsequent request without revalidation.""",
    )
    content_language = _set_property(
        "Content-Language",
        doc="""The Content-Language entity-header field describes the
        natural language(s) of the intended audience for the enclosed
        entity. Note that this might not be equivalent to all the
        languages used within the entity-body.""",
    )
    allow = _set_property(
        "Allow",
        doc="""The Allow entity-header field lists the set of methods
        supported by the resource identified by the Request-URI. The
        purpose of this field is strictly to inform the recipient of
        valid methods associated with the resource. An Allow header
        field MUST be present in a 405 (Method Not Allowed)
        response.""",
    )
    # ETag
    @property
    def cache_control(self) -> ResponseCacheControl:
        """The Cache-Control general-header field is used to specify
        directives that MUST be obeyed by all caching mechanisms along the
        request/response chain.
        """
        def on_update(cache_control: _CacheControl) -> None:
            if not cache_control and "cache-control" in self.headers:
                del self.headers["cache-control"]
            elif cache_control:
                self.headers["Cache-Control"] = cache_control.to_header()
        return parse_cache_control_header(
            self.headers.get("cache-control"), on_update, ResponseCacheControl
        )
    def set_etag(self, etag: str, weak: bool = False) -> None:
        """Set the etag, and override the old one if there was one."""
        self.headers["ETag"] = quote_etag(etag, weak)
    def get_etag(self) -> tuple[str, bool] | tuple[None, None]:
        """Return a tuple in the form ``(etag, is_weak)``.  If there is no
        ETag the return value is ``(None, None)``.
        """
        return unquote_etag(self.headers.get("ETag"))
    accept_ranges = header_property[str](
        "Accept-Ranges",
        doc="""The `Accept-Ranges` header. Even though the name would
        indicate that multiple values are supported, it must be one
        string token only.
        The values ``'bytes'`` and ``'none'`` are common.
        .. versionadded:: 0.7""",
    )
    @property
    def content_range(self) -> ContentRange:
        """The ``Content-Range`` header as a
        :class:`~werkzeug.datastructures.ContentRange` object. Available
        even if the header is not set.
        .. versionadded:: 0.7
        """
        def on_update(rng: ContentRange) -> None:
            if not rng:
                del self.headers["content-range"]
            else:
                self.headers["Content-Range"] = rng.to_header()
        rv = parse_content_range_header(self.headers.get("content-range"), on_update)
        # always provide a content range object to make the descriptor
        # more user friendly.  It provides an unset() method that can be
        # used to remove the header quickly.
        if rv is None:
            rv = ContentRange(None, None, None, on_update=on_update)
        return rv
    @content_range.setter
    def content_range(self, value: ContentRange | str | None) -> None:
        if not value:
            del self.headers["content-range"]
        elif isinstance(value, str):
            self.headers["Content-Range"] = value
        else:
            self.headers["Content-Range"] = value.to_header()
    # Authorization
    @property
    def www_authenticate(self) -> WWWAuthenticate:
        """The ``WWW-Authenticate`` header parsed into a :class:`.WWWAuthenticate`
        object. Modifying the object will modify the header value.
        This header is not set by default. To set this header, assign an instance of
        :class:`.WWWAuthenticate` to this attribute.
        .. code-block:: python
            response.www_authenticate = WWWAuthenticate(
                "basic", {"realm": "Authentication Required"}
            )
        Multiple values for this header can be sent to give the client multiple options.
        Assign a list to set multiple headers. However, modifying the items in the list
        will not automatically update the header values, and accessing this attribute
        will only ever return the first value.
        To unset this header, assign ``None`` or use ``del``.
        .. versionchanged:: 2.3
            This attribute can be assigned to set the header. A list can be assigned
            to set multiple header values. Use ``del`` to unset the header.
        .. versionchanged:: 2.3
            :class:`WWWAuthenticate` is no longer a ``dict``. The ``token`` attribute
            was added for auth challenges that use a token instead of parameters.
        """
        value = WWWAuthenticate.from_header(self.headers.get("WWW-Authenticate"))
        if value is None:
            value = WWWAuthenticate("basic")
        def on_update(value: WWWAuthenticate) -> None:
            self.www_authenticate = value
        value._on_update = on_update
        return value
    @www_authenticate.setter
    def www_authenticate(
        self, value: WWWAuthenticate | list[WWWAuthenticate] | None
    ) -> None:
        if not value:  # None or empty list
            del self.www_authenticate
        elif isinstance(value, list):
            # Clear any existing header by setting the first item.
            self.headers.set("WWW-Authenticate", value[0].to_header())
            for item in value[1:]:
                # Add additional header lines for additional items.
                self.headers.add("WWW-Authenticate", item.to_header())
        else:
            self.headers.set("WWW-Authenticate", value.to_header())
            def on_update(value: WWWAuthenticate) -> None:
                self.www_authenticate = value
            # When setting a single value, allow updating it directly.
            value._on_update = on_update
    @www_authenticate.deleter
    def www_authenticate(self) -> None:
        if "WWW-Authenticate" in self.headers:
            del self.headers["WWW-Authenticate"]
    # CSP
    @property
    def content_security_policy(self) -> ContentSecurityPolicy:
        """The ``Content-Security-Policy`` header as a
        :class:`~werkzeug.datastructures.ContentSecurityPolicy` object. Available
        even if the header is not set.
        The Content-Security-Policy header adds an additional layer of
        security to help detect and mitigate certain types of attacks.
        """
        def on_update(csp: ContentSecurityPolicy) -> None:
            if not csp:
                del self.headers["content-security-policy"]
            else:
                self.headers["Content-Security-Policy"] = csp.to_header()
        rv = parse_csp_header(self.headers.get("content-security-policy"), on_update)
        if rv is None:
            rv = ContentSecurityPolicy(None, on_update=on_update)
        return rv
    @content_security_policy.setter
    def content_security_policy(
        self, value: ContentSecurityPolicy | str | None
    ) -> None:
        if not value:
            del self.headers["content-security-policy"]
        elif isinstance(value, str):
            self.headers["Content-Security-Policy"] = value
        else:
            self.headers["Content-Security-Policy"] = value.to_header()
    @property
    def content_security_policy_report_only(self) -> ContentSecurityPolicy:
        """The ``Content-Security-policy-report-only`` header as a
        :class:`~werkzeug.datastructures.ContentSecurityPolicy` object. Available
        even if the header is not set.
        The Content-Security-Policy-Report-Only header adds a csp policy
        that is not enforced but is reported thereby helping detect
        certain types of attacks.
        """
        def on_update(csp: ContentSecurityPolicy) -> None:
            if not csp:
                del self.headers["content-security-policy-report-only"]
            else:
                self.headers["Content-Security-policy-report-only"] = csp.to_header()
        rv = parse_csp_header(
            self.headers.get("content-security-policy-report-only"), on_update
        )
        if rv is None:
            rv = ContentSecurityPolicy(None, on_update=on_update)
        return rv
    @content_security_policy_report_only.setter
    def content_security_policy_report_only(
        self, value: ContentSecurityPolicy | str | None
    ) -> None:
        if not value:
            del self.headers["content-security-policy-report-only"]
        elif isinstance(value, str):
            self.headers["Content-Security-policy-report-only"] = value
        else:
            self.headers["Content-Security-policy-report-only"] = value.to_header()
    # CORS
    @property
    def access_control_allow_credentials(self) -> bool:
        """Whether credentials can be shared by the browser to
        JavaScript code. As part of the preflight request it indicates
        whether credentials can be used on the cross origin request.
        """
        return "Access-Control-Allow-Credentials" in self.headers
    @access_control_allow_credentials.setter
    def access_control_allow_credentials(self, value: bool | None) -> None:
        if value is True:
            self.headers["Access-Control-Allow-Credentials"] = "true"
        else:
            self.headers.pop("Access-Control-Allow-Credentials", None)
    access_control_allow_headers = header_property(
        "Access-Control-Allow-Headers",
        load_func=parse_set_header,
        dump_func=dump_header,
        doc="Which headers can be sent with the cross origin request.",
    )
    access_control_allow_methods = header_property(
        "Access-Control-Allow-Methods",
        load_func=parse_set_header,
        dump_func=dump_header,
        doc="Which methods can be used for the cross origin request.",
    )
    access_control_allow_origin = header_property[str](
        "Access-Control-Allow-Origin",
        doc="The origin or '*' for any origin that may make cross origin requests.",
    )
    access_control_expose_headers = header_property(
        "Access-Control-Expose-Headers",
        load_func=parse_set_header,
        dump_func=dump_header,
        doc="Which headers can be shared by the browser to JavaScript code.",
    )
    access_control_max_age = header_property(
        "Access-Control-Max-Age",
        load_func=int,
        dump_func=str,
        doc="The maximum age in seconds the access control settings can be cached for.",
    )
    cross_origin_opener_policy = header_property[COOP](
        "Cross-Origin-Opener-Policy",
        load_func=lambda value: COOP(value),
        dump_func=lambda value: value.value,
        default=COOP.UNSAFE_NONE,
        doc="""Allows control over sharing of browsing context group with cross-origin
        documents. Values must be a member of the :class:`werkzeug.http.COOP` enum.""",
    )
    cross_origin_embedder_policy = header_property[COEP](
        "Cross-Origin-Embedder-Policy",
        load_func=lambda value: COEP(value),
        dump_func=lambda value: value.value,
        default=COEP.UNSAFE_NONE,
        doc="""Prevents a document from loading any cross-origin resources that do not
        explicitly grant the document permission. Values must be a member of the
        :class:`werkzeug.http.COEP` enum.""",
    )
from __future__ import annotations
import re
import typing as t
from urllib.parse import quote
from .._internal import _plain_int
from ..exceptions import SecurityError
from ..http import parse_set_header
from ..urls import uri_to_iri
_host_re = re.compile(
    r"""
    (
        [a-z0-9.-]+  # domain or ipv4
    |
        \[[a-f0-9]*:[a-f0-9.:]+]  # ipv6
    )
    (?::[0-9]+)?  # optional port
    """,
    flags=re.ASCII | re.IGNORECASE | re.VERBOSE,
)
def host_is_trusted(
    hostname: str | None, trusted_list: t.Collection[str] | None = None
) -> bool:
    """Perform some checks on a ``Host`` header ``host:port``. The host must be
    made up of valid characters, but this does not check validity beyond that.
    If a list of trusted domains is given, the domain must match one.
    :param hostname: The ``Host`` header ``host:port`` to check.
    :param trusted_list: A list of trusted domains to match. These should
        already be IDNA encoded, but will be encoded if needed. The port is
        ignored for this check. If a name starts with a dot it will match as a
        suffix, accepting all subdomains. If empty or ``None``, all domains are
        allowed.
    .. versionchanged:: 3.2
        The value's characters are validated.
    .. versionchanged:: 3.2
        ``trusted_list`` defaults to ``None``.
    .. versionadded:: 0.9
    """
    if not hostname:
        return False
    if _host_re.fullmatch(hostname) is None:
        return False
    hostname = hostname.partition(":")[0]
    if not trusted_list:
        return True
    if isinstance(trusted_list, str):
        trusted_list = [trusted_list]
    for ref in trusted_list:
        if ref.startswith("."):
            ref = ref[1:]
            suffix_match = True
        else:
            suffix_match = False
        try:
            ref = ref.partition(":")[0].encode("idna").decode("ascii")
        except UnicodeEncodeError:
            return False
        if ref == hostname or (suffix_match and hostname.endswith(f".{ref}")):
            return True
    return False
def get_host(
    scheme: str,
    host_header: str | None,
    server: tuple[str, int | None] | None = None,
    trusted_hosts: t.Collection[str] | None = None,
) -> str:
    """Get and validate a request's ``host:port`` based on the given values.
    The ``Host`` header sent by the client is preferred. Otherwise, the server's
    configured address is used. The port is omitted if it matches the standard
    HTTP or HTTPS ports.
    The value is passed through :func:`host_is_trusted`. The host must be made
    up of valid characters, but this does not check validity beyond that. If a
    list of trusted domains is given, the domain must match one.
    If the host header is not available, such as for HTTP/0.9 and 1.0, or it has
    invalid characters, the empty string is returned. Subdomain and host
    routing, and external URL building, will not work in these cases.
    :param scheme: The protocol of the request. Used to omit the standard ports
        80 and 443.
    :param host_header: The ``Host`` header value.
    :param server: The server's configured address ``(host, port)``. The server
        may be using a Unix socket and give ``(path, None)``; this is ignored as
        it would not produce a useful host value.
    :param trusted_hosts: A list of trusted domains to match. These should
        already be IDNA encoded, but will be encoded if needed. The port is
        ignored for this check. If a name starts with a dot it will match as a
        suffix, accepting all subdomains. If empty or ``None``, all domains are
        allowed.
    :return: Host, with port if necessary.
    :raise .SecurityError: If the host is not trusted.
    .. versionchanged:: 3.1.8
        The empty string is again returned if no host header value is available,
        or if the characters are invalid.
    .. versionchanged:: 3.1.7
        The characters of the host value are validated. The empty string is no
        longer allowed if no header value is available.
    .. versionchanged:: 3.2
        When using the server address, Unix sockets are ignored.
    .. versionchanged:: 3.1.3
        If ``SERVER_NAME`` is IPv6, it is wrapped in ``[]``.
    """
    if host_header is not None:
        host = host_header
    # The port server[1] will be None for a Unix socket. Ignore in that case.
    elif server is not None and server[1] is not None:
        host = server[0]
        # If SERVER_NAME is IPv6, wrap it in [] to match Host header.
        # Check for : because domain or IPv4 can't have that.
        if ":" in host and host[0] != "[":
            host = f"[{host}]"
        host = f"{host}:{server[1]}"
    else:
        # Pass through empty host from HTTP/0.9 and 1.0.
        return ""
    if scheme in {"http", "ws"}:
        host = host.removesuffix(":80")
    elif scheme in {"https", "wss"}:
        host = host.removesuffix(":443")
    if not host_is_trusted(host, trusted_hosts):
        if trusted_hosts:
            raise SecurityError(f"Host {host!r} is not trusted.")
        # Invalid characters, treat as empty.
        return ""
    return host
def get_current_url(
    scheme: str,
    host: str,
    root_path: str | None = None,
    path: str | None = None,
    query_string: bytes | None = None,
) -> str:
    """Recreate the URL for a request. If an optional part isn't
    provided, it and subsequent parts are not included in the URL.
    The URL is an IRI, not a URI, so it may contain Unicode characters.
    Use :func:`~werkzeug.urls.iri_to_uri` to convert it to ASCII.
    :param scheme: The protocol the request used, like ``"https"``.
    :param host: The host the request was made to. See :func:`get_host`.
    :param root_path: Prefix that the application is mounted under. This
        is prepended to ``path``.
    :param path: The path part of the URL after ``root_path``.
    :param query_string: The portion of the URL after the "?".
    """
    url = [scheme, "://", host]
    if root_path is None:
        url.append("/")
        return uri_to_iri("".join(url))
    # safe = https://url.spec.whatwg.org/#url-path-segment-string
    # as well as percent for things that are already quoted
    url.append(quote(root_path.rstrip("/"), safe="!$&'()*+,/:;=@%"))
    url.append("/")
    if path is None:
        return uri_to_iri("".join(url))
    url.append(quote(path.lstrip("/"), safe="!$&'()*+,/:;=@%"))
    if query_string:
        url.append("?")
        url.append(quote(query_string, safe="!$&'()*+,/:;=?@%"))
    return uri_to_iri("".join(url))
def get_content_length(
    http_content_length: str | None = None,
    http_transfer_encoding: str | None = None,
) -> int | None:
    """Return the ``Content-Length`` header value as an int. If the header is not given
    or the ``Transfer-Encoding`` header is ``chunked``, ``None`` is returned to indicate
    a streaming request. If the value is not an integer, or negative, 0 is returned.
    :param http_content_length: The Content-Length HTTP header.
    :param http_transfer_encoding: The Transfer-Encoding HTTP header.
    .. versionadded:: 2.2
    """
    if (
        http_transfer_encoding is not None
        and "chunked" in parse_set_header(http_transfer_encoding)
    ) or http_content_length is None:
        return None
    try:
        return max(0, _plain_int(http_content_length))
    except ValueError:
        return 0
