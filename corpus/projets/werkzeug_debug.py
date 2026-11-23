# Corpus « temoin » — sous-paquet debug de pallets/werkzeug, lignes non vides.
# Licence BSD-3-Clause. Trois sous-paquets du MEME projet : si l ecart de la
# condition B venait de « fichiers entiers contre lignes concatenees », C monterait aussi.
from __future__ import annotations
import getpass
import hashlib
import json
import os
import pkgutil
import re
import sys
import time
import typing as t
import uuid
from contextlib import ExitStack
from io import BytesIO
from itertools import chain
from multiprocessing import Value
from os.path import basename
from os.path import join
from zlib import adler32
from .._internal import _log
from ..exceptions import NotFound
from ..exceptions import SecurityError
from ..http import parse_cookie
from ..sansio.utils import host_is_trusted
from ..security import gen_salt
from ..utils import send_file
from ..wrappers.request import Request
from ..wrappers.response import Response
from .console import Console
from .tbtools import DebugFrameSummary
from .tbtools import DebugTraceback
from .tbtools import render_console_html
if t.TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment
# A week
PIN_TIME = 60 * 60 * 24 * 7
def hash_pin(pin: str) -> str:
    return hashlib.sha1(f"{pin} added salt".encode("utf-8", "replace")).hexdigest()[:12]
_machine_id: str | bytes | None = None
def get_machine_id() -> str | bytes | None:
    global _machine_id
    if _machine_id is not None:
        return _machine_id
    def _generate() -> str | bytes | None:
        linux = b""
        # machine-id is stable across boots, boot_id is not.
        for filename in "/etc/machine-id", "/proc/sys/kernel/random/boot_id":
            try:
                with open(filename, "rb") as f:
                    value = f.readline().strip()
            except OSError:
                continue
            if value:
                linux += value
                break
        # Containers share the same machine id, add some cgroup
        # information. This is used outside containers too but should be
        # relatively stable across boots.
        try:
            with open("/proc/self/cgroup", "rb") as f:
                linux += f.readline().strip().rpartition(b"/")[2]
        except OSError:
            pass
        if linux:
            return linux
        # On OS X, use ioreg to get the computer's serial number.
        try:
            # subprocess may not be available, e.g. Google App Engine
            # https://github.com/pallets/werkzeug/issues/925
            from subprocess import PIPE
            from subprocess import Popen
            dump = Popen(
                ["ioreg", "-c", "IOPlatformExpertDevice", "-d", "2"], stdout=PIPE
            ).communicate()[0]
            match = re.search(b'"serial-number" = <([^>]+)', dump)
            if match is not None:
                return match.group(1)
        except (OSError, ImportError):
            pass
        # On Windows, use winreg to get the machine guid.
        if sys.platform == "win32":
            import winreg
            try:
                with winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Microsoft\\Cryptography",
                    0,
                    winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
                ) as rk:
                    guid: str | bytes
                    guid_type: int
                    guid, guid_type = winreg.QueryValueEx(rk, "MachineGuid")
                    if guid_type == winreg.REG_SZ:
                        return guid.encode()
                    return guid
            except OSError:
                pass
        return None
    _machine_id = _generate()
    return _machine_id
class _ConsoleFrame:
    """Helper class so that we can reuse the frame console code for the
    standalone console.
    """
    def __init__(self, namespace: dict[str, t.Any]):
        self.console = Console(namespace)
        self.id = 0
    def eval(self, code: str) -> t.Any:
        return self.console.eval(code)
def get_pin_and_cookie_name(
    app: WSGIApplication,
) -> tuple[str, str] | tuple[None, None]:
    """Given an application object this returns a semi-stable 9 digit pin
    code and a random key.  The hope is that this is stable between
    restarts to not make debugging particularly frustrating.  If the pin
    was forcefully disabled this returns `None`.
    Second item in the resulting tuple is the cookie name for remembering.
    """
    pin = os.environ.get("WERKZEUG_DEBUG_PIN")
    rv = None
    num = None
    # Pin was explicitly disabled
    if pin == "off":
        return None, None
    # Pin was provided explicitly
    if pin is not None and pin.replace("-", "").isdecimal():
        # If there are separators in the pin, return it directly
        if "-" in pin:
            rv = pin
        else:
            num = pin
    modname = getattr(app, "__module__", t.cast(object, app).__class__.__module__)
    username: str | None
    try:
        # getuser imports the pwd module, which does not exist in Google
        # App Engine. It may also raise a KeyError if the UID does not
        # have a username, such as in Docker.
        username = getpass.getuser()
    # Python >= 3.13 only raises OSError
    except (ImportError, KeyError, OSError):
        username = None
    mod = sys.modules.get(modname)
    # This information only exists to make the cookie unique on the
    # computer, not as a security feature.
    probably_public_bits = [
        username,
        modname,
        getattr(app, "__name__", type(app).__name__),
        getattr(mod, "__file__", None),
    ]
    # This information is here to make it harder for an attacker to
    # guess the cookie name.  They are unlikely to be contained anywhere
    # within the unauthenticated debug page.
    private_bits = [str(uuid.getnode()), get_machine_id()]
    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode()
        h.update(bit)
    h.update(b"cookiesalt")
    cookie_name = f"__wzd{h.hexdigest()[:20]}"
    # If we need to generate a pin we salt it a bit more so that we don't
    # end up with the same value and generate out 9 digits
    if num is None:
        h.update(b"pinsalt")
        num = f"{int(h.hexdigest(), 16):09d}"[:9]
    # Format the pincode in groups of digits for easier remembering if
    # we don't have a result yet.
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x : x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num
    return rv, cookie_name
