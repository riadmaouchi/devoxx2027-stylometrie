# Code genere par un LLM (Claude, modele configure claude-opus-5-5), un seul prompt, aucune consigne de style.
# Domaine : internals d'un micro-framework web. Genere le 3 novembre 2026 par un agent sans contexte.
# Ce fichier n'a pas ete retouche. L'agent ne connaissait ni le talk ni l'experience. Prompt exact, en entier :
# Ce fichier : « Écris en Python les internals d'un micro-framework web : 39 fonctions et 6 classes. Écris le
# Ce fichier : resultat dans le fichier /home/claude/work/ia2/generated.py (crée le dossier s'il n'existe pas).
# Ce fichier : Ne lance rien, n'ajoute aucun autre fichier. Quand c'est fait, réponds seulement « fait » et le
# Ce fichier : nombre de lignes du fichier. »
"""Internals d'un micro-framework web WSGI minimaliste.

Contenu : 39 fonctions de module et 6 classes
(HTTPError, Request, Response, Route, Router, App).
"""

import functools
import hashlib
import html
import io
import json
import mimetypes
import os
import re
import sys
import time
import traceback
from email.utils import formatdate
from urllib.parse import parse_qs, quote, unquote, urlencode


HTTP_REASONS = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    413: "Payload Too Large",
    415: "Unsupported Media Type",
    422: "Unprocessable Entity",
    500: "Internal Server Error",
    501: "Not Implemented",
    503: "Service Unavailable",
}

MAX_BODY_SIZE = 10 * 1024 * 1024

_PARAM_RE = re.compile(r"<(?:(?P<conv>[a-z]+):)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)>")
_TEMPLATE_RE = re.compile(r"\{\{(.+?)\}\}")

_CONVERTERS = {
    "str": (r"[^/]+", str),
    "int": (r"-?\d+", int),
    "float": (r"-?\d+(?:\.\d+)?", float),
    "path": (r".+", str),
    "slug": (r"[A-Za-z0-9_-]+", str),
}


# ---------------------------------------------------------------------------
# Analyse de la requete
# ---------------------------------------------------------------------------

def parse_query_string(qs):
    """Transforme une query string en dict ; les cles repetees donnent des listes."""
    result = {}
    if not qs:
        return result
    for key, values in parse_qs(qs, keep_blank_values=True).items():
        result[key] = values[0] if len(values) == 1 else values
    return result


def parse_cookies(header):
    """Analyse l'en-tete Cookie en dict nom -> valeur."""
    cookies = {}
    if not header:
        return cookies
    for chunk in header.split(";"):
        if "=" not in chunk:
            continue
        name, _, value = chunk.strip().partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        cookies[name.strip()] = unquote(value)
    return cookies


def parse_content_type(header):
    """Retourne (type_mime, parametres) a partir d'un en-tete Content-Type."""
    if not header:
        return "", {}
    parts = header.split(";")
    mime = parts[0].strip().lower()
    params = {}
    for part in parts[1:]:
        key, sep, value = part.strip().partition("=")
        if sep:
            params[key.strip().lower()] = value.strip().strip('"')
    return mime, params


def parse_form_body(body, charset="utf-8"):
    """Decode un corps application/x-www-form-urlencoded."""
    return parse_query_string(body.decode(charset, errors="replace"))


def parse_json_body(body, charset="utf-8"):
    """Decode un corps JSON ; leve une HTTPError 400 s'il est invalide."""
    if not body:
        return None
    try:
        return json.loads(body.decode(charset))
    except (ValueError, UnicodeDecodeError) as exc:
        raise HTTPError(400, "JSON invalide : %s" % exc)


def read_body(environ, limit=MAX_BODY_SIZE):
    """Lit le corps brut de la requete en respectant une taille maximale."""
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        length = 0
    if length > limit:
        raise HTTPError(413)
    if length <= 0:
        return b""
    stream = environ.get("wsgi.input")
    if stream is None:
        return b""
    return stream.read(length)


