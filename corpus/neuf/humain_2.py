# Contributeur de github.com/pallets/flask (BSD-3-Clause), anonymise.
# CODE NEUF : uniquement les lignes ajoutees lors de la CREATION de fichiers
# (git log --diff-filter=A). Ecrit d'un coup, jamais refactore.
# Commits > 300 lignes et posterieurs a juin 2021 exclus.
import pytest
from flask import json_available
def test_json_available():
    with pytest.deprecated_call() as rec:
        assert json_available
        assert json_available == True  # noqa E712
        assert json_available != False  # noqa E712
    assert len(rec.list) == 3
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
from flask import Flask
application = Flask(__name__)
from flask import Flask
app = Flask(__name__)
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