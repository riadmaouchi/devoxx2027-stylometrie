# Contributeur de github.com/pallets/flask (BSD-3-Clause), anonymise.
# Commits de plus de 300 lignes exclus (reformatages, deplacements).
# Periode : APRES juin 2021
        :data:`.session`, :data:`g`, and :data:`.current_app` become available.
        :data:`.session`, :data:`g`, and :data:`.current_app` become available.
        Alternatively, a file-like object opened in binary mode; make
        sure to call ``seek(0)`` if it was already read.
    ["get", "query", "post", "head", "options", "delete", "put", "trace", "patch"]
    @setupmethod
    def query(self, rule: str, **options: t.Any) -> t.Callable[[T_route], T_route]:
        .. versionadded:: 3.2
        return self._method_route("QUERY", rule, options)
from functools import partial
@pytest.mark.parametrize("method", ["get", "query", "post", "put", "delete", "patch"])
    client_method = getattr(
        client, method, partial(client.open, method=method.capitalize())
    )
                Converted to a JSON response.
                Converted to a JSON response.
            assert rv.cache_control.max_age == expected_max_age
        assert rv.cache_control.max_age == 100
    meths = c.open("/", method="OPTIONS").allow
    assert meths == {"GET", "HEAD", "OPTIONS", "POST"}
    meths = client.open("/", method="OPTIONS").allow
    assert meths == {"DELETE", "GET", "HEAD", "OPTIONS", "POST"}
        CELERY={
            "broker_url": "redis://localhost",
            "result_backend": "redis://localhost",
            "task_ignore_result": True,
        },
from js_example import views  # noqa: F401
    source = ctx.get_parameter_source(param.name)
class CertParamType(click.ParamType):  # type: ignore[type-arg]
            value = click.STRING(value, param, ctx).lower()  # type: ignore[union-attr]
    default: t.Callable[[t.Any], t.Any] = staticmethod(_default)
class CertParamType(click.ParamType[t.Any]):
    source = ctx.get_parameter_source(param.name)
class CertParamType(click.ParamType[str | os.PathLike[str] | ssl.SSLContext]):
            value = click.STRING(value, param, ctx).lower()  # type: ignore[union-attr]
        .. versionchanged:: 3.2
            Use case-insensitive comparison instead of only lower case.
        return filename.lower().endswith((".html", ".htm", ".xml", ".xhtml", ".svg"))
    # Store the context that was active when the decorator was applied.
    original = _cv_app.get(None)
    if original is None:
        # Copy the context before pushing, so each worker acts independently.
        with original.copy() as ctx:
from __future__ import annotations
import collections.abc as cabc
from concurrent import futures
from flask.testing import FlaskClient
def test_copy_context_thread(
    request: pytest.FixtureRequest, app: flask.Flask, client: FlaskClient
) -> None:
    executor = futures.ThreadPoolExecutor(max_workers=2)
    request.addfinalizer(lambda: executor.shutdown(cancel_futures=True))
    result: cabc.Iterator[int] | None = None
    @app.route("/")
    def index():
        flask.session["fizz"] = "buzz"
        @flask.copy_current_request_context
        def work(n: int) -> int:
            assert flask.current_app == app
            assert flask.request.path == "/"
            assert flask.request.args["foo"] == "bar"
            assert flask.session["fizz"] == "buzz"
            return n
        nonlocal result
        result = executor.map(work, range(10))
        return "Hello World!"
    rv = client.get(query_string={"foo": "bar"})
    assert rv.text == "Hello World!"
    assert result is not None
    assert set(result) == set(range(10))
    be used when starting a background task, otherwise it will not see the app
    and request objects that were active in the parent.
    .. warning::
        Due to the following caveats, it is often safer (and simpler) to pass
        the data you need when starting the task, rather than using this and
        relying on the context objects.
    In order to avoid execution switching partially though reading data, either
    read the request body (access ``form``, ``json``, ``data``, etc) before
    starting the task, or use a lock. This can be an issue when using threading,
    but shouldn't be an issue when using greenlet/gevent or asyncio.
    If the task will access ``session``, be sure to do so in the parent as well
    so that the ``Vary: cookie`` header will be set. Modifying ``session`` in
    the task should be avoided, as it may execute after the response cookie has
    already been written.
    .. code-block:: python
    .. warning::
        Due to the following caveat, it is often safer to pass the data you
        need as arguments to the generator, rather than relying on the context
        objects.
    More headers cannot be sent after the body has begun. Therefore, you must
    make sure all headers are set before starting the response. In particular,
    if the generator will access ``session``, be sure to do so in the view as
    well so that the ``Vary: cookie`` header will be set. Do not modify the
    session in the generator, as the ``Set-Cookie`` header will already be sent.
from .helpers import _CollectErrors
        .. versionchanged:: 3.2
            All callbacks are called rather than stopping on the first error.
        collect_errors = _CollectErrors()
                    with collect_errors:
                        self.ensure_sync(func)(exc)
        with collect_errors:
            request_tearing_down.send(self, _async_wrapper=self.ensure_sync, exc=exc)
        collect_errors.raise_any("Errors during request teardown")
        .. versionchanged:: 3.2
            All callbacks are called rather than stopping on the first error.
        collect_errors = _CollectErrors()
            with collect_errors:
                self.ensure_sync(func)(exc)
        with collect_errors:
            appcontext_tearing_down.send(self, _async_wrapper=self.ensure_sync, exc=exc)
        collect_errors.raise_any("Errors during app teardown")
from .helpers import _CollectErrors
        collect_errors = _CollectErrors()
        if self._request is not None:
            with collect_errors:
            with collect_errors:
        with collect_errors:
        _cv_app.reset(self._cv_token)
        self._cv_token = None
        with collect_errors:
        collect_errors.raise_any("Errors during context teardown")
from types import TracebackType
class _CollectErrors:
    Used to run all teardown functions, then raise any errors afterward.
    def __init__(self) -> None:
        self.errors: list[BaseException] = []
    def __enter__(self) -> None:
        pass
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_val is not None:
            self.errors.append(exc_val)
        return True
    def raise_any(self, message: str) -> None:
        if self.errors:
            if sys.version_info >= (3, 11):
                raise BaseExceptionGroup(message, self.errors)  # noqa: F821
            else:
                raise self.errors[0]
import sys
from flask.testing import FlaskClient
def test_robust_teardown(app: flask.Flask, client: FlaskClient) -> None:
    count = 0
    @app.teardown_request
    def request_teardown(e: Exception | None) -> None:
        nonlocal count
        count += 1
        raise ValueError("request_teardown")
    @app.teardown_appcontext
    def app_teardown(e: Exception | None) -> None:
        nonlocal count
        count += 1
        raise ValueError("app_teardown")
    @app.get("/")
    def index() -> str:
        return ""
    def request_signal(sender: flask.Flask, exc: Exception | None) -> None:
        nonlocal count
        count += 1
        raise ValueError("request_signal")
    def app_signal(sender: flask.Flask, exc: Exception | None) -> None:
        nonlocal count
        count += 1
        raise ValueError("app_signal")
    with (
        flask.request_tearing_down.connected_to(request_signal, app),
        flask.appcontext_tearing_down.connected_to(app_signal, app),
    ):
        if sys.version_info >= (3, 11):
            with pytest.raises(ExceptionGroup, match="context teardown") as exc_info:  # noqa: F821
                client.get()
            assert len(exc_info.value.exceptions) == 2
            eg1, eg2 = exc_info.value.exceptions
            assert isinstance(eg1, ExceptionGroup)  # noqa: F821
            assert "request teardown" in eg1.message
            assert len(eg1.exceptions) == 2
            assert isinstance(eg2, ExceptionGroup)  # noqa: F821
            assert "app teardown" in eg2.message
            assert len(eg2.exceptions) == 2
        else:
            with pytest.raises(ValueError, match="request_teardown"):
                client.get()
    assert count == 4
    with client.get("/static/index.html") as rv:
        assert rv.status_code == 200
        assert rv.data.strip() == b"<h1>Hello World!</h1>"
        with app.test_request_context():
            assert (
                flask.url_for("static", filename="index.html") == "/static/index.html"
            )
    with app.test_client().get("/foo/index.html") as rv:
        assert rv.status_code == 200
    with app.test_client().get("/foo/index.html") as rv:
        assert rv.status_code == 200
    with app.test_client().open("/static/index.html", method="GET") as rv:
        assert rv.status_code == 200
    with app.test_client().open("/static/index.html", method="GET") as rv:
        assert rv.status_code == 200
    with app.test_client().open("/static/index.html", method="GET") as rv:
        assert rv.status_code == 200
    with c.get("http://example.com/static/index.html") as rv:
        assert rv.status_code == 200
    with client.get("/admin/static/test.txt") as rv:
        assert rv.data.strip() == b"Admin File"
    with client.get("/admin/static/css/test.css") as rv:
        assert rv.data.strip() == b"/* nested file */"
        with client.get("/admin/static/css/test.css") as rv:
            cc = parse_cache_control_header(rv.headers["Cache-Control"])
            assert cc.max_age == expected_max_age
            expect = f.read()
        with flask.send_file("static/index.html") as rv:
            assert rv.direct_passthrough
            assert rv.mimetype == "text/html"
            rv.direct_passthrough = False
            assert rv.data == expect
        with app.send_static_file("index.html") as rv:
            assert rv.cache_control.max_age is None
        with flask.send_file("static/index.html") as rv:
            assert rv.cache_control.max_age is None
        with app.send_static_file("index.html") as rv:
            assert rv.cache_control.max_age == 3600
        with flask.send_file("static/index.html") as rv:
            assert rv.cache_control.max_age == 3600
        with app.send_static_file(FakePath("index.html")) as rv:
            assert rv.cache_control.max_age == 3600
            with app.send_static_file("index.html") as rv:
                assert rv.cache_control.max_age == 10
            with flask.send_file("static/index.html") as rv:
                assert rv.cache_control.max_age == 10
        with flask.send_from_directory("static", "hello.txt") as rv:
            rv.direct_passthrough = False
            assert rv.data.strip() == b"Hello Subdomain"
        with client.get() as rv:
            assert rv.text == "flask"
        with client, client.get() as rv:
            assert rv.text == "flask"
        if not self.session_interface.is_null_session(ctx._get_session()):
            self.session_interface.save_session(self, ctx._get_session(), response)
    def _get_session(self) -> SessionMixin:
    @property
    def session(self) -> SessionMixin:
        :data:`.session`. Only available in request contexts, otherwise raises
        :exc:`RuntimeError`. Accessing this sets :attr:`.SessionMixin.accessed`.
        session = self._get_session()
        session.accessed = True
        return session
        if self._request is not None:
            # Open the session at the moment that the request context is available.
            # This allows a custom open_session method to use the request context.
            self._get_session()
            # Match the request URL after loading the session, so that the
            # session is available in custom URL converters.
            if self.url_adapter is not None:
                self.match_request()
        if not self.session_interface.is_null_session(ctx._session):
            self.session_interface.save_session(self, ctx._session, response)
        self._session: SessionMixin | None = session
            session=self._session,
    @property
    def session(self) -> SessionMixin:
        this context has been pushed. Accessing this property, also accessed by
        the :data:`~flask.session` proxy, sets :attr:`.SessionMixin.accessed`.
        assert self._session is not None, "The session has not yet been opened."
        self._session.accessed = True
        return self._session
        if self._session is None:
            self._session = session_interface.open_session(self.app, self.request)
            if self._session is None:
                self._session = session_interface.make_null_session(self.app)
    accessed = False
    is set when the session object is accessed through the request context,
    including the global :data:`.session` proxy. A ``Vary: cookie`` header will
    be added if this is ``True``.
    .. versionchanged:: 3.1.3
        This is tracked by the request context.
        initial: c.Mapping[str, t.Any] | None = None,
    proxies with their concrete objects for faster access.
        # The session proxy cannot be replaced, accessing it gets
        # RequestContext.session, which sets session.accessed.
from flask.globals import request_ctx
from flask.testing import FlaskClient
def test_session_accessed(app: flask.Flask, client: FlaskClient) -> None:
    @app.post("/")
    def do_set():
    @app.get("/")
    def do_get():
        return flask.session.get("value", "None")
    @app.get("/nothing")
    def do_nothing() -> str:
        return ""
    with client:
        rv = client.get("/nothing")
        assert "cookie" not in rv.vary
        assert not request_ctx._session.accessed
        assert not request_ctx._session.modified
    with client:
        rv = client.post(data={"value": "42"})
        assert rv.text == "value set"
        assert "cookie" in rv.vary
        assert request_ctx._session.accessed
        assert request_ctx._session.modified
    with client:
        rv = client.get()
        assert rv.text == "42"
        assert "cookie" in rv.vary
        assert request_ctx._session.accessed
        assert not request_ctx._session.modified
    with client:
        rv = client.get("/nothing")
        assert rv.text == ""
        assert "cookie" not in rv.vary
        assert not request_ctx._session.accessed
        assert not request_ctx._session.modified
        match_order = [r.endpoint for r in app.url_map.iter_rules()]
        assert "GET, HEAD, OPTIONS, POST" not in output
            if provide_automatic_options is None:
                provide_automatic_options = (
                    "OPTIONS" not in methods
                    and self.config["PROVIDE_AUTOMATIC_OPTIONS"]
                )
        if provide_automatic_options:
            required_methods.add("OPTIONS")
from flask.testing import FlaskClient
def test_provide_automatic_options_attr_disable(
    app: flask.Flask, client: FlaskClient
) -> None:
    app.add_url_rule("/", view_func=index)
    rv = client.options()
def test_provide_automatic_options_attr_enable(
    app: flask.Flask, client: FlaskClient
) -> None:
    enabled by the view function attribute.
    app.config["PROVIDE_AUTOMATIC_OPTIONS"] = False
    def index():
    index.provide_automatic_options = True
    app.add_url_rule("/", view_func=index)
    rv = client.options()
    assert rv.allow == {"GET", "HEAD", "OPTIONS"}
def test_provide_automatic_options_arg_disable(
    app: flask.Flask, client: FlaskClient
) -> None:
    @app.get("/", provide_automatic_options=False)
    def index():
        return "Hello World!"
    rv = client.options()
def test_provide_automatic_options_method_disable(
    app: flask.Flask, client: FlaskClient
) -> None:
    @app.route("/", methods=["OPTIONS"])
    def index():
        return "", {"X-Test": "test"}
    rv = client.options()
    assert rv.headers["X-Test"] == "test"
def test_default_static_max_age(app: flask.Flask) -> None:
    blueprint = MyBlueprint(
        "blueprint", __name__, url_prefix="/bp", static_folder="static"
    )
    with app.test_request_context(), blueprint.send_static_file("index.html") as rv:
        cc = parse_cache_control_header(rv.headers["Cache-Control"])
        assert cc.max_age == 100
        match_order = [
            r.endpoint
            for r in app.url_map.iter_rules()
            if r.endpoint != "_automatic_options"
        ]
        assert "HEAD" not in output
        assert "OPTIONS" not in output
from flask.testing import FlaskClient
def test_view_provide_automatic_options_attr_disable(
    app: flask.Flask, client: FlaskClient
) -> None:
    class Index(flask.views.View):
    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.options()
def test_view_provide_automatic_options_attr_enable(
    app: flask.Flask, client: FlaskClient
) -> None:
    enabled by the view class attribute.
    app.config["PROVIDE_AUTOMATIC_OPTIONS"] = False
    class Index(flask.views.View):
    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.options("/")
    assert rv.allow == {"GET", "HEAD", "OPTIONS"}
def test_provide_automatic_options_method_disable(
    app: flask.Flask, client: FlaskClient
) -> None:
    class Index(flask.views.View):
        methods = ["OPTIONS"]
            return "", {"X-Test": "test"}
    app.add_url_rule("/", view_func=Index.as_view("index"))
    rv = client.options()
    assert rv.headers["X-Test"] == "test"
        app.add_url_rule("/other", view_func=Index.as_view("index"))
import importlib.metadata
werkzeug_3_2 = importlib.metadata.version("werkzeug") >= "3.2."
    ("subdomain_matching", "host_matching", "expect_subdomain", "expect_host"),
        (False, False, "default", "default"),
        (True, False, "abc", "<invalid>"),
        (False, True, "abc", "default"),
    expect_subdomain: str,
    expect_host: str,
    assert r.text == "default"
    assert r.text == expect_subdomain
        if werkzeug_3_2:
            assert r.text == "default"
        else:
            assert r.text == expect_host
    with pytest.warns(match="Current server name"):
    if werkzeug_3_2:
        assert rv.status_code == 200
    else:
    with pytest.warns(match="Current server name") if matching else nullcontext():
        # ip address can't match name, but will fall back to default
    if werkzeug_3_2:
        assert rv.status_code == 204
    else:
        if not self._got_first_request and self.should_ignore_error is not None:
            import warnings
            warnings.warn(
                "The 'should_ignore_error' method is deprecated and will"
                " be removed in Flask 3.3. Handle errors as needed in"
                " teardown handlers instead.",
                DeprecationWarning,
                stacklevel=1,
            )
            if (
                error is not None
                and self.should_ignore_error is not None
                and self.should_ignore_error(error)
            ):
    should_ignore_error: None = None
    teardown handlers, and the context will not be preserved for
    debugging.
    .. deprecated:: 3.2
        Handle errors as needed in teardown handlers instead.
    .. versionadded:: 0.10
                view_func=lambda **kw: self_ref().send_static_file(**kw),  # type: ignore
            except:
    __setitem__ = __delitem__ = clear = pop = popitem = update = setdefault = _fail
    location: str, code: int = 303, Response: type[BaseResponse] | None = None
    .. versionchanged:: 3.2
        ``code`` defaults to ``303`` instead of ``302``.
    def redirect(self, location: str, code: int = 303) -> BaseResponse:
        .. versionchanged:: 3.2
            ``code`` defaults to ``303`` instead of ``302``.
        return self.get("_permanent", False)  # type: ignore[no-any-return]
import inspect
from functools import update_wrapper
from .globals import app_ctx
F = t.TypeVar("F", bound=t.Callable[..., t.Any])
# Other methods may call the overridden method with the new ctx arg. Remove it
# and call the method with the remaining args.
def remove_ctx(f: F) -> F:
    def wrapper(self: Flask, *args: t.Any, **kwargs: t.Any) -> t.Any:
        if args and isinstance(args[0], AppContext):
            args = args[1:]
        return f(self, *args, **kwargs)
    return update_wrapper(wrapper, f)  # type: ignore[return-value]