def normalize_header_name(name):
    """Met un nom d'en-tete sous forme canonique : 'content_type' -> 'Content-Type'."""
    return "-".join(part.capitalize() for part in name.replace("_", "-").split("-"))


def extract_headers(environ):
    """Extrait les en-tetes HTTP d'un environ WSGI."""
    headers = {}
    for key, value in environ.items():
        if key.startswith("HTTP_"):
            headers[normalize_header_name(key[5:])] = value
        elif key in ("CONTENT_TYPE", "CONTENT_LENGTH") and value:
            headers[normalize_header_name(key)] = value
    return headers


# ---------------------------------------------------------------------------
# Utilitaires HTTP
# ---------------------------------------------------------------------------

def reason_phrase(code):
    """Retourne le libelle associe a un code HTTP."""
    return HTTP_REASONS.get(code, "Unknown")


def status_line(code):
    """Construit la ligne de statut WSGI, par exemple '404 Not Found'."""
    return "%d %s" % (code, reason_phrase(code))


def escape_html(value):
    """Echappe une valeur pour une insertion sure dans du HTML."""
    return html.escape(str(value), quote=True)


def format_cookie(name, value, max_age=None, path="/", domain=None,
                  secure=False, httponly=True, samesite="Lax"):
    """Construit la valeur d'un en-tete Set-Cookie."""
    parts = ["%s=%s" % (name, quote(str(value), safe=""))]
    if max_age is not None:
        parts.append("Max-Age=%d" % int(max_age))
        parts.append("Expires=%s" % http_date(time.time() + int(max_age)))
    if path:
        parts.append("Path=%s" % path)
    if domain:
        parts.append("Domain=%s" % domain)
    if secure:
        parts.append("Secure")
    if httponly:
        parts.append("HttpOnly")
    if samesite:
        parts.append("SameSite=%s" % samesite)
    return "; ".join(parts)


def guess_mime_type(filename, default="application/octet-stream"):
    """Devine le type MIME d'un fichier, avec charset pour le texte."""
    mime, _ = mimetypes.guess_type(filename)
    if mime is None:
        return default
    if mime.startswith("text/") or mime in ("application/javascript", "application/json"):
        return mime + "; charset=utf-8"
    return mime


def make_etag(data):
    """Calcule un ETag fort a partir du contenu."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return '"%s"' % hashlib.sha1(data).hexdigest()


def http_date(timestamp=None):
    """Formate un timestamp au format date HTTP (RFC 7231)."""
    return formatdate(timestamp if timestamp is not None else time.time(), usegmt=True)


# ---------------------------------------------------------------------------
# Chemins et routage
# ---------------------------------------------------------------------------

def compile_path(pattern):
    """Compile un motif '/users/<int:id>' en (regex, convertisseurs)."""
    regex = ["^"]
    converters = {}
    pos = 0
    for match in _PARAM_RE.finditer(pattern):
        regex.append(re.escape(pattern[pos:match.start()]))
        conv = match.group("conv") or "str"
        if conv not in _CONVERTERS:
            raise ValueError("Convertisseur inconnu : %s" % conv)
        name = match.group("name")
        if name in converters:
            raise ValueError("Parametre duplique : %s" % name)
        expr, func = _CONVERTERS[conv]
        regex.append("(?P<%s>%s)" % (name, expr))
        converters[name] = func
        pos = match.end()
    regex.append(re.escape(pattern[pos:]))
    regex.append("$")
    return re.compile("".join(regex)), converters


def convert_param(value, converter):
    """Convertit un segment d'URL ; une valeur invalide donne une 404."""
    try:
        return converter(unquote(value))
    except (TypeError, ValueError):
        raise HTTPError(404)