class DebuggedApplication:
    """Enables debugging support for a given application::
        from werkzeug.debug import DebuggedApplication
        from myapp import app
        app = DebuggedApplication(app, evalex=True)
    The ``evalex`` argument allows evaluating expressions in any frame
    of a traceback. This works by preserving each frame with its local
    state. Some state, such as context globals, cannot be restored with
    the frame by default. When ``evalex`` is enabled,
    ``environ["werkzeug.debug.preserve_context"]`` will be a callable
    that takes a context manager, and can be called multiple times.
    Each context manager will be entered before evaluating code in the
    frame, then exited again, so they can perform setup and cleanup for
    each call.
    :param app: the WSGI application to run debugged.
    :param evalex: enable exception evaluation feature (interactive
                   debugging).  This requires a non-forking server.
    :param request_key: The key that points to the request object in this
                        environment.  This parameter is ignored in current
                        versions.
    :param console_path: the URL for a general purpose console.
    :param console_init_func: the function that is executed before starting
                              the general purpose console.  The return value
                              is used as initial namespace.
    :param show_hidden_frames: by default hidden traceback frames are skipped.
                               You can show them by setting this parameter
                               to `True`.
    :param pin_security: can be used to disable the pin based security system.
    :param pin_logging: enables the logging of the pin system.
    .. versionchanged:: 2.2
        Added the ``werkzeug.debug.preserve_context`` environ key.
    """
    _pin: str | None
    _pin_cookie: str
    def __init__(
        self,
        app: WSGIApplication,
        evalex: bool = False,
        request_key: str = "werkzeug.request",
        console_path: str = "/console",
        console_init_func: t.Callable[[], dict[str, t.Any]] | None = None,
        show_hidden_frames: bool = False,
        pin_security: bool = True,
        pin_logging: bool = True,
    ) -> None:
        if not console_init_func:
            console_init_func = None
        self.app = app
        self.evalex = evalex
        self.frames: dict[int, DebugFrameSummary | _ConsoleFrame] = {}
        self.frame_contexts: dict[int, list[t.ContextManager[None]]] = {}
        self.request_key = request_key
        self.console_path = console_path
        self.console_init_func = console_init_func
        self.show_hidden_frames = show_hidden_frames
        self.secret = gen_salt(20)
        self._failed_pin_auth = Value("B")
        self.pin_logging = pin_logging
        if pin_security:
            # Print out the pin for the debugger on standard out.
            if os.environ.get("WERKZEUG_RUN_MAIN") == "true" and pin_logging:
                _log("warning", " * Debugger is active!")
                if self.pin is None:
                    _log("warning", " * Debugger PIN disabled. DEBUGGER UNSECURED!")
                else:
                    _log("info", " * Debugger PIN: %s", self.pin)
        else:
            self.pin = None
        self.trusted_hosts: list[str] = [".localhost", "127.0.0.1"]
        """List of domains to allow requests to the debugger from. A leading dot
        allows all subdomains. This only allows ``".localhost"`` domains by
        default.
        .. versionadded:: 3.0.3
        """
    @property
    def pin(self) -> str | None:
        if not hasattr(self, "_pin"):
            pin_cookie = get_pin_and_cookie_name(self.app)
            self._pin, self._pin_cookie = pin_cookie  # type: ignore
        return self._pin
    @pin.setter
    def pin(self, value: str | None) -> None:
        if value is None:
            # Set _pin to None explicitly to prevent regeneration by the getter
            self._pin = None
        else:
            self._pin = value
    @property
    def pin_cookie_name(self) -> str:
        """The name of the pin cookie."""
        if not hasattr(self, "_pin_cookie"):
            pin_cookie = get_pin_and_cookie_name(self.app)
            self._pin, self._pin_cookie = pin_cookie  # type: ignore
        return self._pin_cookie
    def debug_application(
        self, environ: WSGIEnvironment, start_response: StartResponse
    ) -> t.Iterator[bytes]:
        """Run the application and conserve the traceback frames."""
        contexts: list[t.ContextManager[t.Any]] = []
        if self.evalex:
            environ["werkzeug.debug.preserve_context"] = contexts.append
        app_iter = None
        try:
            app_iter = self.app(environ, start_response)
            yield from app_iter
            if hasattr(app_iter, "close"):
                app_iter.close()
        except Exception as e:
            if hasattr(app_iter, "close"):
                app_iter.close()  # type: ignore
            tb = DebugTraceback(e, skip=1, hide=not self.show_hidden_frames)
            for frame in tb.all_frames:
                self.frames[id(frame)] = frame
                self.frame_contexts[id(frame)] = contexts
            is_trusted = bool(self.check_pin_trust(environ))
            html = tb.render_debugger_html(
                evalex=self.evalex and self.check_host_trust(environ),
                secret=self.secret,
                evalex_trusted=is_trusted,
            )
            response = Response(html, status=500, mimetype="text/html")
            try:
                yield from response(environ, start_response)
            except Exception:
                # if we end up here there has been output but an error
                # occurred.  in that situation we can do nothing fancy any
                # more, better log something into the error log and fall
                # back gracefully.
                environ["wsgi.errors"].write(
                    "Debugging middleware caught exception in streamed "
                    "response at a point where response headers were already "
                    "sent.\n"
                )
            environ["wsgi.errors"].write("".join(tb.render_traceback_text()))
    def execute_command(
        self,
        request: Request,
        command: str,
        frame: DebugFrameSummary | _ConsoleFrame,
    ) -> Response:
        """Execute a command in a console."""
        if not self.check_host_trust(request.environ):
            return SecurityError()  # type: ignore[return-value]
        contexts = self.frame_contexts.get(id(frame), [])
        with ExitStack() as exit_stack:
            for cm in contexts:
                exit_stack.enter_context(cm)
            return Response(frame.eval(command), mimetype="text/html")
    def display_console(self, request: Request) -> Response:
        """Display a standalone shell."""
        if not self.check_host_trust(request.environ):
            return SecurityError()  # type: ignore[return-value]
        if 0 not in self.frames:
            if self.console_init_func is None:
                ns = {}
            else:
                ns = dict(self.console_init_func())
            ns.setdefault("app", self.app)
            self.frames[0] = _ConsoleFrame(ns)
        is_trusted = bool(self.check_pin_trust(request.environ))
        return Response(
            render_console_html(secret=self.secret, evalex_trusted=is_trusted),
            mimetype="text/html",
        )
    def get_resource(self, request: Request, filename: str) -> Response:
        """Return a static resource from the shared folder."""
        path = join("shared", basename(filename))
        try:
            data = pkgutil.get_data(__package__, path)
        except OSError:
            return NotFound()  # type: ignore[return-value]
        else:
            if data is None:
                return NotFound()  # type: ignore[return-value]
            etag = str(adler32(data) & 0xFFFFFFFF)
            return send_file(
                BytesIO(data), request.environ, download_name=filename, etag=etag
            )
    def check_pin_trust(self, environ: WSGIEnvironment) -> bool | None:
        """Checks if the request passed the pin test.  This returns `True` if the
        request is trusted on a pin/cookie basis and returns `False` if not.
        Additionally if the cookie's stored pin hash is wrong it will return
        `None` so that appropriate action can be taken.
        """
        if self.pin is None:
            return True
        # If we failed too many times, then we're locked out.
        if self._failed_pin_auth.value >= 10:
            return False
        val = parse_cookie(environ).get(self.pin_cookie_name)
        if not val or "|" not in val:
            return False
        ts_str, pin_hash = val.split("|", 1)
        try:
            ts = int(ts_str)
        except ValueError:
            return False
        if pin_hash != hash_pin(self.pin):
            return None
        return (time.time() - PIN_TIME) < ts
    def check_host_trust(self, environ: WSGIEnvironment) -> bool:
        return host_is_trusted(environ.get("HTTP_HOST"), self.trusted_hosts)
    def _fail_pin_auth(self) -> None:
        with self._failed_pin_auth.get_lock():
            count = self._failed_pin_auth.value
            self._failed_pin_auth.value = count + 1
        time.sleep(5.0 if count > 5 else 0.5)
    def pin_auth(self, request: Request) -> Response:
        """Authenticates with the pin."""
        if not self.check_host_trust(request.environ):
            return SecurityError()  # type: ignore[return-value]
        exhausted = False
        auth = False
        trust = self.check_pin_trust(request.environ)
        pin = t.cast(str, self.pin)
        # If the trust return value is `None` it means that the cookie is
        # set but the stored pin hash value is bad.  This means that the
        # pin was changed.  In this case we count a bad auth and unset the
        # cookie.  This way it becomes harder to guess the cookie name
        # instead of the pin as we still count up failures.
        bad_cookie = False
        if trust is None:
            self._fail_pin_auth()
            bad_cookie = True
        # If we're trusted, we're authenticated.
        elif trust:
            auth = True
        # If we failed too many times, then we're locked out.
        elif self._failed_pin_auth.value >= 10:
            exhausted = True
        # Otherwise go through pin based authentication
        else:
            entered_pin = request.args["pin"]
            if entered_pin.strip().replace("-", "") == pin.replace("-", ""):
                self._failed_pin_auth.value = 0
                auth = True
            else:
                self._fail_pin_auth()
        rv = Response(
            json.dumps({"auth": auth, "exhausted": exhausted}),
            mimetype="application/json",
        )
        if auth:
            rv.set_cookie(
                self.pin_cookie_name,
                f"{int(time.time())}|{hash_pin(pin)}",
                httponly=True,
                samesite="Strict",
                secure=request.is_secure,
            )
        elif bad_cookie:
            rv.delete_cookie(self.pin_cookie_name)
        return rv
    def log_pin_request(self, request: Request) -> Response:
        """Log the pin if needed."""
        if not self.check_host_trust(request.environ):
            return SecurityError()  # type: ignore[return-value]
        if self.pin_logging and self.pin is not None:
            _log(
                "info", " * To enable the debugger you need to enter the security pin:"
            )
            _log("info", " * Debugger pin code: %s", self.pin)
        return Response("")
    def __call__(
        self, environ: WSGIEnvironment, start_response: StartResponse
    ) -> t.Iterable[bytes]:
        """Dispatch the requests."""
        # important: don't ever access a function here that reads the incoming
        # form data!  Otherwise the application won't have access to that data
        # any more!
        request = Request(environ)
        response = self.debug_application
        if request.args.get("__debugger__") == "yes":
            cmd = request.args.get("cmd")
            arg = request.args.get("f")
            secret = request.args.get("s")
            frame = self.frames.get(request.args.get("frm", type=int))  # type: ignore
            if cmd == "resource" and arg:
                response = self.get_resource(request, arg)  # type: ignore
            elif cmd == "pinauth" and secret == self.secret:
                response = self.pin_auth(request)  # type: ignore
            elif cmd == "printpin" and secret == self.secret:
                response = self.log_pin_request(request)  # type: ignore
            elif (
                self.evalex
                and cmd is not None
                and frame is not None
                and self.secret == secret
                and self.check_pin_trust(environ)
            ):
                response = self.execute_command(request, cmd, frame)  # type: ignore
        elif (
            self.evalex
            and self.console_path is not None
            and request.path == self.console_path
        ):
            response = self.display_console(request)  # type: ignore
        return response(environ, start_response)