# The overridden method may call super().base_method without the new ctx arg.
# Add it to the args for the call.
def add_ctx(f: F) -> F:
    def wrapper(self: Flask, *args: t.Any, **kwargs: t.Any) -> t.Any:
        if not args:
            args = (app_ctx._get_current_object(),)
        elif not isinstance(args[0], AppContext):
            args = (app_ctx._get_current_object(), *args)
        return f(self, *args, **kwargs)
    return update_wrapper(wrapper, f)  # type: ignore[return-value]
    def __init_subclass__(cls, **kwargs: t.Any) -> None:
        import warnings
        # These method signatures were updated to take a ctx param. Detect
        # overridden methods in subclasses that still have the old signature.
        # Show a deprecation warning and wrap to call with correct args.
        for method in (
            cls.handle_http_exception,
            cls.handle_user_exception,
            cls.handle_exception,
            cls.log_exception,
            cls.dispatch_request,
            cls.full_dispatch_request,
            cls.finalize_request,
            cls.make_default_options_response,
            cls.preprocess_request,
            cls.process_response,
            cls.do_teardown_request,
            cls.do_teardown_appcontext,
        ):
            base_method = getattr(Flask, method.__name__)
            if method is base_method:
                # not overridden
                continue
            # get the second parameter (first is self)
            iter_params = iter(inspect.signature(method).parameters.values())
            next(iter_params)
            param = next(iter_params, None)
            # must have second parameter named ctx or annotated AppContext
            if param is None or not (
                # no annotation, match name
                (param.annotation is inspect.Parameter.empty and param.name == "ctx")
                or (
                    # string annotation, access path ends with AppContext
                    isinstance(param.annotation, str)
                    and param.annotation.rpartition(".")[2] == "AppContext"
                )
                or (
                    # class annotation
                    inspect.isclass(param.annotation)
                    and issubclass(param.annotation, AppContext)
                )
            ):
                warnings.warn(
                    f"The '{method.__name__}' method now takes 'ctx: AppContext'"
                    " as the first parameter. The old signature is deprecated"
                    " and will not be supported in Flask 4.0.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                setattr(cls, method.__name__, remove_ctx(method))
                setattr(Flask, method.__name__, add_ctx(base_method))
    def update_template_context(
        self, ctx: AppContext, context: dict[str, t.Any]
    ) -> None:
        if ctx.has_request:
        self, ctx: AppContext, e: HTTPException
        handler = self._find_error_handler(e, ctx.request.blueprints)
        self, ctx: AppContext, e: Exception
            return self.handle_http_exception(ctx, e)
        handler = self._find_error_handler(e, ctx.request.blueprints)
    def handle_exception(self, ctx: AppContext, e: Exception) -> Response:
        self.log_exception(ctx, exc_info)
        handler = self._find_error_handler(server_error, ctx.request.blueprints)
        return self.finalize_request(ctx, server_error, from_error_handler=True)
        ctx: AppContext,
        exc_info: tuple[type, BaseException, TracebackType] | tuple[None, None, None],
            f"Exception on {ctx.request.path} [{ctx.request.method}]", exc_info=exc_info
    def dispatch_request(self, ctx: AppContext) -> ft.ResponseReturnValue:
        req = ctx.request
            return self.make_default_options_response(ctx)
    def full_dispatch_request(self, ctx: AppContext) -> Response:
            rv = self.preprocess_request(ctx)
                rv = self.dispatch_request(ctx)
            rv = self.handle_user_exception(ctx, e)
        return self.finalize_request(ctx, rv)
        ctx: AppContext,
            response = self.process_response(ctx, response)
    def make_default_options_response(self, ctx: AppContext) -> Response:
        methods = ctx.url_adapter.allowed_methods()  # type: ignore[union-attr]
    def preprocess_request(self, ctx: AppContext) -> ft.ResponseReturnValue | None:
        req = ctx.request
    def process_response(self, ctx: AppContext, response: Response) -> Response:
    def do_teardown_request(
        self, ctx: AppContext, exc: BaseException | None = None
    ) -> None:
        for name in chain(ctx.request.blueprints, (None,)):
    def do_teardown_appcontext(
        self, ctx: AppContext, exc: BaseException | None = None
    ) -> None:
                response = self.full_dispatch_request(ctx)
                response = self.handle_exception(ctx, e)
                environ["werkzeug.debug.preserve_context"](ctx)
                self.app.do_teardown_request(self, exc)
            self.app.do_teardown_appcontext(self, exc)
from .ctx import AppContext
from .globals import app_ctx
    ctx = app_ctx._get_current_object()
    rv: dict[str, t.Any] = {"g": ctx.g}
    if ctx.has_request:
        rv["request"] = ctx.request
        rv["session"] = ctx.session
def _render(ctx: AppContext, template: Template, context: dict[str, t.Any]) -> str:
    app = ctx.app
    app.update_template_context(ctx, context)
    ctx = app_ctx._get_current_object()
    template = ctx.app.jinja_env.get_or_select_template(template_name_or_list)
    return _render(ctx, template, context)
    ctx = app_ctx._get_current_object()
    template = ctx.app.jinja_env.from_string(source)
    return _render(ctx, template, context)
    ctx: AppContext, template: Template, context: dict[str, t.Any]
    app = ctx.app
    app.update_template_context(ctx, context)
    ctx = app_ctx._get_current_object()
    template = ctx.app.jinja_env.get_or_select_template(template_name_or_list)
    return _stream(ctx, template, context)
    ctx = app_ctx._get_current_object()
    template = ctx.app.jinja_env.from_string(source)
    return _stream(ctx, template, context)
    with app.request_context(environ) as ctx:
        response = app.full_dispatch_request(ctx)
    with app.request_context(environ) as ctx:
        response = app.full_dispatch_request(ctx)
        def log_exception(self, ctx, exc_info):
    @t.overload
    def template_filter(self, name: T_template_filter) -> T_template_filter: ...
    @t.overload
    def template_filter(
        self, name: str | None = None
    ) -> t.Callable[[T_template_filter], T_template_filter]: ...
        self, name: T_template_filter | str | None = None
    ) -> T_template_filter | t.Callable[[T_template_filter], T_template_filter]:
        is optional. The decorator may be used without parentheses.
        .. code-block:: python
            @app.template_filter("reverse")
            def reverse_filter(s):
                return reversed(s)
        The :meth:`add_template_filter` method may be used to register a
        function later rather than decorating.
        :param name: The name to register the filter as. If not given, uses the
            function's name.
            self.add_template_filter(name)
            return name
        The :meth:`template_filter` decorator can be used to register a function
        by decorating instead.
        :param f: The function to register.
        :param name: The name to register the filter as. If not given, uses the
            function's name.
    @t.overload
    def template_test(self, name: T_template_test) -> T_template_test: ...
    @t.overload
    def template_test(
        self, name: str | None = None
    ) -> t.Callable[[T_template_test], T_template_test]: ...
        self, name: T_template_test | str | None = None
    ) -> T_template_test | t.Callable[[T_template_test], T_template_test]:
        is optional. The decorator may be used without parentheses.
        .. code-block:: python
            @app.template_test("prime")
            def is_prime_test(n):
        The :meth:`add_template_test` method may be used to register a function
        later rather than decorating.
        :param name: The name to register the filter as. If not given, uses the
            function's name.
            self.add_template_test(name)
            return name  # type: ignore[return-value]
        The :meth:`template_test` decorator can be used to register a function
        by decorating instead.
        :param f: The function to register.
        :param name: The name to register the test as. If not given, uses the
            function's name.
        .. versionadded:: 0.10
    @t.overload
    def template_global(self, name: T_template_global) -> T_template_global: ...
    @t.overload
    def template_global(
        self, name: str | None = None
    ) -> t.Callable[[T_template_global], T_template_global]: ...
        self, name: T_template_global | str | None = None
    ) -> T_template_global | t.Callable[[T_template_global], T_template_global]:
        is optional. The decorator may be used without parentheses.
        .. code-block:: python
        The :meth:`add_template_global` method may be used to register a
        function later rather than decorating.
        :param name: The name to register the global as. If not given, uses the
            function's name.
        .. versionadded:: 0.10
            self.add_template_global(name)
            return name
        The :meth:`template_global` decorator can be used to register a function
        by decorating instead.
        :param f: The function to register.
        :param name: The name to register the global as. If not given, uses the
            function's name.
        .. versionadded:: 0.10
    @t.overload
    def app_template_filter(self, name: T_template_filter) -> T_template_filter: ...
    @t.overload
    def app_template_filter(
        self, name: str | None = None
    ) -> t.Callable[[T_template_filter], T_template_filter]: ...
        self, name: T_template_filter | str | None = None
    ) -> T_template_filter | t.Callable[[T_template_filter], T_template_filter]:
        is optional. The decorator may be used without parentheses.
        The :meth:`add_app_template_filter` method may be used to register a
        function later rather than decorating.
        The filter is available in all templates, not only those under this
        blueprint. Equivalent to :meth:`.Flask.template_filter`.
        :param name: The name to register the filter as. If not given, uses the
            function's name.
        if callable(name):
            self.add_app_template_filter(name)
            return name
        The :meth:`app_template_filter` decorator can be used to register a
        function by decorating instead.
        The filter is available in all templates, not only those under this
        blueprint. Equivalent to :meth:`.Flask.add_template_filter`.
        :param f: The function to register.
        :param name: The name to register the filter as. If not given, uses the
            function's name.
        def register_template_filter(state: BlueprintSetupState) -> None:
            state.app.add_template_filter(f, name=name)
        self.record_once(register_template_filter)
    @t.overload
    def app_template_test(self, name: T_template_test) -> T_template_test: ...
    @t.overload
    def app_template_test(
        self, name: str | None = None
    ) -> t.Callable[[T_template_test], T_template_test]: ...
        self, name: T_template_test | str | None = None
    ) -> T_template_test | t.Callable[[T_template_test], T_template_test]:
        is optional. The decorator may be used without parentheses.
        The :meth:`add_app_template_test` method may be used to register a
        function later rather than decorating.
        The test is available in all templates, not only those under this
        blueprint. Equivalent to :meth:`.Flask.template_test`.
        :param name: The name to register the filter as. If not given, uses the
            function's name.
        .. versionadded:: 0.10
        if callable(name):
            self.add_app_template_test(name)
            return name  # type: ignore[return-value]
        The :meth:`app_template_test` decorator can be used to register a
        function by decorating instead.
        The test is available in all templates, not only those under this
        blueprint. Equivalent to :meth:`.Flask.add_template_test`.
        :param f: The function to register.
        :param name: The name to register the test as. If not given, uses the
            function's name.
        .. versionadded:: 0.10
        def register_template_test(state: BlueprintSetupState) -> None:
            state.app.add_template_test(f, name=name)
        self.record_once(register_template_test)
    @t.overload
    def app_template_global(self, name: T_template_global) -> T_template_global: ...
    @t.overload
    def app_template_global(
        self, name: str | None = None
    ) -> t.Callable[[T_template_global], T_template_global]: ...
        self, name: T_template_global | str | None = None
    ) -> T_template_global | t.Callable[[T_template_global], T_template_global]:
        is optional. The decorator may be used without parentheses.
        The :meth:`add_app_template_global` method may be used to register a
        function later rather than decorating.
        The global is available in all templates, not only those under this
        blueprint. Equivalent to :meth:`.Flask.template_global`.
        :param name: The name to register the global as. If not given, uses the
            function's name.
        .. versionadded:: 0.10
            self.add_app_template_global(name)
            return name
        The :meth:`app_template_global` decorator can be used to register a function
        by decorating instead.
        The global is available in all templates, not only those under this
        blueprint. Equivalent to :meth:`.Flask.add_template_global`.
        :param f: The function to register.
        :param name: The name to register the global as. If not given, uses the
            function's name.
        .. versionadded:: 0.10
        def register_template_global(state: BlueprintSetupState) -> None:
            state.app.add_template_global(f, name=name)
        self.record_once(register_template_global)
from .globals import _cv_app
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.
    Use it as a decorator on a generator function:
    .. code-block:: python
        @app.get("/stream")
                yield "Hello "
                yield request.args["name"]
                yield "!"
    Or use it as a wrapper around a created generator:
    .. code-block:: python
        @app.get("/stream")
                yield "Hello "
                yield request.args["name"]
                yield "!"
    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]
        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
                # Clean up in case the user wrapped a WSGI iterator.
    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    return wrapped_g
    def test_async_view(self, app, client):
        @app.route("/")
        async def index():
            flask.session["test"] = "flask"
            @flask.stream_with_context
            def gen():
                yield flask.session["test"]
            return flask.Response(gen())
        # response is closed without reading stream
        client.get().close()
        # response stream is read
        assert client.get().text == "flask"
        # same as above, but with client context preservation
        with client:
            client.get().close()
        with client:
            assert client.get().text == "flask"
        for cm in self._new_contexts:
        self._new_contexts.clear()
def test_redirect_session(app, client, app_ctx):
    @app.route("/redirect")
        flask.session["redirect"] = True
        return flask.redirect("/target")
    @app.route("/target")
        flask.session["target"] = True
        return ""
        client.get("/redirect", follow_redirects=True)
        assert flask.session["redirect"] is True
        assert flask.session["target"] is True
html_logo = "_static/flask-logo.svg"
html_favicon = "_static/flask-icon.svg"
html_logo = "_static/flask-vertical.svg"
        with ctx:
            return ctx.app.ensure_sync(f)(*args, **kwargs)
        _root_path=current_app.root_path,
    def name(self) -> str:
        self.static_folder = static_folder
    __setitem__ = __delitem__ = clear = pop = popitem = update = setdefault = _fail  # noqa: B950
    def json_dumps(self, obj: t.Any, **kwargs: t.Any) -> str:
        for ep in importlib.metadata.entry_points(group="flask.commands"):
    default: t.Callable[[t.Any], t.Any] = staticmethod(_default)
    secret_key = ConfigAttribute[str | bytes | None]("SECRET_KEY")
HeaderValue = str | list[str] | tuple[str, ...]
AppOrBlueprintKey = str | None  # The App key is None, whereas blueprints are named
AfterRequestCallable = (
    t.Callable[[ResponseClass], ResponseClass]
    | t.Callable[[ResponseClass], t.Awaitable[ResponseClass]]
)
BeforeFirstRequestCallable = t.Callable[[], None] | t.Callable[[], t.Awaitable[None]]
BeforeRequestCallable = (
    t.Callable[[], ResponseReturnValue | None]
    | t.Callable[[], t.Awaitable[ResponseReturnValue | None]]
)
TeardownCallable = (
    t.Callable[[BaseException | None], None]
    | t.Callable[[BaseException | None], t.Awaitable[None]]
)
TemplateContextProcessorCallable = (
    t.Callable[[], dict[str, t.Any]] | t.Callable[[], t.Awaitable[dict[str, t.Any]]]
)
URLValuePreprocessorCallable = t.Callable[[str | None, dict[str, t.Any] | None], None]
ErrorHandlerCallable = (
    t.Callable[[t.Any], ResponseReturnValue]
    | t.Callable[[t.Any], t.Awaitable[ResponseReturnValue]]
)
RouteCallable = (
    t.Callable[..., ResponseReturnValue]
    | t.Callable[..., t.Awaitable[ResponseReturnValue]]
)
        for expect, line in zip(order, output.splitlines()[2:], strict=False):
                    rv,  # pyright: ignore
                    rv,  # pyright: ignore
    "ghsa": ("https://github.com/pallets/flask/security/advisories/GHSA-%s", "GHSA-%s"),
    modules_tmp_path, modules_tmp_path_prefix, purge_module, site_packages
    modules_tmp_path, modules_tmp_path_prefix, purge_module, monkeypatch
    modules_tmp_path, modules_tmp_path_prefix, purge_module, site_packages
if not t.TYPE_CHECKING:
    def __getattr__(name: str) -> t.Any:
        if name == "__version__":
            import importlib.metadata
            import warnings
            warnings.warn(
                "The '__version__' attribute is deprecated and will be removed in"
                " Flask 3.2. Use feature detection or"
                " 'importlib.metadata.version(\"flask\")' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            return importlib.metadata.version("flask")
        raise AttributeError(name)
            assert bool(static_host) == host_matching, (
                "Invalid static_host/host_matching combination"
            )
        ) != bool(subdomain or url_scheme), (
            'Cannot pass "subdomain" or "url_scheme" with "base_url".'
        )
            " Flask 3.2. Use feature detection or"
gettext_uuid = True
gettext_compact = False
import collections.abc as c
class SessionMixin(MutableMapping[str, t.Any]):
class SecureCookieSession(CallbackDict[str, t.Any], SessionMixin):
    def __init__(
        self,
        initial: c.Mapping[str, t.Any] | c.Iterable[tuple[str, t.Any]] | None = None,
    ) -> None:
from werkzeug.wsgi import get_host
            "TRUSTED_HOSTS": None,
            if (trusted_hosts := self.config["TRUSTED_HOSTS"]) is not None:
                request.trusted_hosts = trusted_hosts
            # Check trusted_hosts here until bind_to_environ does.
            request.host = get_host(request.environ, request.trusted_hosts)  # pyright: ignore
def test_trusted_hosts_config(app: Flask) -> None:
    app.config["TRUSTED_HOSTS"] = ["example.test", ".other.test"]
    @app.get("/")
    def index() -> str:
        return ""
    client = app.test_client()
    r = client.get(base_url="http://example.test")
    assert r.status_code == 200
    r = client.get(base_url="http://a.other.test")
    assert r.status_code == 200
    r = client.get(base_url="http://bad.test")
    assert r.status_code == 400
        .. versionchanged:: 3.1
            If :data:`SERVER_NAME` is set, it does not restrict requests to
            only that domain, for both ``subdomain_matching`` and
            ``host_matching``.
        .. versionchanged:: 0.9
           This can be called outside a request when the URL adapter is created
           for an application context.
        .. versionadded:: 0.6
            subdomain = None
            server_name = self.config["SERVER_NAME"]
            if self.url_map.host_matching:
                # Don't pass SERVER_NAME, otherwise it's used and the actual
                # host is ignored, which breaks host matching.
                server_name = None
            elif not self.subdomain_matching:
                # Werkzeug doesn't implement subdomain matching yet. Until then,
                # disable it by forcing the current subdomain to the default, or
                # the empty string.
                subdomain = self.url_map.default_subdomain or ""
                request.environ, server_name=server_name, subdomain=subdomain
        # Need at least SERVER_NAME to match/build outside a request.
from contextlib import nullcontext
@pytest.mark.parametrize(
    ("subdomain_matching", "host_matching", "expect_base", "expect_abc", "expect_xyz"),
    [
        (False, False, "default", "default", "default"),
        (True, False, "default", "abc", "<invalid>"),
        (False, True, "default", "abc", "default"),
    ],
)
def test_server_name_matching(
    subdomain_matching: bool,
    host_matching: bool,
    expect_base: str,
    expect_abc: str,
    expect_xyz: str,
) -> None:
    app = flask.Flask(
        __name__,
        subdomain_matching=subdomain_matching,
        host_matching=host_matching,
        static_host="example.test" if host_matching else None,
    )
    app.config["SERVER_NAME"] = "example.test"
    @app.route("/", defaults={"name": "default"}, host="<name>")
    @app.route("/", subdomain="<name>", host="<name>.example.test")
    def index(name: str) -> str:
        return name
    client = app.test_client()
    r = client.get(base_url="http://example.test")
    assert r.text == expect_base
    r = client.get(base_url="http://abc.example.test")
    assert r.text == expect_abc
    with pytest.warns() if subdomain_matching else nullcontext():
        r = client.get(base_url="http://xyz.other.test")
    assert r.text == expect_xyz
    app.subdomain_matching = True
    app.config["SERVER_NAME"] = "example.test"
    client.allow_subdomain_redirects = True
    app.register_blueprint(parent, subdomain="api")
    response = client.get("/child/", base_url="http://api.example.test")
    app.subdomain_matching = True
    app.config["SERVER_NAME"] = "example.test"
    client.allow_subdomain_redirects = True
    child = flask.Blueprint("child", __name__, subdomain="api")
    app.register_blueprint(parent, subdomain="parent")
    response = client.get("/", base_url="http://api.parent.example.test")
    response = client.get("/", base_url="http://parent.example.test")
            "SECRET_KEY_FALLBACKS": None,
        keys: list[str | bytes] = [app.secret_key]
        if fallbacks := app.config["SECRET_KEY_FALLBACKS"]:
            keys.extend(fallbacks)
            keys,  # type: ignore[arg-type]
            signer_kwargs={
                "key_derivation": self.key_derivation,
                "digest_method": self.digest_method,
            },
import typing as t
def test_session_secret_key_fallbacks(app, client) -> None:
    @app.post("/")
    def set_session() -> str:
        flask.session["a"] = 1
        return ""
    @app.get("/")
    def get_session() -> dict[str, t.Any]:
        return dict(flask.session)
    # Set session with initial secret key
    client.post()
    assert client.get().json == {"a": 1}
    # Change secret key, session can't be loaded and appears empty
    app.secret_key = "new test key"
    assert client.get().json == {}
    # Add initial secret key as fallback, session can be loaded
    app.config["SECRET_KEY_FALLBACKS"] = ["test key"]
    assert client.get().json == {"a": 1}
    .. versionchanged:: 3.1
        Added the ``load_dotenv_defaults`` parameter and attribute.
        load_dotenv_defaults: bool = True,
        self.load_dotenv_defaults = get_load_dotenv(load_dotenv_defaults)
        ``ScriptInfo`` doesn't load anything, this is for reference when doing
        the load elsewhere during processing.
        .. versionadded:: 3.1
        import dotenv  # noqa: F401
        # Only show an error if a value was passed, otherwise we still want to
        # call load_dotenv and show a message without exiting.
        if value is not None:
            raise click.BadParameter(
                "python-dotenv must be installed to load an env file.",
                ctx=ctx,
                param=param,
            ) from None
    # Load if a value was passed, or we want to load default files, or both.
    if value is not None or ctx.obj.load_dotenv_defaults:
        load_dotenv(value, load_defaults=ctx.obj.load_dotenv_defaults)
    help=(
        "Load environment variables from this file, taking precedence over"
        " those set by '.env' and '.flaskenv'. Variables set directly in the"
        " environment take highest precedence. python-dotenv must be installed."
    ),
    .. versionchanged:: 3.1
        ``-e path`` takes precedence over default ``.env`` and ``.flaskenv`` files.
                create_app=self.create_app,
                set_debug_flag=self.set_debug_flag,
                load_dotenv_defaults=self.load_dotenv,
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.
    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.
    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
    data: dict[str, str | None] = {}
    if load_defaults:
        for default_name in (".flaskenv", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue
            data |= dotenv.dotenv_values(default_path, encoding="utf-8")
    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")
    for key, value in data.items():
        if key in os.environ or value is None:
        os.environ[key] = value
    return bool(data)  # True if at least one env var was loaded.
    try:
        runner = CliRunner(mix_stderr=False)
    except (DeprecationWarning, TypeError):
        # Click >= 8.2
        runner = CliRunner()
    try:
        runner = CliRunner(mix_stderr=False)
    except (DeprecationWarning, TypeError):
        # Click >= 8.2
        runner = CliRunner()
    try:
        runner = CliRunner(mix_stderr=False)
    except (DeprecationWarning, TypeError):
        # Click >= 8.2
        runner = CliRunner()
    assert not load_dotenv("non-existent-file", load_defaults=False)
            rv.headers.update(headers)
from datetime import datetime
sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))
        ("/", "fetch.html"),
            "SESSION_COOKIE_PARTITIONED": False,
    def get_cookie_partitioned(self, app: Flask) -> bool:
        the value of :data:`SESSION_COOKIE_PARTITIONED`.
        .. versionadded:: 3.1
        return app.config["SESSION_COOKIE_PARTITIONED"]  # type: ignore[no-any-return]
        partitioned = self.get_cookie_partitioned(app)
                    partitioned=partitioned,
            partitioned=partitioned,
        SESSION_COOKIE_PARTITIONED=True,
    assert "partitioned" in cookie
    assert "partitioned" in cookie
            "MAX_FORM_MEMORY_SIZE": 500_000,
            "MAX_FORM_PARTS": 1_000,
    _max_content_length: int | None = None
    _max_form_memory_size: int | None = None
    _max_form_parts: int | None = None
    def max_content_length(self) -> int | None:
        this limit is exceeded, a 413 :exc:`~werkzeug.exceptions.RequestEntityTooLarge`
        error is raised. If it is set to ``None``, no limit is enforced at the
        Flask application level. However, if it is ``None`` and the request has
        no ``Content-Length`` header and the WSGI server does not indicate that
        it terminates the stream, then no data is read to avoid an infinite
        stream.
        Each request defaults to the :data:`MAX_CONTENT_LENGTH` config, which
        defaults to ``None``. It can be set on a specific ``request`` to apply
        the limit to that specific view. This should be set appropriately based
        on an application's or view's specific needs.
        .. versionchanged:: 3.1
            This can be set per-request.
        .. versionchanged:: 0.6
            This is configurable through Flask config.
        if self._max_content_length is not None:
            return self._max_content_length
        if not current_app:
            return super().max_content_length
        return current_app.config["MAX_CONTENT_LENGTH"]  # type: ignore[no-any-return]
    @max_content_length.setter
    def max_content_length(self, value: int | None) -> None:
        self._max_content_length = value
    @property
    def max_form_memory_size(self) -> int | None:
        ``multipart/form-data`` body. If this limit is exceeded, a 413
        :exc:`~werkzeug.exceptions.RequestEntityTooLarge` error is raised. If it
        is set to ``None``, no limit is enforced at the Flask application level.
        Each request defaults to the :data:`MAX_FORM_MEMORY_SIZE` config, which
        defaults to ``500_000``. It can be set on a specific ``request`` to
        apply the limit to that specific view. This should be set appropriately
        based on an application's or view's specific needs.
        .. versionchanged:: 3.1
            This is configurable through Flask config.
        if self._max_form_memory_size is not None:
            return self._max_form_memory_size
        if not current_app:
            return super().max_form_memory_size
        return current_app.config["MAX_FORM_MEMORY_SIZE"]  # type: ignore[no-any-return]
    @max_form_memory_size.setter
    def max_form_memory_size(self, value: int | None) -> None:
        self._max_form_memory_size = value
    @property  # type: ignore[override]
    def max_form_parts(self) -> int | None:
        ``multipart/form-data`` body. If this limit is exceeded, a 413
        :exc:`~werkzeug.exceptions.RequestEntityTooLarge` error is raised. If it
        is set to ``None``, no limit is enforced at the Flask application level.
        Each request defaults to the :data:`MAX_FORM_PARTS` config, which
        defaults to ``1_000``. It can be set on a specific ``request`` to apply
        the limit to that specific view. This should be set appropriately based
        on an application's or view's specific needs.
        .. versionchanged:: 3.1
            This is configurable through Flask config.
        if self._max_form_parts is not None:
            return self._max_form_parts
        if not current_app:
            return super().max_form_parts
        return current_app.config["MAX_FORM_PARTS"]  # type: ignore[no-any-return]
    @max_form_parts.setter
    def max_form_parts(self, value: int | None) -> None:
        self._max_form_parts = value