def match_path(regex, converters, path):
    """Teste un chemin contre une regex compilee et retourne les parametres convertis."""
    match = regex.match(path)
    if match is None:
        return None
    return {
        name: convert_param(value, converters[name])
        for name, value in match.groupdict().items()
    }


def split_path(path):
    """Decoupe un chemin en segments non vides."""
    return [segment for segment in path.split("/") if segment]


def join_paths(*parts):
    """Joint plusieurs morceaux de chemin en un chemin absolu propre."""
    segments = []
    for part in parts:
        segments.extend(split_path(part or ""))
    return "/" + "/".join(segments)


def normalize_path(path):
    """Resout '.' et '..' et retire les doubles slashs, sans sortir de la racine."""
    stack = []
    for segment in split_path(path):
        if segment == ".":
            continue
        if segment == "..":
            if stack:
                stack.pop()
            continue
        stack.append(segment)
    result = "/" + "/".join(stack)
    if path.endswith("/") and len(result) > 1:
        result += "/"
    return result


# ---------------------------------------------------------------------------
# Fabriques de reponses
# ---------------------------------------------------------------------------

def json_response(data, status=200, **kwargs):
    """Construit une reponse JSON."""
    body = json.dumps(data, ensure_ascii=False, default=str)
    return Response(body, status=status, content_type="application/json; charset=utf-8", **kwargs)


def html_response(body, status=200, **kwargs):
    """Construit une reponse HTML."""
    return Response(body, status=status, content_type="text/html; charset=utf-8", **kwargs)


def text_response(body, status=200, **kwargs):
    """Construit une reponse texte brut."""
    return Response(body, status=status, content_type="text/plain; charset=utf-8", **kwargs)


def redirect(location, status=302):
    """Construit une reponse de redirection."""
    response = Response(b"", status=status)
    response.headers["Location"] = location
    return response


def abort(code, message=None):
    """Interrompt le traitement avec une erreur HTTP."""
    raise HTTPError(code, message)


def error_response(error, debug=False):
    """Transforme une HTTPError en reponse HTML (avec trace en mode debug)."""
    reason = reason_phrase(error.code)
    message = error.message or reason
    body = "<h1>%d %s</h1><p>%s</p>" % (error.code, escape_html(reason), escape_html(message))
    if debug and error.__traceback__ is not None:
        trace = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        body += "<pre>%s</pre>" % escape_html(trace)
    response = html_response(body, status=error.code)
    response.headers.update(error.headers)
    return response


def send_file(path, root, request=None):
    """Sert un fichier situe sous root, avec ETag et protection contre la traversee."""
    root = os.path.abspath(root)
    full = os.path.abspath(os.path.join(root, normalize_path(path).lstrip("/")))
    if full != root and not full.startswith(root + os.sep):
        raise HTTPError(403)
    if not os.path.isfile(full):
        raise HTTPError(404)
    stat = os.stat(full)
    etag = '"%x-%x"' % (int(stat.st_mtime), stat.st_size)
    if request is not None and request.header("If-None-Match") == etag:
        response = Response(b"", status=304)
        response.headers["ETag"] = etag
        return response
    with open(full, "rb") as handle:
        data = handle.read()
    response = Response(data, content_type=guess_mime_type(full))
    response.headers["ETag"] = etag
    response.headers["Last-Modified"] = http_date(stat.st_mtime)
    return response


def render_template(template, context=None, autoescape=True):
    """Moteur de gabarits minimal : {{ var }}, {{ obj.attr }}, {{ var|safe }}."""
    context = context or {}
    output = []
    pos = 0
    for match in _TEMPLATE_RE.finditer(template):
        output.append(template[pos:match.start()])
        expr = match.group(1).strip()
        raw = expr.endswith("|safe")
        if raw:
            expr = expr[:-5].strip()
        value = context
        for part in expr.split("."):
            if isinstance(value, dict):
                value = value.get(part, "")
            else:
                value = getattr(value, part, "")
        text = "" if value is None else str(value)
        output.append(text if raw or not autoescape else escape_html(text))
        pos = match.end()
    output.append(template[pos:])
    return "".join(output)