from __future__ import annotations
import code
import sys
import typing as t
from contextvars import ContextVar
from types import CodeType
from markupsafe import escape
from .repr import debug_repr
from .repr import dump
from .repr import helper
_stream: ContextVar[HTMLStringO] = ContextVar("werkzeug.debug.console.stream")
_ipy: ContextVar[_InteractiveConsole] = ContextVar("werkzeug.debug.console.ipy")
class HTMLStringO:
    """A StringO version that HTML escapes on write."""
    def __init__(self) -> None:
        self._buffer: list[str] = []
    def isatty(self) -> bool:
        return False
    def close(self) -> None:
        pass
    def flush(self) -> None:
        pass
    def seek(self, n: int, mode: int = 0) -> None:
        pass
    def readline(self) -> str:
        if len(self._buffer) == 0:
            return ""
        ret = self._buffer[0]
        del self._buffer[0]
        return ret
    def reset(self) -> str:
        val = "".join(self._buffer)
        del self._buffer[:]
        return val
    def _write(self, x: str) -> None:
        self._buffer.append(x)
    def write(self, x: str) -> None:
        self._write(escape(x))
    def writelines(self, x: t.Iterable[str]) -> None:
        self._write(escape("".join(x)))
class ThreadedStream:
    """Thread-local wrapper for sys.stdout for the interactive console."""
    @staticmethod
    def push() -> None:
        if not isinstance(sys.stdout, ThreadedStream):
            sys.stdout = t.cast(t.TextIO, ThreadedStream())
        _stream.set(HTMLStringO())
    @staticmethod
    def fetch() -> str:
        try:
            stream = _stream.get()
        except LookupError:
            return ""
        return stream.reset()
    @staticmethod
    def displayhook(obj: object) -> None:
        try:
            stream = _stream.get()
        except LookupError:
            return _displayhook(obj)  # type: ignore
        # stream._write bypasses escaping as debug_repr is
        # already generating HTML for us.
        if obj is not None:
            _ipy.get().locals["_"] = obj
            stream._write(debug_repr(obj))
    def __setattr__(self, name: str, value: t.Any) -> None:
        raise AttributeError(f"read only attribute {name}")
    def __dir__(self) -> list[str]:
        return dir(sys.__stdout__)
    def __getattribute__(self, name: str) -> t.Any:
        try:
            stream = _stream.get()
        except LookupError:
            stream = sys.__stdout__  # type: ignore[assignment]
        return getattr(stream, name)
    def __repr__(self) -> str:
        return repr(sys.__stdout__)
