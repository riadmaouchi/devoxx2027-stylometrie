# Contributeur de github.com/pallets/flask (BSD-3-Clause), anonymise.
# CODE NEUF : uniquement les lignes ajoutees lors de la CREATION de fichiers
# (git log --diff-filter=A). Ecrit d'un coup, jamais refactore.
# Commits > 300 lignes et posterieurs a juin 2021 exclus.
# -*- coding: utf-8 -*-
    tests.test_instance
    ~~~~~~~~~~~~~~~~~~~
    :copyright: (c) 2014 by the Flask Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
import os
import sys
import pytest
import flask
from flask._compat import PY2
def test_explicit_instance_paths(modules_tmpdir):
    with pytest.raises(ValueError) as excinfo:
        flask.Flask(__name__, instance_path='instance')
    assert 'must be absolute' in str(excinfo.value)
    app = flask.Flask(__name__, instance_path=str(modules_tmpdir))
    assert app.instance_path == str(modules_tmpdir)
def test_main_module_paths(modules_tmpdir, purge_module):
    app = modules_tmpdir.join('main_app.py')
    app.write('import flask\n\napp = flask.Flask("__main__")')
    purge_module('main_app')
    from main_app import app
    here = os.path.abspath(os.getcwd())
    assert app.instance_path == os.path.join(here, 'instance')
def test_uninstalled_module_paths(modules_tmpdir, purge_module):
    app = modules_tmpdir.join('config_module_app.py').write(
        'import os\n'
        'import flask\n'
        'here = os.path.abspath(os.path.dirname(__file__))\n'
        'app = flask.Flask(__name__)\n'
    )
    purge_module('config_module_app')
    from config_module_app import app
    assert app.instance_path == str(modules_tmpdir.join('instance'))
def test_uninstalled_package_paths(modules_tmpdir, purge_module):
    app = modules_tmpdir.mkdir('config_package_app')
    init = app.join('__init__.py')
    init.write(
        'import os\n'
        'import flask\n'
        'here = os.path.abspath(os.path.dirname(__file__))\n'
        'app = flask.Flask(__name__)\n'
    )
    purge_module('config_package_app')
    from config_package_app import app
    assert app.instance_path == str(modules_tmpdir.join('instance'))
def test_installed_module_paths(modules_tmpdir, modules_tmpdir_prefix,
                                purge_module, site_packages, limit_loader):
    site_packages.join('site_app.py').write(
        'import flask\n'
        'app = flask.Flask(__name__)\n'
    )
    purge_module('site_app')
    from site_app import app
    assert app.instance_path == \
        modules_tmpdir.join('var').join('site_app-instance')
def test_installed_package_paths(limit_loader, modules_tmpdir,
                                 modules_tmpdir_prefix, purge_module,
                                 monkeypatch):
    installed_path = modules_tmpdir.mkdir('path')
    monkeypatch.syspath_prepend(installed_path)
    app = installed_path.mkdir('installed_package')
    init = app.join('__init__.py')
    init.write('import flask\napp = flask.Flask(__name__)')
    purge_module('installed_package')
    from installed_package import app
    assert app.instance_path == \
        modules_tmpdir.join('var').join('installed_package-instance')
def test_prefix_package_paths(limit_loader, modules_tmpdir,
                              modules_tmpdir_prefix, purge_module,
                              site_packages):
    app = site_packages.mkdir('site_package')
    init = app.join('__init__.py')
    init.write('import flask\napp = flask.Flask(__name__)')
    purge_module('site_package')
    import site_package
    assert site_package.app.instance_path == \
        modules_tmpdir.join('var').join('site_package-instance')
def test_egg_installed_paths(install_egg, modules_tmpdir,
                             modules_tmpdir_prefix):
    modules_tmpdir.mkdir('site_egg').join('__init__.py').write(
        'import flask\n\napp = flask.Flask(__name__)'
    )
    install_egg('site_egg')
    try:
        import site_egg
        assert site_egg.app.instance_path == \
            str(modules_tmpdir.join('var/').join('site_egg-instance'))
    finally:
        if 'site_egg' in sys.modules:
            del sys.modules['site_egg']