# ---------------------------------------------------------------------------
# Middlewares : signature middleware(request, call_next) -> Response
# ---------------------------------------------------------------------------

def compose_middleware(handler, middlewares):
    """Enchaine les middlewares autour du handler ; le premier est le plus externe."""
    composed = handler
    for middleware in reversed(list(middlewares)):
        composed = functools.partial(middleware, call_next=composed)
    return composed


def logging_middleware(request, call_next):
    """Journalise methode, chemin, statut et duree de chaque requete."""
    start = time.perf_counter()
    response = call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    stream = request.environ.get("wsgi.errors", sys.stderr)
    stream.write("%s %s -> %d (%.1f ms)\n" % (request.method, request.path, response.status, elapsed))
    return response


def cors_middleware(request, call_next):
    """Gere les en-tetes CORS et les requetes preflight."""
    config = request.app.config if request.app else {}
    origins = config.get("cors_origins", "*")
    origin = request.header("Origin")
    if request.method == "OPTIONS" and origin and request.header("Access-Control-Request-Method"):
        response = Response(b"", status=204)
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = request.header(
            "Access-Control-Request-Headers", "Content-Type")
        response.headers["Access-Control-Max-Age"] = "600"
    else:
        response = call_next(request)
    if origin and (origins == "*" or origin in origins):
        response.headers["Access-Control-Allow-Origin"] = "*" if origins == "*" else origin
        response.headers["Vary"] = "Origin"
    return response


def exception_middleware(request, call_next):
    """Convertit les exceptions en reponses d'erreur."""
    debug = request.app.debug if request.app else False
    try:
        return call_next(request)
    except HTTPError as error:
        return error_response(error, debug=debug)
    except Exception as exc:
        traceback.print_exc(file=request.environ.get("wsgi.errors", sys.stderr))
        error = HTTPError(500, str(exc) if debug else None).with_traceback(exc.__traceback__)
        return error_response(error, debug=debug)


def static_middleware(request, call_next):
    """Sert les fichiers statiques sous config['static_prefix']."""
    config = request.app.config if request.app else {}
    prefix = config.get("static_prefix", "/static/")
    root = config.get("static_root")
    if root and request.method in ("GET", "HEAD") and request.path.startswith(prefix):
        return send_file(request.path[len(prefix):], root, request)
    return call_next(request)


def method_override_middleware(request, call_next):
    """Permet a un POST de se faire passer pour PUT, PATCH ou DELETE."""
    if request.method == "POST":
        override = request.header("X-HTTP-Method-Override")
        if not override and request.content_type == "application/x-www-form-urlencoded":
            override = request.form.get("_method")
        if override and override.upper() in ("PUT", "PATCH", "DELETE"):
            request.method = override.upper()
    return call_next(request)


# ---------------------------------------------------------------------------
# Outils WSGI
# ---------------------------------------------------------------------------

def build_environ(method="GET", path="/", query="", body=b"", headers=None):
    """Fabrique un environ WSGI synthetique (tests)."""
    if "?" in path and not query:
        path, _, query = path.partition("?")
    if isinstance(body, str):
        body = body.encode("utf-8")
    environ = {
        "REQUEST_METHOD": method.upper(),
        "PATH_INFO": path,
        "QUERY_STRING": query,
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "http",
        "wsgi.input": io.BytesIO(body),
        "wsgi.errors": io.StringIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
    }
    for name, value in (headers or {}).items():
        key = name.upper().replace("-", "_")
        if key in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            environ[key] = value
        else:
            environ["HTTP_" + key] = value
    return environ