# add the threaded stream as display hook
_displayhook = sys.displayhook
sys.displayhook = ThreadedStream.displayhook
class _ConsoleLoader:
    def __init__(self) -> None:
        self._storage: dict[int, str] = {}
    def register(self, code: CodeType, source: str) -> None:
        self._storage[id(code)] = source
        # register code objects of wrapped functions too.
        for var in code.co_consts:
            if isinstance(var, CodeType):
                self._storage[id(var)] = source
    def get_source_by_code(self, code: CodeType) -> str | None:
        try:
            return self._storage[id(code)]
        except KeyError:
            return None
class _InteractiveConsole(code.InteractiveInterpreter):
    locals: dict[str, t.Any]
    def __init__(self, globals: dict[str, t.Any], locals: dict[str, t.Any]) -> None:
        self.loader = _ConsoleLoader()
        locals = {
            **globals,
            **locals,
            "dump": dump,
            "help": helper,
            "__loader__": self.loader,
        }
        super().__init__(locals)
        original_compile = self.compile
        def compile(source: str, filename: str, symbol: str) -> CodeType | None:
            code = original_compile(source, filename, symbol)
            if code is not None:
                self.loader.register(code, source)
            return code
        self.compile = compile  # type: ignore[assignment]
        self.more = False
        self.buffer: list[str] = []
    def runsource(self, source: str, **kwargs: t.Any) -> str:  # type: ignore
        source = f"{source.rstrip()}\n"
        ThreadedStream.push()
        prompt = "... " if self.more else ">>> "
        try:
            source_to_eval = "".join(self.buffer + [source])
            if super().runsource(source_to_eval, "<debugger>", "single"):
                self.more = True
                self.buffer.append(source)
            else:
                self.more = False
                del self.buffer[:]
        finally:
            output = ThreadedStream.fetch()
        return f"{prompt}{escape(source)}{output}"
    def runcode(self, code: CodeType) -> None:
        try:
            exec(code, self.locals)
        except Exception:
            self.showtraceback()
    def showtraceback(self) -> None:
        from .tbtools import DebugTraceback
        exc = t.cast(BaseException, sys.exc_info()[1])
        te = DebugTraceback(exc, skip=1)
        sys.stdout._write(te.render_traceback_html())  # type: ignore
    def showsyntaxerror(self, filename: str | None = None) -> None:
        from .tbtools import DebugTraceback
        exc = t.cast(BaseException, sys.exc_info()[1])
        te = DebugTraceback(exc, skip=4)
        sys.stdout._write(te.render_traceback_html())  # type: ignore
    def write(self, data: str) -> None:
        sys.stdout.write(data)
