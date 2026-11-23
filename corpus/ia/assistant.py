# Code genere par un LLM (ChatGPT), un seul prompt, aucune consigne de style. Prompt exact, date et version du modele : non conserves.
# Domaine : internals d'un micro-framework web. 39 fonctions + 6 classes, 452 lignes.
# Ce fichier est la version SAINE : l'indentation est intacte, le fichier parse.
# Le meme code passe par un PDF (indentation detruite sur ~20 % des lignes) est
# conserve dans assistant_via_pdf.py : c'est l'illustration vivante du PIEGE 2 (le label).
import json
import re
import html
import os
import time
import secrets
from http import HTTPStatus
from http.cookies import SimpleCookie
from functools import wraps
from urllib.parse import parse_qs, urlsplit


def compile_route(pattern):
    parts = pattern.strip('/').split('/') if pattern.strip('/') else []
    converters = {'int': r'\d+', 'str': r'[^/]+', 'path': r'.+'}
    names = []
    regex = []
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            spec = part[1:-1]
            if ':' in spec:
                name, kind = spec.split(':', 1)
            else:
                name, kind = spec, 'str'
            names.append(name)
            regex.append(f'(?P<{name}>{converters.get(kind, converters["str"])})')
        else:
            regex.append(re.escape(part))
    return re.compile('^/' + '/'.join(regex) + '/?$'), names


def match_route(pattern, path):
    regex, _ = compile_route(pattern)
    match = regex.match(path)
    return match.groupdict() if match else None


def route_url(pattern, **values):
    result = pattern
    for match in re.finditer(r'<([^>]+)>', pattern):
        name = match.group(1).split(':', 1)[0]
        if name not in values:
            raise KeyError(name)
        result = result.replace(match.group(0), str(values[name]), 1)
    return result


def normalize_path(path):
    parsed = urlsplit(path)
    clean = re.sub(r'/+', '/', parsed.path or '/')
    if clean != '/' and clean.endswith('/'):
        clean = clean[:-1]
    return clean


def parse_query_string(query):
    parsed = parse_qs(query, keep_blank_values=True)
    return {key: values[0] if len(values) == 1 else values
            for key, values in parsed.items()}


def parse_headers(raw_headers):
    headers = {}
    for line in raw_headers.splitlines():
        if line.strip() and ':' in line:
            name, value = line.split(':', 1)
            headers[name.strip().lower()] = value.strip()
    return headers


def get_header(headers, name, default=None):
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted:
            return value
    return default


def parse_accept(header):
    choices = []
    for item in (header or '').split(','):
        chunks = [x.strip() for x in item.split(';')]
        media = chunks[0]
        quality = 1.0
        for parameter in chunks[1:]:
            if parameter.startswith('q='):
                try:
                    quality = float(parameter[2:])
                except ValueError:
                    quality = 0.0
        choices.append((media, quality))
    return sorted(choices, key=lambda item: item[1], reverse=True)


def parse_content_type(value):
    if not value:
        return None, {}
    pieces = [part.strip() for part in value.split(';')]
    media_type = pieces[0].lower()
    parameters = {}
    for piece in pieces[1:]:
        if '=' in piece:
            key, val = piece.split('=', 1)
            parameters[key.strip().lower()] = val.strip().strip('"')
    return media_type, parameters


def parse_authorization(value):
    if not value:
        return None, None
    parts = value.split(None, 1)
    return parts[0].lower(), parts[1] if len(parts) == 2 else ''


def json_dumps(value, pretty=False):
    options = {'ensure_ascii': False, 'allow_nan': False, 'separators': (',', ':')}
    if pretty:
        options.update(indent=2, separators=(',', ': '))
    return json.dumps(value, **options)


def json_response(data, status=200, headers=None):
    body = json_dumps(data).encode('utf-8')
    result = {'Content-Type': 'application/json; charset=utf-8',
              'Content-Length': str(len(body))}
    if headers:
        result.update(headers)
    return status, result, body


def json_loads(body):
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return None if not body.strip() else json.loads(body)


def merge_config(base, override):
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result


def load_config_from_env(prefix='APP_'):
    config = {}
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        name = key[len(prefix):].lower()
        if value.lower() in {'true', 'false'}:
            parsed = value.lower() == 'true'
        else:
            try:
                parsed = int(value)
            except ValueError:
                try:
                    parsed = float(value)
                except ValueError:
                    parsed = value
        config[name] = parsed
    return config


def load_config_file(path):
    namespace = {}
    with open(path, 'r', encoding='utf-8') as handle:
        source = handle.read()
    exec(compile(source, path, 'exec'), {}, namespace)
    return {key: value for key, value in namespace.items() if not key.startswith('_')}


def get_config(config, key, default=None, cast=None):
    value = config.get(key, default)
    if value is None or cast is None:
        return value
    try:
        return cast(value)
    except (TypeError, ValueError):
        return default


class RequestContext:
    def __init__(self, method='GET', path='/', headers=None, body=b''):
        self.method = method.upper()
        self.path = normalize_path(path)
        self.headers = headers or {}
        self.body = body
        self.params = {}
        self.state = {}
        self.started_at = time.monotonic()

    def header(self, name, default=None):
        return get_header(self.headers, name, default)

    def json(self):
        return json_loads(self.body)


class ResponseContext:
    def __init__(self, body='', status=200, headers=None):
        self.status = status
        self.headers = dict(headers or {})
        self.body = body.encode('utf-8') if isinstance(body, str) else body

    def set_header(self, name, value):
        self.headers[name] = str(value)

    def finalize(self):
        self.headers.setdefault('Content-Length', str(len(self.body)))
        return self.status, self.headers, self.body