def call_wsgi(app, environ):
    """Appelle une application WSGI et retourne (statut, en-tetes, corps)."""
    captured = {}
    start_response = lambda status, headers, exc_info=None: captured.update(  # noqa: E731
        status=status, headers=headers)
    chunks = app(environ, start_response)
    try:
        body = b"".join(chunks)
    finally:
        if hasattr(chunks, "close"):
            chunks.close()
    code = int(captured.get("status", "500").split(" ", 1)[0])
    return code, dict(captured.get("headers", [])), body


def run_server(app, host="127.0.0.1", port=8000):
    """Lance un serveur de developpement wsgiref."""
    from wsgiref.simple_server import make_server

    with make_server(host, port, app) as server:
        sys.stderr.write("Serveur sur http://%s:%d\n" % (host, port))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def create_app(name=None, debug=False, **config):
    """Cree une App preconfiguree avec les middlewares usuels."""
    app = App(name or "app", debug=debug, config=config)
    if debug:
        app.use(logging_middleware)
    app.use(exception_middleware)
    if config.get("static_root"):
        app.use(static_middleware)
    if config.get("cors_origins"):
        app.use(cors_middleware)
    app.use(method_override_middleware)
    return app


# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class HTTPError(Exception):
    """Erreur HTTP portant un code, un message et des en-tetes optionnels."""

    def __init__(self, code, message=None, headers=None):
        super().__init__(message or reason_phrase(code))
        self.code = code
        self.message = message
        self.headers = dict(headers or {})

    def __repr__(self):
        return "HTTPError(%d, %r)" % (self.code, self.message)


class Request:
    """Requete HTTP construite a partir d'un environ WSGI, avec analyse paresseuse."""

    def __init__(self, environ, app=None):
        self.environ = environ
        self.app = app
        self.method = environ.get("REQUEST_METHOD", "GET").upper()
        self.path = normalize_path(environ.get("PATH_INFO") or "/")
        self.query_string = environ.get("QUERY_STRING", "")
        self.headers = extract_headers(environ)
        self.params = {}
        self.route = None
        self.state = {}
        self._query = None
        self._body = None
        self._form = None
        self._cookies = None
        self._json = None
        self._json_loaded = False

    def header(self, name, default=None):
        return self.headers.get(normalize_header_name(name), default)

    @property
    def query(self):
        if self._query is None:
            self._query = parse_query_string(self.query_string)
        return self._query

    @property
    def content_type(self):
        return parse_content_type(self.header("Content-Type"))[0]

    @property
    def charset(self):
        return parse_content_type(self.header("Content-Type"))[1].get("charset", "utf-8")

    @property
    def body(self):
        if self._body is None:
            limit = MAX_BODY_SIZE
            if self.app is not None:
                limit = self.app.config.get("max_body_size", MAX_BODY_SIZE)
            self._body = read_body(self.environ, limit)
        return self._body

    @property
    def form(self):
        if self._form is None:
            if self.content_type == "application/x-www-form-urlencoded":
                self._form = parse_form_body(self.body, self.charset)
            else:
                self._form = {}
        return self._form

    @property
    def json(self):
        if not self._json_loaded:
            ctype = self.content_type
            if ctype == "application/json" or ctype.endswith("+json"):
                self._json = parse_json_body(self.body, self.charset)
            self._json_loaded = True
        return self._json

    @property
    def cookies(self):
        if self._cookies is None:
            self._cookies = parse_cookies(self.header("Cookie"))
        return self._cookies

    @property
    def url(self):
        scheme = self.environ.get("wsgi.url_scheme", "http")
        host = self.header("Host") or "%s:%s" % (
            self.environ.get("SERVER_NAME", "localhost"),
            self.environ.get("SERVER_PORT", "80"),
        )
        url = "%s://%s%s" % (scheme, host, quote(self.path))
        if self.query_string:
            url += "?" + self.query_string
        return url

    def wants_json(self):
        accept = self.header("Accept", "")
        return "application/json" in accept and "text/html" not in accept

    def __repr__(self):
        return "<Request %s %s>" % (self.method, self.path)