class Console:
    """An interactive console."""
    def __init__(
        self,
        globals: dict[str, t.Any] | None = None,
        locals: dict[str, t.Any] | None = None,
    ) -> None:
        if locals is None:
            locals = {}
        if globals is None:
            globals = {}
        self._ipy = _InteractiveConsole(globals, locals)
    def eval(self, code: str) -> str:
        _ipy.set(self._ipy)
        old_sys_stdout = sys.stdout
        try:
            return self._ipy.runsource(code)
        finally:
            sys.stdout = old_sys_stdout
"""Object representations for debugging purposes. Unlike the default
repr, these expose more information and produce HTML instead of ASCII.
Together with the CSS and JavaScript of the debugger this gives a
colorful and more compact output.
"""
from __future__ import annotations
import codecs
import re
import sys
import typing as t
from collections import deque
from traceback import format_exception_only
from markupsafe import escape
missing = object()
_paragraph_re = re.compile(r"(?:\r\n|\r|\n){2,}")
RegexType = type(_paragraph_re)
HELP_HTML = """\
<div class=box>
  <h3>%(title)s</h3>
  <pre class=help>%(text)s</pre>
</div>\
"""
OBJECT_DUMP_HTML = """\
<div class=box>
  <h3>%(title)s</h3>
  %(repr)s
  <table>%(items)s</table>
</div>\
"""
def debug_repr(obj: object) -> str:
    """Creates a debug repr of an object as HTML string."""
    return DebugReprGenerator().repr(obj)
def dump(obj: object = missing) -> None:
    """Print the object details to stdout._write (for the interactive
    console of the web debugger.
    """
    gen = DebugReprGenerator()
    if obj is missing:
        rv = gen.dump_locals(sys._getframe(1).f_locals)
    else:
        rv = gen.dump_object(obj)
    sys.stdout._write(rv)  # type: ignore
class _Helper:
    """Displays an HTML version of the normal help, for the interactive
    debugger only because it requires a patched sys.stdout.
    """
    def __repr__(self) -> str:
        return "Type help(object) for help about object."
    def __call__(self, topic: t.Any | None = None) -> None:
        if topic is None:
            sys.stdout._write(f"<span class=help>{self!r}</span>")  # type: ignore
            return
        import pydoc
        pydoc.help(topic)
        rv = sys.stdout.reset()  # type: ignore
        paragraphs = _paragraph_re.split(rv)
        if len(paragraphs) > 1:
            title = paragraphs[0]
            text = "\n\n".join(paragraphs[1:])
        else:
            title = "Help"
            text = paragraphs[0]
        sys.stdout._write(HELP_HTML % {"title": title, "text": text})  # type: ignore
helper = _Helper()
def _add_subclass_info(inner: str, obj: object, base: type | tuple[type, ...]) -> str:
    if isinstance(base, tuple):
        for cls in base:
            if type(obj) is cls:
                return inner
    elif type(obj) is base:
        return inner
    module = ""
    if obj.__class__.__module__ not in ("__builtin__", "exceptions"):
        module = f'<span class="module">{obj.__class__.__module__}.</span>'
    return f"{module}{type(obj).__name__}({inner})"
def _sequence_repr_maker(
    left: str, right: str, base: type, limit: int = 8
) -> t.Callable[[DebugReprGenerator, t.Iterable[t.Any], bool], str]:
    def proxy(self: DebugReprGenerator, obj: t.Iterable[t.Any], recursive: bool) -> str:
        if recursive:
            return _add_subclass_info(f"{left}...{right}", obj, base)
        buf = [left]
        have_extended_section = False
        for idx, item in enumerate(obj):
            if idx:
                buf.append(", ")
            if idx == limit:
                buf.append('<span class="extended">')
                have_extended_section = True
            buf.append(self.repr(item))
        if have_extended_section:
            buf.append("</span>")
        buf.append(right)
        return _add_subclass_info("".join(buf), obj, base)
    return proxy