from __future__ import annotations
from flask import Flask
from flask import Request
from flask import request
from flask.testing import FlaskClient
def test_max_content_length(app: Flask, client: FlaskClient) -> None:
    app.config["MAX_CONTENT_LENGTH"] = 50
    @app.post("/")
    def index():
        request.form["myfile"]
        AssertionError()
    @app.errorhandler(413)
    def catcher(error):
        return "42"
    rv = client.post("/", data={"myfile": "foo" * 50})
    assert rv.data == b"42"
def test_limit_config(app: Flask):
    app.config["MAX_CONTENT_LENGTH"] = 100
    app.config["MAX_FORM_MEMORY_SIZE"] = 50
    app.config["MAX_FORM_PARTS"] = 3
    r = Request({})
    # no app context, use Werkzeug defaults
    assert r.max_content_length is None
    assert r.max_form_memory_size == 500_000
    assert r.max_form_parts == 1_000
    # in app context, use config
    with app.app_context():
        assert r.max_content_length == 100
        assert r.max_form_memory_size == 50
        assert r.max_form_parts == 3
    # regardless of app context, use override
    r.max_content_length = 90
    r.max_form_memory_size = 30
    r.max_form_parts = 4
    assert r.max_content_length == 90
    assert r.max_form_memory_size == 30
    assert r.max_form_parts == 4
    with app.app_context():
        assert r.max_content_length == 90
        assert r.max_form_memory_size == 30
        assert r.max_form_parts == 4
            rv.headers.update(headers)
            key = key.removeprefix(prefix)
from functools import cache
@cache
                    if package_path.is_relative_to(location)
    if pathlib.PurePath(package_path).is_relative_to(py_prefix):
    list[t.Any],
HeaderValue = t.Union[str, list[str], tuple[str, ...]]
    t.Sequence[tuple[str, HeaderValue]],
    tuple[ResponseValue, HeadersValue],
    tuple[ResponseValue, int],
    tuple[ResponseValue, int, HeadersValue],
ShellContextProcessorCallable = t.Callable[[], dict[str, t.Any]]
    t.Callable[[], dict[str, t.Any]],
    t.Callable[[], t.Awaitable[dict[str, t.Any]]],
URLDefaultCallable = t.Callable[[str, dict[str, t.Any]], None]
    [t.Optional[str], t.Optional[dict[str, t.Any]]], None
        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
        return dataclasses.asdict(o)  # type: ignore[arg-type]
@t.overload
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr],
) -> t.Iterator[t.AnyStr]: ...
@t.overload
def stream_with_context(
    generator_or_function: t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]: ...
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
        return dataclasses.asdict(o)  # type: ignore[call-overload]
    def open_resource(
        self, resource: str, mode: str = "rb", encoding: str | None = None
    ) -> t.IO[t.AnyStr]:
        :param resource: Path to the resource relative to :attr:`root_path`.
        :param mode: Open the file in this mode. Only reading is supported,
            valid values are ``"r"`` (or ``"rt"``) and ``"rb"``.
        :param encoding: Open the file with this encoding when opening in text
            mode. This is ignored when opening in binary mode.
        .. versionchanged:: 3.1
            Added the ``encoding`` parameter.
        path = os.path.join(self.root_path, resource)
        if mode == "rb":
            return open(path, mode)
        return open(path, mode, encoding=encoding)
    def open_instance_resource(
        self, resource: str, mode: str = "rb", encoding: str | None = "utf-8"
    ) -> t.IO[t.AnyStr]:
        :attr:`instance_path`. Unlike :meth:`open_resource`, files in the
        instance folder can be opened for writing.
        :param resource: Path to the resource relative to :attr:`instance_path`.
        :param mode: Open the file in this mode.
        :param encoding: Open the file with this encoding when opening in text
            mode. This is ignored when opening in binary mode.
        .. versionchanged:: 3.1
            Added the ``encoding`` parameter.
        path = os.path.join(self.instance_path, resource)
        if "b" in mode:
            return open(path, mode)
        return open(path, mode, encoding=encoding)
    def open_resource(
        self, resource: str, mode: str = "rb", encoding: str | None = "utf-8"
    ) -> t.IO[t.AnyStr]:
        blueprint-relative equivalent of the app's :meth:`~.Flask.open_resource`
        method.
        :param resource: Path to the resource relative to :attr:`root_path`.
        :param mode: Open the file in this mode. Only reading is supported,
            valid values are ``"r"`` (or ``"rt"``) and ``"rb"``.
        :param encoding: Open the file with this encoding when opening in text
            mode. This is ignored when opening in binary mode.
        .. versionchanged:: 3.1
            Added the ``encoding`` parameter.
        path = os.path.join(self.root_path, resource)
        if mode == "rb":
            return open(path, mode)
        return open(path, mode, encoding=encoding)
@pytest.mark.parametrize("mode", ("r", "rb", "rt"))
def test_open_resource(mode):
    app = flask.Flask(__name__)
    with app.open_resource("static/index.html", mode) as f:
        assert "<h1>Hello World!</h1>" in str(f.read())
@pytest.mark.parametrize("mode", ("w", "x", "a", "r+"))
def test_open_resource_exceptions(mode):
    app = flask.Flask(__name__)
    with pytest.raises(ValueError):
        app.open_resource("static/index.html", mode)
@pytest.mark.parametrize("encoding", ("utf-8", "utf-16-le"))
def test_open_resource_with_encoding(tmp_path, encoding):
    app = flask.Flask(__name__, root_path=os.fspath(tmp_path))
    (tmp_path / "test").write_text("test", encoding=encoding)
    with app.open_resource("test", mode="rt", encoding=encoding) as f:
        assert f.read() == "test"
        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type, return-value]
        val = self.get_signing_serializer(app).dumps(dict(session))  # type: ignore[union-attr]
            val,
            return self.url_rule.endpoint  # type: ignore[no-any-return]
def _lazy_sha1(string: bytes = b"") -> t.Any:
    SHA-1, in which case the import and use as a default would fail before the
    developer can configure something else.
    return hashlib.sha1(string)
    digest_method = staticmethod(_lazy_sha1)
default_role = "code"
    "sphinx.ext.extlinks",
    "pallets_sphinx_themes",
autodoc_member_order = "bysource"
autodoc_preserve_defaults = True
extlinks = {
    "issue": ("https://github.com/pallets/flask/issues/%s", "#%s"),
    "pr": ("https://github.com/pallets/flask/pull/%s", "#%s"),
}
) -> Flask: ...
) -> Flask | None: ...
    def __get__(self, obj: None, owner: None) -> te.Self: ...
    def __get__(self, obj: App, owner: type[App]) -> T: ...
    test_uuid = uuid.UUID(bytes=b"\xde\xad\xbe\xef" * 4)
def before_sync() -> None: ...
async def before_async() -> None: ...
def teardown_sync(exc: BaseException | None) -> None: ...
async def teardown_async(exc: BaseException | None) -> None: ...
    f: ft.AfterRequestCallable[t.Any],
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
    def _untag_scan(self, value: t.Any) -> t.Any:
        if isinstance(value, dict):
            # untag each item recursively
            value = {k: self._untag_scan(v) for k, v in value.items()}
            # untag the dict itself
            value = self.untag(value)
        elif isinstance(value, list):
            # untag each item recursively
            value = [self._untag_scan(item) for item in value]
        return value
        return self._untag_scan(loads(value))
from . import app
    from . import db
    from . import auth
    from . import blog
from .db import get_db
from .auth import login_required
from .db import get_db
                        rv,  # type: ignore[arg-type]
                        request.environ,
        self,
        exc: BaseException | None = _sentinel,  # type: ignore[assignment]
        self,
        exc: BaseException | None = _sentinel,  # type: ignore[assignment]
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]]
    default: t.Callable[[t.Any], t.Any] = staticmethod(_default)  # type: ignore[assignment]
    from .blueprints import Blueprint
            location,
            code=code,
            Response=self.response_class,  # type: ignore[arg-type]
    from .wrappers import Request
    from .wrappers import Response
        raise ZeroDivisionError
    with app.app_context():
        called.append(flask.current_app.name)
    from werkzeug.routing import Rule
    from werkzeug.routing import Submount
    from werkzeug.routing import Rule
    from werkzeug.routing import Submount
        assert type(s["b"]) is bytes  # noqa: E721
        assert type(s["m"]) is Markup  # noqa: E721
        raise ZeroDivisionError
        raise ZeroDivisionError
        raise ZeroDivisionError
            raise ZeroDivisionError
            raise ZeroDivisionError
        raise ZeroDivisionError
    def template_string():
        return flask.render_template_string(
            "{% if notanswer %}{{ notanswer }} is not the answer. {% endif %}"
            "{% if answer %}{{ answer }} is the answer.{% endif %}"
        )
        raise ZeroDivisionError
        raise ZeroDivisionError
        raise ZeroDivisionError
    with client:
    with pytest.raises(RuntimeError):
        flask.g.value  # noqa: B018
            raise ZeroDivisionError
            raise ZeroDivisionError