class Response:
    """Reponse HTTP, appelable comme une application WSGI."""

    def __init__(self, body=b"", status=200, content_type="text/html; charset=utf-8", headers=None):
        self.status = status
        self.headers = dict(headers or {})
        self.headers.setdefault("Content-Type", content_type)
        self._cookies = []
        self._body = b""
        self.body = body

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if value is None:
            value = b""
        if isinstance(value, str):
            value = value.encode("utf-8")
        self._body = bytes(value)

    @property
    def status_text(self):
        return status_line(self.status)

    def set_cookie(self, name, value, **options):
        self._cookies.append(format_cookie(name, value, **options))

    def delete_cookie(self, name, path="/"):
        self._cookies.append(format_cookie(name, "", max_age=0, path=path))

    def add_etag(self, request=None):
        etag = make_etag(self._body)
        self.headers["ETag"] = etag
        if (request is not None and self.status == 200
                and request.method in ("GET", "HEAD")
                and request.header("If-None-Match") == etag):
            self.status = 304
            self._body = b""
        return self

    def header_list(self):
        headers = [(name, str(value)) for name, value in self.headers.items()]
        if self.status in (204, 304):
            headers = [(n, v) for n, v in headers if n.lower() not in ("content-type", "content-length")]
        else:
            headers = [(n, v) for n, v in headers if n.lower() != "content-length"]
            headers.append(("Content-Length", str(len(self._body))))
        headers.extend(("Set-Cookie", cookie) for cookie in self._cookies)
        return headers

    def __call__(self, environ, start_response):
        start_response(self.status_text, self.header_list())
        if environ.get("REQUEST_METHOD") == "HEAD" or self.status in (204, 304):
            return [b""]
        return [self._body]

    def __repr__(self):
        return "<Response %s>" % self.status_text


class Route:
    """Association d'un motif de chemin, de methodes et d'un handler."""

    def __init__(self, pattern, handler, methods=("GET",), name=None):
        self.pattern = normalize_path(pattern)
        self.handler = handler
        self.methods = {method.upper() for method in methods}
        if "GET" in self.methods:
            self.methods.add("HEAD")
        self.name = name or getattr(handler, "__name__", self.pattern)
        self.regex, self.converters = compile_path(self.pattern)

    def match(self, path):
        return match_path(self.regex, self.converters, path)

    def allows(self, method):
        return method.upper() in self.methods

    def build(self, **params):
        missing = set(self.converters) - set(params)
        if missing:
            raise ValueError("Parametres manquants pour %s : %s" % (self.name, ", ".join(sorted(missing))))
        path = _PARAM_RE.sub(
            lambda m: quote(str(params[m.group("name")]), safe="/" if m.group("conv") == "path" else ""),
            self.pattern,
        )
        extra = {key: value for key, value in params.items() if key not in self.converters}
        if extra:
            path += "?" + urlencode(extra, doseq=True)
        return path

    def __repr__(self):
        return "<Route %s %s -> %s>" % (",".join(sorted(self.methods)), self.pattern, self.name)