class DebugReprGenerator:
    def __init__(self) -> None:
        self._stack: list[t.Any] = []
    list_repr = _sequence_repr_maker("[", "]", list)
    tuple_repr = _sequence_repr_maker("(", ")", tuple)
    set_repr = _sequence_repr_maker("set([", "])", set)
    frozenset_repr = _sequence_repr_maker("frozenset([", "])", frozenset)
    deque_repr = _sequence_repr_maker(
        '<span class="module">collections.</span>deque([', "])", deque
    )
    def regex_repr(self, obj: t.Pattern[t.AnyStr]) -> str:
        pattern = repr(obj.pattern)
        pattern = codecs.decode(pattern, "unicode-escape", "ignore")
        pattern = f"r{pattern}"
        return f're.compile(<span class="string regex">{pattern}</span>)'
    def string_repr(self, obj: str | bytes, limit: int = 70) -> str:
        buf = ['<span class="string">']
        r = repr(obj)
        # shorten the repr when the hidden part would be at least 3 chars
        if len(r) - limit > 2:
            buf.extend(
                (
                    escape(r[:limit]),
                    '<span class="extended">',
                    escape(r[limit:]),
                    "</span>",
                )
            )
        else:
            buf.append(escape(r))
        buf.append("</span>")
        out = "".join(buf)
        # if the repr looks like a standard string, add subclass info if needed
        if r[0] in "'\"" or (r[0] == "b" and r[1] in "'\""):
            return _add_subclass_info(out, obj, (bytes, str))
        # otherwise, assume the repr distinguishes the subclass already
        return out
    def dict_repr(
        self,
        d: dict[int, None] | dict[str, int] | dict[str | int, int],
        recursive: bool,
        limit: int = 5,
    ) -> str:
        if recursive:
            return _add_subclass_info("{...}", d, dict)
        buf = ["{"]
        have_extended_section = False
        for idx, (key, value) in enumerate(d.items()):
            if idx:
                buf.append(", ")
            if idx == limit - 1:
                buf.append('<span class="extended">')
                have_extended_section = True
            buf.append(
                f'<span class="pair"><span class="key">{self.repr(key)}</span>:'
                f' <span class="value">{self.repr(value)}</span></span>'
            )
        if have_extended_section:
            buf.append("</span>")
        buf.append("}")
        return _add_subclass_info("".join(buf), d, dict)
    def object_repr(self, obj: t.Any) -> str:
        r = repr(obj)
        return f'<span class="object">{escape(r)}</span>'
    def dispatch_repr(self, obj: t.Any, recursive: bool) -> str:
        if obj is helper:
            return f'<span class="help">{helper!r}</span>'
        if isinstance(obj, (int, float, complex)):
            return f'<span class="number">{obj!r}</span>'
        if isinstance(obj, str) or isinstance(obj, bytes):
            return self.string_repr(obj)
        if isinstance(obj, RegexType):
            return self.regex_repr(obj)
        if isinstance(obj, list):
            return self.list_repr(obj, recursive)
        if isinstance(obj, tuple):
            return self.tuple_repr(obj, recursive)
        if isinstance(obj, set):
            return self.set_repr(obj, recursive)
        if isinstance(obj, frozenset):
            return self.frozenset_repr(obj, recursive)
        if isinstance(obj, dict):
            return self.dict_repr(obj, recursive)
        if isinstance(obj, deque):
            return self.deque_repr(obj, recursive)
        return self.object_repr(obj)
    def fallback_repr(self) -> str:
        try:
            info = "".join(format_exception_only(*sys.exc_info()[:2]))
        except Exception:
            info = "?"
        return (
            '<span class="brokenrepr">'
            f"&lt;broken repr ({escape(info.strip())})&gt;</span>"
        )
    def repr(self, obj: object) -> str:
        recursive = False
        for item in self._stack:
            if item is obj:
                recursive = True
                break
        self._stack.append(obj)
        try:
            try:
                return self.dispatch_repr(obj, recursive)
            except Exception:
                return self.fallback_repr()
        finally:
            self._stack.pop()
    def dump_object(self, obj: object) -> str:
        repr = None
        items: list[tuple[str, str]] | None = None
        if isinstance(obj, dict):
            title = "Contents of"
            items = []
            for key, value in obj.items():
                if not isinstance(key, str):
                    items = None
                    break
                items.append((key, self.repr(value)))
        if items is None:
            items = []
            repr = self.repr(obj)
            for key in dir(obj):
                try:
                    items.append((key, self.repr(getattr(obj, key))))
                except Exception:
                    pass
            title = "Details for"
        title += f" {object.__repr__(obj)[1:-1]}"
        return self.render_object_dump(items, title, repr)
    def dump_locals(self, d: dict[str, t.Any]) -> str:
        items = [(key, self.repr(value)) for key, value in d.items()]
        return self.render_object_dump(items, "Local variables in frame")
    def render_object_dump(
        self, items: list[tuple[str, str]], title: str, repr: str | None = None
    ) -> str:
        html_items = []
        for key, value in items:
            html_items.append(f"<tr><th>{escape(key)}<td><pre class=repr>{value}</pre>")
        if not html_items:
            html_items.append("<tr><td><em>Nothing</em>")
        return OBJECT_DUMP_HTML % {
            "title": escape(title),
            "repr": f"<pre class=repr>{repr if repr else ''}</pre>",
            "items": "\n".join(html_items),
        }