@pytest.mark.skipif(not PY2, reason='This only works under Python 2.')
def test_meta_path_loader_without_is_package():
    class Loader(object):
        def find_module(self, name):
            return self
    sys.meta_path.append(Loader())
    try:
        with pytest.raises(AttributeError):
            flask.Flask(__name__)
    finally:
        sys.meta_path.pop()
# -*- coding: utf-8 -*-
    tests.conftest
    ~~~~~~~~~~~~~~
    :copyright: (c) 2014 by the Flask Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
import pkgutil
import pytest
import sys
import textwrap
@pytest.fixture(params=(True, False))
def limit_loader(request, monkeypatch):
    This provides for tests where a system has custom loaders, e.g. Google App
    Engine's HardenedModulesHook, which have neither the `get_filename` method
    nor the `archive` attribute.
    This fixture will run the testcase twice, once with and once without the
    limitation/mock.
    if not request.param:
        return
    class LimitedLoader(object):
        def __init__(self, loader):
            self.loader = loader
        def __getattr__(self, name):
            if name in ('archive', 'get_filename'):
                msg = 'Mocking a loader which does not have `%s.`' % name
                raise AttributeError(msg)
            return getattr(self.loader, name)
    old_get_loader = pkgutil.get_loader
    def get_loader(*args, **kwargs):
        return LimitedLoader(old_get_loader(*args, **kwargs))
    monkeypatch.setattr(pkgutil, 'get_loader', get_loader)
@pytest.fixture
def apps_tmpdir(tmpdir, monkeypatch):
    rv = tmpdir.mkdir('test_apps')
    monkeypatch.syspath_prepend(str(rv))
    return rv
@pytest.fixture
def apps_tmpdir_prefix(apps_tmpdir, monkeypatch):
    monkeypatch.setattr(sys, 'prefix', str(apps_tmpdir))
    return apps_tmpdir
@pytest.fixture
def site_packages(apps_tmpdir, monkeypatch):
    rv = apps_tmpdir \
        .mkdir('lib')\
        .mkdir('python{x[0]}.{x[1]}'.format(x=sys.version_info))\
        .mkdir('site-packages')
    monkeypatch.syspath_prepend(str(rv))
    return rv