class Router:
    """Table de routes avec resolution, decorateurs et construction d'URL."""

    def __init__(self, prefix=""):
        self.prefix = prefix
        self.routes = []
        self._by_name = {}

    def add(self, pattern, handler, methods=("GET",), name=None):
        route = Route(join_paths(self.prefix, pattern), handler, methods, name)
        if route.name in self._by_name:
            raise ValueError("Nom de route deja utilise : %s" % route.name)
        self.routes.append(route)
        self._by_name[route.name] = route
        return route

    def route(self, pattern, methods=("GET",), name=None):
        return lambda handler: (self.add(pattern, handler, methods, name), handler)[1]

    def get(self, pattern, name=None):
        return self.route(pattern, ("GET",), name)

    def post(self, pattern, name=None):
        return self.route(pattern, ("POST",), name)

    def put(self, pattern, name=None):
        return self.route(pattern, ("PUT",), name)

    def delete(self, pattern, name=None):
        return self.route(pattern, ("DELETE",), name)

    def include(self, other, prefix=""):
        for route in other.routes:
            self.add(join_paths(prefix, route.pattern), route.handler,
                     route.methods - {"HEAD"}, route.name)

    def resolve(self, method, path):
        path = path.rstrip("/") or "/"
        allowed = set()
        for route in self.routes:
            params = route.match(path)
            if params is None:
                continue
            if route.allows(method):
                return route, params
            allowed |= route.methods
        if allowed:
            raise HTTPError(405, headers={"Allow": ", ".join(sorted(allowed))})
        raise HTTPError(404)

    def url_for(self, name, **params):
        route = self._by_name.get(name)
        if route is None:
            raise LookupError("Route inconnue : %s" % name)
        return route.build(**params)


class App:
    """Application WSGI : routage, middlewares, hooks et gestionnaires d'erreurs."""

    def __init__(self, name="app", debug=False, config=None):
        self.name = name
        self.debug = debug
        self.config = dict(config or {})
        self.router = Router()
        self.middlewares = []
        self.error_handlers = {}
        self.before_hooks = []
        self.after_hooks = []
        self._pipeline = None

    def route(self, pattern, methods=("GET",), name=None):
        return self.router.route(pattern, methods, name)

    def get(self, pattern, name=None):
        return self.router.get(pattern, name)

    def post(self, pattern, name=None):
        return self.router.post(pattern, name)

    def use(self, middleware):
        self.middlewares.append(middleware)
        self._pipeline = None
        return middleware

    def before_request(self, func):
        self.before_hooks.append(func)
        return func

    def after_request(self, func):
        self.after_hooks.append(func)
        return func

    def errorhandler(self, code):
        return lambda func: (self.error_handlers.__setitem__(code, func), func)[1]

    def url_for(self, name, **params):
        return self.router.url_for(name, **params)

    def make_response(self, result):
        if isinstance(result, Response):
            return result
        status = 200
        if isinstance(result, tuple):
            result, status = result[0], result[1]
        if isinstance(result, Response):
            result.status = status
            return result
        if result is None:
            return Response(b"", status=204 if status == 200 else status)
        if isinstance(result, (dict, list)):
            return json_response(result, status)
        if isinstance(result, bytes):
            return Response(result, status=status, content_type="application/octet-stream")
        return html_response(str(result), status)

    def dispatch(self, request):
        for hook in self.before_hooks:
            early = hook(request)
            if early is not None:
                return self.make_response(early)
        try:
            route, params = self.router.resolve(request.method, request.path)
            request.route = route
            request.params = params
            response = self.make_response(route.handler(request, **params))
        except HTTPError as error:
            handler = self.error_handlers.get(error.code)
            if handler is None:
                raise
            response = self.make_response(handler(request, error))
            if response.status == 200:
                response.status = error.code
        for hook in self.after_hooks:
            response = hook(request, response) or response
        return response

    def handle(self, request):
        if self._pipeline is None:
            self._pipeline = compose_middleware(self.dispatch, self.middlewares)
        return self._pipeline(request)

    def __call__(self, environ, start_response):
        request = Request(environ, app=self)
        try:
            response = self.handle(request)
        except HTTPError as error:
            response = error_response(error, self.debug)
        except Exception as exc:
            traceback.print_exc(file=environ.get("wsgi.errors", sys.stderr))
            error = HTTPError(500, str(exc) if self.debug else None).with_traceback(exc.__traceback__)
            response = error_response(error, self.debug)
        return response(environ, start_response)

    def test(self, method="GET", path="/", **kwargs):
        return call_wsgi(self, build_environ(method, path, **kwargs))

    def run(self, host="127.0.0.1", port=8000):
        run_server(self, host, port)