from __future__ import annotations
import itertools
import linecache
import os
import re
import sys
import sysconfig
import traceback
import typing as t
from markupsafe import escape
from ..utils import cached_property
from .console import Console
HEADER = """\
<!doctype html>
<html lang=en>
  <head>
    <title>%(title)s // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css">
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script>
      var CONSOLE_MODE = %(console)s,
          EVALEX = %(evalex)s,
          EVALEX_TRUSTED = %(evalex_trusted)s,
          SECRET = "%(secret)s";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
"""
FOOTER = """\
      <div class="footer">
        Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
        friendly Werkzeug powered traceback interpreter.
      </div>
    </div>
    <div class="pin-prompt">
      <div class="inner">
        <h3>Console Locked</h3>
        <p>
          The console is locked and needs to be unlocked by entering the PIN.
          You can find the PIN printed out on the standard output of your
          shell that runs the server.
        <form>
          <p>PIN:
            <input type=text name=pin size=14>
            <input type=submit name=btn value="Confirm Pin">
        </form>
      </div>
    </div>
  </body>
</html>
"""
PAGE_HTML = (
    HEADER
    + """\
<h1>%(exception_type)s</h1>
<div class="detail">
  <p class="errormsg">%(exception)s</p>
</div>
<h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
%(summary)s
<div class="plain">
    <p>
      This is the Copy/Paste friendly version of the traceback.
    </p>
    <textarea cols="50" rows="10" name="code" readonly>%(plaintext)s</textarea>
</div>
<div class="explanation">
  The debugger caught an exception in your WSGI application.  You can now
  look at the traceback which led to the error.  <span class="nojavascript">
  If you enable JavaScript you can also use additional features such as code
  execution (if the evalex feature is enabled), automatic pasting of the
  exceptions and much more.</span>
</div>
"""
    + FOOTER
    + """
<!--
%(plaintext_cs)s
-->
"""
)
CONSOLE_HTML = (
    HEADER
    + """\
<h1>Interactive Console</h1>
<div class="explanation">
In this console you can execute Python expressions in the context of the
application.  The initial namespace was created by the debugger automatically.
</div>
<div class="console"><div class="inner">The Console requires JavaScript.</div></div>
"""
    + FOOTER
)
SUMMARY_HTML = """\
<div class="%(classes)s">
  %(title)s
  <ul>%(frames)s</ul>
  %(description)s
</div>
"""
FRAME_HTML = """\
<div class="frame" id="frame-%(id)d">
  <h4>File <cite class="filename">"%(filename)s"</cite>,
      line <em class="line">%(lineno)s</em>,
      in <code class="function">%(function_name)s</code></h4>
  <div class="source %(library)s">%(lines)s</div>
</div>
"""
def _process_traceback(
    exc: BaseException,
    te: traceback.TracebackException | None = None,
    *,
    skip: int = 0,
    hide: bool = True,
) -> traceback.TracebackException:
    if te is None:
        te = traceback.TracebackException.from_exception(exc, lookup_lines=False)
    # Get the frames the same way StackSummary.extract did, in order
    # to match each frame with the FrameSummary to augment.
    frame_gen = traceback.walk_tb(exc.__traceback__)
    limit = getattr(sys, "tracebacklimit", None)
    if limit is not None:
        if limit < 0:
            limit = 0
        frame_gen = itertools.islice(frame_gen, limit)
    if skip:
        frame_gen = itertools.islice(frame_gen, skip, None)
        del te.stack[:skip]
    new_stack: list[DebugFrameSummary] = []
    hidden = False
    # Match each frame with the FrameSummary that was generated.
    # Hide frames using Paste's __traceback_hide__ rules. Replace
    # all visible FrameSummary with DebugFrameSummary.
    for (f, _), fs in zip(frame_gen, te.stack):
        if hide:
            hide_value = f.f_locals.get("__traceback_hide__", False)
            if hide_value in {"before", "before_and_this"}:
                new_stack = []
                hidden = False
                if hide_value == "before_and_this":
                    continue
            elif hide_value in {"reset", "reset_and_this"}:
                hidden = False
                if hide_value == "reset_and_this":
                    continue
            elif hide_value in {"after", "after_and_this"}:
                hidden = True
                if hide_value == "after_and_this":
                    continue
            elif hide_value or hidden:
                continue
        frame_args: dict[str, t.Any] = {
            "filename": fs.filename,
            "lineno": fs.lineno,
            "name": fs.name,
            "locals": f.f_locals,
            "globals": f.f_globals,
        }
        if sys.version_info >= (3, 11):
            frame_args["colno"] = fs.colno
            frame_args["end_colno"] = fs.end_colno
        new_stack.append(DebugFrameSummary(**frame_args))
    # The codeop module is used to compile code from the interactive
    # debugger. Hide any codeop frames from the bottom of the traceback.
    while new_stack:
        module = new_stack[0].global_ns.get("__name__")
        if module is None:
            module = new_stack[0].local_ns.get("__name__")
        if module == "codeop":
            del new_stack[0]
        else:
            break
    te.stack[:] = new_stack
    if te.__context__:
        context_exc = t.cast(BaseException, exc.__context__)
        te.__context__ = _process_traceback(context_exc, te.__context__, hide=hide)
    if te.__cause__:
        cause_exc = t.cast(BaseException, exc.__cause__)
        te.__cause__ = _process_traceback(cause_exc, te.__cause__, hide=hide)
    return te