@pytest.fixture
def install_egg(apps_tmpdir, monkeypatch):
    sys.path'''
    def inner(name, base=apps_tmpdir):
        if not isinstance(name, str):
            raise ValueError(name)
        base.join(name).ensure_dir()
        base.join(name).join('__init__.py').ensure()
        egg_setup = base.join('setup.py')
        egg_setup.write(textwrap.dedent("""
        from setuptools import setup
        setup(name='{0}',
              version='1.0',
              packages=['site_egg'],
              zip_safe=True)
        import subprocess
        subprocess.check_call(
            [sys.executable, 'setup.py', 'bdist_egg'],
            cwd=str(apps_tmpdir)
        )
        egg_path, = apps_tmpdir.join('dist/').listdir()
        monkeypatch.syspath_prepend(str(egg_path))
        return egg_path
    return inner
@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner
# -*- coding: utf-8 -*-
    Blueprint Example Tests
    ~~~~~~~~~~~~~~
    Tests the Blueprint example app
import pytest
import blueprintexample
@pytest.fixture
def client():
    return blueprintexample.app.test_client()
def test_urls(client):
    r = client.get('/')
    assert r.status_code == 200
    r = client.get('/hello')
    assert r.status_code == 200
    r = client.get('/world')
    assert r.status_code == 200
    # second blueprint instance
    r = client.get('/pages/hello')
    assert r.status_code == 200
    r = client.get('/pages/world')
    assert r.status_code == 200
# -*- coding: utf-8 -*-
    Flaskr Tests
    ~~~~~~~~~~~~
    Tests the Flaskr application.
    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import pytest
import os
import flaskr
import tempfile
@pytest.fixture
def client(request):
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()
    with flaskr.app.app_context():
        flaskr.init_db()
    def teardown():
        os.close(db_fd)
        os.unlink(flaskr.app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client
def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)
def logout(client):
    return client.get('/logout', follow_redirects=True)
def test_empty_db(client):
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
def test_login_logout(client):
    rv = login(client, flaskr.app.config['USERNAME'],
               flaskr.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, flaskr.app.config['USERNAME'] + 'x',
               flaskr.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, flaskr.app.config['USERNAME'],
               flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data
def test_messages(client):
    login(client, flaskr.app.config['USERNAME'],
          flaskr.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
# -*- coding: utf-8 -*-
    MiniTwit Tests
    ~~~~~~~~~~~~~~
    Tests the MiniTwit application.
    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import os
import minitwit
import tempfile
import pytest
@pytest.fixture
def client(request):
    db_fd, minitwit.app.config['DATABASE'] = tempfile.mkstemp()
    client = minitwit.app.test_client()
    with minitwit.app.app_context():
        minitwit.init_db()
    def teardown():
        os.close(db_fd)
        os.unlink(minitwit.app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client
def register(client, username, password, password2=None, email=None):
    if password2 is None:
        password2 = password
    if email is None:
        email = username + '@example.com'
    return client.post('/register', data={
        'username':     username,
        'password':     password,
        'password2':    password2,
        'email':        email,
    }, follow_redirects=True)
def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)
def register_and_login(client, username, password):
    register(client, username, password)
    return login(client, username, password)
def logout(client):
    return client.get('/logout', follow_redirects=True)
def add_message(client, text):
    rv = client.post('/add_message', data={'text': text},
                     follow_redirects=True)
    if text:
        assert b'Your message was recorded' in rv.data
    return rv
def test_register(client):
    rv = register(client, 'user1', 'default')
    assert b'You were successfully registered ' \
           b'and can login now' in rv.data
    rv = register(client, 'user1', 'default')
    assert b'The username is already taken' in rv.data
    rv = register(client, '', 'default')
    assert b'You have to enter a username' in rv.data
    rv = register(client, 'meh', '')
    assert b'You have to enter a password' in rv.data
    rv = register(client, 'meh', 'x', 'y')
    assert b'The two passwords do not match' in rv.data
    rv = register(client, 'meh', 'foo', email='broken')
    assert b'You have to enter a valid email address' in rv.data
def test_login_logout(client):
    rv = register_and_login(client, 'user1', 'default')
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, 'user1', 'wrongpassword')
    assert b'Invalid password' in rv.data
    rv = login(client, 'user2', 'wrongpassword')
    assert b'Invalid username' in rv.data
def test_message_recording(client):
    register_and_login(client, 'foo', 'default')
    add_message(client, 'test message 1')
    add_message(client, '<test message 2>')
    rv = client.get('/')
    assert b'test message 1' in rv.data
    assert b'&lt;test message 2&gt;' in rv.data
def test_timelines(client):
    register_and_login(client, 'foo', 'default')
    add_message(client, 'the message by foo')
    logout(client)
    register_and_login(client, 'bar', 'default')
    add_message(client, 'the message by bar')
    rv = client.get('/public')
    assert b'the message by foo' in rv.data
    assert b'the message by bar' in rv.data
    # bar's timeline should just show bar's message
    rv = client.get('/')
    assert b'the message by foo' not in rv.data
    assert b'the message by bar' in rv.data
    # now let's follow foo
    rv = client.get('/foo/follow', follow_redirects=True)
    assert b'You are now following &#34;foo&#34;' in rv.data
    # we should now see foo's message
    rv = client.get('/')
    assert b'the message by foo' in rv.data
    assert b'the message by bar' in rv.data
    # but on the user's page we only want the user's message
    rv = client.get('/bar')
    assert b'the message by foo' not in rv.data
    assert b'the message by bar' in rv.data
    rv = client.get('/foo')
    assert b'the message by foo' in rv.data
    assert b'the message by bar' not in rv.data
    # now unfollow and check if that worked
    rv = client.get('/foo/unfollow', follow_redirects=True)
    assert b'You are no longer following &#34;foo&#34;' in rv.data
    rv = client.get('/')
    assert b'the message by foo' not in rv.data
    assert b'the message by bar' in rv.data