class URLRouter:
    def __init__(self):
        self.routes = []

    def add(self, pattern, handler, methods=('GET',)):
        regex, _ = compile_route(pattern)
        self.routes.append((regex, {m.upper() for m in methods}, handler))

    def dispatch(self, path, method='GET'):
        for regex, methods, handler in self.routes:
            match = regex.match(normalize_path(path))
            if match and method.upper() in methods:
                return handler, match.groupdict()
        return None, {}


def parse_cookie_header(value):
    cookies = SimpleCookie()
    cookies.load(value or '')
    return {key: morsel.value for key, morsel in cookies.items()}


def make_cookie(name, value, max_age=None, path='/', secure=False, httponly=True):
    cookie = SimpleCookie()
    cookie[name] = value
    morsel = cookie[name]
    morsel['path'] = path
    if max_age is not None:
        morsel['max-age'] = str(max_age)
    if secure:
        morsel['secure'] = True
    if httponly:
        morsel['httponly'] = True
    return morsel.OutputString()


def delete_cookie(name, path='/'):
    return make_cookie(name, '', max_age=0, path=path)


class Session:
    def __init__(self, cookies=None, key='session'):
        self.key = key
        self.data = dict((cookies or {}).get(key, {}))
        self.modified = False

    def get(self, name, default=None):
        return self.data.get(name, default)

    def set(self, name, value):
        self.data[name] = value
        self.modified = True

    def pop(self, name, default=None):
        value = self.data.pop(name, default)
        self.modified = True
        return value


def sign_value(value, secret):
    import hashlib
    import hmac
    digest = hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()
    return f'{value}.{digest}'


def verify_signed_value(signed, secret):
    import hashlib
    import hmac
    try:
        value, signature = signed.rsplit('.', 1)
    except ValueError:
        return None
    expected = hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()
    return value if hmac.compare_digest(signature, expected) else None


class HTTPError(Exception):
    def __init__(self, status, message=None, headers=None):
        self.status = int(status)
        self.message = message or HTTPStatus(self.status).phrase
        self.headers = headers or {}
        super().__init__(self.message)


def http_error_response(error):
    return json_response({'error': error.message, 'status': error.status},
                         error.status, error.headers)


def not_found_response(message='Not Found'):
    return json_response({'error': message}, 404)


def method_not_allowed_response(allowed):
    headers = {'Allow': ', '.join(sorted(set(allowed)))}
    return json_response({'error': 'Method Not Allowed'}, 405, headers)


def abort(status, message=None):
    raise HTTPError(status, message)


class TestResponse:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def text(self):
        return self.body.decode('utf-8')

    def json(self):
        return json_loads(self.body)


def make_test_request(method='GET', path='/', headers=None, body=b''):
    return RequestContext(method=method, path=path, headers=headers or {}, body=body)


def assert_response(response, status=None, contains=None):
    if status is not None and response.status != status:
        raise AssertionError(f'expected status {status}, got {response.status}')
    if contains is not None and contains not in response.text:
        raise AssertionError(f'{contains!r} not found in response body')
    return True


def render_template(source, context=None, escape=True):
    values = context or {}

    def replace(match):
        name = match.group(1).strip()
        value = values.get(name, '')
        text = str(value)
        return html.escape(text) if escape else text

    return re.sub(r'{{\s*([^{}]+?)\s*}}', replace, source)


def load_template(path, context=None, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as handle:
        source = handle.read()
    return render_template(source, context)


def template_from_string(source, **context):
    return render_template(source, context)


def before_request(callback):
    @wraps(callback)
    def wrapper(request, *args, **kwargs):
        result = callback(request)
        return result
    return wrapper


def after_request(callback):
    @wraps(callback)
    def wrapper(response, *args, **kwargs):
        result = callback(response)
        return response if result is None else result
    return wrapper


def route(pattern, methods=('GET',)):
    def decorator(handler):
        handler.route_pattern = pattern
        handler.route_methods = tuple(method.upper() for method in methods)
        return handler
    return decorator


def require_methods(*methods):
    allowed = {method.upper() for method in methods}

    def decorator(handler):
        @wraps(handler)
        def wrapper(request, *args, **kwargs):
            if request.method not in allowed:
                raise HTTPError(405, 'Method Not Allowed',
                                {'Allow': ', '.join(sorted(allowed))})
            return handler(request, *args, **kwargs)
        return wrapper
    return decorator


def cached_response(max_age=60):
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            response = handler(*args, **kwargs)
            if isinstance(response, ResponseContext):
                response.set_header('Cache-Control', f'public, max-age={int(max_age)}')
            return response
        return wrapper
    return decorator


def cors(allow_origin='*'):
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            response = handler(*args, **kwargs)
            if isinstance(response, ResponseContext):
                response.set_header('Access-Control-Allow-Origin', allow_origin)
            return response
        return wrapper
    return decorator


def generate_session_id(length=32):
    if length < 16:
        raise ValueError('session identifiers should be at least 16 characters')
    return secrets.token_urlsafe(length)[:length]


def parse_range_header(value, size):
    if not value or not value.startswith('bytes='):
        return None
    first = value[6:].split(',', 1)[0].strip()
    if '-' not in first:
        return None
    start, end = first.split('-', 1)
    try:
        if not start:
            length = int(end)
            return max(0, size - length), size - 1
        start = int(start)
        end = int(end) if end else size - 1
    except ValueError:
        return None
    if start < 0 or start >= size or end < start:
        return None
    return start, min(end, size - 1)