class DebugTraceback:
    __slots__ = ("_te", "_cache_all_tracebacks", "_cache_all_frames")
    def __init__(
        self,
        exc: BaseException,
        te: traceback.TracebackException | None = None,
        *,
        skip: int = 0,
        hide: bool = True,
    ) -> None:
        self._te = _process_traceback(exc, te, skip=skip, hide=hide)
    def __str__(self) -> str:
        return f"<{type(self).__name__} {self._te}>"
    @cached_property
    def all_tracebacks(
        self,
    ) -> list[tuple[str | None, traceback.TracebackException]]:
        out: list[tuple[str | None, traceback.TracebackException]] = []
        current: traceback.TracebackException | None = self._te
        while current is not None:
            if current.__cause__ is not None:
                chained_msg = (
                    "The above exception was the direct cause of the"
                    " following exception"
                )
                chained_exc = current.__cause__
            elif current.__context__ is not None and not current.__suppress_context__:
                chained_msg = (
                    "During handling of the above exception, another exception occurred"
                )
                chained_exc = current.__context__
            else:
                chained_msg = None
                chained_exc = None
            out.append((chained_msg, current))
            current = chained_exc
        return out
    @cached_property
    def all_frames(self) -> list[DebugFrameSummary]:
        return [
            f  # type: ignore[misc]
            for _, te in self.all_tracebacks
            for f in te.stack
        ]
    def render_traceback_text(self) -> str:
        return "".join(self._te.format())
    def render_traceback_html(self, include_title: bool = True) -> str:
        library_frames = [f.is_library for f in self.all_frames]
        mark_library = 0 < sum(library_frames) < len(library_frames)
        rows = []
        if not library_frames:
            classes = "traceback noframe-traceback"
        else:
            classes = "traceback"
            for msg, current in reversed(self.all_tracebacks):
                row_parts = []
                if msg is not None:
                    row_parts.append(f'<li><div class="exc-divider">{msg}:</div>')
                for frame in current.stack:
                    frame = t.cast(DebugFrameSummary, frame)
                    info = f' title="{escape(frame.info)}"' if frame.info else ""
                    row_parts.append(f"<li{info}>{frame.render_html(mark_library)}")
                rows.append("\n".join(row_parts))
        if sys.version_info < (3, 13):
            exc_type_str = self._te.exc_type.__name__
        else:
            exc_type_str = self._te.exc_type_str
        is_syntax_error = exc_type_str == "SyntaxError"
        if include_title:
            if is_syntax_error:
                title = "Syntax Error"
            else:
                title = "Traceback <em>(most recent call last)</em>:"
        else:
            title = ""
        exc_full = escape("".join(self._te.format_exception_only()))
        if is_syntax_error:
            description = f"<pre class=syntaxerror>{exc_full}</pre>"
        else:
            description = f"<blockquote>{exc_full}</blockquote>"
        return SUMMARY_HTML % {
            "classes": classes,
            "title": f"<h3>{title}</h3>",
            "frames": "\n".join(rows),
            "description": description,
        }
    def render_debugger_html(
        self, evalex: bool, secret: str, evalex_trusted: bool
    ) -> str:
        exc_lines = list(self._te.format_exception_only())
        plaintext = "".join(self._te.format())
        if sys.version_info < (3, 13):
            exc_type_str = self._te.exc_type.__name__
        else:
            exc_type_str = self._te.exc_type_str
        return PAGE_HTML % {
            "evalex": "true" if evalex else "false",
            "evalex_trusted": "true" if evalex_trusted else "false",
            "console": "false",
            "title": escape(exc_lines[0]),
            "exception": escape("".join(exc_lines)),
            "exception_type": escape(exc_type_str),
            "summary": self.render_traceback_html(include_title=False),
            "plaintext": escape(plaintext),
            "plaintext_cs": re.sub("-{2,}", "-", plaintext),
            "secret": secret,
        }
class DebugFrameSummary(traceback.FrameSummary):
    """A :class:`traceback.FrameSummary` that can evaluate code in the
    frame's namespace.
    """
    __slots__ = (
        "local_ns",
        "global_ns",
        "_cache_info",
        "_cache_is_library",
        "_cache_console",
    )
    def __init__(
        self,
        *,
        locals: dict[str, t.Any],
        globals: dict[str, t.Any],
        **kwargs: t.Any,
    ) -> None:
        super().__init__(locals=None, **kwargs)
        self.local_ns = locals
        self.global_ns = globals
    @cached_property
    def info(self) -> str | None:
        return self.local_ns.get("__traceback_info__")
    @cached_property
    def is_library(self) -> bool:
        return any(
            self.filename.startswith((path, os.path.realpath(path)))
            for path in sysconfig.get_paths().values()
        )
    @cached_property
    def console(self) -> Console:
        return Console(self.global_ns, self.local_ns)
    def eval(self, code: str) -> t.Any:
        return self.console.eval(code)
    def render_html(self, mark_library: bool) -> str:
        context = 5
        lines = linecache.getlines(self.filename)
        line_idx = self.lineno - 1  # type: ignore[operator]
        start_idx = max(0, line_idx - context)
        stop_idx = min(len(lines), line_idx + context + 1)
        rendered_lines = []
        def render_line(line: str, cls: str) -> None:
            line = line.expandtabs().rstrip()
            stripped_line = line.strip()
            prefix = len(line) - len(stripped_line)
            colno = getattr(self, "colno", 0)
            end_colno = getattr(self, "end_colno", 0)
            if cls == "current" and colno and end_colno:
                arrow = (
                    f'\n<span class="ws">{" " * prefix}</span>'
                    f"{' ' * (colno - prefix)}{'^' * (end_colno - colno)}"
                )
            else:
                arrow = ""
            rendered_lines.append(
                f'<pre class="line {cls}"><span class="ws">{" " * prefix}</span>'
                f"{escape(stripped_line) if stripped_line else ' '}"
                f"{arrow if arrow else ''}</pre>"
            )
        if line_idx < len(lines):
            for line in lines[start_idx:line_idx]:
                render_line(line, "before")
            render_line(lines[line_idx], "current")
            for line in lines[line_idx + 1 : stop_idx]:
                render_line(line, "after")
        return FRAME_HTML % {
            "id": id(self),
            "filename": escape(self.filename),
            "lineno": self.lineno,
            "function_name": escape(self.name),
            "lines": "\n".join(rendered_lines),
            "library": "library" if mark_library and self.is_library else "",
        }
def render_console_html(secret: str, evalex_trusted: bool) -> str:
    return CONSOLE_HTML % {
        "evalex": "true",
        "evalex_trusted": "true" if evalex_trusted else "false",
        "console": "true",
        "title": "Console",
        "secret": secret,
    }