def teardown_sync(exc: BaseException | None) -> None:
async def teardown_async(exc: BaseException | None) -> None:
def hello_json_dict() -> dict[str, t.Any]:
def hello_json_list() -> list[t.Any]:
from __future__ import annotations
import typing as t
def __getattr__(name: str) -> t.Any:
    if name == "__version__":
        import importlib.metadata
        import warnings
        warnings.warn(
            "The '__version__' attribute is deprecated and will be removed in"
            " Flask 3.1. Use feature detection or"
            " 'importlib.metadata.version(\"flask\")' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return importlib.metadata.version("flask")
    raise AttributeError(name)
import importlib.metadata
    flask_version = importlib.metadata.version("flask")
    werkzeug_version = importlib.metadata.version("werkzeug")
        f"Flask {flask_version}\n"
        f"Werkzeug {werkzeug_version}",
import importlib.metadata
_werkzeug_version = ""
def _get_werkzeug_version() -> str:
    global _werkzeug_version
    if not _werkzeug_version:
        _werkzeug_version = importlib.metadata.version("werkzeug")
    return _werkzeug_version
            "HTTP_USER_AGENT": f"Werkzeug/{_get_werkzeug_version()}",
import importlib.metadata
import platform
    assert f"Python {platform.python_version()}" in out
    assert f"Flask {importlib.metadata.version('flask')}" in out
    assert f"Werkzeug {importlib.metadata.version('werkzeug')}" in out
import importlib.metadata
def test_environ_base_default(app, client):
        flask.g.remote_addr = flask.request.remote_addr
        flask.g.user_agent = flask.request.user_agent.string
        return ""
    with client:
        client.get("/")
        assert flask.g.remote_addr == "127.0.0.1"
        assert flask.g.user_agent == (
            f"Werkzeug/{importlib.metadata.version('werkzeug')}"
        )
def test_environ_base_modified(app, client):
        flask.g.remote_addr = flask.request.remote_addr
        flask.g.user_agent = flask.request.user_agent.string
        return ""
    client.environ_base["REMOTE_ADDR"] = "192.168.0.22"
    with client:
        client.get("/")
        assert flask.g.remote_addr == "192.168.0.22"
        assert flask.g.user_agent == "Foo"
        removed because it was unreliable. Pass a filename if you are
__version__ = "3.0.0.dev"
        assert type(s["b"]) is bytes
        assert type(s["m"]) is Markup
        assert type(exc) is ZeroDivisionError
        assert type(exc) is ZeroDivisionError
        assert type(s["b"]) is bytes
        assert type(s["m"]) is Markup
        assert type(exc) is ZeroDivisionError
        assert type(exc) is ZeroDivisionError
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            raise ValueError
    except (ImportError, ValueError):
        loader = None
    else:
        loader = spec.loader
    if loader is None:
        # ImportError: the machinery told us it does not exist
        # ValueError:
        #    - the module name was invalid
        #    - the module name is __main__
        #    - we raised `ValueError` due to `root_spec` being `None`
    if root_spec.origin in {"namespace", None}:
        # namespace package
        package_spec = importlib.util.find_spec(import_name)
        if package_spec is not None and package_spec.submodule_search_locations:
            # Pick the path in the namespace that contains the submodule.
            package_path = pathlib.Path(
                os.path.commonpath(package_spec.submodule_search_locations)
            )
            search_location = next(
                location
                for location in root_spec.submodule_search_locations
                if _path_is_relative_to(package_path, location)
            )
        else:
            # Pick the first path.
            search_location = root_spec.submodule_search_locations[0]
        return os.path.dirname(search_location)
    elif root_spec.submodule_search_locations:
        # package with __init__.py
        return os.path.dirname(os.path.dirname(root_spec.origin))
    else:
        # module
        return os.path.dirname(root_spec.origin)
import importlib.util
    spec = importlib.util.find_spec(import_name)
    loader = spec.loader if spec is not None else None
    spec = importlib.util.find_spec(root_mod_name)
    loader = spec.loader if spec is not None else None
__version__ = "2.3.3.dev"
def modules_tmp_path(tmp_path, monkeypatch):
    rv = tmp_path / "modules_tmp"
    rv.mkdir()
    monkeypatch.syspath_prepend(os.fspath(rv))
def modules_tmp_path_prefix(modules_tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "prefix", os.fspath(modules_tmp_path))
    return modules_tmp_path
def site_packages(modules_tmp_path, monkeypatch):
    py_dir = f"python{sys.version_info.major}.{sys.version_info.minor}"
    rv = modules_tmp_path / "lib" / py_dir / "site-packages"
    rv.mkdir(parents=True)
    monkeypatch.syspath_prepend(os.fspath(rv))
def test_from_pyfile_weird_encoding(tmp_path, encoding):
    f = tmp_path / "my_config.py"
    f.write_text(f'# -*- coding: {encoding} -*-\nTEST_VALUE = "föö"\n', encoding)
    app.config.from_pyfile(os.fspath(f))
    def test_name_with_import_error(self, modules_tmp_path):
        (modules_tmp_path / "importerror.py").write_text("raise NotImplementedError()")
import os
def test_explicit_instance_paths(modules_tmp_path):
    with pytest.raises(ValueError, match=".*must be absolute"):
    app = flask.Flask(__name__, instance_path=os.fspath(modules_tmp_path))
    assert app.instance_path == os.fspath(modules_tmp_path)
def test_uninstalled_module_paths(modules_tmp_path, purge_module):
    (modules_tmp_path / "config_module_app.py").write_text(
    assert app.instance_path == os.fspath(modules_tmp_path / "instance")
def test_uninstalled_package_paths(modules_tmp_path, purge_module):
    app = modules_tmp_path / "config_package_app"
    app.mkdir()
    (app / "__init__.py").write_text(
    assert app.instance_path == os.fspath(modules_tmp_path / "instance")
def test_uninstalled_namespace_paths(tmp_path, monkeypatch, purge_module):
        project = tmp_path / f"project-{package}"
        monkeypatch.syspath_prepend(os.fspath(project))
        ns = project / "namespace" / package
        ns.mkdir(parents=True)
        (ns / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    assert app.instance_path == os.fspath(project2 / "instance")
    modules_tmp_path, modules_tmp_path_prefix, purge_module, site_packages, limit_loader
    (site_packages / "site_app.py").write_text(
    assert app.instance_path == os.fspath(
        modules_tmp_path / "var" / "site_app-instance"
    )
    limit_loader, modules_tmp_path, modules_tmp_path_prefix, purge_module, monkeypatch
    installed_path = modules_tmp_path / "path"
    installed_path.mkdir()
    app = installed_path / "installed_package"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    assert app.instance_path == os.fspath(
        modules_tmp_path / "var" / "installed_package-instance"
    limit_loader, modules_tmp_path, modules_tmp_path_prefix, purge_module, site_packages
    app = site_packages / "site_package"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    assert site_package.app.instance_path == os.fspath(
        modules_tmp_path / "var" / "site_package-instance"
        # zipimporter's loader.archive points to the .zip file.
__version__ = "2.3.2"
        if self._cookies is None:
        self._add_cookies_to_wsgi(ctx.request.environ)
        self._update_cookies_from_response(
            ctx.request.host.partition(":")[0],
            ctx.request.path,
            resp.headers.getlist("Set-Cookie"),
        )
        # Add a "Vary: Cookie" header if the session was accessed at all.
        if session.accessed:
            response.vary.add("Cookie")
                response.vary.add("Cookie")
        response.vary.add("Cookie")
    @app.route("/clear")
    def clear():
        flask.session.clear()
        return ""
    expect("/clear")
def test_session_refresh_vary(app, client):
    @app.get("/login")
    def login():
        flask.session["user_id"] = 1
        flask.session.permanent = True
        return ""
    @app.get("/ignored")
    def ignored():
        return ""
    rv = client.get("/login")
    assert rv.headers["Vary"] == "Cookie"
    rv = client.get("/ignored")
    assert rv.headers["Vary"] == "Cookie"
            rv.headers.update(headers)  # type: ignore[arg-type]
__version__ = "2.3.2.dev"
__version__ = "2.3.1"
__version__ = "2.3.1.dev"
__version__ = "2.3.0"
            rv.headers.update(headers)
html_favicon = "_static/shortcut-icon.png"
html_logo = "_static/flask-vertical.png"
from inspect import iscoroutinefunction
    def raise_routing_exception(self, request: Request) -> t.NoReturn:
def abort(code: int | BaseResponse, *args: t.Any, **kwargs: t.Any) -> t.NoReturn:
    def _fail(self, *args: t.Any, **kwargs: t.Any) -> t.NoReturn:
class StatusJSON(t.TypedDict):
from __future__ import annotations
def _make_timedelta(value: timedelta | int | None) -> timedelta | None:
    json_provider_class: type[JSONProvider] = DefaultJSONProvider
    test_client_class: type[FlaskClient] | None = None
    test_cli_runner_class: type[FlaskCliRunner] | None = None
        static_url_path: str | None = None,
        static_folder: str | os.PathLike | None = "static",
        static_host: str | None = None,
        template_folder: str | os.PathLike | None = "templates",
        instance_path: str | None = None,
        root_path: str | None = None,
        self.url_build_error_handlers: list[
            t.Callable[[Exception, str, dict[str, t.Any]], str]
        self.teardown_appcontext_funcs: list[ft.TeardownCallable] = []
        self.shell_context_processors: list[ft.ShellContextProcessorCallable] = []
        self.blueprints: dict[str, Blueprint] = {}
        names: t.Iterable[str | None] = (None,)
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
    def test_client(self, use_cookies: bool = True, **kwargs: t.Any) -> FlaskClient:
    def test_cli_runner(self, **kwargs: t.Any) -> FlaskCliRunner:
    def register_blueprint(self, blueprint: Blueprint, **options: t.Any) -> None:
    def iter_blueprints(self) -> t.ValuesView[Blueprint]:
        endpoint: str | None = None,
        view_func: ft.RouteCallable | None = None,
        provide_automatic_options: bool | None = None,
        self, name: str | None = None
        self, f: ft.TemplateFilterCallable, name: str | None = None
        self, name: str | None = None
        self, f: ft.TemplateTestCallable, name: str | None = None
        self, name: str | None = None
        self, f: ft.TemplateGlobalCallable, name: str | None = None
    def _find_error_handler(self, e: Exception) -> ft.ErrorHandlerCallable | None:
    ) -> HTTPException | ft.ResponseReturnValue:
    ) -> HTTPException | ft.ResponseReturnValue:
        server_error: InternalServerError | ft.ResponseReturnValue
        exc_info: (tuple[type, BaseException, TracebackType] | tuple[None, None, None]),
    def raise_routing_exception(self, request: Request) -> te.NoReturn:
        view_args: dict[str, t.Any] = req.view_args  # type: ignore[assignment]
        rv: ft.ResponseReturnValue | HTTPException,
    def should_ignore_error(self, error: BaseException | None) -> bool:
        _anchor: str | None = None,
        _method: str | None = None,
        _scheme: str | None = None,
        _external: bool | None = None,
    def create_url_adapter(self, request: Request | None) -> MapAdapter | None:
        names: t.Iterable[str | None] = (None,)
        self, error: BuildError, endpoint: str, values: dict[str, t.Any]
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        self, exc: BaseException | None = _sentinel  # type: ignore
        self, exc: BaseException | None = _sentinel  # type: ignore
        error: BaseException | None = None
from __future__ import annotations
        blueprint: Blueprint,
        app: Flask,
        endpoint: str | None = None,
        view_func: t.Callable | None = None,
        static_folder: str | os.PathLike | None = None,
        static_url_path: str | None = None,
        template_folder: str | os.PathLike | None = None,
        url_prefix: str | None = None,
        subdomain: str | None = None,
        url_defaults: dict | None = None,
        root_path: str | None = None,
        cli_group: str | None = _sentinel,  # type: ignore
        self.deferred_functions: list[DeferredSetupFunction] = []
        self._blueprints: list[tuple[Blueprint, dict]] = []
        self, app: Flask, options: dict, first_registration: bool = False
    def register_blueprint(self, blueprint: Blueprint, **options: t.Any) -> None:
    def register(self, app: Flask, options: dict) -> None:
        endpoint: str | None = None,
        view_func: ft.RouteCallable | None = None,
        provide_automatic_options: bool | None = None,
        self, name: str | None = None
        self, f: ft.TemplateFilterCallable, name: str | None = None
        self, name: str | None = None
        self, f: ft.TemplateTestCallable, name: str | None = None
        self, name: str | None = None
        self, f: ft.TemplateGlobalCallable, name: str | None = None
        self, code: type[Exception] | int
        self.data: dict[t.Any, t.Any] = {}
from __future__ import annotations
    def __init__(self, name: str, get_converter: t.Callable | None = None) -> None:
    def __init__(self, root_path: str, defaults: dict | None = None) -> None:
    def from_object(self, obj: object | str) -> None:
        self, mapping: t.Mapping[str, t.Any] | None = None, **kwargs: t.Any
        mappings: dict[str, t.Any] = {}
    ) -> dict[str, t.Any]:
from __future__ import annotations
    def get(self, name: str, default: t.Any | None = None) -> t.Any:
    def __init__(self, app: Flask) -> None:
        self._cv_tokens: list[contextvars.Token] = []
    def pop(self, exc: BaseException | None = _sentinel) -> None:  # type: ignore
    def __enter__(self) -> AppContext:
        exc_type: type | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
        app: Flask,
        request: Request | None = None,
        session: SessionMixin | None = None,
        self.flashes: list[tuple[str, str]] | None = None
        self.session: SessionMixin | None = session
        self._after_request_functions: list[ft.AfterRequestCallable] = []
        self._cv_tokens: list[tuple[contextvars.Token, AppContext | None]] = []
    def copy(self) -> RequestContext:
    def pop(self, exc: BaseException | None = _sentinel) -> None:  # type: ignore
    def __enter__(self) -> RequestContext:
        exc_type: type | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
from __future__ import annotations
from __future__ import annotations
    def top(self) -> t.Any | None:
_cv_app: ContextVar[AppContext] = ContextVar("flask.app_ctx")
app_ctx: AppContext = LocalProxy(  # type: ignore[assignment]
current_app: Flask = LocalProxy(  # type: ignore[assignment]
g: _AppCtxGlobals = LocalProxy(  # type: ignore[assignment]
_cv_request: ContextVar[RequestContext] = ContextVar("flask.request_ctx")
request_ctx: RequestContext = LocalProxy(  # type: ignore[assignment]
request: Request = LocalProxy(  # type: ignore[assignment]
session: SessionMixin = LocalProxy(  # type: ignore[assignment]
from __future__ import annotations
    generator_or_function: (
        t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]]
    )
def make_response(*args: t.Any) -> Response:
    _anchor: str | None = None,
    _method: str | None = None,
    _scheme: str | None = None,
    _external: bool | None = None,
    location: str, code: int = 302, Response: type[BaseResponse] | None = None
) -> BaseResponse:
def abort(code: int | BaseResponse, *args: t.Any, **kwargs: t.Any) -> te.NoReturn:
) -> list[str] | list[tuple[str, str]]:
def _prepare_send_file_kwargs(**kwargs: t.Any) -> dict[str, t.Any]:
    path_or_file: os.PathLike | str | t.BinaryIO,
    mimetype: str | None = None,
    download_name: str | None = None,
    etag: bool | str = True,
    last_modified: datetime | int | float | None = None,
    max_age: None | (int | t.Callable[[str | None], int | None]) = None,
) -> Response:
    directory: os.PathLike | str,
    path: os.PathLike | str,
) -> Response:
        name: str | None = None,
        doc: str | None = None,
def _split_blueprint_path(name: str) -> list[str]:
    out: list[str] = [name]
        self, args: tuple[t.Any, ...], kwargs: dict[str, t.Any]
        dump_args: dict[str, t.Any] = {}
from __future__ import annotations
    key: str | None = None
    def __init__(self, serializer: TaggedJSONSerializer) -> None:
        self.tags: dict[str, JSONTag] = {}
        self.order: list[JSONTag] = []
        tag_class: type[JSONTag],
        index: int | None = None,
    def tag(self, value: t.Any) -> dict[str, t.Any]:
    def untag(self, value: dict[str, t.Any]) -> t.Any:
from __future__ import annotations
def create_logger(app: Flask) -> logging.Logger:
from __future__ import annotations
    _static_folder: str | None = None
    _static_url_path: str | None = None
        static_folder: str | os.PathLike | None = None,
        static_url_path: str | None = None,
        template_folder: str | os.PathLike | None = None,
        root_path: str | None = None,
        self.view_functions: dict[str, t.Callable] = {}
        self.error_handler_spec: dict[
            dict[int | None, dict[type[Exception], ft.ErrorHandlerCallable]],
        self.before_request_funcs: dict[
            ft.AppOrBlueprintKey, list[ft.BeforeRequestCallable]
        self.after_request_funcs: dict[
            ft.AppOrBlueprintKey, list[ft.AfterRequestCallable]
        self.teardown_request_funcs: dict[
            ft.AppOrBlueprintKey, list[ft.TeardownCallable]
        self.template_context_processors: dict[
            ft.AppOrBlueprintKey, list[ft.TemplateContextProcessorCallable]
        self.url_value_preprocessors: dict[
            list[ft.URLValuePreprocessorCallable],
        self.url_default_functions: dict[
            ft.AppOrBlueprintKey, list[ft.URLDefaultCallable]
    def static_folder(self) -> str | None:
    def static_folder(self, value: str | os.PathLike | None) -> None:
    def static_url_path(self) -> str | None:
    def static_url_path(self, value: str | None) -> None:
    def get_send_file_max_age(self, filename: str | None) -> int | None:
    def send_static_file(self, filename: str) -> Response:
    def jinja_loader(self) -> FileSystemLoader | None:
        endpoint: str | None = None,
        view_func: ft.RouteCallable | None = None,
        provide_automatic_options: bool | None = None,
        self, code_or_exception: type[Exception] | int
        code_or_exception: type[Exception] | int,
        exc_class_or_code: type[Exception] | int,
    ) -> tuple[type[Exception], int | None]:
        exc_class: type[Exception]
from __future__ import annotations
    def _fail(self, *args: t.Any, **kwargs: t.Any) -> te.NoReturn:
    def make_null_session(self, app: Flask) -> NullSession:
    def get_cookie_name(self, app: Flask) -> str:
    def get_cookie_domain(self, app: Flask) -> str | None:
    def get_cookie_path(self, app: Flask) -> str:
    def get_cookie_httponly(self, app: Flask) -> bool:
    def get_cookie_secure(self, app: Flask) -> bool:
    def get_cookie_samesite(self, app: Flask) -> str:
    def get_expiration_time(self, app: Flask, session: SessionMixin) -> datetime | None:
    def should_set_cookie(self, app: Flask, session: SessionMixin) -> bool:
    def open_session(self, app: Flask, request: Request) -> SessionMixin | None:
        self, app: Flask, session: SessionMixin, response: Response
    def get_signing_serializer(self, app: Flask) -> URLSafeTimedSerializer | None:
    def open_session(self, app: Flask, request: Request) -> SecureCookieSession | None:
        self, app: Flask, session: SessionMixin, response: Response
from __future__ import annotations
def _default_template_ctx_processor() -> dict[str, t.Any]:
    rv: dict[str, t.Any] = {}
    def __init__(self, app: Flask, **options: t.Any) -> None:
    def __init__(self, app: Flask) -> None:
    ) -> tuple[str, str | None, t.Callable | None]:
    ) -> tuple[str, str | None, t.Callable | None]:
        rv: tuple[str, str | None, t.Callable[[], bool] | None] | None
        trv: None | (tuple[str, str | None, t.Callable[[], bool] | None]) = None
    ) -> tuple[str, str | None, t.Callable | None]:
    ) -> t.Generator[tuple[Scaffold, BaseLoader], None, None]:
    def list_templates(self) -> list[str]:
def _render(app: Flask, template: Template, context: dict[str, t.Any]) -> str:
    template_name_or_list: str | Template | list[str | Template],
    app: Flask, template: Template, context: dict[str, t.Any]
    template_name_or_list: str | Template | list[str | Template],
from __future__ import annotations
        app: Flask,
        base_url: str | None = None,
        subdomain: str | None = None,
        url_scheme: str | None = None,
    application: Flask
        self._new_contexts: list[t.ContextManager[t.Any]] = []
    ) -> TestResponse:
    def __enter__(self) -> FlaskClient:
        exc_type: type | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    def __init__(self, app: Flask, **kwargs: t.Any) -> None:
from __future__ import annotations
from __future__ import annotations
    methods: t.ClassVar[t.Collection[str] | None] = None
    provide_automatic_options: t.ClassVar[bool | None] = None
    decorators: t.ClassVar[list[t.Callable]] = []
from __future__ import annotations
    url_rule: Rule | None = None
    view_args: dict[str, t.Any] | None = None
    routing_exception: Exception | None = None
    def max_content_length(self) -> int | None:  # type: ignore
    def endpoint(self) -> str | None:
    def blueprint(self) -> str | None:
    def blueprints(self) -> list[str]:
    def on_json_loading_failed(self, e: ValueError | None) -> t.Any:
    default_mimetype: str | None = "text/html"
from operator import itemgetter
    type=click.Choice(("endpoint", "methods", "domain", "rule", "match")),
        "Method to sort routes by. 'match' is the order that Flask will match routes"
        " when dispatching a request."
    ignored_methods = set() if all_methods else {"HEAD", "OPTIONS"}
    host_matching = current_app.url_map.host_matching
    has_domain = any(rule.host if host_matching else rule.subdomain for rule in rules)
    rows = []
    for rule in rules:
        row = [
            rule.endpoint,
            ", ".join(sorted((rule.methods or set()) - ignored_methods)),
        ]
        if has_domain:
            row.append((rule.host if host_matching else rule.subdomain) or "")
        row.append(rule.rule)
        rows.append(row)
    headers = ["Endpoint", "Methods"]
    sorts = ["endpoint", "methods"]
    if has_domain:
        headers.append("Host" if host_matching else "Subdomain")
        sorts.append("domain")
    headers.append("Rule")
    sorts.append("rule")
    try:
        rows.sort(key=itemgetter(sorts.index(sort)))
    except ValueError:
        pass
    rows.insert(0, headers)
    widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    rows.insert(1, ["-" * w for w in widths])
    template = "  ".join(f"{{{i}:<{w}}}" for i, w in enumerate(widths))
    for row in rows:
        click.echo(template.format(*row))
        app.add_url_rule(
            "/get_post/<int:x>/<int:y>",
            methods=["GET", "POST"],
            endpoint="yyy_get_post",
        )
        app.add_url_rule("/zzz_post", methods=["POST"], endpoint="aaa_post")
    def test_no_routes(self, runner):
        app = Flask(__name__, static_folder=None)
        cli = FlaskGroup(create_app=lambda: app)
        result = runner.invoke(cli, ["routes"])
    def test_subdomain(self, runner):
        app = Flask(__name__, static_folder=None)
        app.add_url_rule("/a", subdomain="a", endpoint="a")
        app.add_url_rule("/b", subdomain="b", endpoint="b")
        cli = FlaskGroup(create_app=lambda: app)
        result = runner.invoke(cli, ["routes"])
        assert result.exit_code == 0
        assert "Subdomain" in result.output
    def test_host(self, runner):
        app = Flask(__name__, static_folder=None, host_matching=True)
        app.add_url_rule("/a", host="a", endpoint="a")
        app.add_url_rule("/b", host="b", endpoint="b")
        cli = FlaskGroup(create_app=lambda: app)
        result = runner.invoke(cli, ["routes"])
        assert result.exit_code == 0
        assert "Host" in result.output
    if name == "signals_available":
        import warnings
        warnings.warn(
            "'signals_available' is deprecated and will be removed in Flask 2.4."
            " Signals are always available",
            DeprecationWarning,
            stacklevel=2,
        )
        return True
from __future__ import annotations
import typing as t
import warnings
from blinker import Namespace
# This namespace is only for signals provided by Flask itself.
def __getattr__(name: str) -> t.Any:
    if name == "signals_available":
        warnings.warn(
            "The 'signals_available' attribute is deprecated and will be removed in"
            " Flask 2.4. Signals are always available.",
            DeprecationWarning,
            stacklevel=2,
        )
        return True
    raise AttributeError(name)
import warnings
    .. deprecated:: 2.3
        Will be removed in Flask 2.4.
    warnings.warn(
        "The 'is_ip' function is deprecated and will be removed in Flask 2.4.",
        DeprecationWarning,
        stacklevel=2,
    )
        browsers will only send the cookie to the exact domain it was set from.
        Otherwise, they will send it to any subdomain of the given value as well.
        Uses the :data:`SESSION_COOKIE_DOMAIN` config.
        .. versionchanged:: 2.3
            Not set by default, does not fall back to ``SERVER_NAME``.
        return rv if rv else None
def test_session_path(app, client):
    app.config.update(APPLICATION_ROOT="/foo")
        # new cookie interface for Werkzeug >= 2.3
        cookie_storage = self._cookies if hasattr(self, "_cookies") else self.cookie_jar
        if cookie_storage is None:
            raise TypeError(
                "Cookies are disabled. Create a client with 'use_cookies=True'."
        ctx = app.test_request_context(*args, **kwargs)
        if hasattr(self, "_add_cookies_to_wsgi"):
            self._add_cookies_to_wsgi(ctx.request.environ)
        else:
            self.cookie_jar.inject_wsgi(ctx.request.environ)  # type: ignore[union-attr]
        with ctx:
            sess = app.session_interface.open_session(app, ctx.request)
        if sess is None:
            raise RuntimeError("Session backend did not open a session.")
        yield sess
        resp = app.response_class()
        if app.session_interface.is_null_session(sess):
            return
        with ctx:
            app.session_interface.save_session(app, sess, resp)
        if hasattr(self, "_update_cookies_from_response"):
            self._update_cookies_from_response(
                ctx.request.host.partition(":")[0], resp.headers.getlist("Set-Cookie")
            )
        else:
            self.cookie_jar.extract_wsgi(  # type: ignore[union-attr]
                ctx.request.environ, resp.headers
            )
    cookie = rv.headers["set-cookie"].lower()
    # or condition for Werkzeug < 2.3
    assert "domain=example.com" in cookie or "domain=.example.com" in cookie
    cookie = rv.headers["set-cookie"].lower()
    # or condition for Werkzeug < 2.3
    assert "domain=example.com" in cookie or "domain=.example.com" in cookie
    # or condition for Werkzeug < 2.3
    assert "domain=example.com" in cookie or "domain=.example.com" in cookie
    # or condition for Werkzeug < 2.3
    assert "domain=example.com" in cookie or "domain=.example.com" in cookie
    with pytest.raises(TypeError, match="Cookies are disabled."):
from urllib.parse import quote as _url_quote
            _anchor = _url_quote(_anchor, safe="%!#$&'()*+,/:;=?@")
            rv = f"{rv}#{_anchor}"
from urllib.parse import urlsplit
            url = urlsplit(path)
from werkzeug.utils import cached_property
    @cached_property
    @cached_property
    @cached_property
    .. deprecated:: 2.3
        Will be removed in Flask 2.4. Use a lock inside the decorated function if
        locking is needed.
        import warnings
        warnings.warn(
            "'locked_cached_property' is deprecated and will be removed in Flask 2.4."
            " Use a lock inside the decorated function if locking is needed.",
            DeprecationWarning,
            stacklevel=2,
        )
from werkzeug.utils import cached_property
    @cached_property
            raise AssertionError(
                f"The setup method '{f_name}' can no longer be called on the blueprint"
                f" '{self.name}'. It has already been registered at least once, any"
                " changes will not be applied consistently.\n"
                "Make sure all imports, decorators, functions, etc. needed to set up"
                " the blueprint are done before registering it."
        .. deprecated:: 2.3
            Will be removed in Flask 2.4.
        import warnings
        warnings.warn(
            "'got_first_request' is deprecated and will be removed in Flask 2.4.",
            DeprecationWarning,
            stacklevel=2,
        )
    if name == "escape":
        import warnings
        from markupsafe import escape
        warnings.warn(
            "'flask.escape' is deprecated and will be removed in Flask 2.4. Import"
            " 'markupsafe.escape' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return escape
    if name == "escape":
        import warnings
        from markupsafe import Markup
        warnings.warn(
            "'flask.Markup' is deprecated and will be removed in Flask 2.4. Import"
            " 'markupsafe.Markup' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return Markup
from markupsafe import Markup
        flask.session["m"] = Markup("<html>")
        assert type(s["m"]) == Markup
        assert s["m"] == Markup("<html>")
        flask.flash(Markup("<em>Testing</em>"), "warning")
            Markup("<em>Testing</em>"),
            ("warning", Markup("<em>Testing</em>")),
            ("warning", Markup("<em>Testing</em>")),
        assert messages[1] == Markup("<em>Testing</em>")
from markupsafe import Markup
from markupsafe import Markup
            "escaping_template.html", text=text, html=Markup(text)
            "non_escaping_template.txt", text=text, html=Markup(text)
            "'_app_ctx_stack' is deprecated and will be removed in Flask 2.4.",
            "'_request_ctx_stack' is deprecated and will be removed in Flask 2.4.",
            # if set, env var overrides existing value
            if "FLASK_DEBUG" in os.environ:
        If :data:`PROPAGATE_EXCEPTIONS` is ``True``, such as in debug
        self._got_first_request = True
        .. versionchanged:: 2.1
            Registering the same blueprint with the same name multiple
            times is an error.
    @property
    def top(self) -> t.Optional[t.Any]:
            f"'_{self.name}_ctx_stack' is deprecated and will be removed in Flask 2.4."
            f" Use 'g' to store data, or '{self.name}_ctx' to access the current"
            " context.",
            stacklevel=2,
            "'_app_ctx_stack' is deprecated and will be removed in Flask 2.4.",
            "'_request_ctx_stack' is deprecated and will be removed in Flask 2.4.",
    return bool(val and val.lower() not in {"0", "false", "no"})
def dumps(obj: t.Any, **kwargs: t.Any) -> str:
    .. versionchanged:: 2.3
        The ``app`` parameter was removed.
    if current_app:
        return current_app.json.dumps(obj, **kwargs)
def dump(obj: t.Any, fp: t.IO[str], **kwargs: t.Any) -> None:
    .. versionchanged:: 2.3
        The ``app`` parameter was removed.
    if current_app:
        current_app.json.dump(obj, fp, **kwargs)
def loads(s: str | bytes, **kwargs: t.Any) -> t.Any:
    .. versionchanged:: 2.3
        The ``app`` parameter was removed.
    if current_app:
        return current_app.json.loads(s, **kwargs)
def load(fp: t.IO[t.AnyStr], **kwargs: t.Any) -> t.Any:
    .. versionchanged:: 2.3
        The ``app`` parameter was removed.
    if current_app:
        return current_app.json.load(fp, **kwargs)
        kwargs.setdefault("default", self.default)
        kwargs.setdefault("ensure_ascii", self.ensure_ascii)
        kwargs.setdefault("sort_keys", self.sort_keys)
        if (self.compact is None and self._app.debug) or self.compact is False:
            f"{self.dumps(obj, **dump_args)}\n", mimetype=self.mimetype
    assert evts == ["before", "after", "teardown"]
    assert evts == ["before", "after", "teardown"] * 2
        ("debug", "expect"),
            ("", False),
            ("0", False),
            ("False", False),
            ("No", False),
            ("True", True),
    def test_get_debug_flag(self, monkeypatch, debug, expect):
        assert get_debug_flag() == expect
            from .testing import FlaskClient as cls
            from .testing import FlaskCliRunner as cls
__version__ = "2.2.3"
    **context: t.Any,
    **context: t.Any,
        full documentation.
        The URL rule is prefixed with the blueprint's URL prefix. The endpoint name,
        used with :func:`url_for`, is prefixed with the blueprint's name.
        application. Equivalent to :meth:`.Flask.template_filter`.
        application. Works like the :meth:`app_template_filter` decorator. Equivalent to
        :meth:`.Flask.add_template_filter`.
        application. Equivalent to :meth:`.Flask.template_test`.
        application. Works like the :meth:`app_template_test` decorator. Equivalent to
        :meth:`.Flask.add_template_test`.
        application. Equivalent to :meth:`.Flask.template_global`.
        application. Works like the :meth:`app_template_global` decorator. Equivalent to
        :meth:`.Flask.add_template_global`.
        by the blueprint. Equivalent to :meth:`.Flask.before_request`.
        handled by the worker. Equivalent to :meth:`.Flask.before_first_request`.
        by the blueprint. Equivalent to :meth:`.Flask.after_request`.
        handled by the blueprint. Equivalent to :meth:`.Flask.teardown_request`.
        only by the blueprint. Equivalent to :meth:`.Flask.context_processor`.
        the blueprint. Equivalent to :meth:`.Flask.errorhandler`.
        handled by the blueprint. Equivalent to :meth:`.Flask.url_value_preprocessor`.
        the blueprint. Equivalent to :meth:`.Flask.url_defaults`.
        This is available on both app and blueprint objects. When used on an app, this
        executes before every request. When used on a blueprint, this executes before
        every request that the blueprint handles. To register with a blueprint and
        execute before every request, use :meth:`.Blueprint.before_app_request`.
        This is available on both app and blueprint objects. When used on an app, this
        executes after every request. When used on a blueprint, this executes after
        every request that the blueprint handles. To register with a blueprint and
        execute after every request, use :meth:`.Blueprint.after_app_request`.
        This is available on both app and blueprint objects. When used on an app, this
        executes after every request. When used on a blueprint, this executes after
        every request that the blueprint handles. To register with a blueprint and
        execute after every request, use :meth:`.Blueprint.teardown_app_request`.
        rendering a template. The keys of the returned dict are added as variables
        available in the template.
        This is available on both app and blueprint objects. When used on an app, this
        is called for every rendered template. When used on a blueprint, this is called
        for templates rendered from the blueprint's views. To register with a blueprint
        and affect every template, use :meth:`.Blueprint.app_context_processor`.
        This is available on both app and blueprint objects. When used on an app, this
        is called for every request. When used on a blueprint, this is called for
        requests that the blueprint handles. To register with a blueprint and affect
        every request, use :meth:`.Blueprint.app_url_value_preprocessor`.
        This is available on both app and blueprint objects. When used on an app, this
        is called for every request. When used on a blueprint, this is called for
        requests that the blueprint handles. To register with a blueprint and affect
        every request, use :meth:`.Blueprint.app_url_defaults`.
        This is available on both app and blueprint objects. When used on an app, this
        can handle errors from every request. When used on a blueprint, this can handle
        errors from requests that the blueprint handles. To register with a blueprint
        and affect every request, use :meth:`.Blueprint.app_errorhandler`.
from task_app import create_app
flask_app = create_app()
celery_app = flask_app.extensions["celery"]
from celery import Celery
from celery import Task
from flask import Flask
from flask import render_template
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    @app.route("/")
    def index() -> str:
        return render_template("index.html")
    from . import views
    app.register_blueprint(views.bp)
    return app
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
import time
from celery import shared_task
from celery import Task
@shared_task(ignore_result=False)
def add(a: int, b: int) -> int:
    return a + b
@shared_task()
def block() -> None:
    time.sleep(5)
@shared_task(bind=True, ignore_result=False)
def process(self: Task, total: int) -> object:
    for i in range(total):
        self.update_state(state="PROGRESS", meta={"current": i + 1, "total": total})
        time.sleep(1)
    return {"current": total, "total": total}
from celery.result import AsyncResult
from flask import Blueprint
from flask import request
from . import tasks
bp = Blueprint("tasks", __name__, url_prefix="/tasks")
@bp.get("/result/<id>")
def result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    ready = result.ready()
    return {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }
@bp.post("/add")
def add() -> dict[str, object]:
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = tasks.add.delay(a, b)
    return {"result_id": result.id}
@bp.post("/block")
def block() -> dict[str, object]:
    result = tasks.block.delay()
    return {"result_id": result.id}
@bp.post("/process")
def process() -> dict[str, object]:
    result = tasks.process.delay(total=request.form.get("total", type=int))
    return {"result_id": result.id}
from js_example import views  # noqa: E402, F401
        raise ValueError("dummy")
    with pytest.raises(ValueError, match="dummy"):
    assert isinstance(cleanup_stuff[0], ValueError)
from blueprintapp.apps.admin import admin  # noqa: E402
from blueprintapp.apps.frontend import frontend  # noqa: E402
    with pytest.raises(AssertionError):
    with pytest.raises(AssertionError):
from js_example import views  # noqa: E402, F401
from blueprintapp.apps.admin import admin  # noqa: E402
from blueprintapp.apps.frontend import frontend  # noqa: E402
        raise ValueError("dummy")
    with pytest.raises(ValueError, match="dummy"):
    assert isinstance(cleanup_stuff[0], ValueError)
    with pytest.raises(AssertionError):
    with pytest.raises(AssertionError):
    def json_encoder(self) -> t.Type[json.JSONEncoder]:
    def json_decoder(self) -> t.Type[json.JSONDecoder]:
    @property
    def json_encoder(
    @property
    def json_decoder(
            request.json_module = app.json
                    gen.close()
def abort(
        filepath = loader.get_filename(import_name)
        response.json_module = self.application.json  # type: ignore[assignment]
    json_module: t.Any = json
    return Response()
    return Response()
__version__ = "2.2.3"
__version__ = "2.2.2"
        "Werkzeug >= 2.2.2",
        f"App: {current_app.import_name}\n"
        defaults["ENV"] = os.environ.get("FLASK_ENV") or "production"
__version__ = "2.2.2.dev"
__version__ = "2.2.1"
import json
    _json_encoder: t.Union[t.Type[json.JSONEncoder], None] = None
    _json_decoder: t.Union[t.Type[json.JSONDecoder], None] = None
    @property  # type: ignore[override]
    def json_encoder(self) -> t.Type[json.JSONEncoder]:  # type: ignore[override]
        :class:`~flask.json.JSONEncoder`.
        .. deprecated:: 2.2
             Will be removed in Flask 2.3. Customize
             :attr:`json_provider_class` instead.
        .. versionadded:: 0.10
        import warnings
        warnings.warn(
            "'app.json_encoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        if self._json_encoder is None:
            from . import json
            return json.JSONEncoder
        return self._json_encoder
    @json_encoder.setter
    def json_encoder(self, value: t.Type[json.JSONEncoder]) -> None:
        import warnings
        warnings.warn(
            "'app.json_encoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._json_encoder = value
    @property  # type: ignore[override]
    def json_decoder(self) -> t.Type[json.JSONDecoder]:  # type: ignore[override]
        :class:`~flask.json.JSONDecoder`.
        .. deprecated:: 2.2
             Will be removed in Flask 2.3. Customize
             :attr:`json_provider_class` instead.
        .. versionadded:: 0.10
        import warnings
        warnings.warn(
            "'app.json_decoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        if self._json_decoder is None:
            from . import json
            return json.JSONDecoder
        return self._json_decoder
    @json_decoder.setter
    def json_decoder(self, value: t.Type[json.JSONDecoder]) -> None:
        import warnings
        warnings.warn(
            "'app.json_decoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._json_decoder = value
import json
    _json_encoder: t.Union[t.Type[json.JSONEncoder], None] = None
    _json_decoder: t.Union[t.Type[json.JSONDecoder], None] = None
    @property  # type: ignore[override]
    def json_encoder(  # type: ignore[override]
        self,
    ) -> t.Union[t.Type[json.JSONEncoder], None]:
        .. deprecated:: 2.2
             Will be removed in Flask 2.3. Customize
             :attr:`json_provider_class` instead.
        .. versionadded:: 0.10
        import warnings
        warnings.warn(
            "'bp.json_encoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._json_encoder
    @json_encoder.setter
    def json_encoder(self, value: t.Union[t.Type[json.JSONEncoder], None]) -> None:
        import warnings
        warnings.warn(
            "'bp.json_encoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._json_encoder = value
    @property  # type: ignore[override]
    def json_decoder(  # type: ignore[override]
        self,
    ) -> t.Union[t.Type[json.JSONDecoder], None]:
        .. deprecated:: 2.2
             Will be removed in Flask 2.3. Customize
             :attr:`json_provider_class` instead.
        .. versionadded:: 0.10
        import warnings
        warnings.warn(
            "'bp.json_decoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._json_decoder
    @json_decoder.setter
    def json_decoder(self, value: t.Union[t.Type[json.JSONDecoder], None]) -> None:
        import warnings
        warnings.warn(
            "'bp.json_decoder' is deprecated and will be removed in Flask 2.3."
            " Customize 'app.json_provider_class' or 'app.json' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._json_decoder = value
        cls = self._app._json_encoder
        if bp is not None and bp._json_encoder is not None:
            cls = bp._json_encoder
        cls = self._app._json_decoder
        if bp is not None and bp._json_decoder is not None:
            cls = bp._json_decoder
import json
    json_encoder: t.Union[t.Type[json.JSONEncoder], None] = None
    json_decoder: t.Union[t.Type[json.JSONDecoder], None] = None
__version__ = "2.2.1.dev"
__version__ = "2.2.0"
def _make_timedelta(value: t.Union[timedelta, int, None]) -> t.Optional[timedelta]:
    @property
    def session_cookie_name(self) -> str:
        .. deprecated:: 2.2
            Will be removed in Flask 2.3. Use ``app.config["SESSION_COOKIE_NAME"]``
            instead.
        import warnings
        warnings.warn(
            "'session_cookie_name' is deprecated and will be removed in Flask 2.3. Use"
            " 'SESSION_COOKIE_NAME' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.config["SESSION_COOKIE_NAME"]
    @session_cookie_name.setter
    def session_cookie_name(self, value: str) -> None:
        import warnings
        warnings.warn(
            "'session_cookie_name' is deprecated and will be removed in Flask 2.3. Use"
            " 'SESSION_COOKIE_NAME' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.config["SESSION_COOKIE_NAME"] = value
    @property
    def send_file_max_age_default(self) -> t.Optional[timedelta]:
        is ``None``, which tells the browser to use conditional requests instead of a
        timed cache.
        .. deprecated:: 2.2
            Will be removed in Flask 2.3. Use
            ``app.config["SEND_FILE_MAX_AGE_DEFAULT"]`` instead.
        .. versionchanged:: 2.0
            Defaults to ``None`` instead of 12 hours.
        import warnings
        warnings.warn(
            "'send_file_max_age_default' is deprecated and will be removed in Flask"
            " 2.3. Use 'SEND_FILE_MAX_AGE_DEFAULT' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _make_timedelta(self.config["SEND_FILE_MAX_AGE_DEFAULT"])
    @send_file_max_age_default.setter
    def send_file_max_age_default(self, value: t.Union[int, timedelta, None]) -> None:
        import warnings
        warnings.warn(
            "'send_file_max_age_default' is deprecated and will be removed in Flask"
            " 2.3. Use 'SEND_FILE_MAX_AGE_DEFAULT' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.config["SEND_FILE_MAX_AGE_DEFAULT"] = _make_timedelta(value)
    @property
    def use_x_sendfile(self) -> bool:
        it, from :func:`~flask.send_file`.
        .. deprecated:: 2.2
            Will be removed in Flask 2.3. Use ``app.config["USE_X_SENDFILE"]`` instead.
        import warnings
        warnings.warn(
            "'use_x_sendfile' is deprecated and will be removed in Flask 2.3. Use"
            " 'USE_X_SENDFILE' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.config["USE_X_SENDFILE"]
    @use_x_sendfile.setter
    def use_x_sendfile(self, value: bool) -> None:
        import warnings
        warnings.warn(
            "'use_x_sendfile' is deprecated and will be removed in Flask 2.3. Use"
            " 'USE_X_SENDFILE' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.config["USE_X_SENDFILE"] = value
        .. deprecated:: 2.2
            Will be removed in Flask 2.3.
        import warnings
        warnings.warn(
            "'propagate_exceptions' is deprecated and will be removed in Flask 2.3.",
            DeprecationWarning,
            stacklevel=2,
        )
        :meth:`create_jinja_environment`. It is enabled by default in debug mode.
        .. deprecated:: 2.2
            Will be removed in Flask 2.3. Use ``app.config["TEMPLATES_AUTO_RELOAD"]``
            instead.
        import warnings
        warnings.warn(
            "'templates_auto_reload' is deprecated and will be removed in Flask 2.3."
            " Use 'TEMPLATES_AUTO_RELOAD' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        import warnings
        warnings.warn(
            "'templates_auto_reload' is deprecated and will be removed in Flask 2.3."
            " Use 'TEMPLATES_AUTO_RELOAD' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
            auto_reload = self.config["TEMPLATES_AUTO_RELOAD"]
            if auto_reload is None:
                auto_reload = self.debug
            options["auto_reload"] = auto_reload
        if self.config["TEMPLATES_AUTO_RELOAD"] is None:
            self.jinja_env.auto_reload = value
        propagate = self.config["PROPAGATE_EXCEPTIONS"]
        if propagate is None:
            propagate = self.testing or self.debug
        if propagate:
        use_x_sendfile=current_app.config["USE_X_SENDFILE"],
from datetime import timedelta
        value = current_app.config["SEND_FILE_MAX_AGE_DEFAULT"]
        if isinstance(value, timedelta):
            return int(value.total_seconds())
        return value
        return app.config["SESSION_COOKIE_NAME"]
        defaults["ENV"] = os.environ.get("FLASK_ENV") or "development"
    @property
    def env(self) -> str:
        key.
        **Do not enable development when deploying in production.**
        Default: ``'production'``
        .. deprecated:: 2.2
            Will be removed in Flask 2.3.
        import warnings
        warnings.warn(
            "'app.env' is deprecated and will be removed in Flask 2.3."
            " Use 'app.debug' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.config["ENV"]
    @env.setter
    def env(self, value: str) -> None:
        import warnings
        warnings.warn(
            "'app.env' is deprecated and will be removed in Flask 2.3."
            " Use 'app.debug' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.config["ENV"] = value
        development server, an interactive debugger will be shown for unhandled
        exceptions, and the server will be reloaded when code changes. This maps to the
        :data:`DEBUG` config key. It may not behave as expected if set late.
        Default: ``False``
            The :envvar:`FLASK_DEBUG` environment variable will override :attr:`debug`.
                print(
                    "'FLASK_ENV' is deprecated and will not be used in"
                    " Flask 2.3. Use 'FLASK_DEBUG' instead.",
                    file=sys.stderr,
                )
                self.config["ENV"] = os.environ.get("FLASK_ENV") or "production"
        cli.show_server_banner(self.debug, self.name)
from werkzeug import run_simple
    help="Set debug mode.",
    :param set_debug_flag: Set the app's debug flag.
        Added the ``-A/--app``, ``--debug/--no-debug``, ``-e/--env-file`` options.
        params.extend((_env_file_option, _app_option, _debug_option))
def show_server_banner(debug, app_import_path):
    click.secho(
        "WARNING: This is a development server. Do not use it in a production"
        " deployment. Use a production WSGI server instead.",
        fg="red",
        bold=True,
    )
    The reloader and debugger are enabled by default with the '--debug'
    option.
    show_server_banner(debug, info.app_import_path)
    .. deprecated:: 2.2
        Will be removed in Flask 2.3.
    import warnings
    warnings.warn(
        "'FLASK_ENV' and 'get_env' are deprecated and will be removed"
        " in Flask 2.3. Use 'FLASK_DEBUG' instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    :envvar:`FLASK_DEBUG` environment variable. The default is ``False``.
        env = os.environ.get("FLASK_ENV")
        if env is not None:
            print(
                "'FLASK_ENV' is deprecated and will not be used in"
                " Flask 2.3. Use 'FLASK_DEBUG' instead.",
                file=sys.stderr,
            )
            return env == "development"
        return False
    return val.lower() not in {"0", "false", "no"}
        cli.show_server_banner(self.env, self.debug, self.name)
def show_server_banner(env, debug, app_import_path):
        click.echo(f" * Serving Flask app '{app_import_path}'")
    try:
        app = info.load_app()
    except Exception as e:
        if is_running_from_reloader():
            # When reloading, print out the error immediately, but raise
            # it later so the debugger or server can handle it.
            traceback.print_exc()
            err = e
            def app(environ, start_response):
                raise err from None
        else:
            # When not reloading, raise the error immediately so the
            # command fails.
            raise e from None
    show_server_banner(get_env(), debug, info.app_import_path)
    return _cv_request.get(None) is not None
    return _cv_app.get(None) is not None
    "blinker": ("https://blinker.readthedocs.io/", None),
        "Werkzeug >= 2.2.0",
__version__ = "2.1.3"
        context is popped. The application context is typically popped
        after the request context for each request, at the end of CLI
        commands, or after a manually pushed context ends.
        .. code-block:: python
            with app.app_context():
                ...
        When the ``with`` block exits (or ``ctx.pop()`` is called), the
        teardown functions are called just before the app context is
        made inactive. Since a request context typically also manages an
        application context it would also be called when you pop a
        request context.
        When a teardown function was called because of an unhandled
        exception it will be passed an error object. If an
        :meth:`errorhandler` is registered, it will handle the exception
        and the teardown will not receive it.
        Teardown functions must avoid raising exceptions. If they
        execute code that might fail they must surround that code with a
        ``try``/``except`` block and log any errors.
    context is created and pushed at the beginning of each request if
    one is not already active. An app context is also pushed when
    running CLI commands.
    app creates and pushes it at the beginning of the request, then pops
    it at the end of the request. It will create the URL adapter and
    request object for the WSGI environment provided.
        popped. Typically this happens at the end of each request, but
        contexts may be pushed manually as well during testing.
        .. code-block:: python
            with app.test_request_context():
                ...
        When the ``with`` block exits (or ``ctx.pop()`` is called), the
        teardown functions are called just before the request context is
        made inactive.
        When a teardown function was called because of an unhandled
        exception it will be passed an error object. If an
        :meth:`errorhandler` is registered, it will handle the exception
        and the teardown will not receive it.
        Teardown functions must avoid raising exceptions. If they
        execute code that might fail they must surround that code with a
        ``try``/``except`` block and log any errors.
    Flask's contexts to defer the cleanup of the request context until
    the end of a ``with`` block. For general information about how to
    use this class refer to :class:`werkzeug.test.Client`.
from .globals import _cv_app
from .globals import _cv_req
from .globals import request_ctx
        req = request_ctx.request
        rule: Rule = req.url_rule  # type: ignore[assignment]
        view_args: t.Dict[str, t.Any] = req.view_args  # type: ignore[assignment]
        return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
        adapter = request_ctx.url_adapter
        methods = adapter.allowed_methods()  # type: ignore[union-attr]
        req_ctx = _cv_req.get(None)
            app_ctx = _cv_app.get(None)
            rv = url_adapter.build(  # type: ignore[union-attr]
        ctx = request_ctx._get_current_object()  # type: ignore[attr-defined]
                environ["werkzeug.debug.preserve_context"](_cv_app.get())
                environ["werkzeug.debug.preserve_context"](_cv_req.get())
        f"App: {current_app.import_name} [{current_app.env}]\n"
        f"Instance: {current_app.instance_path}"
    ctx.update(current_app.make_shell_context())
        ctx = _cv_app.get(None)
        if ctx is not None:
            return f"<flask.g of '{ctx.app.name}'>"
    ctx = _cv_req.get(None)
    if ctx is None:
            "'after_this_request' can only be used when a request"
            " context is active, such as in a view function."
    ctx._after_request_functions.append(f)
    ctx = _cv_req.get(None)
    if ctx is None:
            "'copy_current_request_context' can only be used when a"
            " request context is active, such as in a view function."
    ctx = ctx.copy()
        with ctx:
            return ctx.app.ensure_sync(f)(*args, **kwargs)
        self.g: _AppCtxGlobals = app.app_ctx_globals_class()
        self.request: Request = request
        self.flashes: t.Optional[t.List[t.Tuple[str, str]]] = None
        self.session: t.Optional["SessionMixin"] = session
from .globals import request_ctx
    if request_ctx and request_ctx.request.blueprint is not None:
        blueprint = request_ctx.request.blueprint
from .globals import _cv_req
from .globals import request_ctx
        ctx = _cv_req.get(None)
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
    flashes = request_ctx.flashes
        flashes = session.pop("_flashes") if "_flashes" in session else []
        request_ctx.flashes = flashes
from .globals import _cv_app
from .globals import _cv_req
    appctx = _cv_app.get(None)
    reqctx = _cv_req.get(None)
    rv: t.Dict[str, t.Any] = {}
def _render(app: "Flask", template: Template, context: t.Dict[str, t.Any]) -> str:
    app.update_template_context(context)
    :param template_name_or_list: The name of the template to render. If
        a list is given, the first name to exist will be rendered.
    :param context: The variables to make available in the template.
    app = current_app._get_current_object()  # type: ignore[attr-defined]
    template = app.jinja_env.get_or_select_template(template_name_or_list)
    return _render(app, template, context)
    context.
    :param source: The source code of the template to render.
    :param context: The variables to make available in the template.
    app = current_app._get_current_object()  # type: ignore[attr-defined]
    template = app.jinja_env.from_string(source)
    return _render(app, template, context)
            token = _cv_req.set(outer_reqctx)  # type: ignore[arg-type]
from flask import Flask
from flask.globals import request_ctx
    app.config.update(
        TESTING=True,
        SECRET_KEY="test key",
    )
    while request_ctx:
        leaks.append(request_ctx._get_current_object())
        request_ctx.pop()
from flask.globals import app_ctx
from flask.globals import request_ctx
        assert flask.current_app._get_current_object() is app
    assert not flask.current_app
        assert flask.current_app._get_current_object() is app
    assert not flask.current_app
        with app_ctx:
            with request_ctx:
        assert flask.request.environ["werkzeug.request"] is not None
    with pytest.raises(DebugFilesKeyError) as e:
        client.post("/fail", data={"foo": "index.txt"})
    assert "no file contents were transmitted" in str(e.value)
    assert "This was submitted: 'index.txt'" in str(e.value)
@pytest.mark.parametrize("key", ["TESTING", "PROPAGATE_EXCEPTIONS", "DEBUG", None])
def test_exception_propagation(app, client, key):
    app.testing = False
    @app.route("/")
    def index():
        1 // 0
    if key is not None:
        app.config[key] = True
        with pytest.raises(ZeroDivisionError):
            client.get("/")
    else:
        assert client.get("/").status_code == 500
from flask.globals import request_ctx
    assert not flask.request
            reqctx = request_ctx.copy()
from flask.globals import request_ctx
            request_ctx.match_request()
from flask.globals import _cv_req
    assert _cv_req.get(None) is req_ctx
def __getattr__(name):
    if name == "_app_ctx_stack":
        import warnings
        from .globals import __app_ctx_stack
        warnings.warn(
            "'_app_ctx_stack' is deprecated and will be removed in Flask 2.3.",
            DeprecationWarning,
            stacklevel=2,
        )
        return __app_ctx_stack
    if name == "_request_ctx_stack":
        import warnings
        from .globals import __request_ctx_stack
        warnings.warn(
            "'_request_ctx_stack' is deprecated and will be removed in Flask 2.3.",
            DeprecationWarning,
            stacklevel=2,
        )
        return __request_ctx_stack
    raise AttributeError(name)
import contextvars
from .globals import _cv_app
from .globals import _cv_req
    return _cv_app.get(None) is not None
    return _cv_req.get(None) is not None
        self._cv_tokens: t.List[contextvars.Token] = []
        self._cv_tokens.append(_cv_app.set(self))
            if len(self._cv_tokens) == 1:
            ctx = _cv_app.get()
            _cv_app.reset(self._cv_tokens.pop())
        if ctx is not self:
            raise AssertionError(
                f"Popped wrong app context. ({ctx!r} instead of {self!r})"
            )
        self._cv_tokens: t.List[t.Tuple[contextvars.Token, t.Optional[AppContext]]] = []
        app_ctx = _cv_app.get(None)
        if app_ctx is None or app_ctx.app is not self.app:
            app_ctx = None
        self._cv_tokens.append((_cv_req.set(self), app_ctx))
        clear_request = len(self._cv_tokens) == 1
            if clear_request:
            ctx = _cv_req.get()
            token, app_ctx = self._cv_tokens.pop()
            _cv_req.reset(token)
                ctx.request.environ["werkzeug.request"] = None
            if ctx is not self:
                raise AssertionError(
                    f"Popped wrong request context. ({ctx!r} instead of {self!r})"
                )
from werkzeug.local import LocalProxy
class _FakeStack:
    def __init__(self, name: str, cv: ContextVar[t.Any]) -> None:
        self.name = name
        self.cv = cv
    def _warn(self):
        import warnings
        warnings.warn(
            f"'_{self.name}_ctx_stack' is deprecated and will be"
            " removed in Flask 2.3. Use 'g' to store data, or"
            f" '{self.name}_ctx' to access the current context.",
            DeprecationWarning,
            stacklevel=3,
        )
    def push(self, obj: t.Any) -> None:
        self._warn()
        self.cv.set(obj)
    def pop(self) -> t.Any:
        self._warn()
        ctx = self.cv.get(None)
        self.cv.set(None)
        return ctx
    @property
    def top(self) -> t.Optional[t.Any]:
        self._warn()
        return self.cv.get(None)
_cv_app: ContextVar["AppContext"] = ContextVar("flask.app_ctx")
__app_ctx_stack = _FakeStack("app", _cv_app)
app_ctx: "AppContext" = LocalProxy(  # type: ignore[assignment]
    _cv_app, unbound_message=_no_app_msg
current_app: "Flask" = LocalProxy(  # type: ignore[assignment]
    _cv_app, "app", unbound_message=_no_app_msg
g: "_AppCtxGlobals" = LocalProxy(  # type: ignore[assignment]
    _cv_app, "g", unbound_message=_no_app_msg
_cv_req: ContextVar["RequestContext"] = ContextVar("flask.request_ctx")
__request_ctx_stack = _FakeStack("request", _cv_req)
request_ctx: "RequestContext" = LocalProxy(  # type: ignore[assignment]
    _cv_req, unbound_message=_no_req_msg
request: "Request" = LocalProxy(  # type: ignore[assignment]
    _cv_req, "request", unbound_message=_no_req_msg
session: "SessionMixin" = LocalProxy(  # type: ignore[assignment]
    _cv_req, "session", unbound_message=_no_req_msg
def __getattr__(name: str) -> t.Any:
    if name == "_app_ctx_stack":
        import warnings
        warnings.warn(
            "'_app_ctx_stack' is deprecated and will be remoevd in Flask 2.3.",
            DeprecationWarning,
            stacklevel=2,
        )
        return __app_ctx_stack
    if name == "_request_ctx_stack":
        import warnings
        warnings.warn(
            "'_request_ctx_stack' is deprecated and will be remoevd in Flask 2.3.",
            DeprecationWarning,
            stacklevel=2,
        )
        return __request_ctx_stack
    raise AttributeError(name)
from .globals import _cv_req
        outer_reqctx = _cv_req.get(None)
            token = _cv_req.set(outer_reqctx)
                _cv_req.reset(token)
from contextvars import ContextVar
    from .ctx import AppContext
    from .ctx import RequestContext
_no_app_msg = """\
the current application. To solve this, set up an application context
with app.app_context(). See the documentation for more information.\
_cv_app: ContextVar[t.List["AppContext"]] = ContextVar("flask.app_ctx")
_app_ctx_stack: LocalStack["AppContext"] = LocalStack(_cv_app)
app_ctx: "AppContext" = _app_ctx_stack(  # type: ignore[assignment]
    unbound_message=_no_app_msg
)
current_app: "Flask" = _app_ctx_stack(  # type: ignore[assignment]
    "app", unbound_message=_no_app_msg
)
g: "_AppCtxGlobals" = _app_ctx_stack(  # type: ignore[assignment]
    "g", unbound_message=_no_app_msg
)
_no_req_msg = """\
Working outside of request context.
This typically means that you attempted to use functionality that needed
an active HTTP request. Consult the documentation on testing for
information about how to avoid this problem.\
_cv_req: ContextVar[t.List["RequestContext"]] = ContextVar("flask.request_ctx")
_request_ctx_stack: LocalStack["RequestContext"] = LocalStack(_cv_req)
request_ctx: "RequestContext" = _request_ctx_stack(  # type: ignore[assignment]
    unbound_message=_no_req_msg
)
request: "Request" = _request_ctx_stack(  # type: ignore[assignment]
    "request", unbound_message=_no_req_msg
)
session: "SessionMixin" = _request_ctx_stack(  # type: ignore[assignment]
    "session", unbound_message=_no_req_msg
        "Werkzeug >= 2.2.0a1",
    "Response",
    str,
    bytes,
    t.List[t.Any],
    t.Dict[str, t.Any],
    t.Iterator[str],
    t.Iterator[bytes],
    return jsonify("Hello, World!")
@app.route("/json/dict")
def hello_json_dict() -> t.Dict[str, t.Any]:
    return {"response": "Hello, World!"}
@app.route("/json/dict")
def hello_json_list() -> t.List[t.Any]:
    return [{"message": "Hello"}, {"message": "World"}]
                        " dict, list, tuple with headers or status,"
                        " Response instance, or WSGI callable, but it"
                        f" was a {type(rv).__name__}."
                    " dict, list, tuple with headers or status,"
                    " Response instance, or WSGI callable, but it was a"
                    f" {type(rv).__name__}."
    def app(self):
        app = Flask(__name__)
        app.testing = True
        @app.route("/get_post/<int:x>/<int:y>", methods=["GET", "POST"])
        def yyy_get_post(x, y):
            pass
        @app.route("/zzz_post", methods=["POST"])
        def aaa_post():
            pass
        return app
    @pytest.fixture
    def invoke(self, app, runner):
        cli = FlaskGroup(create_app=lambda: app)
    def test_sort(self, app, invoke):
        match_order = [r.endpoint for r in app.url_map.iter_rules()]
        self.expect_order(match_order, invoke(["routes", "-s", "match"]).output)
def _prepare_send_file_kwargs(**kwargs: t.Any) -> t.Dict[str, t.Any]:
    if kwargs.get("max_age") is None:
        kwargs["max_age"] = current_app.get_send_file_max_age
) -> "Response":
    return werkzeug.utils.send_file(  # type: ignore[return-value]
    return werkzeug.utils.send_from_directory(  # type: ignore[return-value]
            if "werkzeug.debug.preserve_context" in environ:
                environ["werkzeug.debug.preserve_context"](_app_ctx_stack.top)
                environ["werkzeug.debug.preserve_context"](_request_ctx_stack.top)
            if error is not None and self.should_ignore_error(error):
            ctx.pop(error)
    The request context is automatically popped at the end of the
    request. When using the interactive debugger, the context will be
    restored so ``request`` is still accessible. Similarly, the test
    client can preserve the context after the request ends. However,
    teardown functions may already have closed some resources such as
    database connections.
        .. deprecated:: 2.2
            Will be removed in Flask 2.3.
        import warnings
        warnings.warn(
            "'ctx.auto_pop' is deprecated and will be removed in Flask 2.3.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.pop(exc)
        self.pop(exc_value)
from contextlib import ExitStack
        self.preserve_context = False
        self._new_contexts: t.List[t.ContextManager[t.Any]] = []
        self._context_stack = ExitStack()
        out = {**self.environ_base, **other}
        if self.preserve_context:
            out["werkzeug.debug.preserve_context"] = self._new_contexts.append
        return out
        # Pop any previously preserved contexts. This prevents contexts
        # from being preserved across redirects or multiple requests
        # within a single block.
        self._context_stack.close()
        response = super().open(
        # Re-push contexts that were preserved during the request.
        while self._new_contexts:
            cm = self._new_contexts.pop()
            self._context_stack.enter_context(cm)
        return response
        self._context_stack.close()
    with pytest.raises(KeyboardInterrupt):
        client.get("/")
def test_appcontext_signals(app, client):
        rv = client.get("/")
        assert rv.data == b"Hello"
def test_appcontext_tearing_down_signal(app, client):
    app.testing = False
    def record_teardown(sender, exc):
        recorded.append(exc)
        rv = client.get("/")
        assert rv.status_code == 500
        assert len(recorded) == 1
        assert isinstance(recorded[0], ZeroDivisionError)
        # stream_with_context pushes a third context, preserved by response
        return flask.stream_with_context("hello")
    # req_ctx fixture pushed an initial context
        rv = client.get("/")
    # close the response, releasing the context held by stream_with_context
    rv.close()
                    " * Ignoring a call to 'app.run()' that would block"
                    " the current 'flask' CLI command.\n"
        # Set a flag to tell app.run to become a no-op. If app.run was
        # not in a __name__ == __main__ guard, it would start the server
        # when importing, blocking whatever command is being called.
        os.environ["FLASK_RUN_FROM_CLI"] = "true"
        return same_app, value
    assert result.return_value == (True, True)
    script's application context.
    Custom commands (and their options) registered under ``app.cli`` or
    ``blueprint.cli`` will always have an app context available, this
    decorator is not required in that case.
    .. versionchanged:: 2.2
        The app context is active for subcommands as well as the
        decorated callback. The app context is always available to
        ``app.cli`` command and parameter callbacks.
        if not current_app:
            app = __ctx.ensure_object(ScriptInfo).load_app()
            __ctx.with_resource(app.app_context())
        return __ctx.invoke(f, *args, **kwargs)
    .. versionchanged:: 2.2
        An app context is pushed when running ``app.cli`` commands, so
        ``@with_appcontext`` is no longer required for those commands.
            app = info.load_app()
            return None
        # Push an app context for the loaded app unless it is already
        # active somehow. This makes the context available to parameter
        # and command callbacks without needing @with_appcontext.
        if not current_app or current_app._get_current_object() is not app:
            ctx.with_resource(app.app_context())
        return app.cli.get_command(ctx, name)
from flask import _app_ctx_stack
def test_app_cli_has_app_context(app, runner):
    def _param_cb(ctx, param, value):
        # current_app should be available in parameter callbacks
        return bool(current_app)
    @app.cli.command()
    @click.argument("value", callback=_param_cb)
    def check(value):
        app = click.get_current_context().obj.load_app()
        # the loaded app should be the same as current_app
        same_app = current_app._get_current_object() is app
        # only one app context should be pushed
        stack_size = len(_app_ctx_stack._local.stack)
        return same_app, stack_size, value
    cli = FlaskGroup(create_app=lambda: app)
    result = runner.invoke(cli, ["check", "x"], standalone_mode=False)
    assert result.return_value == (True, 1, True)
def test_appgroup_app_context(runner):
    @cli.command()
    @subgroup.command()
def test_flaskgroup_app_context(runner):
        (os.environ, "FLASK_ENV_FILE", monkeypatch.notset),
from __future__ import annotations
from click.core import ParameterSource
if t.TYPE_CHECKING:
    from .app import Flask
            f" '{module.__name__}'. Use '{module.__name__}:name'"
            " to specify the correct one."
                    f"Detected factory '{attr_name}' in module '{module.__name__}',"
                    f" '{module.__name__}:{attr_name}(args)'"
        f" '{module.__name__}'. Use '{module.__name__}:name'"
    help="Show the Flask version.",
    def __init__(
        self,
        app_import_path: str | None = None,
        create_app: t.Callable[..., Flask] | None = None,
        set_debug_flag: bool = True,
    ) -> None:
        self.app_import_path = app_import_path
        self.data: t.Dict[t.Any, t.Any] = {}
        self._loaded_app: Flask | None = None
    def load_app(self) -> Flask:
                "Could not locate a Flask application. Use the"
                " 'flask --app' option, 'FLASK_APP' environment"
                " variable, or a 'wsgi.py' or 'app.py' file in the"
                " current directory."
def _set_app(ctx: click.Context, param: click.Option, value: str | None) -> str | None:
    if value is None:
        return None
    info = ctx.ensure_object(ScriptInfo)
    info.app_import_path = value
    return value
# This option is eager so the app will be available if --help is given.
# --help is also eager, so --app must be before it in the param list.
# no_args_is_help bypasses eager processing, so this option must be
# processed manually in that case to ensure FLASK_APP gets picked up.
_app_option = click.Option(
    ["-A", "--app"],
    metavar="IMPORT",
    help=(
        "The Flask application or factory function to load, in the form 'module:name'."
        " Module can be a dotted import or file path. Name is not required if it is"
        " 'app', 'application', 'create_app', or 'make_app', and can be 'name(args)' to"
        " pass arguments."
    ),
    is_eager=True,
    expose_value=False,
    callback=_set_app,
)
def _set_env(ctx: click.Context, param: click.Option, value: str | None) -> str | None:
    if value is None:
        return None
    # Set with env var instead of ScriptInfo.load so that it can be
    # accessed early during a factory function.
    os.environ["FLASK_ENV"] = value
    return value
_env_option = click.Option(
    ["-E", "--env"],
    metavar="NAME",
    help=(
        "The execution environment name to set in 'app.env'. Defaults to"
        " 'production'. 'development' will enable 'app.debug' and start the"
        " debugger and reloader when running the server."
    ),
    expose_value=False,
    callback=_set_env,
)
def _set_debug(ctx: click.Context, param: click.Option, value: bool) -> bool | None:
    # If the flag isn't provided, it will default to False. Don't use
    # that, let debug be set by env in that case.
    source = ctx.get_parameter_source(param.name)  # type: ignore[arg-type]
    if source is not None and source in (
        ParameterSource.DEFAULT,
        ParameterSource.DEFAULT_MAP,
    ):
        return None
    # Set with env var instead of ScriptInfo.load so that it can be
    # accessed early during a factory function.
    os.environ["FLASK_DEBUG"] = "1" if value else "0"
    return value
_debug_option = click.Option(
    ["--debug/--no-debug"],
    help="Set 'app.debug' separately from '--env'.",
    expose_value=False,
    callback=_set_debug,
)
def _env_file_callback(
    ctx: click.Context, param: click.Option, value: str | None
) -> str | None:
    if value is None:
        return None
    import importlib
    try:
        importlib.import_module("dotenv")
    except ImportError:
        raise click.BadParameter(
            "python-dotenv must be installed to load an env file.",
            ctx=ctx,
            param=param,
        ) from None
    # Don't check FLASK_SKIP_DOTENV, that only disables automatically
    # loading .env and .flaskenv files.
    load_dotenv(value)
    return value
# This option is eager so env vars are loaded as early as possible to be
# used by other options.
_env_file_option = click.Option(
    ["-e", "--env-file"],
    type=click.Path(exists=True, dir_okay=False),
    help="Load environment variables from this file. python-dotenv must be installed.",
    is_eager=True,
    expose_value=False,
    callback=_env_file_callback,
)
    .. versionchanged:: 2.2
        Added the ``-A/--app``, ``-E/--env``, ``--debug/--no-debug``,
        and ``-e/--env-file`` options.
        add_default_commands: bool = True,
        create_app: t.Callable[..., Flask] | None = None,
        add_version_option: bool = True,
        load_dotenv: bool = True,
        set_debug_flag: bool = True,
        **extra: t.Any,
    ) -> None:
        # Processing is done with option callbacks instead of a group
        # callback. This allows users to make a custom group callback
        # without losing the behavior. --env-file must come first so
        # that it is eagerly evaluated before --app.
        params.extend((_env_file_option, _app_option, _env_option, _debug_option))
        info_name: str | None,
        args: list[str],
        parent: click.Context | None = None,
        # Attempt to load .env and .flask env files. The --env-file
        # option can cause another file to be loaded.
    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        if not args and self.no_args_is_help:
            # Attempt to load --env-file and --app early in case they
            # were given as env vars. Otherwise no_args_is_help will not
            # see commands from app.cli.
            _env_file_option.handle_parse_result(ctx, {}, [])
            _app_option.handle_parse_result(ctx, {}, [])
        return super().parse_args(ctx, args)
def load_dotenv(path: str | os.PathLike | None = None) -> bool:
    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.
    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.
    # Always return after attempting to load a given path, don't load
    # the default files.
    loaded = False
        loaded = True
    return loaded  # True if at least one file was located and loaded.
    The reloader and debugger are enabled by default with the
    '--env development' or '--debug' options.
    app = DispatchingApp(info.load_app, use_eager_loading=eager_loading)
An application to load must be given with the '--app' option,
'FLASK_APP' environment variable, or with a 'wsgi.py' or 'app.py' file
in the current directory.
    setting :envvar:`FLASK_SKIP_DOTENV`. The default is ``True``, load
    the files.
import typing as t
        if "context_settings" not in extra:
            extra["context_settings"] = {}
        extra["context_settings"].setdefault("auto_envvar_prefix", "FLASK")
        super().__init__(params=params, **extra)
    def make_context(
        self,
        info_name: t.Optional[str],
        args: t.List[str],
        parent: t.Optional[click.Context] = None,
        **extra: t.Any,
    ) -> click.Context:
        if "obj" not in extra and "obj" not in self.context_settings:
            extra["obj"] = ScriptInfo(
        return super().make_context(info_name, args, parent=parent, **extra)
    name="flask",
    ),
def test_flaskgroup_nested(app, runner):
    cli = click.Group("cli")
    flask_group = FlaskGroup(name="flask", create_app=lambda: app)
    cli.add_command(flask_group)
    @flask_group.command()
    def show():
        click.echo(current_app.name)
    result = runner.invoke(cli, ["flask", "show"])
    assert result.output == "flask_test\n"
import click
from werkzeug.serving import is_running_from_reloader
        # Ignore this call so that it doesn't start another server if
        # the 'flask run' command is used.
            if not is_running_from_reloader():
                click.secho(
                    " * Ignoring a call to 'app.run()', the server is"
                    " already being run with the 'flask run' command.\n"
                    "   Only call 'app.run()' in an 'if __name__ =="
                    ' "__main__"\' guard.',
                    fg="red",
                )
from werkzeug.serving import is_running_from_reloader
            use_eager_loading = not is_running_from_reloader()
    if is_running_from_reloader():
            " a production deployment.\n   Use a production WSGI server"
            " instead.",
@app.route("/", defaults={"js": "fetch"})
@app.route("/<any(xhr, jquery, fetch):js>")
        ("/", "xhr.html"),
        ("/plain", "xhr.html"),
    methods: t.ClassVar[t.Optional[t.Collection[str]]] = None
class MethodView(View):
    def __init_subclass__(cls, **kwargs: t.Any) -> None:
        super().__init_subclass__(**kwargs)
        if "methods" not in cls.__dict__:
            methods = set()
            for base in cls.__bases__:
                if getattr(base, "methods", None):
                    methods.update(base.methods)  # type: ignore[attr-defined]
            for key in http_method_funcs:
                if hasattr(cls, key):
                    methods.add(key.upper())
            if methods:
                cls.methods = methods
    create a generic class-based view. Call :meth:`as_view` to create a
    view function that creates an instance of the class with the given
    arguments and calls its ``dispatch_request`` method with any URL
    variables.
    See :doc:`views` for a detailed guide.
    .. code-block:: python
        class Hello(View):
            init_every_request = False
            def dispatch_request(self, name):
                return f"Hello, {name}!"
        app.add_url_rule(
            "/hello/<name>", view_func=Hello.as_view("hello")
        )
    Set :attr:`methods` on the class to change what methods the view
    accepts.
    Set :attr:`decorators` on the class to apply a list of decorators to
    the generated view function. Decorators applied to the class itself
    will not be applied to the generated view function!
    Set :attr:`init_every_request` to ``False`` for efficiency, unless
    you need to store request-global data on ``self``.
    #: The methods this view is registered for. Uses the same default
    #: (``["GET", "HEAD", "OPTIONS"]``) as ``route`` and
    #: ``add_url_rule`` by default.
    methods: t.ClassVar[t.Optional[t.List[str]]] = None
    #: Control whether the ``OPTIONS`` method is handled automatically.
    #: Uses the same default (``True``) as ``route`` and
    #: ``add_url_rule`` by default.
    provide_automatic_options: t.ClassVar[t.Optional[bool]] = None
    #: A list of decorators to apply, in order, to the generated view
    #: function. Remember that ``@decorator`` syntax is applied bottom
    #: to top, so the first decorator in the list would be the bottom
    #: decorator.
    decorators: t.ClassVar[t.List[t.Callable]] = []
        this and return a valid response. Any variables from the URL
        rule are passed as keyword arguments.
    For example, if you implement a ``get`` method, it will be used to
    handle ``GET`` requests.
    This can be useful for defining a REST API.
    :attr:`methods` is automatically set based on the methods defined on
    the class.
    See :doc:`views` for a detailed guide.
    .. code-block:: python
                return str(session.get("counter", 0))
                session["counter"] = session.get("counter", 0) + 1
                return redirect(url_for("counter"))
        app.add_url_rule(
            "/counter", view_func=CounterAPI.as_view("counter")
        )
    #: Create a new instance of this view class for every request by
    #: default. If a view subclass sets this to ``False``, the same
    #: instance is used for every request.
    #:
    #: A single instance is more efficient, especially if complex setup
    #: is done during init. However, storing data on ``self`` is no
    #: longer safe across requests, and :data:`~flask.g` should be used
    #: instead.
    #:
    #: .. versionadded:: 2.2
    init_every_request: t.ClassVar[bool] = True
    ) -> ft.ViewCallable:
        for a route.
        By default, the generated view will create a new instance of the
        view class for every request and call its
        :meth:`dispatch_request` method. If the view class sets
        :attr:`init_every_request` to ``False``, the same instance will
        be used for every request.
        The arguments passed to this method are forwarded to the view
        class ``__init__`` method.
        .. versionchanged:: 2.2
            Added the ``init_every_request`` class attribute.
        if cls.init_every_request:
            def view(**kwargs: t.Any) -> ft.ResponseReturnValue:
                self = view.view_class(  # type: ignore[attr-defined]
                    *class_args, **class_kwargs
                )
                return current_app.ensure_sync(self.dispatch_request)(**kwargs)
        else:
            self = cls(*class_args, **class_kwargs)
            def view(**kwargs: t.Any) -> ft.ResponseReturnValue:
                return current_app.ensure_sync(self.dispatch_request)(**kwargs)
    def dispatch_request(self, **kwargs: t.Any) -> ft.ResponseReturnValue:
        return current_app.ensure_sync(meth)(**kwargs)
def test_init_once(app, client):
    n = 0
    class CountInit(flask.views.View):
        init_every_request = False
        def __init__(self):
            nonlocal n
            n += 1
        def dispatch_request(self):
            return str(n)
    app.add_url_rule("/", view_func=CountInit.as_view("index"))
    assert client.get("/").data == b"1"
    assert client.get("/").data == b"1"
        #: .. deprecated:: 2.2
        #:     Will be removed in Flask 2.3. Run setup code when
        #:     creating the application instead.
        #:
        .. deprecated:: 2.2
            Will be removed in Flask 2.3. Run setup code when creating
            the application instead.
        import warnings
        warnings.warn(
            "'before_first_request' is deprecated and will be removed"
            " in Flask 2.3. Run setup code while creating the"
            " application instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        # Run before_first_request functions if this is the thread's first request.
        # Inlined to avoid a method call on subsequent requests.
        # This is deprecated, will be removed in Flask 2.3.
        if not self._got_first_request:
            with self._before_request_lock:
                if not self._got_first_request:
                    for func in self.before_first_request_funcs:
                        self.ensure_sync(func)()
                    self._got_first_request = True
        .. deprecated:: 2.2
            Will be removed in Flask 2.3. Run setup code when creating
            the application instead.
        import warnings
        warnings.warn(
            "'before_app_first_request' is deprecated and will be"
            " removed in Flask 2.3. Use 'record_once' instead to run"
            " setup code when registering the blueprint.",
            DeprecationWarning,
            stacklevel=2,
        )
    with pytest.deprecated_call():
        @app.before_first_request
        async def before_first():
            nonlocal app_first_called
            app_first_called = True
    with pytest.deprecated_call():
        @app.before_first_request
        def foo():
            got.append(42)
    with pytest.deprecated_call():
        @app.before_first_request
        def foo():
            time.sleep(0.2)
            got.append(42)
    with pytest.deprecated_call():
        @bp.before_app_first_request
        def before_first_request():
            evts.append("first")
import pathlib
def _path_is_relative_to(path: pathlib.PurePath, base: str) -> bool:
    # Path.is_relative_to doesn't exist until Python 3.9
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False
                package_path = pathlib.Path(
                    os.path.commonpath(package_spec.submodule_search_locations)
                    if _path_is_relative_to(package_path, location)
    if _path_is_relative_to(pathlib.PurePath(package_path), py_prefix):
    def app_errorhandler(
        self, code: t.Union[t.Type[Exception], int]
    ) -> t.Callable[[ft.ErrorHandlerDecorator], ft.ErrorHandlerDecorator]:
        def decorator(f: ft.ErrorHandlerDecorator) -> ft.ErrorHandlerDecorator:
    ) -> t.Callable[[ft.ErrorHandlerDecorator], ft.ErrorHandlerDecorator]:
        def decorator(f: ft.ErrorHandlerDecorator) -> ft.ErrorHandlerDecorator:
ErrorHandlerDecorator = t.TypeVar("ErrorHandlerDecorator", bound=ErrorHandlerCallable)
from __future__ import annotations
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound
from flask import Flask
app = Flask(__name__)
@app.errorhandler(400)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
@app.errorhandler(BadRequest)
def handle_400(e: BadRequest) -> str:
    return ""
@app.errorhandler(ValueError)
def handle_custom(e: ValueError) -> str:
    return ""
@app.errorhandler(ValueError)
def handle_accept_base(e: Exception) -> str:
    return ""
@app.errorhandler(BadRequest)
@app.errorhandler(404)
def handle_multiple(e: BadRequest | NotFound) -> str:
    return ""
        view_func: t.Optional[ft.ViewCallable] = None,
                    rv, status = rv  # type: ignore[assignment,misc]
        view_func: t.Optional[ft.ViewCallable] = None,
    ) -> t.Callable[[ft.RouteDecorator], ft.RouteDecorator]:
    def get(
        self, rule: str, **options: t.Any
    ) -> t.Callable[[ft.RouteDecorator], ft.RouteDecorator]:
    def post(
        self, rule: str, **options: t.Any
    ) -> t.Callable[[ft.RouteDecorator], ft.RouteDecorator]:
    def put(
        self, rule: str, **options: t.Any
    ) -> t.Callable[[ft.RouteDecorator], ft.RouteDecorator]:
    def delete(
        self, rule: str, **options: t.Any
    ) -> t.Callable[[ft.RouteDecorator], ft.RouteDecorator]:
    def patch(
        self, rule: str, **options: t.Any
    ) -> t.Callable[[ft.RouteDecorator], ft.RouteDecorator]:
    def route(
        self, rule: str, **options: t.Any
    ) -> t.Callable[[ft.RouteDecorator], ft.RouteDecorator]:
        def decorator(f: ft.RouteDecorator) -> ft.RouteDecorator:
        view_func: t.Optional[ft.ViewCallable] = None,
ResponseValue = t.Union["Response", str, bytes, t.Dict[str, t.Any]]
# This should be a Union, but mypy doesn't pass unless it's a TypeVar.
    "Headers",
    t.Mapping[str, HeaderValue],
    t.Sequence[t.Tuple[str, HeaderValue]],
    t.Tuple[ResponseValue, int],
    t.Tuple[ResponseValue, int, HeadersValue],
ViewCallable = t.Callable[..., ResponseReturnValue]
RouteDecorator = t.TypeVar("RouteDecorator", bound=ViewCallable)
from __future__ import annotations
@app.route("/str")
def hello_str() -> str:
@app.route("/bytes")
def hello_bytes() -> bytes:
    return b"<p>Hello, World!</p>"
def hello_json() -> Response:
@app.route("/status")
@app.route("/status/<int:code>")
def tuple_status(code: int = 200) -> tuple[str, int]:
    return "hello", code
@app.route("/status-enum")
def tuple_status_enum() -> tuple[str, int]:
    return "hello", HTTPStatus.OK
@app.route("/headers")
def tuple_headers() -> tuple[str, dict[str, str]]:
    return "Hello, World!", {"Content-Type": "text/plain"}
@app.route("/template")
@app.route("/template/<name>")
def return_template(name: str | None = None) -> str:
    return render_template("index.html", name=name)
    def __init__(self: RenderTemplateView, template_name: str) -> None:
    def dispatch_request(self: RenderTemplateView) -> str:
from . import typing as ft
        self.before_first_request_funcs: t.List[ft.BeforeFirstRequestCallable] = []
        self.teardown_appcontext_funcs: t.List[ft.TeardownCallable] = []
    ) -> t.Callable[[ft.TemplateFilterCallable], ft.TemplateFilterCallable]:
        def decorator(f: ft.TemplateFilterCallable) -> ft.TemplateFilterCallable:
        self, f: ft.TemplateFilterCallable, name: t.Optional[str] = None
    ) -> t.Callable[[ft.TemplateTestCallable], ft.TemplateTestCallable]:
        def decorator(f: ft.TemplateTestCallable) -> ft.TemplateTestCallable:
        self, f: ft.TemplateTestCallable, name: t.Optional[str] = None
    ) -> t.Callable[[ft.TemplateGlobalCallable], ft.TemplateGlobalCallable]:
        def decorator(f: ft.TemplateGlobalCallable) -> ft.TemplateGlobalCallable:
        self, f: ft.TemplateGlobalCallable, name: t.Optional[str] = None
        self, f: ft.BeforeFirstRequestCallable
    ) -> ft.BeforeFirstRequestCallable:
    def teardown_appcontext(self, f: ft.TeardownCallable) -> ft.TeardownCallable:
    def _find_error_handler(self, e: Exception) -> t.Optional[ft.ErrorHandlerCallable]:
    ) -> t.Union[HTTPException, ft.ResponseReturnValue]:
    ) -> t.Union[HTTPException, ft.ResponseReturnValue]:
        server_error: t.Union[InternalServerError, ft.ResponseReturnValue]
    def dispatch_request(self) -> ft.ResponseReturnValue:
        rv: t.Union[ft.ResponseReturnValue, HTTPException],
    def make_response(self, rv: ft.ResponseReturnValue) -> Response:
                    rv = self.response_class.force_type(
                        rv, request.environ  # type: ignore[arg-type]
                    )
    def preprocess_request(self) -> t.Optional[ft.ResponseReturnValue]:
from . import typing as ft
    ) -> t.Callable[[ft.TemplateFilterCallable], ft.TemplateFilterCallable]:
        def decorator(f: ft.TemplateFilterCallable) -> ft.TemplateFilterCallable:
        self, f: ft.TemplateFilterCallable, name: t.Optional[str] = None
    ) -> t.Callable[[ft.TemplateTestCallable], ft.TemplateTestCallable]:
        def decorator(f: ft.TemplateTestCallable) -> ft.TemplateTestCallable:
        self, f: ft.TemplateTestCallable, name: t.Optional[str] = None
    ) -> t.Callable[[ft.TemplateGlobalCallable], ft.TemplateGlobalCallable]:
        def decorator(f: ft.TemplateGlobalCallable) -> ft.TemplateGlobalCallable:
        self, f: ft.TemplateGlobalCallable, name: t.Optional[str] = None
    def before_app_request(
        self, f: ft.BeforeRequestCallable
    ) -> ft.BeforeRequestCallable:
        self, f: ft.BeforeFirstRequestCallable
    ) -> ft.BeforeFirstRequestCallable:
    def after_app_request(self, f: ft.AfterRequestCallable) -> ft.AfterRequestCallable:
    def teardown_app_request(self, f: ft.TeardownCallable) -> ft.TeardownCallable:
        self, f: ft.TemplateContextProcessorCallable
    ) -> ft.TemplateContextProcessorCallable:
        def decorator(f: ft.ErrorHandlerCallable) -> ft.ErrorHandlerCallable:
        self, f: ft.URLValuePreprocessorCallable
    ) -> ft.URLValuePreprocessorCallable:
    def app_url_defaults(self, f: ft.URLDefaultCallable) -> ft.URLDefaultCallable:
from . import typing as ft
def after_this_request(f: ft.AfterRequestCallable) -> ft.AfterRequestCallable:
        self._after_request_functions: t.List[ft.AfterRequestCallable] = []
from . import typing as ft
            ft.AppOrBlueprintKey,
            t.Dict[t.Optional[int], t.Dict[t.Type[Exception], ft.ErrorHandlerCallable]],
            ft.AppOrBlueprintKey, t.List[ft.BeforeRequestCallable]
            ft.AppOrBlueprintKey, t.List[ft.AfterRequestCallable]
            ft.AppOrBlueprintKey, t.List[ft.TeardownCallable]
            ft.AppOrBlueprintKey, t.List[ft.TemplateContextProcessorCallable]
            ft.AppOrBlueprintKey,
            t.List[ft.URLValuePreprocessorCallable],
            ft.AppOrBlueprintKey, t.List[ft.URLDefaultCallable]
    def before_request(self, f: ft.BeforeRequestCallable) -> ft.BeforeRequestCallable:
    def after_request(self, f: ft.AfterRequestCallable) -> ft.AfterRequestCallable:
    def teardown_request(self, f: ft.TeardownCallable) -> ft.TeardownCallable:
        self, f: ft.TemplateContextProcessorCallable
    ) -> ft.TemplateContextProcessorCallable:
        self, f: ft.URLValuePreprocessorCallable
    ) -> ft.URLValuePreprocessorCallable:
    def url_defaults(self, f: ft.URLDefaultCallable) -> ft.URLDefaultCallable:
    ) -> t.Callable[[ft.ErrorHandlerCallable], ft.ErrorHandlerCallable]:
        def decorator(f: ft.ErrorHandlerCallable) -> ft.ErrorHandlerCallable:
        f: ft.ErrorHandlerCallable,
from . import typing as ft
    def dispatch_request(self) -> ft.ResponseReturnValue:
        def view(*args: t.Any, **kwargs: t.Any) -> ft.ResponseReturnValue:
    def dispatch_request(self, *args: t.Any, **kwargs: t.Any) -> ft.ResponseReturnValue:
__version__ = "2.1.3.dev0"
        if sys.version_info >= (3, 10):
            from importlib import metadata
        else:
            # Use a backport on Python < 3.10. We technically have
            # importlib.metadata on 3.8+, but the API changed in 3.10,
            # so use the backport for consistency.
            import importlib_metadata as metadata
    try:
        import dotenv
    except ImportError:
        try:
            import ssl
        except ImportError:
            ) from None
    try:
        import ssl
    except ImportError:
        is_context = False
    else:
        is_context = isinstance(cert, ssl.SSLContext)
def dotenv_not_available():
    try:
        import dotenv  # noqa: F401
    except ImportError:
        return True
    return False
need_dotenv = pytest.mark.skipif(
    dotenv_not_available(), reason="dotenv is not installed"
)
    monkeypatch.setitem(sys.modules, "dotenv", None)
    monkeypatch.setitem(sys.modules, "ssl", None)
    @app.route("/clear")
    def clear():
        flask.session.pop("testing", None)
        return "Goodbye World"
@pytest.mark.parametrize(
    ("debug", "trap", "expect_key", "expect_abort"),
    [(False, None, True, True), (True, None, False, True), (False, True, False, False)],
)
def test_trap_bad_request_key_error(app, client, debug, trap, expect_key, expect_abort):
    app.config["DEBUG"] = debug
    app.config["TRAP_BAD_REQUEST_ERRORS"] = trap
    if expect_key:
        rv = client.get("/key")
        assert rv.status_code == 400
        assert b"missing_key" not in rv.data
    else:
        with pytest.raises(KeyError) as exc_info:
            client.get("/key")
        assert exc_info.errisinstance(BadRequest)
        assert "missing_key" in exc_info.value.get_description()
    if expect_abort:
        rv = client.get("/abort")
        assert rv.status_code == 400
    else:
        with pytest.raises(BadRequest):
            client.get("/abort")
def test_no_setup_after_first_request(app, client):
    with pytest.raises(AssertionError) as exc_info:
    assert "setup method 'add_url_rule'" in str(exc_info.value)
    app.config["DEBUG"] = True
    @app.route("/user/", methods=["GET", "POST"])
    def user():
        return flask.request.form["status"]
    # default redirect code preserves form data
    rv = client.post("/user", data={"status": "success"}, follow_redirects=True)
    assert rv.data == b"success"
    # 301 and 302 raise error
    with client, pytest.raises(AssertionError) as exc_info:
        client.post("/user", data={"status": "error"}, follow_redirects=True)
    assert "canonical URL 'http://localhost/user/'" in str(exc_info.value)
    def _check_setup_finished(self, f_name: str) -> None:
        if self._got_first_request:
            raise AssertionError(
                f"The setup method '{f_name}' can no longer be called"
                " on the application. It has already handled its first"
                " request, any changes will not be applied"
                " consistently.\n"
                "Make sure all imports, decorators, functions, etc."
                " needed to set up the application are done before"
                " running it."
            )
from .scaffold import setupmethod
    def _check_setup_finished(self, f_name: str) -> None:
        if self._got_registered_once:
            import warnings
            warnings.warn(
                f"The setup method '{f_name}' can no longer be called on"
                f" the blueprint '{self.name}'. It has already been"
                " registered at least once, any changes will not be"
                " applied consistently.\n"
                "Make sure all imports, decorators, functions, etc."
                " needed to set up the blueprint are done before"
                " registering it.\n"
                "This warning will become an exception in Flask 2.3.",
                UserWarning,
                stacklevel=3,
            )
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    f_name = f.__name__
        self._check_setup_finished(f_name)
    def _check_setup_finished(self, f_name: str) -> None:
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
    @setupmethod
        #:     Moved from ``flask.abort``, which calls this object.
            url_for=self.url_for,
            Moved from ``flask.redirect``, which calls this method.
from .globals import _app_ctx_stack
        #: A list of functions that are called by
        #: :meth:`handle_url_build_error` when :meth:`.url_for` raises a
        #: :exc:`~werkzeug.routing.BuildError`. Each function is called
        #: with ``error``, ``endpoint`` and ``values``. If a function
        #: returns ``None`` or raises a ``BuildError``, it is skipped.
        #: Otherwise, its return value is returned by ``url_for``.
            t.Callable[[Exception, str, t.Dict[str, t.Any]], str]
        *,
        _anchor: t.Optional[str] = None,
        _method: t.Optional[str] = None,
        _scheme: t.Optional[str] = None,
        _external: t.Optional[bool] = None,
        This is called by :func:`flask.url_for`, and can be called
        directly as well.
        An *endpoint* is the name of a URL rule, usually added with
        :meth:`@app.route() <route>`, and usually the same name as the
        view function. A route defined in a :class:`~flask.Blueprint`
        will prepend the blueprint's name separated by a ``.`` to the
        endpoint.
        In some cases, such as email messages, you want URLs to include
        the scheme and domain, like ``https://example.com/hello``. When
        not in an active request, URLs will be external by default, but
        this requires setting :data:`SERVER_NAME` so Flask knows what
        domain to use. :data:`APPLICATION_ROOT` and
        :data:`PREFERRED_URL_SCHEME` should also be configured as
        needed. This config is only used when not in an active request.
        Functions can be decorated with :meth:`url_defaults` to modify
        keyword arguments before the URL is built.
        If building fails for some reason, such as an unknown endpoint
        or incorrect values, the app's :meth:`handle_url_build_error`
        method is called. If that returns a string, that is returned,
        otherwise a :exc:`~werkzeug.routing.BuildError` is raised.
        :param endpoint: The endpoint name associated with the URL to
            generate. If this starts with a ``.``, the current blueprint
            name (if any) will be used.
        :param _anchor: If given, append this as ``#anchor`` to the URL.
        :param _method: If given, generate the URL associated with this
            method for the endpoint.
        :param _scheme: If given, the URL will have this scheme if it
            is external.
        :param _external: If given, prefer the URL to be internal
            (False) or require it to be external (True). External URLs
            include the scheme and domain. When not in an active
            request, URLs are external by default.
        :param values: Values to use for the variable parts of the URL
            rule. Unknown keys are appended as query string arguments,
            like ``?a=b&c=d``.
        .. versionadded:: 2.2
            Moved from ``flask.url_for``, which calls this method.
        req_ctx = _request_ctx_stack.top
        if req_ctx is not None:
            url_adapter = req_ctx.url_adapter
            blueprint_name = req_ctx.request.blueprint
            # If the endpoint starts with "." and the request matches a
            # blueprint, the endpoint is relative to the blueprint.
            if endpoint[:1] == ".":
                if blueprint_name is not None:
                    endpoint = f"{blueprint_name}{endpoint}"
                else:
                    endpoint = endpoint[1:]
            # When in a request, generate a URL without scheme and
            # domain by default, unless a scheme is given.
            if _external is None:
                _external = _scheme is not None
        else:
            app_ctx = _app_ctx_stack.top
            # If called by helpers.url_for, an app context is active,
            # use its url_adapter. Otherwise, app.url_for was called
            # directly, build an adapter.
            if app_ctx is not None:
                url_adapter = app_ctx.url_adapter
            else:
                url_adapter = self.create_url_adapter(None)
            if url_adapter is None:
                raise RuntimeError(
                    "Unable to build URLs outside an active request"
                    " without 'SERVER_NAME' configured. Also configure"
                    " 'APPLICATION_ROOT' and 'PREFERRED_URL_SCHEME' as"
                    " needed."
            # When outside a request, generate a URL with scheme and
            # domain by default.
            if _external is None:
                _external = True
        # It is an error to set _scheme when _external=False, in order
        # to avoid accidental insecure URLs.
        if _scheme is not None and not _external:
            raise ValueError("When specifying '_scheme', '_external' must be True.")
        self.inject_url_defaults(endpoint, values)
        try:
            rv = url_adapter.build(
                endpoint,
                values,
                method=_method,
                url_scheme=_scheme,
                force_external=_external,
            )
            values.update(
                _anchor=_anchor, _method=_method, _scheme=_scheme, _external=_external
            )
        if _anchor is not None:
            rv = f"{rv}#{url_quote(_anchor)}"
        self, error: BuildError, endpoint: str, values: t.Dict[str, t.Any]
        :exc:`~werkzeug.routing.BuildError` was raised. If this returns
        a value, it will be returned by ``url_for``, otherwise the error
        will be re-raised.
        Each function in :attr:`url_build_error_handlers` is called with
        ``error``, ``endpoint`` and ``values``. If a function returns
        ``None`` or raises a ``BuildError``, it is skipped. Otherwise,
        its return value is returned by ``url_for``.
        :param error: The active ``BuildError`` being handled.
        :param endpoint: The endpoint being built.
        :param values: The keyword arguments passed to ``url_for``.
def url_for(
    endpoint: str,
    *,
    _anchor: t.Optional[str] = None,
    _method: t.Optional[str] = None,
    _scheme: t.Optional[str] = None,
    _external: t.Optional[bool] = None,
    **values: t.Any,
) -> str:
    This requires an active request or application context, and calls
    :meth:`current_app.url_for() <flask.Flask.url_for>`. See that method
    for full documentation.
    :param endpoint: The endpoint name associated with the URL to
        generate. If this starts with a ``.``, the current blueprint
        name (if any) will be used.
    :param _anchor: If given, append this as ``#anchor`` to the URL.
    :param _method: If given, generate the URL associated with this
        method for the endpoint.
    :param _scheme: If given, the URL will have this scheme if it is
        external.
    :param _external: If given, prefer the URL to be internal (False) or
        require it to be external (True). External URLs include the
        scheme and domain. When not in an active request, URLs are
        external by default.
    :param values: Values to use for the variable parts of the URL rule.
        Unknown keys are appended as query string arguments, like
        ``?a=b&c=d``.
    .. versionchanged:: 2.2
        Calls ``current_app.url_for``, allowing an app to override the
        behavior.
    .. versionchanged:: 0.10
       The ``_scheme`` parameter was added.
    .. versionchanged:: 0.9
       The ``_anchor`` and ``_method`` parameters were added.
    .. versionchanged:: 0.9
       Calls ``app.handle_url_build_error`` on build errors.
    return current_app.url_for(
        endpoint,
        _anchor=_anchor,
        _method=_method,
        _scheme=_scheme,
        _external=_external,
        **values,
    )
        app.add_url_rule("/", endpoint="index")
        # Implicit external with scheme.
        url = flask.url_for("index", _scheme="https")
        assert url == "https://localhost/"
        # Error when external=False with scheme
        with pytest.raises(ValueError):
            flask.url_for("index", _scheme="https", _external=False)
        This is called by :func:`flask.redirect`, and can be called
        directly as well.
        :param location: The URL to redirect to.
        :param code: The status code for the redirect.
    If :data:`~flask.current_app` is available, it will use its
    :meth:`~flask.Flask.redirect` method, otherwise it will use
        Calls ``current_app.redirect`` if available instead of always
        using Werkzeug's default ``redirect``.
__version__ = "2.1.2"
    with pytest.raises(Exception, match="dummy"):
        app.add_url_rule("/", methods="GET POST", endpoint="test")
    with client:
        with pytest.raises(KeyboardInterrupt):
            client.get("/")
    assert "returned None" in str(e.value)
    assert "from_none" in str(e.value)
    assert "tuple must have the form" in str(e.value)
    with pytest.raises(TypeError):
        c.get("/large_tuple")
    assert "it was a bool" in str(e.value)
    with pytest.raises(TypeError):
        c.get("/bad_wsgi")
    with pytest.raises(AssertionError) as e:
        app.add_url_rule("/foo", endpoint="late")
    # reduce flakiness by waiting for the internal loading lock
    with lazy._lock:
        with pytest.raises(BadExc):
    assert "'FOO_SETTINGS' is not set" in str(e.value)
    app = flask.Flask(__name__)
__version__ = "2.1.2.dev0"
__version__ = "2.1.1"
        "importlib-metadata >= 3.6.0; python_version < '3.10'",
__version__ = "2.1.1.dev0"
__version__ = "2.2.0.dev0"
__version__ = "2.1.0"
    def on_json_loading_failed(self, e: t.Optional[ValueError]) -> t.Any:
    if os.name != "nt":
        assert app.config["EXIST"] == {
            "ok": "other",
            "flag": True,
            "inner": {"ik": 2},
            "new": {"more": {"k": False}},
        }
    else:
        # Windows env var keys are always uppercase.
        assert app.config["EXIST"] == {
            "ok": "value",
            "OK": "other",
            "flag": True,
            "inner": {"ik": 1},
            "INNER": {"IK": 2},
            "NEW": {"MORE": {"k": False}},
        }
        super().__init__(defaults or {})
        self, prefix: str = "FLASK", *, loads: t.Callable[[str], t.Any] = json.loads
        dropping the prefix from the env key for the config key. Values
        are passed through a loading function to attempt to convert them
        to more specific types than strings.
        Keys are loaded in :func:`sorted` order.
        The default loading function attempts to parse values as any
        valid JSON type, including dicts and lists.
        Specific items in nested dicts can be set by separating the
        keys with double underscores (``__``). If an intermediate key
        doesn't exist, it will be initialized to an empty dict.
        :param prefix: Load env vars that start with this prefix,
            separated with an underscore (``_``).
        :param loads: Pass each string value to this function and use
            the returned value as the config value. If any error is
            raised it is ignored and the value remains a string. The
            default is :func:`json.loads`.
        .. versionadded:: 2.1
        prefix = f"{prefix}_"
        len_prefix = len(prefix)
        for key in sorted(os.environ):
            if not key.startswith(prefix):
                continue
            value = os.environ[key]
            try:
                value = loads(value)
            except Exception:
                # Keep the value as a string if loading failed.
                pass
            # Change to key.removeprefix(prefix) on Python >= 3.9.
            key = key[len_prefix:]
            if "__" not in key:
                # A non-nested key, set directly.
                self[key] = value
                continue
            # Traverse nested dictionaries with keys separated by "__".
            current = self
            *parts, tail = key.split("__")
            for part in parts:
                # If an intermediate dict does not exist, create it.
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[tail] = value
        return True
def test_from_prefixed_env(monkeypatch):
    monkeypatch.setenv("FLASK_STRING", "value")
    monkeypatch.setenv("FLASK_BOOL", "true")
    monkeypatch.setenv("FLASK_INT", "1")
    monkeypatch.setenv("FLASK_FLOAT", "1.2")
    monkeypatch.setenv("FLASK_LIST", "[1, 2]")
    monkeypatch.setenv("FLASK_DICT", '{"k": "v"}')
    monkeypatch.setenv("NOT_FLASK_OTHER", "other")
    assert app.config["STRING"] == "value"
    assert app.config["BOOL"] is True
    assert app.config["INT"] == 1
    assert app.config["FLOAT"] == 1.2
    assert app.config["LIST"] == [1, 2]
    assert app.config["DICT"] == {"k": "v"}
    assert "OTHER" not in app.config
def test_from_prefixed_env_custom_prefix(monkeypatch):
    monkeypatch.setenv("FLASK_A", "a")
    monkeypatch.setenv("NOT_FLASK_A", "b")
    app = flask.Flask(__name__)
    app.config.from_prefixed_env("NOT_FLASK")
    assert app.config["A"] == "b"
def test_from_prefixed_env_nested(monkeypatch):
    monkeypatch.setenv("FLASK_EXIST__ok", "other")
    monkeypatch.setenv("FLASK_EXIST__inner__ik", "2")
    monkeypatch.setenv("FLASK_EXIST__new__more", '{"k": false}')
    monkeypatch.setenv("FLASK_NEW__K", "v")
    app.config["EXIST"] = {"ok": "value", "flag": True, "inner": {"ik": 1}}
    app.config.from_prefixed_env()
    assert app.config["EXIST"] == {
        "ok": "other",
        "flag": True,
        "inner": {"ik": 2},
        "new": {"more": {"k": False}},
    }
    assert app.config["NEW"] == {"K": "v"}
    assert response.headers["Location"] == "/auth/login"
    assert response.headers["Location"] == "/"
    assert response.headers["Location"] == "/auth/login"
    assert response.headers["Location"] == "/"
    autocorrect_location_header = False
        location_parts = rv.headers["Location"].rpartition("/")
        if location_parts[0]:
            # For older Werkzeug that used absolute redirects.
            assert location_parts[0] == "http://localhost"
        assert location_parts[2] == "test"
    def on_json_loading_failed(self, e: ValueError) -> t.Any:
        try:
            return super().on_json_loading_failed(e)
        except BadRequest as e:
            if current_app and current_app.debug:
                raise
            raise BadRequest() from e
    about ``enctype=multipart/form-data``.
    :param request: The request to patch.
    :meta private:
                return super().__getitem__(key)
                raise DebugFilesKeyError(request, key).with_traceback(
                    e.__traceback__
                ) from None
        super()._load_form_data()
        In debug mode, intercept a routing redirect and replace it with
        an error if the body will be discarded.
        With modern Werkzeug this shouldn't occur, since it now uses a
        308 status which tells the browser to resend the method and
        body.
        .. versionchanged:: 2.1
            Don't intercept 307 and 308 redirects.
        :meta private:
            or request.routing_exception.code in {307, 308}
            or request.method in {"GET", "HEAD", "OPTIONS"}
    would cause the browser to drop the method or body. This happens
    when method is not GET, HEAD or OPTIONS and the status code is not
    307 or 308.
            f"A request was sent to '{request.url}', but routing issued"
            f" a redirect to the canonical URL '{exc.new_url}'."
        if f"{request.base_url}/" == exc.new_url.partition("?")[0]:
                " The URL was defined with a trailing slash. Flask"
                " will redirect to the URL with a trailing slash if it"
                " was accessed without one."
            " Send requests to the canonical URL, or use 307 or 308 for"
            " routing redirects. Otherwise, browsers will drop form"
            " data.\n\n"
            "This exception is only raised in debug mode."
        super().__init__("".join(buf))
from werkzeug.routing import RequestRedirect
def test_routing_redirect_debugging(monkeypatch, app, client):
    app.debug = False
    rv = client.post("/foo", data={}, follow_redirects=True)
    assert rv.data == b"success"
    app.debug = True
        rv = client.get("/foo", data={}, follow_redirects=True)
        assert rv.data == b"success"
    monkeypatch.setattr(RequestRedirect, "code", 301)
    with client, pytest.raises(AssertionError) as e:
        client.post("/foo", data={})
    assert "canonical URL 'http://localhost/foo/'" in str(e.value)
        self,
        exc_type: t.Optional[type],
        exc_value: t.Optional[BaseException],
        tb: t.Optional[TracebackType],
        self,
        exc_type: t.Optional[type],
        exc_value: t.Optional[BaseException],
        tb: t.Optional[TracebackType],
        self,
        exc_type: t.Optional[type],
        exc_value: t.Optional[BaseException],
        tb: t.Optional[TracebackType],
                rv, status, headers = rv  # type: ignore[misc]
                    rv, status = rv  # type: ignore[misc]
                rv = self.response_class(
                    rv,
                    status=status,
                    headers=headers,  # type: ignore[arg-type]
                )
                rv.status = status
            rv.headers.update(headers)  # type: ignore[arg-type]
    return current_app.make_response(args)  # type: ignore
    from werkzeug.wrappers.response import Response  # noqa: F401
    str,
    bytes,
    t.Iterator[str],
    t.Iterator[bytes],
    def _find_error_handler(self, e: Exception) -> t.Optional["ErrorHandlerCallable"]:
        def decorator(f: "ErrorHandlerCallable") -> "ErrorHandlerCallable":
            t.Dict[t.Optional[int], t.Dict[t.Type[Exception], "ErrorHandlerCallable"]],
        self, code_or_exception: t.Union[t.Type[Exception], int]
    ) -> t.Callable[["ErrorHandlerCallable"], "ErrorHandlerCallable"]:
        def decorator(f: "ErrorHandlerCallable") -> "ErrorHandlerCallable":
        code_or_exception: t.Union[t.Type[Exception], int],
        f: "ErrorHandlerCallable",
        self.error_handler_spec[None][code][exc_class] = f
# This should take Exception, but that either breaks typing the argument
# with a specific exception, or decorating multiple times with different
# exceptions (and using a union type on the argument).
# https://github.com/pallets/flask/issues/4095
# https://github.com/pallets/flask/issues/4295
# https://github.com/pallets/flask/issues/4297
ErrorHandlerCallable = t.Callable[[t.Any], ResponseReturnValue]
        # Store the Click context and push it in the loader thread so
        # script_info is still available.
        ctx = click.get_current_context(silent=True)
                if ctx is not None:
                    click.globals.push_context(ctx)
    def _copy_environ(self, other):
        return {
            **self.environ_base,
            **other,
            "flask._preserve_context": self.preserve_context,
        }
    def _request_from_builder_args(self, args, kwargs):
        kwargs["environ_base"] = self._copy_environ(kwargs.get("environ_base", {}))
        builder = EnvironBuilder(self.application, *args, **kwargs)
        try:
            return builder.get_request()
        finally:
            builder.close()
        if args and isinstance(
            args[0], (werkzeug.test.EnvironBuilder, dict, BaseRequest)
        ):
            if isinstance(args[0], werkzeug.test.EnvironBuilder):
                builder = copy(args[0])
                builder.environ_base = self._copy_environ(builder.environ_base or {})
            elif isinstance(args[0], dict):
                    args[0], app=self.application, environ_base=self._copy_environ({})
            else:
                # isinstance(args[0], BaseRequest)
                request = copy(args[0])
                request.environ = self._copy_environ(request.environ)
        else:
            # request is None
            request = self._request_from_builder_args(args, kwargs)
import warnings
    # suppress Werkzeug 0.15 warning about name mismatch
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Current server name", UserWarning, "flask.app"
        )
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Current server name", UserWarning, "flask.app"
        )
import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Current server name", UserWarning, "flask.app"
        )
        return super().open(
            request,
            buffered=buffered,
            follow_redirects=follow_redirects,
        )
            "This decorator can only be used when a request context is"
            " active, such as within a view function."
    top._after_request_functions.append(f)
            "This decorator can only be used when a request context is"
            " active, such as within a view function."
    if mod is not None and hasattr(mod, "__file__") and mod.__file__ is not None:
    def g(self) -> _AppCtxGlobals:
        import warnings
        warnings.warn(
            "Accessing 'g' on the request context is deprecated and"
            " will be removed in Flask 2.2. Access `g` directly or from"
            "the application context instead.",
            DeprecationWarning,
            stacklevel=2,
        )
    def g(self, value: _AppCtxGlobals) -> None:
        import warnings
        warnings.warn(
            "Setting 'g' on the request context is deprecated and"
            " will be removed in Flask 2.2. Set it on the application"
            " context instead.",
            DeprecationWarning,
            stacklevel=2,
        )
    Multiple requests with the same session may be sent and handled
    concurrently. When implementing a new session interface, consider
    whether reads or writes to the backing store must be synchronized.
    There is no guarantee on the order in which the session for each
    request is opened or saved, it will occur in the order that requests
    begin and end processing.
        pushing the request context, before matching the URL.
        This must return an object which implements a dictionary-like
        interface as well as the :class:`SessionMixin` interface.
        This will return ``None`` to indicate that loading failed in
        some way that is not immediately an error. The request
        context will fall back to using :meth:`make_null_session`
        in this case.
        a response, before removing the request context. It is skipped
        if :meth:`is_null_session` returns ``True``.
from .globals import _request_ctx_stack
    from werkzeug.test import TestResponse
    def open(
    ) -> "TestResponse":
        as_tuple = kwargs.pop("as_tuple", None)
        if as_tuple is not None:
            import warnings
            warnings.warn(
                "'as_tuple' is deprecated and will be removed in"
                " Werkzeug 2.1 and Flask 2.1. Use"
                " 'response.request.environ' instead.",
                DeprecationWarning,
                stacklevel=3,
            )
            return super().open(
                request,
                as_tuple=as_tuple,
                buffered=buffered,
                follow_redirects=follow_redirects,
            )
        else:
            return super().open(
                request,
                buffered=buffered,
                follow_redirects=follow_redirects,
            )
            cli = self.app.cli  # type: ignore
            " 2.2.",
            " 'max_age'. The old name will be removed in Flask 2.2.",
            " old name will be removed in Flask 2.2.",
            " old name will be removed in Flask 2.2.",
            bp_desc = "this" if app.blueprints[name] is self else "a different"
            raise ValueError(
                f"The name '{self_name}' is already registered for"
                f" {bp_desc} blueprint{existing_at}. Use 'name=' to"
                f" provide a unique name."
            )
    with pytest.raises(ValueError):
        app.register_blueprint(bp)  # same bp, same name, error
    return _json.dumps(obj, **kwargs)
            import json
            app.config.from_file("config.json", load=json.load)
def find_best_app(module):
                app = app_factory()
def find_app_by_string(module, app_name):
        args = []
        kwargs = {}
            app = attr(*args, **kwargs)
def locate_app(module_name, app_name, raise_if_not_found=True):
        return find_best_app(module)
        return find_app_by_string(module, app_name)
            app = self.create_app()
                app = locate_app(import_name, name)
                    app = locate_app(import_name, None, raise_if_not_found=False)
    cli.main()
    assert find_best_app(Module) == Module.app
    assert find_best_app(Module) == Module.application
    assert find_best_app(Module) == Module.myapp
    app = find_best_app(Module)
    app = find_best_app(Module)
    app = find_best_app(Module)
    assert find_best_app(Module) == Module.myapp
    assert find_best_app(Module) == Module.myapp
    pytest.raises(NoAppException, find_best_app, Module)
    pytest.raises(NoAppException, find_best_app, Module)
    pytest.raises(NoAppException, find_best_app, Module)
    pytest.raises(TypeError, find_best_app, Module)
    assert locate_app(iname, aname).name == result
        locate_app(iname, aname)
    app = locate_app("notanapp.py", None, raise_if_not_found=False)
        locate_app("cliapp.importerrorapp", None, raise_if_not_found=False)
import dataclasses
import platform
@pytest.mark.xfail(platform.python_implementation() == "PyPy", reason="flaky on pypy")
        # reduce flakiness by waiting for the internal loading lock
        with lazy._lock:
            lazy._flush_bg_loading_exception()
__version__ = "2.0.2"
        names: t.Iterable[t.Optional[str]] = (None,)
        # A template may be rendered outside a request context.
        if request:
            names = chain(names, reversed(request.blueprints))
        # The values passed to render_template take precedence. Keep a
        # copy to re-apply after all context functions.
        for name in names:
            if name in self.template_context_processors:
                for func in self.template_context_processors[name]:
                    context.update(func())
        names = (*request.blueprints, None)
        for c in (code, None) if code is not None else (None,):
            for name in names:
        names: t.Iterable[t.Optional[str]] = (None,)
        # url_for may be called outside a request context, parse the
        # passed endpoint instead of using request.blueprints.
            names = chain(
                names, reversed(_split_blueprint_path(endpoint.rpartition(".")[0]))
        for name in names:
            if name in self.url_default_functions:
                for func in self.url_default_functions[name]:
                    func(endpoint, values)
        names = (None, *reversed(request.blueprints))
        for name in names:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)
        for name in names:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()
                    if rv is not None:
                        return rv
        for func in ctx._after_request_functions:
            response = self.ensure_sync(func)(response)
        for name in chain(request.blueprints, (None,)):
                for func in reversed(self.after_request_funcs[name]):
                    response = self.ensure_sync(func)(response)
        for name in chain(request.blueprints, (None,)):
                for func in reversed(self.teardown_request_funcs[name]):
                    self.ensure_sync(func)(exc)
            ) from None
                    ).with_traceback(sys.exc_info()[2]) from None
            except TypeError as e:
                ) from e
        ) from None
            ) from None
    except AttributeError as e:
        ) from e
        except TypeError as e:
            ) from e
    except ImportError as e:
                f"While importing {module_name!r}, an ImportError was raised."
            ) from e
            raise NoAppException(f"Could not import {module_name!r}.") from e
                    ) from None
            except KeyError as e:
                raise DebugFilesKeyError(request, key) from e
            ) from None
            ) from None
def test_lazy_load_error(monkeypatch):
    re-raised.
    class BadExc(Exception):
        pass
    def bad_load():
        raise BadExc
    lazy = DispatchingApp(bad_load, use_eager_loading=False)
    with pytest.raises(BadExc):
        lazy._flush_bg_loading_exception()