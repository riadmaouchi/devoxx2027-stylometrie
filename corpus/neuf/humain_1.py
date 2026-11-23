# Contributeur de github.com/pallets/flask (BSD-3-Clause), anonymise.
# CODE NEUF : uniquement les lignes ajoutees lors de la CREATION de fichiers
# (git log --diff-filter=A). Ecrit d'un coup, jamais refactore.
# Commits > 300 lignes et posterieurs a juin 2021 exclus.
# -*- coding: utf-8 -*-
    flask.run
    ~~~~~~~~~
    A simple command line application to run flask apps.
    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import os
import sys
from threading import Lock
from contextlib import contextmanager
import click
from ._compat import iteritems
class NoAppException(click.UsageError):
def find_best_app(module):
    application in the module or raises an exception.
    from . import Flask
    # Search for the most common names first.
    for attr_name in 'app', 'application':
        app = getattr(module, attr_name, None)
        if app is not None and isinstance(app, Flask):
            return app
    # Otherwise find the only object that is a Flask instance.
    matches = [v for k, v in iteritems(module.__dict__)
               if isinstance(v, Flask)]
    if matches:
        if len(matches) > 1:
            raise NoAppException('More than one possible Flask application '
                                 'found in module "%s", none of which are called '
                                 '"app".  Be explicit!' % module.__name__)
        return matches[0]
    raise NoAppException('Failed to find application in module "%s".  Are '
                         'you sure it contains a Flask application?  Maybe '
                         'you wrapped it in a WSGI middleware or you are '
                         'using a factory function.' % module.__name__)
def prepare_exec_for_file(filename):
    module = []
    # Chop off file extensions or package markers
    if filename.endswith('.py'):
        filename = filename[:-3]
    elif os.path.split(filename)[1] == '__init__.py':
        filename = os.path.dirname(filename)
    filename = os.path.realpath(filename)
    dirpath = filename
    while 1:
        dirpath, extra = os.path.split(dirpath)
        module.append(extra)
        if not os.path.isfile(os.path.join(dirpath, '__init__.py')):
            break
    sys.path.insert(0, dirpath)
    return '.'.join(module[::-1])
def locate_app(app_id, debug=None):
    if ':' in app_id:
        module, app_obj = app_id.split(':', 1)
    else:
        module = app_id
        app_obj = None
    __import__(module)
    mod = sys.modules[module]
    if app_obj is None:
        app = find_best_app(mod)
    else:
        app = getattr(mod, app_obj, None)
        if app is None:
            raise RuntimeError('Failed to find application in module "%s"'
                               % module)
    if debug is not None:
        app.debug = debug
    return app
class DispatchingApp(object):
    is imported by name on first request.  This is safer than importing
    the application upfront because it means that we can forward all
    errors for import problems into the browser as error.
    def __init__(self, app_id, debug=None, use_eager_loading=False):
        self.app_id = app_id
        self.app = None
        self.debug = debug
        self._lock = Lock()
        if use_eager_loading:
            self._load_unlocked()
    def _load_unlocked(self):
        self.app = rv = locate_app(self.app_id, self.debug)
        return rv
    def __call__(self, environ, start_response):
        if self.app is not None:
            return self.app(environ, start_response)
        with self._lock:
            if self.app is not None:
                rv = self.app
            else:
                rv = self._load_unlocked()
            return rv(environ, start_response)
class ScriptInfo(object):
    necessary to interface with as it's used internally in the dispatching
    to click.
    def __init__(self):
        self.app_import_path = None
        self.debug = None
        self._loaded_app = None
    def get_app_import_path(self):
        not yet set.
        if self.app_import_path is not None:
            return self.app_import_path
        raise NoAppException('Could not locate application. '
                             'You did not provide FLASK_APP or the '
                             '--app parameter.')
    def load_app(self):
        if self._loaded_app is not None:
            return self._loaded_app
        rv = locate_app(self.get_app_import_path(), self.debug)
        self._loaded_app = rv
        return rv
    @contextmanager
    def conditional_context(self, with_context=True):
        given parameter but always works as context manager.
        if with_context:
            with self.load_app().app_context() as ctx:
                yield ctx
        else:
            yield None
pass_script_info = click.make_pass_decorator(ScriptInfo)
def without_appcontext(f):
    created.  This only works for commands directly registered to
    the toplevel system.  This really is only useful for very
    special commands like the runserver one.
    f.__flask_without_appcontext__ = True
    return f
class FlaskClickGroup(click.Group):
    loading more commands from the configured Flask app.
    def __init__(self, help=None):
        def set_app_id(ctx, value):
            if value is not None:
                if os.path.isfile(value) or os.sep in value or \
                   os.altsep is not None and os.altsep in value:
                    value = prepare_exec_for_file(value)
            ctx.obj.app_import_path = value
        def set_debug(ctx, value):
            ctx.obj.debug = value
        click.Group.__init__(self, help=help, params=[
            click.Option(['-a', '--app'],
                         help='The application to run',
                         callback=set_app_id, is_eager=True),
            click.Option(['--debug/--no-debug'],
                         help='Enable or disable debug mode.',
                         default=None, callback=set_debug)
        ])
    def get_command(self, ctx, name):
        info = ctx.find_object(ScriptInfo)
        # Find the command in the application first, if we can find it.
        # If the app is not available, we just ignore this silently.
        try:
            rv = info.load_app().cli.get_command(ctx, name)
            if rv is not None:
                return rv
        except NoAppException:
            pass
        return click.Group.get_command(self, ctx, name)
    def list_commands(self, ctx):
        # The commands available is the list of both the application (if
        # available) plus the builtin commands.
        rv = set(click.Group.list_commands(self, ctx))
        info = ctx.find_object(ScriptInfo)
        try:
            rv.update(info.load_app().cli.list_commands(ctx))
        except NoAppException:
            pass
        return sorted(rv)
    def invoke_subcommand(self, ctx, cmd, cmd_name, args):
        with_context = cmd.callback is None or \
           not getattr(cmd.callback, '__flask_without_appcontext__', False)
        with ctx.find_object(ScriptInfo).conditional_context(with_context):
            return click.Group.invoke_subcommand(
                self, ctx, cmd, cmd_name, args)
cli = FlaskClickGroup(help='''\
This shell command acts as general utility script for Flask applications.
It loads the application configured (either through the FLASK_APP environment
variable or the --app parameter) and then provides commands either provided
by the application or Flask itself.
The most useful commands are the "run" and "shell" command.
Example usage:
  flask --app=hello --debug run
@cli.command('run', short_help='Runs a development server.')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=5000,
              help='The port to bind to.')
@click.option('--reload/--no-reload', default=None,
              help='Enable or disable the reloader.  By default the reloader '
              'is active is debug is enabled.')
@click.option('--debugger/--no-debugger', default=None,
              help='Enable or disable the debugger.  By default the debugger '
              'is active if debug is enabled.')
@click.option('--eager-loading/--lazy-loader', default=None,
              help='Enable or disable eager loading.  By default eager '
              'loading is enabled if the reloader is disabled.')
@click.option('--with-threads/--without-threads', default=False,
              help='Enable or disable multithreading.')
@without_appcontext
@pass_script_info
def run_command(info, host, port, reload, debugger, eager_loading,
                with_threads):
    from werkzeug.serving import run_simple
    app_id = info.get_app_import_path()
    if reload is None:
        reload = info.debug
    if debugger is None:
        debugger = info.debug
    if eager_loading is None:
        eager_loading = not reload
    # Extra startup messages.  This depends a but on Werkzeug internals to
    # not double execute when the reloader kicks in.
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        print(' * Serving Flask app "%s"' % app_id)
        if info.debug is not None:
            print(' * Forcing debug %s' % (info.debug and 'on' or 'off'))
    app = DispatchingApp(app_id, info.debug, eager_loading)
    run_simple(host, port, app, use_reloader=reload,
               use_debugger=debugger, threaded=with_threads)
@cli.command('shell', short_help='Runs a shell in the app context.')
def shell_command():
    Flask application.  The application will populate the default
    namespace of this shell according to it's configuration.
    This is useful for executing small snippets of management code
    without having to manually configuring the application.
    import code
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    banner = 'Python %s on %s\nApp: %s%s\nInstance: %s' % (
        sys.version,
        sys.platform,
        app.import_name,
        app.debug and ' [debug]' or '',
        app.instance_path,
    )
    code.interact(banner=banner, local=app.make_shell_context())
def make_default_cli(app):
    there are no default commands registered because all builtin commands
    are registered on the actual cmd object here.
    return click.Group()
def main(as_module=False):
    this_module = __package__ + '.cli'
    args = sys.argv[1:]
    if as_module:
        if sys.version_info >= (2, 7):
            name = 'python -m ' + this_module.rsplit('.', 1)[0]
        else:
            name = 'python -m ' + this_module
        # This module is always executed as "python -m flask.run" and as such
        # we need to ensure that we restore the actual command line so that
        # the reloader can properly operate.
        sys.argv = ['-m', this_module] + sys.argv[1:]
    else:
        name = 'flask'
    cli.main(args=args, prog_name=name, obj=ScriptInfo(),
             auto_envvar_prefix='FLASK')
if __name__ == '__main__':
    main(as_module=True)
# -*- coding: utf-8 -*-
    flask.__main__
    ~~~~~~~~~~~~~~
    Alias for flask.run for the command line.
    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
if __name__ == '__main__':
    from run import main
    main(as_module=True)
import os
import sys
from threading import Lock
from optparse import OptionParser
from werkzeug.serving import run_simple
from ._compat import iteritems
def find_best_app(module):
    in the module or raises a RuntimeError.
    from flask import Flask
    # The app name wins, even if it's not a flask object.
    app = getattr(module, 'app', None)
    if app is not None and callable(app):
        return app
    # Otherwise find the first object named Flask
    matches = []
    for key, value in iteritems(module.__dict__):
        if isinstance(value, Flask):
            matches.append(value)
    if matches:
        if len(matches) > 1:
            raise RuntimeError('More than one possible Flask application '
                               'found in module "%s", none of which are called '
                               '"app".  Be explicit!' % module)
        return matches[0]
    raise RuntimeError('Failed to find application in module "%s".  Are '
                       'you sure it contains a Flask application?  Maybe '
                       'you wrapped it in a WSGI middleware or you are '
                       'using a factory function.' % module)
def prepare_exec_for_file(filename):
    module = []
    # Chop off file extensions or package markers
    if filename.endswith('.py'):
        filename = filename[:-3]
    elif os.path.split(filename)[1] == '__init__.py':
        filename = os.path.dirname(filename)
    filename = os.path.realpath(filename)
    dirpath = filename
    while 1:
        dirpath, extra = os.path.split(dirpath)
        module.append(extra)
        if not os.path.isfile(os.path.join(dirpath, '__init__.py')):
            break
    sys.path.insert(0, dirpath)
    return '.'.join(module[::-1])
def locate_app(app_id, debug=None):
    if ':' in app_id:
        module, app_obj = app_id.split(':', 1)
    else:
        module = app_id
        app_obj = None
    __import__(module)
    mod = sys.modules[module]
    if app_obj is None:
        app = find_best_app(mod)
    else:
        app = getattr(mod, app_obj, None)
        if app is None:
            raise RuntimeError('Failed to find application in module "%s"'
                               % module)
    if debug is not None:
        app.debug = debug
    return app
class DispatchingApp(object):
    is imported by name on first request.  This is safer than importing
    the application upfront because it means that we can forward all
    errors for import problems into the browser as error.
    def __init__(self, app_id, debug=None, use_eager_loading=False):
        self.app_id = app_id
        self.app = None
        self.debug = debug
        self._lock = Lock()
        if use_eager_loading:
            self._load_unlocked()
    def _load_unlocked(self):
        self.app = rv = locate_app(self.app_id, self.debug)
        return rv
    def __call__(self, environ, start_response):
        if self.app is not None:
            return self.app(environ, start_response)
        with self._lock:
            if self.app is not None:
                rv = self.app
            else:
                rv = self._load_unlocked()
            return rv(environ, start_response)
def run_application(app_id, host='127.0.0.1', port=5000, debug=None,
                    use_reloader=False, use_debugger=False,
                    use_eager_loading=None, magic_app_id=True):
    is known by it's import name.  By default the app ID can also be a
    full file name in which case Flask attempts to reconstruct the import
    name from it and do the right thing.
    :param app_id: the import name of the application module.  If a colon
                   is provided, everything afterwards is the application
                   object name.  In case the magic app id is enabled this
                   can also be a filename.
    :param host: the host to bind to.
    :param port: the port to bind to.
    :param debug: if set to something other than None then the application's
                  debug flag will be set to this.
    :param use_reloader: enables or disables the reloader.
    :param use_debugger: enables or disables the builtin debugger.
    :param use_eager_loading: enables or disables eager loading.  This is
                              normally conditional to the reloader.
    :param magic_app_id: if this is enabled then the app id can also be a
                         filename instead of an import module and Flask
                         will attempt to reconstruct the import name.
    if magic_app_id:
        if os.path.isfile(app_id) or os.sep in app_id or \
           os.altsep is not None and os.altsep in app_id:
            app_id = prepare_exec_for_file(app_id)
    if use_eager_loading is None:
        use_eager_loading = not use_reloader
    # Extra startup messages.  This depends a but on Werkzeug internals to
    # not double execute when the reloader kicks in.
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        print ' * Serving Flask app "%s"' % app_id
        if debug is not None:
            print ' * Forcing debug %s' % (debug and 'on' or 'off')
    app = DispatchingApp(app_id, debug, use_eager_loading)
    run_simple(host, port, app, use_reloader=use_reloader,
               use_debugger=use_debugger)
def main(as_module=False):
    this_module = __package__ + '.run'
    if as_module:
        name = 'python -m ' + this_module
    else:
        name = 'flask-run'
    parser = OptionParser(usage='%prog [options] module', prog=name)
    parser.add_option('--debug', action='store_true',
                      dest='debug', help='Flip debug flag on.  If enabled '
                      'this also affects debugger and reloader defaults.')
    parser.add_option('--no-debug', action='store_false',
                      dest='debug', help='Flip debug flag off.')
    parser.add_option('--host', default='127.0.0.1',
                      help='The host to bind on. (defaults to 127.0.0.1)')
    parser.add_option('--port', default=5000,
                      help='The port to bind on. (defaults to 5000)')
    parser.add_option('--with-reloader', action='store_true',
                      dest='with_reloader',
                      help='Enable the reloader.')
    parser.add_option('--without-reloader', action='store_false',
                      dest='with_reloader',
                      help='Disable the reloader.')
    parser.add_option('--with-debugger', action='store_true',
                      dest='with_debugger',
                      help='Enable the debugger.')
    parser.add_option('--without-debugger', action='store_false',
                      dest='with_debugger',
                      help='Disable the debugger.')
    parser.add_option('--with-eager-loading', action='store_true',
                      dest='with_eager_loading',
                      help='Force enable the eager-loading.  This makes the '
                      'application load immediately but makes development '
                      'flows harder.  It\'s not recommended to enable eager '
                      'loading when the reloader is enabled as it can lead '
                      'to unexpected crashes.')
    parser.add_option('--without-eager-loading', action='store_false',
                      dest='with_eager_loading',
                      help='Disable the eager-loading.')
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('Expected exactly one argument which is the import '
                     'name of the application.')
    if opts.with_debugger is None:
        opts.with_debugger = opts.debug
    if opts.with_reloader is None:
        opts.with_reloader = opts.debug
    # This module is always executed as "python -m flask.run" and as such
    # we need to ensure that we restore the actual command line so that
    # the reloader can properly operate.
    sys.argv = ['-m', this_module] + sys.argv[1:]
    run_application(args[0], opts.host, opts.port, debug=opts.debug,
                    use_reloader=opts.with_reloader,
                    use_debugger=opts.with_debugger,
                    use_eager_loading=opts.with_eager_loading)
if __name__ == '__main__':
    main(as_module=True)
from flask import Flask, render_template, session, request, json, abort, g
import requests
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='my development key',
    PERSONA_JS='https://login.persona.org/include.js',
    PERSONA_VERIFIER='https://verifier.login.persona.org/verify',
)
app.config.from_envvar('PERSONA_SETTINGS', silent=True)
@app.before_request
def get_current_user():
    g.user = None
    email = session.get('email')
    if email is not None:
        g.user = email
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/_auth/login', methods=['GET', 'POST'])
def login_handler():
    verification securely from the server side.  If all is okay
    the email address is remembered on the server.
    resp = requests.post(app.config['PERSONA_VERIFIER'], data={
        'assertion': request.form['assertion'],
        'audience': request.host_url,
    }, verify=True)
    if resp.ok:
        verification_data = json.loads(resp.content)
        if verification_data['status'] == 'okay':
            session['email'] = verification_data['email']
            return 'OK'
    abort(400)
@app.route('/_auth/logout', methods=['POST'])
def logout_handler():
    out again.
    session.clear()
    return 'OK'
if __name__ == '__main__':
    app.run()
# -*- coding: utf-8 -*-
    flask.testsuite.reqctx
    ~~~~~~~~~~~~~~~~~~~~~~
    Tests the request context.
    :copyright: (c) 2012 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from __future__ import with_statement
import flask
import unittest
try:
    from greenlet import greenlet
except ImportError:
    greenlet = None
from flask.testsuite import FlaskTestCase
class RequestContextTestCase(FlaskTestCase):
    def test_teardown_on_pop(self):
        buffer = []
        app = flask.Flask(__name__)
        @app.teardown_request
        def end_of_request(exception):
            buffer.append(exception)
        ctx = app.test_request_context()
        ctx.push()
        self.assert_equal(buffer, [])
        ctx.pop()
        self.assert_equal(buffer, [None])
    def test_proper_test_request_context(self):
        app = flask.Flask(__name__)
        app.config.update(
            SERVER_NAME='localhost.localdomain:5000'
        )
        @app.route('/')
        def index():
            return None
        @app.route('/', subdomain='foo')
        def sub():
            return None
        with app.test_request_context('/'):
            self.assert_equal(flask.url_for('index', _external=True), 'http://localhost.localdomain:5000/')
        with app.test_request_context('/'):
            self.assert_equal(flask.url_for('sub', _external=True), 'http://foo.localhost.localdomain:5000/')
        try:
            with app.test_request_context('/', environ_overrides={'HTTP_HOST': 'localhost'}):
                pass
        except Exception, e:
            self.assert_(isinstance(e, ValueError))
            self.assert_equal(str(e), "the server name provided " +
                    "('localhost.localdomain:5000') does not match the " + \
                    "server name from the WSGI environment ('localhost')")
        try:
            app.config.update(SERVER_NAME='localhost')
            with app.test_request_context('/', environ_overrides={'SERVER_NAME': 'localhost'}):
                pass
        except ValueError, e:
            raise ValueError(
                "No ValueError exception should have been raised \"%s\"" % e
            )
        try:
            app.config.update(SERVER_NAME='localhost:80')
            with app.test_request_context('/', environ_overrides={'SERVER_NAME': 'localhost:80'}):
                pass
        except ValueError, e:
            raise ValueError(
                "No ValueError exception should have been raised \"%s\"" % e
            )
    def test_context_binding(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return 'Hello %s!' % flask.request.args['name']
        @app.route('/meh')
        def meh():
            return flask.request.url
        with app.test_request_context('/?name=World'):
            self.assert_equal(index(), 'Hello World!')
        with app.test_request_context('/meh'):
            self.assert_equal(meh(), 'http://localhost/meh')
        self.assert_(flask._request_ctx_stack.top is None)
    def test_context_test(self):
        app = flask.Flask(__name__)
        self.assert_(not flask.request)
        self.assert_(not flask.has_request_context())
        ctx = app.test_request_context()
        ctx.push()
        try:
            self.assert_(flask.request)
            self.assert_(flask.has_request_context())
        finally:
            ctx.pop()
    def test_manual_context_binding(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return 'Hello %s!' % flask.request.args['name']
        ctx = app.test_request_context('/?name=World')
        ctx.push()
        self.assert_equal(index(), 'Hello World!')
        ctx.pop()
        try:
            index()
        except RuntimeError:
            pass
        else:
            self.assert_(0, 'expected runtime error')
    def test_greenlet_context_copying(self):
        app = flask.Flask(__name__)
        greenlets = []
        @app.route('/')
        def index():
            reqctx = flask._request_ctx_stack.top.copy()
            def g():
                self.assert_(not flask.request)
                self.assert_(not flask.current_app)
                with reqctx:
                    self.assert_(flask.request)
                    self.assert_equal(flask.current_app, app)
                    self.assert_equal(flask.request.path, '/')
                    self.assert_equal(flask.request.args['foo'], 'bar')
                self.assert_(not flask.request)
                return 42
            greenlets.append(greenlet(g))
            return 'Hello World!'
        rv = app.test_client().get('/?foo=bar')
        self.assert_equal(rv.data, 'Hello World!')
        result = greenlets[0].run()
        self.assert_equal(result, 42)
    def test_greenlet_context_copying_api(self):
        app = flask.Flask(__name__)
        greenlets = []
        @app.route('/')
        def index():
            reqctx = flask._request_ctx_stack.top.copy()
            @flask.copy_current_request_context
            def g():
                self.assert_(flask.request)
                self.assert_equal(flask.current_app, app)
                self.assert_equal(flask.request.path, '/')
                self.assert_equal(flask.request.args['foo'], 'bar')
                return 42
            greenlets.append(greenlet(g))
            return 'Hello World!'
        rv = app.test_client().get('/?foo=bar')
        self.assert_equal(rv.data, 'Hello World!')
        result = greenlets[0].run()
        self.assert_equal(result, 42)
    # Disable test if we don't have greenlets available
    if greenlet is None:
        test_greenlet_context_copying = None
        test_greenlet_context_copying_api = None
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RequestContextTestCase))
    return suite
# -*- coding: utf-8 -*-
    flask.jsonimpl
    ~~~~~~~~~~~~~~
    Implementation helpers for the JSON support in Flask.
    :copyright: (c) 2012 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from datetime import datetime
from .globals import current_app, request
from werkzeug.http import http_date
# Use the same json implementation as itsdangerous on which we
# depend anyways.
from itsdangerous import simplejson as _json
# figure out if simplejson escapes slashes.  This behavior was changed
# from one version to another without reason.
_slash_escape = '\\/' not in _json.dumps('/')
__all__ = ['dump', 'dumps', 'load', 'loads', 'htmlsafe_dump',
           'htmlsafe_dumps', 'JSONDecoder', 'JSONEncoder',
           'jsonify']
class JSONEncoder(_json.JSONEncoder):
    encoder by also supporting ``datetime`` objects as well as ``Markup``
    objects which are serialized as RFC 822 datetime strings (same as the HTTP
    date format).  In order to support more data types override the
    :meth:`default` method.
    def default(self, o):
        serializable object for ``o``, or calls the base implementation (to
        raise a ``TypeError``).
        For example, to support arbitrary iterators, you could implement
        default like this::
            def default(self, o):
                try:
                    iterable = iter(o)
                except TypeError:
                    pass
                else:
                    return list(iterable)
                return JSONEncoder.default(self, o)
        if isinstance(o, datetime):
            return http_date(o)
        if hasattr(o, '__html__'):
            return unicode(o.__html__())
        return _json.JSONEncoder.default(self, o)
class JSONDecoder(_json.JSONDecoder):
    the default simplejson encoder.  Consult the :mod:`json` documentation
    for more information.  This decoder is not only used for the load
    functions of this module but also :attr:`~flask.Request`.
def dumps(obj, **kwargs):
    configured encoder (:attr:`~flask.Flask.json_encoder`).
    kwargs.setdefault('cls', current_app.json_encoder)
    return _json.dumps(obj, **kwargs)
def dump(obj, fp, **kwargs):
    kwargs.setdefault('cls', current_app.json_encoder)
    return _json.dump(obj, fp, **kwargs)
def loads(s, **kwargs):
    configured decoder (:attr:`~flask.Flask.json_decoder`).
    kwargs.setdefault('cls', current_app.json_decoder)
    return _json.loads(s, **kwargs)
def load(fp, **kwargs):
    kwargs.setdefault('cls', current_app.json_decoder)
    return _json.load(fp, **kwargs)
def htmlsafe_dumps(obj, **kwargs):
    tags.  It accepts the same arguments and returns a JSON string.  Note that
    this is available in templates through the ``|tojson`` filter but it will
    have to be wrapped in ``|safe`` unless **true** XHTML is being used.
    rv = dumps(obj, **kwargs)
    if _slash_escape:
        rv = rv.replace('/', '\\/')
    return rv.replace('<!', '<\\u0021')
def htmlsafe_dump(obj, fp, **kwargs):
    fp.write(htmlsafe_dumps(obj, **kwargs))
def jsonify(*args, **kwargs):
    the given arguments with an `application/json` mimetype.  The arguments
    to this function are the same as to the :class:`dict` constructor.
    Example usage::
        @app.route('/_get_current_user')
        def get_current_user():
            return jsonify(username=g.user.username,
                           email=g.user.email,
                           id=g.user.id)
    This will send a JSON response like this to the browser::
        {
            "username": "admin",
            "email": "admin@localhost",
            "id": 42
        }
    This requires Python 2.6 or an installed version of simplejson.  For
    security reasons only objects are supported toplevel.  For more
    information about this, have a look at :ref:`json-security`.
    .. versionadded:: 0.2
    return current_app.response_class(dumps(dict(*args, **kwargs),
        indent=None if request.is_xhr else 2),
        mimetype='application/json')
# -*- coding: utf-8 -*-
    flask.testsuite.appctx
    ~~~~~~~~~~~~~~~~~~~~~~
    Tests the application context.
    :copyright: (c) 2012 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from __future__ import with_statement
import flask
import unittest
from flask.testsuite import FlaskTestCase
class AppContextTestCase(FlaskTestCase):
    def test_basic_support(self):
        app = flask.Flask(__name__)
        app.config['SERVER_NAME'] = 'localhost'
        app.config['PREFERRED_URL_SCHEME'] = 'https'
        @app.route('/')
        def index():
            pass
        with app.app_context():
            rv = flask.url_for('index')
            self.assert_equal(rv, 'https://localhost/')
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AppContextTestCase))
    return suite
# -*- coding: utf-8 -*-
    flask.testsuite.regression
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Tests regressions.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from __future__ import with_statement
import gc
import sys
import flask
import threading
import unittest
from werkzeug.test import run_wsgi_app, create_environ
from flask.testsuite import FlaskTestCase
_gc_lock = threading.Lock()
class _NoLeakAsserter(object):
    def __init__(self, testcase):
        self.testcase = testcase
    def __enter__(self):
        gc.disable()
        _gc_lock.acquire()
        loc = flask._request_ctx_stack._local
        # Force Python to track this dictionary at all times.
        # This is necessary since Python only starts tracking
        # dicts if they contain mutable objects.  It's a horrible,
        # horrible hack but makes this kinda testable.
        loc.__storage__['FOOO'] = [1, 2, 3]
        gc.collect()
        self.old_objects = len(gc.get_objects())
    def __exit__(self, exc_type, exc_value, tb):
        if not hasattr(sys, 'getrefcount'):
            gc.collect()
        new_objects = len(gc.get_objects())
        if new_objects > self.old_objects:
            self.testcase.fail('Example code leaked')
        _gc_lock.release()
        gc.enable()
class MemoryTestCase(FlaskTestCase):
    def assert_no_leak(self):
        return _NoLeakAsserter(self)
    def test_memory_consumption(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return flask.render_template('simple_template.html', whiskey=42)
        def fire():
            with app.test_client() as c:
                rv = c.get('/')
                self.assert_equal(rv.status_code, 200)
                self.assert_equal(rv.data, '<h1>42</h1>')
        # Trigger caches
        fire()
        with self.assert_no_leak():
            for x in xrange(10):
                fire()
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MemoryTestCase))
    return suite
# -*- coding: utf-8 -*-
    flask.exthook
    ~~~~~~~~~~~~~
    Redirect imports for extensions.  This module basically makes it possible
    for us to transition from flaskext.foo to flask_foo without having to
    force all extensions to upgrade at the same time.
    When a user does ``from flask.ext.foo import bar`` it will attempt to
    import ``from flask_foo import bar`` first and when that fails it will
    try to import ``from flaskext.foo import bar``.
    We're switching from namespace packages because it was just too painful for
    everybody involved.
    This is used by `flask.ext`.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import sys
import os
class ExtensionImporter(object):
    This makes it possible to transition from the old flaskext.name to the
    newer flask_name without people having a hard time.
    def __init__(self, module_choices, wrapper_module):
        self.module_choices = module_choices
        self.wrapper_module = wrapper_module
        self.prefix = wrapper_module + '.'
        self.prefix_cutoff = wrapper_module.count('.') + 1
    def __eq__(self, other):
        return self.__class__.__module__ == other.__class__.__module__ and \
               self.__class__.__name__ == other.__class__.__name__ and \
               self.wrapper_module == other.wrapper_module and \
               self.module_choices == other.module_choices
    def __ne__(self, other):
        return not self.__eq__(other)
    def install(self):
        sys.meta_path[:] = [x for x in sys.meta_path if self != x] + [self]
    def find_module(self, fullname, path=None):
        if fullname.startswith(self.prefix):
            return self
    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        modname = fullname.split('.', self.prefix_cutoff)[self.prefix_cutoff]
        for path in self.module_choices:
            realname = path % modname
            try:
                __import__(realname)
            except ImportError:
                exc_type, exc_value, tb = sys.exc_info()
                # since we only establish the entry in sys.modules at the
                # very this seems to be redundant, but if recursive imports
                # happen we will call into the move import a second time.
                # On the second invocation we still don't have an entry for
                # fullname in sys.modules, but we will end up with the same
                # fake module name and that import will succeed since this
                # one already has a temporary entry in the modules dict.
                # Since this one "succeeded" temporarily that second
                # invocation now will have created a fullname entry in
                # sys.modules which we have to kill.
                sys.modules.pop(fullname, None)
                # If it's an important traceback we reraise it, otherwise
                # we swallow it and try the next choice.  The skipped frame
                # is the one from __import__ above which we don't care about
                if self.is_important_traceback(realname, tb):
                    raise exc_type, exc_value, tb.tb_next
                continue
            module = sys.modules[fullname] = sys.modules[realname]
            if '.' not in modname:
                setattr(sys.modules[self.wrapper_module], modname, module)
            return module
        raise ImportError('No module named %s' % fullname)
    def is_important_traceback(self, important_module, tb):
        originated in the given important module.  If that is the case then we
        were able to import the module itself but apparently something went
        wrong when the module was imported.  (Eg: import of an import failed).
        while tb is not None:
            if self.is_important_frame(important_module, tb):
                return True
            tb = tb.tb_next
        return False
    def is_important_frame(self, important_module, tb):
        g = tb.tb_frame.f_globals
        if '__name__' not in g:
            return False
        module_name = g['__name__']
        # Python 2.7 Behavior.  Modules are cleaned up late so the
        # name shows up properly here.  Success!
        if module_name == important_module:
            return True
        # Some python verisons will will clean up modules so early that the
        # module name at that point is no longer set.  Try guessing from
        # the filename then.
        filename = os.path.abspath(tb.tb_frame.f_code.co_filename)
        test_string = os.path.sep + important_module.replace('.', os.path.sep)
        return test_string + '.py' in filename or \
               test_string + os.path.sep + '__init__.py' in filename
import flask.ext.broken.b
import missing_module
# -*- coding: utf-8 -*-
    flaskext_compat
    ~~~~~~~~~~~~~~~
    Implements the ``flask.ext`` virtual package for versions of Flask
    older than 0.7.  This module is a noop if Flask 0.8 was detected.
    Usage::
        import flaskext_compat
        from flask.ext import foo
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
class _ExtensionImporter(object):
    This makes it possible to transition from the old flaskext.name to the
    newer flask_name without people having a hard time.
    _module_choices = ['flask_%s', 'flaskext.%s']
    def __init__(self):
        from sys import meta_path
        self.prefix = __name__ + '.'
        self.prefix_cutoff = __name__.count('.') + 1
        # since people might reload the flask.ext module (by accident or
        # intentionally) we have to make sure to not add more than one
        # import hook.  We can't check class types here either since a new
        # class will be created on reload.  As a result of that we check
        # the name of the class and remove stale instances.
        def _name(x):
            cls = type(x)
            return cls.__module__ + '.' + cls.__name__
        this = _name(self)
        meta_path[:] = [x for x in meta_path if _name(x) != this] + [self]
    def find_module(self, fullname, path=None):
        if fullname.startswith(self.prefix):
            return self
    def load_module(self, fullname):
        from sys import modules
        if fullname in modules:
            return modules[fullname]
        modname = fullname.split('.', self.prefix_cutoff)[self.prefix_cutoff]
        for path in self._module_choices:
            realname = path % modname
            try:
                __import__(realname)
            except ImportError:
                continue
            module = modules[fullname] = modules[realname]
            if '.' not in modname:
                setattr(modules[__name__], modname, module)
            return module
        raise ImportError(fullname)
import sys
import flask
try:
    __import__('flask.ext')
except ImportError:
    sys.modules['flask.ext'] = flask.ext = sys.modules[__name__]
    __name__ = __package__ = 'flask.ext'
    __path__ = []
    _ExtensionImporter()
del _ExtensionImporter, sys, flask
ext_id = 'oldext_package'
def test_function():
    return 42
ext_id = 'oldext_simple'
# -*- coding: utf-8 -*-
    flask.testsuite.ext
    ~~~~~~~~~~~~~~~~~~~
    Tests the extension import thing.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import sys
import unittest
from flask.testsuite import FlaskTestCase
class ExtImportHookTestCase(FlaskTestCase):
    def setup(self):
        for entry, value in sys.modules.items():
            if entry.startswith('flask.ext.') and value is not None:
                sys.modules.pop(entry, None)
        from flask import ext
        reload(ext)
        # reloading must not add more hooks
        import_hooks = 0
        for item in sys.meta_path:
            cls = type(item)
            if cls.__module__ == 'flask.ext' and \
               cls.__name__ == '_ExtensionImporter':
                import_hooks += 1
        self.assert_equal(import_hooks, 1)
    def test_flaskext_simple_import_normal(self):
        from flask.ext.newext_simple import ext_id
        self.assert_equal(ext_id, 'newext_simple')
    def test_flaskext_simple_import_module(self):
        from flask.ext import newext_simple
        self.assert_equal(newext_simple.ext_id, 'newext_simple')
        self.assert_equal(newext_simple.__name__, 'flask_newext_simple')
    def test_flaskext_package_import_normal(self):
        from flask.ext.newext_package import ext_id
        self.assert_equal(ext_id, 'newext_package')
    def test_flaskext_package_import_module(self):
        from flask.ext import newext_package
        self.assert_equal(newext_package.ext_id, 'newext_package')
        self.assert_equal(newext_package.__name__, 'flask_newext_package')
    def test_flaskext_package_import_submodule(self):
        from flask.ext.newext_package import submodule
        self.assert_equal(submodule.__name__, 'flask_newext_package.submodule')
        self.assert_equal(submodule.test_function(), 42)
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ExtImportHookTestCase))
    return suite
ext_id = 'newext_package'
def test_function():
    return 42
ext_id = 'newext_simple'
# -*- coding: utf-8 -*-
    flask.ext
    ~~~~~~~~~
    Redirect imports for extensions.  This module basically makes it possible
    for us to transition from flaskext.foo to flask_foo without having to
    force all extensions to upgrade at the same time.
    When a user does ``from flask.ext.foo import bar`` it will attempt to
    imprt ``from flask_foo import bar`` first and when that fails it will
    try to import ``from flaskext.foo import bar``.
    We're switching from namespace packages because it was just too painful for
    everybody involved.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import sys
class _ExtensionImporter(object):
    locations.  This makes it possible to transition from the old
    flaskext.name to the newer flask_name without people having a
    hard time.
    _module_choices = ['flask_%s', 'flaskext.%s']
    _modules = sys.modules
    def find_module(self, fullname, path=None):
        if fullname.rsplit('.', 1)[0] == __name__:
            return self
    def load_module(self, fullname):
        if fullname in self._modules:
            return self._modules[fullname]
        packname, modname = fullname.rsplit('.', 1)
        for path in self._module_choices:
            realname = path % modname
            try:
                __import__(realname)
            except ImportError:
                continue
            module = self._modules[fullname] = self._modules[realname]
            setattr(self._modules[__name__], modname, module)
            module.__loader__ = self
            return module
        raise ImportError(fullname)
sys.meta_path.append(_ExtensionImporter())
del sys, _ExtensionImporter
# -*- coding: utf-8 -*-
    flask.testsuite.subclassing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Test that certain behavior of flask can be customized by
    subclasses.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import flask
import unittest
from StringIO import StringIO
from logging import StreamHandler
from flask.testsuite import FlaskTestCase
class FlaskSubclassingTestCase(FlaskTestCase):
    def test_supressed_exception_logging(self):
        class SupressedFlask(flask.Flask):
            def log_exception(self, exc_info):
                pass
        out = StringIO()
        app = SupressedFlask(__name__)
        app.logger_name = 'flask_tests/test_supressed_exception_logging'
        app.logger.addHandler(StreamHandler(out))
        @app.route('/')
        def index():
            1/0
        rv = app.test_client().get('/')
        self.assert_equal(rv.status_code, 500)
        self.assert_('Internal Server Error' in rv.data)
        err = out.getvalue()
        self.assert_equal(err, '')
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlaskSubclassingTestCase))
    return suite
import sys
import unittest
from unittest.loader import TestLoader
from flask.testsuite import suite
common_prefix = suite.__module__ + '.'
def find_all_tests():
    suites = [suite()]
    while suites:
        s = suites.pop()
        try:
            suites.extend(s)
        except TypeError:
            yield s
def find_all_tests_with_name():
    for testcase in find_all_tests():
        yield testcase, '%s.%s.%s' % (
            testcase.__class__.__module__,
            testcase.__class__.__name__,
            testcase._testMethodName
        )
class BetterLoader(TestLoader):
    def loadTestsFromName(self, name, module=None):
        if name == 'suite':
            return suite()
        for testcase, testname in find_all_tests_with_name():
            if testname == name:
                return testcase
            if testname.startswith(common_prefix):
                if testname[len(common_prefix):] == name:
                    return testcase
        all_results = []
        for testcase, testname in find_all_tests_with_name():
            if testname.endswith('.' + name):
                all_results.append((testcase, testname))
        if len(all_results) == 1:
            return all_results[0][0]
        elif not len(all_results):
            error = 'could not find testcase "%s"' % name
        else:
            error = 'Too many matches: for "%s"\n%s' % \
                (name, '\n'.join('  - ' + n for c, n in all_results))
        print >> sys.stderr, 'Error: %s' % error
        sys.exit(1)
unittest.main(testLoader=BetterLoader(), defaultTest='suite')
import re
import inspect
_internal_mark_re = re.compile(r'^\s*:internal:\s*$(?m)')
def skip_member(app, what, name, obj, skip, options):
    docstring = inspect.getdoc(obj)
    if skip:
        return True
    return _internal_mark_re.search(docstring or '') is not None
def setup(app):
    app.connect('autodoc-skip-member', skip_member)
# -*- coding: utf-8 -*-
    flask.debughelpers
    ~~~~~~~~~~~~~~~~~~
    Various helpers to make the development experience better.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
class DebugFilesKeyError(KeyError, AssertionError):
    provide a better error message than just a generic KeyError/BadRequest.
    def __init__(self, request, key):
        form_matches = request.form.getlist(key)
        buf = ['You tried to access the file "%s" in the request.files '
               'dictionary but it does not exist.  The mimetype for the request '
               'is "%s" instead of "multipart/form-data" which means that no '
               'files were transmitted.  To fix this error you most likely have '
               'to provide enctype="multipart/form-data" in your form.' %
               (key, request.mimetype)]
        if form_matches:
            buf.append('\n\nThe browser instead most likely submitted the '
                       'filenames in the form.  This was submitted: %s' %
                       ', '.join('"%s"' % x for x in form_matches))
        self.msg = ''.join(buf)
    def __str__(self):
        return self.msg
def make_enctype_error_multidict(request):
    request is detected that does not use multipart form data but the files
    object is accessed.
    oldcls = request.files.__class__
    class newcls(oldcls):
        def __getitem__(self, key):
            try:
                return oldcls.__getitem__(self, key)
            except KeyError, e:
                if key not in request.form:
                    raise
                raise DebugFilesKeyError(request, key)
    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
# -*- coding: utf-8 -*-
    flask.sessions
    ~~~~~~~~~~~~~~
    Implements cookie based sessions based on Werkzeug's secure cookie
    system.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from datetime import datetime
from werkzeug.contrib.securecookie import SecureCookie
class SessionMixin(object):
    by Flask extensions and users for the session.
    def _get_permanent(self):
        return self.get('_permanent', False)
    def _set_permanent(self, value):
        self['_permanent'] = bool(value)
    permanent = property(_get_permanent, _set_permanent)
    del _get_permanent, _set_permanent
    new = False
    modified = True
class SecureCookieSession(SecureCookie, SessionMixin):
    and non-permanent sessions.
class NullSession(SecureCookieSession):
    available.  Will still allow read-only access to the empty session
    but fail on setting.
    def _fail(self, *args, **kwargs):
        raise RuntimeError('the session is unavailable because no secret '
                           'key was set.  Set the secret_key on the '
                           'application to something unique and secret.')
    __setitem__ = __delitem__ = clear = pop = popitem = \
        update = setdefault = _fail
    del _fail
class SessionInterface(object):
    default session interface which uses werkzeug's securecookie
    implementation.  The only methods you have to implement are
    :meth:`open_session` and :meth:`save_session`, the others have
    useful defaults which you don't need to change.
    The session object returned by the :meth:`open_session` method has to
    provide a dictionary like interface plus the properties and methods
    from the :class:`SessionMixin`.  We recommend just subclassing a dict
    and adding that mixin::
        class Session(dict, SessionMixin):
            pass
    If :meth:`open_session` returns `None` Flask will call into
    :meth:`make_null_session` to create a session that acts as replacement
    if the session support cannot work because some requirement is not
    fulfilled.  The default :class:`NullSession` class that is created
    will complain that the secret key was not set.
    To replace the session interface on an application all you have to do
    is to assign :attr:`flask.Flask.session_interface`::
        app = Flask(__name__)
        app.session_interface = MySessionInterface()
    .. versionadded:: 0.7
    #: :meth:`make_null_session` will look here for the class that should
    #: be created when a null session is requested.  Likewise the
    #: :meth:`is_null_session` method will perform a typecheck against
    #: this type.
    null_session_class = NullSession
    def make_null_session(self, app):
        real session support could not be loaded due to a configuration
        error.  This mainly aids the user experience because the job of the
        null session is to still support lookup without complaining but
        modifications are answered with a helpful error message of what
        failed.
        This creates an instance of :attr:`null_session_class` by default.
        return self.null_session_class()
    def is_null_session(self, obj):
        not asked to be saved.
        This checks if the object is an instance of :attr:`null_session_class`
        by default.
        return isinstance(obj, self.null_session_class)
    def get_cookie_domain(self, app):
        be used for the session cookie if session cookies are used.
        if app.config['SERVER_NAME'] is not None:
            # chop of the port which is usually not supported by browsers
            return '.' + app.config['SERVER_NAME'].rsplit(':', 1)[0]
    def get_expiration_time(self, app, session):
        or `None` if the session is linked to the browser session.  The
        default implementation returns now + the permanent session
        lifetime configured on the application.
        if session.permanent:
            return datetime.utcnow() + app.permanent_session_lifetime
    def open_session(self, app, request):
        in case the loading failed because of a configuration error or an
        instance of a session object which implements a dictionary like
        interface + the methods and attributes on :class:`SessionMixin`.
        raise NotImplementedError()
    def save_session(self, app, session, response):
        at the end of the request.  This is still called during a request
        context so if you absolutely need access to the request you can do
        that.
        raise NotImplementedError()
class SecureCookieSessionInterface(SessionInterface):
    as client side session backend.
    session_class = SecureCookieSession
    def open_session(self, app, request):
        key = app.secret_key
        if key is not None:
            return self.session_class.load_cookie(request,
                                                  app.session_cookie_name,
                                                  secret_key=key)
    def save_session(self, app, session, response):
        expires = self.get_expiration_time(app, session)
        domain = self.get_cookie_domain(app)
        if session.modified and not session:
            response.delete_cookie(app.session_cookie_name,
                                   domain=domain)
        else:
            session.save_cookie(response, app.session_cookie_name,
                                expires=expires, httponly=True, domain=domain)
# -*- coding: utf-8 -*-
    flask.views
    ~~~~~~~~~~~
    This module provides class based views inspired by the ones in Django.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from .globals import request
http_method_funcs = frozenset(['get', 'post', 'head', 'options',
                               'delete', 'put', 'trace'])
class View(object):
    :meth:`dispatch_request` which is called with the view arguments from
    the URL routing system.  If :attr:`methods` is provided the methods
    do not have to be passed to the :meth:`~flask.Flask.add_url_rule`
    method explicitly::
        class MyView(View):
            methods = ['GET']
            def dispatch_request(self, name):
                return 'Hello %s!' % name
        app.add_url_rule('/hello/<name>', view_func=MyView.as_view('myview'))
    methods = None
    def dispatch_request(self):
        raise NotImplementedError()
    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        used with the routing system.  What it does internally is generating
        a function on the fly that will instanciate the :class:`View`
        on each request and call the :meth:`dispatch_request` method on it.
        The arguments passed to :meth:`as_view` are forwarded to the
        constructor of the class.
        def view(*args, **kwargs):
            self = cls(*class_args, **class_kwargs)
            return self.dispatch_request(*args, **kwargs)
        view.__name__ = name
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.methods = cls.methods
        return view
class MethodViewType(type):
    def __new__(cls, name, bases, d):
        rv = type.__new__(cls, name, bases, d)
        if rv.methods is None:
            methods = []
            for key, value in d.iteritems():
                if key in http_method_funcs:
                    methods.append(key.upper())
            # if we have no method at all in there we don't want to
            # add a method list.  (This is for instance the case for
            # the baseclass or another subclass of a base method view
            # that does not introduce new methods).
            if methods:
                rv.methods = methods
        return rv
class MethodView(View):
    particular methods.  For instance if you implement a method called
    :meth:`get` it means you will response to ``'GET'`` requests and
    the :meth:`dispatch_request` implementation will automatically
    forward your request to that.  Also :attr:`options` is set for you
    automatically::
        class CounterAPI(MethodView):
            def get(self):
                return session.get('counter', 0)
            def post(self):
                session['counter'] = session.get('counter', 0) + 1
                return 'OK'
        app.add_url_rule('/counter', view_func=CounterAPI.as_view('counter'))
    __metaclass__ = MethodViewType
    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        assert meth is not None, 'Not implemented method'
        return meth(*args, **kwargs)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
    make-release
    ~~~~~~~~~~~~
    Helper script that performs a release.  Does pretty much everything
    automatically for us.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import sys
import os
import re
from datetime import datetime, date
from subprocess import Popen, PIPE
def parse_changelog():
    with open('CHANGES') as f:
        lineiter = iter(f)
        for line in lineiter:
            match = re.search('^Version\s+(.*)', line.strip())
            if match is None:
                continue
            length = len(match.group(1))
            version = match.group(1).strip()
            if lineiter.next().count('-') != len(match.group(0)):
                continue
            while 1:
                change_info = lineiter.next().strip()
                if change_info:
                    break
            match = re.match(r'^released on (\w+\s+\d+\w+\s+\d+)'
                             r'(?:, codename (.*))?(?i)', change_info)
            if match is None:
                continue
            datestr, codename = match.groups()
            return version, parse_date(datestr), codename
def parse_date(string):
    string = string.replace('th ', ' ').replace('nd ', ' ') \
                   .replace('rd ', ' ').replace('st ', ' ')
    return datetime.strptime(string, '%B %d %Y')
def set_filename_version(filename, version_number, pattern):
    changed = []
    def inject_version(match):
        before, old, after = match.groups()
        changed.append(True)
        return before + version_number + after
    with open(filename) as f:
        contents = re.sub(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern,
                          inject_version, f.read())
    if not changed:
        fail('Could not find %s in %s', pattern, filename)
    with open(filename, 'w') as f:
        f.write(contents)
def set_init_version(version):
    info('Setting __init__.py version to %s', version)
    set_filename_version('flask/__init__.py', version, '__version__')
def set_setup_version(version):
    info('Setting setup.py version to %s', version)
    set_filename_version('setup.py', version, 'version')
def build_and_upload():
    Popen([sys.executable, 'setup.py', 'sdist', 'release']).wait()
def fail(message, *args):
    print >> sys.stderr, 'Error:', message % args
    sys.exit(1)
def info(message, *args):
    print >> sys.stderr, message % args
def get_git_tags():
    return set(Popen(['git', 'tag'], stdout=PIPE).communicate()[0].splitlines())
def git_is_clean():
    return Popen(['git', 'diff', '--quiet']).wait() == 0
def make_git_commit(message, *args):
    message = message % args
    Popen(['git', 'commit', '-am', message]).wait()
def make_git_tag(tag):
    info('Tagging "%s"', tag)
    Popen(['git', 'tag', tag]).wait()
def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    rv = parse_changelog()
    if rv is None:
        fail('Could not parse changelog')
    version, release_date, codename = rv
    info('Releasing %s (codename %s, release date %s)',
         version, codename, release_date.strftime('%d/%m/%Y'))
    tags = get_git_tags()
    if version in tags:
        fail('Version "%s" is already tagged', version)
    if release_date.date() != date.today():
        fail('Release date is not today (%s != %s)')
    if not git_is_clean():
        fail('You have uncommitted changes in git')
    set_init_version(version)
    set_setup_version(version)
    make_git_commit('Bump version number to %s', version)
    make_git_tag(version)
    build_and_upload()
if __name__ == '__main__':
    main()
from flask import Flask
app = Flask(__name__)
from moduleapp.apps.admin import admin
from moduleapp.apps.frontend import frontend
app.register_blueprint(admin)
app.register_blueprint(frontend)
from flask import Blueprint, render_template
admin = Blueprint(__name__, url_prefix='/admin')
@admin.route('/')
def index():
    return render_template('admin/index.html')
@admin.route('/index2')
def index2():
    return render_template('./admin/index.html')
from flask import Blueprint, render_template
frontend = Blueprint(__name__)
@frontend.route('/')
def index():
    return render_template('frontend/index.html')
from flask import Flask, Module
mod = Module(__name__)
mod2 = Module(__name__, 'testmod2')
app = Flask(__name__)
app.register_module(mod)
app.register_module(mod2)
@app.after_request
def after_request(response):
    g.db.close()
    return response
@mod.route('/')
def index():
    return render_template('test/index.html')
@mod2.route('/')
def index():
    return render_template('testmod2/index.html')
@mod2.route('/')
def index():
    return render_template('something-else/index.html')
#!/usr/bin/env python
# -*- coding: utf-8 -*-
    flask-07-upgrade
    ~~~~~~~~~~~~~~~~
    This command line script scans a whole application tree and attempts to
    output an unified diff with all the changes that are necessary to easily
    upgrade the application to 0.7 and to not yield deprecation warnings.
    This will also attempt to find `after_request` functions that don't modify
    the response and appear to be better suited for `teardown_request`.
    :copyright: (c) Copyright 2011 by Armin Ronacher.
    :license: see LICENSE for more details.
import re
import os
import sys
import inspect
import difflib
import posixpath
from optparse import OptionParser
try:
    import ast
except ImportError:
    ast = None
_string_re_part = r"('([^'\\]*(?:\\.[^'\\]*)*)'" \
                  r'|"([^"\\]*(?:\\.[^"\\]*)*)")'
_url_for_re = re.compile(r'\b(url_for\()(%s)' % _string_re_part)
_after_request_re = re.compile(r'((?:@\S+\.(?:app_)?))(after_request)(\b\s*$)(?m)')
def error(message):
    print >> sys.stderr, 'error:', message
    sys.exit(1)
def make_diff(filename, old, new):
    for line in difflib.unified_diff(old.splitlines(), new.splitlines(),
                     posixpath.normpath(posixpath.join('a', filename)),
                     posixpath.normpath(posixpath.join('b', filename)),
                     lineterm=''):
        print line
def fix_url_for(contents):
    def handle_match(match):
        prefix = match.group(1)
        endpoint = ast.literal_eval(match.group(2))
        if endpoint.startswith('.'):
            endpoint = endpoint[1:]
        else:
            endpoint = '.' + endpoint
        return prefix + repr(endpoint)
    return _url_for_re.sub(handle_match, contents)
def looks_like_teardown_function(node):
    returns = [x for x in ast.walk(node) if isinstance(x, ast.Return)]
    if len(returns) != 1:
        return
    return_def = returns[0]
    resp_name = node.args.args[0]
    if not isinstance(return_def.value, ast.Name) or \
       return_def.value.id != resp_name.id:
        return
    for body_node in node.body:
        for child in ast.walk(body_node):
            if isinstance(child, ast.Name) and \
               child.id == resp_name.id:
                if child is not return_def.value:
                    return
    return resp_name.id
def fix_teardown_funcs(contents):
    def is_return_line(line):
        args = line.strip().split()
        return args and args[0] == 'return'
    def fix_single(match, lines, lineno):
        if not lines[lineno + 1].startswith('def'):
            return
        block_lines = inspect.getblock(lines[lineno + 1:])
        func_code = ''.join(block_lines)
        if func_code[0].isspace():
            node = ast.parse('if 1:\n' + func_code).body[0].body
        else:
            node = ast.parse(func_code).body[0]
        response_param_name = looks_like_teardown_function(node)
        if response_param_name is None:
            return
        before = lines[:lineno]
        decorator = [match.group(1) +
                     match.group(2).replace('after_', 'teardown_') +
                     match.group(3)]
        body = [line.replace(response_param_name, 'exception')
                for line in block_lines if
                not is_return_line(line)]
        after = lines[lineno + len(block_lines) + 1:]
        return before + decorator + body + after
    content_lines = contents.splitlines(True)
    while 1:
        found_one = False
        for idx, line in enumerate(content_lines):
            match = _after_request_re.match(line)
            if match is None:
                continue
            new_content_lines = fix_single(match, content_lines, idx)
            if new_content_lines is not None:
                content_lines = new_content_lines
                break
        else:
            break
    return ''.join(content_lines)
def upgrade_python_file(filename, contents, teardown):
    new_contents = fix_url_for(contents)
    if teardown:
        new_contents = fix_teardown_funcs(contents)
    make_diff(filename, contents, new_contents)
def upgrade_template_file(filename, contents):
    new_contents = fix_url_for(contents)
    make_diff(filename, contents, new_contents)
def scan_path(path=None, teardown=True):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            with open(filename) as f:
                contents = f.read()
            if filename.endswith('.py'):
                upgrade_python_file(filename, contents, teardown)
            elif '{% for' or '{% if' or '{{ url_for' in contents:
                upgrade_template_file(filename, contents)
def main():
    if ast is None:
        error('Python 2.6 or later is required to run the upgrade script.\n'
              'The runtime requirements for Flask 0.7 however are still '
              'Python 2.5.')
    parser = OptionParser()
    parser.add_option('-T', '--no-teardown-detection', dest='no_teardown',
                      action='store_true', help='Do not attempt to '
                      'detect teardown function rewrites.')
    options, args = parser.parse_args()
    if not args:
        args = ['.']
    for path in args:
        scan_path(path, teardown=not options.no_teardown)
if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
    flask.blueprints
    ~~~~~~~~~~~~~~~~
    Blueprints are the recommended way to implement larger or more
    pluggable applications in Flask 0.7 and later.
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import os
from .helpers import _PackageBoundObject, _endpoint_from_view_func
class BlueprintSetupState(object):
    application.
    def __init__(self, blueprint, app, options):
        self.app = app
        self.blueprint = blueprint
        self.options = options
        subdomain = self.options.get('subdomain')
        if subdomain is None:
            subdomain = self.blueprint.subdomain
        self.subdomain = subdomain
        url_prefix = self.options.get('url_prefix')
        if url_prefix is None:
            url_prefix = self.blueprint.url_prefix
        self.url_prefix = url_prefix
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if self.url_prefix:
            rule = self.url_prefix + rule
        options.setdefault('subdomain', self.subdomain)
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        self.app.add_url_rule(rule, '%s.%s' % (self.blueprint.name, endpoint),
                              view_func, **options)
class Blueprint(_PackageBoundObject):
    .. versionadded:: 0.7
    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, url_prefix=None,
                 subdomain=None):
        _PackageBoundObject.__init__(self, import_name)
        self.name = name
        self.url_prefix = url_prefix
        self.subdomain = subdomain
        self.static_folder = static_folder
        self.static_url_path = static_url_path
        self.deferred_functions = []
    def _record(self, func):
        self.deferred_functions.append(func)
    def make_setup_state(self, app, options):
        return BlueprintSetupState(self, app, options)
    def register(self, app, options):
        on the application.  This can be overridden to customize the register
        behavior.  Keyword arguments from
        :func:`~flask.Flask.register_blueprint` are directly forwarded to this
        method in the `options` dictionary.
        state = self.make_setup_state(app, options)
        if self.has_static_folder:
            state.add_url_rule(self.static_url_path + '/<path:filename>',
                               view_func=self.send_static_file,
                               endpoint='static')
        for deferred in self.deferred_functions:
            deferred(state)
    def route(self, rule, **options):
        :func:`url_for` function is prefixed with the name of the module.
        def decorator(f):
            self.add_url_rule(rule, f.__name__, f, **options)
            return f
        return decorator
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        the :func:`url_for` function is prefixed with the name of the module.
        def register_rule(state):
            state.add_url_rule(rule, endpoint, view_func, **options)
        self._record(register_rule)
    def endpoint(self, endpoint):
        prefix the endpoint with the module name, this has to be done
        explicitly by the user of this method.
        def decorator(f):
            def register_endpoint(state):
                state.app.view_functions[endpoint] = f
            self._record(register_endpoint)
            return f
        return decorator
    def before_request(self, f):
        is only executed before each request that is handled by a function of
        that module.
        self._record(lambda s: s.app.before_request_funcs
            .setdefault(self.name, []).append(f))
        return f
    def before_app_request(self, f):
        before each request, even if outside of a module.
        self._record(lambda s: s.app.before_request_funcs
            .setdefault(None, []).append(f))
        return f
    def after_request(self, f):
        is only executed after each request that is handled by a function of
        that module.
        self._record(lambda s: s.app.after_request_funcs
            .setdefault(self.name, []).append(f))
        return f
    def after_app_request(self, f):
        is executed after each request, even if outside of the module.
        self._record(lambda s: s.app.after_request_funcs
            .setdefault(None, []).append(f))
        return f
    def context_processor(self, f):
        function is only executed for requests handled by a module.
        self._record(lambda s: s.app.template_context_processors
            .setdefault(self.name, []).append(f))
        return f
    def app_context_processor(self, f):
        function is executed each request, even if outside of the module.
        self._record(lambda s: s.app.template_context_processors
            .setdefault(None, []).append(f))
        return f
    def app_errorhandler(self, code):
        handler is used for all requests, even if outside of the module.
        def decorator(f):
            self._record(lambda s: s.app.errorhandler(code)(f))
            return f
        return decorator
from flask import Module
mod = Module(__name__, 'foo', subdomain='foo')
# -*- coding: utf-8 -*-
    Flask Extension Tests
    ~~~~~~~~~~~~~~~~~~~~~
    Tests the Flask extensions.
    :copyright: (c) 2010 by Ali Afshar.
    :license: BSD, see LICENSE for more details.
from __future__ import with_statement
import tempfile, subprocess, urllib2, os
from flask import json
from setuptools.package_index import PackageIndex
from setuptools.archive_util import unpack_archive
flask_svc_url = 'http://flask.pocoo.org/extensions/'
tdir = tempfile.mkdtemp()
def run_tests(checkout_dir):
    cmd = ['tox']
    return subprocess.call(cmd, cwd=checkout_dir,
                           stdout=open(os.path.join(tdir, 'tox.log'), 'w'),
                           stderr=subprocess.STDOUT)
def get_test_command(checkout_dir):
    files = set(os.listdir(checkout_dir))
    if 'Makefile' in files:
        return 'make test'
    elif 'conftest.py' in files:
        return 'py.test'
    else:
        return 'nosetests'
def fetch_extensions_list():
    req = urllib2.Request(flask_svc_url, headers={'accept':'application/json'})
    d = urllib2.urlopen(req).read()
    data = json.loads(d)
    for ext in data['extensions']:
        yield ext
def checkout_extension(ext):
    name = ext['name']
    root = os.path.join(tdir, name)
    os.mkdir(root)
    checkout_path = PackageIndex().download(ext['name'], root)
    unpack_archive(checkout_path, root)
    path = None
    for fn in os.listdir(root):
        path = os.path.join(root, fn)
        if os.path.isdir(path):
            break
    return path
tox_template = """[tox]
envlist=py26
[testenv]
commands=
%s
downloadcache=
%s
def create_tox_ini(checkout_path):
    tox_path = os.path.join(checkout_path, 'tox.ini')
    if not os.path.exists(tox_path):
        with open(tox_path, 'w') as f:
            f.write(tox_template % (get_test_command(checkout_path), tdir))
# XXX command line
only_approved = True
def test_all_extensions(only_approved=only_approved):
    for ext in fetch_extensions_list():
        if ext['approved'] or not only_approved:
            checkout_path = checkout_extension(ext)
            create_tox_ini(checkout_path)
            ret = run_tests(checkout_path)
            yield ext['name'], ret
def main():
    for name, ret in test_all_extensions():
        print name, ret
if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
    flask.signals
    ~~~~~~~~~~~~~
    Implements signals based on blinker if available, otherwise
    falls silently back to a noop
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
signals_available = False
try:
    from blinker import Namespace
    signals_available = True
    _signals = Namespace()
except ImportError:
    class Namespace(object):
        def signal(self, name, doc=None):
            return _FakeSignal(name, doc)
    class _FakeSignal(object):
        interface that allows sending of signals but will fail with an
        error on anything else.  Instead of doing anything on send, it
        will just ignore the arguments and do nothing instead.
        def __init__(self, name, doc=None):
            self.name = name
            self.__doc__ = doc
        def _fail(self, *args, **kwargs):
            raise RuntimeError('signalling support is unavailable '
                               'because the blinker library is '
                               'not installed.')
        send = lambda *a, **kw: None
        connect = disconnect = has_receivers_for = receivers_for = \
            temporarily_connected_to = _fail
        del _fail
# the namespace for code signals.  If you are not flask code, do
# not put signals in here.  Create your own namespace instead.
_signals = Namespace()
# core signals.  For usage examples grep the sourcecode or consult
# the API documentation in docs/api.rst as well as docs/signals.rst
template_rendered = _signals.signal('template-rendered')
request_started = _signals.signal('request-started')
request_finished = _signals.signal('request-finished')
got_request_exception = _signals.signal('got-request-exception')
# -*- coding: utf-8 -*-
    flask.logging
    ~~~~~~~~~~~~~
    Implements the logging support for Flask.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from __future__ import absolute_import
from logging import getLogger, StreamHandler, Formatter, Logger,  DEBUG
def create_logger(app):
    similar to a regular Python logger but changes the effective logging
    level based on the application's debug flag.  Furthermore this
    function also removes all attached handlers in case there was a
    logger with the log name before.
    class DebugLogger(Logger):
        def getEffectiveLevel(x):
            return DEBUG if app.debug else Logger.getEffectiveLevel(x)
    class DebugHandler(StreamHandler):
        def emit(x, record):
            StreamHandler.emit(x, record) if app.debug else None
    handler = DebugHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(app.debug_log_format))
    logger = getLogger(app.logger_name)
    # just in case that was not a new logger, get rid of all the handlers
    # already attached to it.
    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(handler)
    return logger
# -*- coding: utf-8 -*-
    flask.testing
    ~~~~~~~~~~~~~
    Implements test support helpers.  This module is lazily imported
    and usually not used in production environments.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from werkzeug import Client
from flask import _request_ctx_stack
class FlaskClient(Client):
    preserve_context = context_preserved = False
    def open(self, *args, **kwargs):
        if self.context_preserved:
            _request_ctx_stack.pop()
            self.context_preserved = False
        kwargs.setdefault('environ_overrides', {}) \
            ['flask._preserve_context'] = self.preserve_context
        old = _request_ctx_stack.top
        try:
            return Client.open(self, *args, **kwargs)
        finally:
            self.context_preserved = _request_ctx_stack.top is not old
    def __enter__(self):
        self.preserve_context = True
        return self
    def __exit__(self, exc_type, exc_value, tb):
        self.preserve_context = False
        if self.context_preserved:
            _request_ctx_stack.pop()
from flask import Flask
app = Flask(__name__)
from moduleapp.apps.admin import admin
from moduleapp.apps.frontend import frontend
app.register_module(admin)
app.register_module(frontend)
from flask import Module, render_template
admin = Module(__name__, url_prefix='/admin')
@admin.route('/')
def index():
    return render_template('admin/index.html')
from flask import Module, render_template
frontend = Module(__name__)
@frontend.route('/')
def index():
    return render_template('frontend/index.html')
# -*- coding: utf-8 -*-
    flask.templating
    ~~~~~~~~~~~~~~~~
    Implements the bridge to Jinja2.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from jinja2 import BaseLoader, FileSystemLoader, TemplateNotFound
from flask.globals import _request_ctx_stack
class _DispatchingJinjaLoader(BaseLoader):
    the module folders.
    def __init__(self, app):
        self.app = app
    def get_source(self, environment, template):
        name = template
        loader = None
        try:
            module, name = template.split('/', 1)
            loader = self.app.modules[module].jinja_loader
        except (ValueError, KeyError):
            pass
        if loader is None:
            loader = self.app.jinja_loader
        try:
            return loader.get_source(environment, name)
        except TemplateNotFound:
            # re-raise the exception with the correct fileame here.
            # (the one that includes the prefix)
            raise TemplateNotFound(template)
    def list_templates(self):
        result = self.app.jinja_loader.list_templates()
        for name, module in self.app.modules.iteritems():
            if module.jinja_loader is not None:
                for template in module.jinja_loader.list_templates():
                    result.append('%s/%s' % (name, template))
        return result
def render_template(template_name, **context):
    context.
    :param template_name: the name of the template to be rendered
    :param context: the variables that should be available in the
                    context of the template.
    ctx = _request_ctx_stack.top
    ctx.app.update_template_context(context)
    return ctx.app.jinja_env.get_template(template_name).render(context)
def render_template_string(source, **context):
    with the given context.
    :param template_name: the sourcecode of the template to be
                          rendered
    :param context: the variables that should be available in the
                    context of the template.
    ctx = _request_ctx_stack.top
    ctx.app.update_template_context(context)
    return ctx.app.jinja_env.from_string(source).render(context)
# -*- coding: utf-8 -*-
    OpenID Example
    ~~~~~~~~~~~~~~
    This simple application shows how OpenID can be used in an application.
    Dependencies:
    -   python-openid
    -   SQLAlchemy
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from simpleopenid import SimpleOpenID
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# configuration
DATABASE_URI = 'sqlite:////tmp/openidexample.db'
OPENID_FS_PATH = '/tmp/openidexample-store'
SECRET_KEY = 'development key'
DEBUG = True
# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
# setup simpleopenid
oid = SimpleOpenID(OPENID_FS_PATH)
# setup sqlalchemy
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
def init_db():
    Base.metadata.create_all(bind=engine)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(200))
    openid = Column(String(200))
    def __init__(self, name, email, openid):
        self.name = name
        self.email = email
        self.openid = openid
@app.before_request
def before_request():
    g.user = None
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    to start the OpenID machinery.
    # if we are already logged in, go back to were we came from
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid)
    return render_template('login.html', next_url=oid.get_next_url())
@oid.after_login
def create_or_login(identity_url):
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    session['openid'] = identity_url
    user = User.query.filter_by(openid=identity_url).first()
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile', next=oid.get_next_url()))
@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    will redirect here so that the user can set up his profile.
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            db_session.add(User(name, email, session['openid']))
            db_session.commit()
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url())
@app.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    if g.user is None:
        abort(401)
    form = dict(name=g.user.name, email=g.user.email)
    if request.method == 'POST':
        if 'delete' in request.form:
            db_session.delete(g.user)
            db_session.commit()
            session['openid'] = None
            flash(u'Profile deleted')
            return redirect(url_for('index'))
        form['name'] = request.form['name']
        form['email'] = request.form['email']
        if not form['name']:
            flash(u'Error: you have to provide a name')
        elif '@' not in form['email']:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            g.user.name = form['name']
            g.user.email = form['email']
            db_session.commit()
            return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', form=form)
@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You were signed out')
    return redirect(oid.get_next_url())
if __name__ == '__main__':
    app.run()
# -*- coding: utf-8 -*-
    simpleopenid
    ~~~~~~~~~~~~
    Tiny wrapper around python-openid to make working with the basic
    API in a flask application easier.  Adapt this code for your own
    project if necessary.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from functools import wraps
from flask import request, session, flash, redirect
from werkzeug import url_quote
from openid.association import Association
from openid.store.interface import OpenIDStore
from openid.store.filestore import FileOpenIDStore
from openid.consumer.consumer import Consumer, SUCCESS, CANCEL
from openid.consumer import discover
from openid.store import nonce
# python-openid is a really stupid library in that regard, we have
# to disable logging by monkey patching
from openid import oidutil
oidutil.log = lambda *a, **kw: None
class SimpleOpenID(object):
    def __init__(self, store_path):
        self.store_path = store_path
        self.after_login_func = None
    def create_store(self):
        return FileOpenIDStore(self.store_path)
    def signal_error(self, msg):
        flash(u'Error: ' + msg)
    def get_next_url(self):
        return request.values.get('next') or \
               request.referrer or \
               request.url_root
    def get_current_url(self):
        return request.base_url + '?next=' + url_quote(self.get_next_url())
    def get_success_url(self):
        return self.get_current_url() + '&openid_complete=yes'
    def errorhandler(f):
        ``'Error: message'`` is flashed.
        self.signal_error = f
        return f
    def after_login(self, f):
        a different place and remember the user somewhere.  The session
        is not modified by SimpleOpenID.
        self.after_login_func = f
        return f
    def loginhandler(self, f):
        more OpenID required logic.
        self.login_endpoint = f.__name__
        @wraps(f)
        def decorated(*args, **kwargs):
            if request.args.get('openid_complete') != u'yes':
                return f(*args, **kwargs)
            consumer = Consumer(session, self.create_store())
            openid_response = consumer.complete(request.args.to_dict(),
                                                self.get_current_url())
            if openid_response.status == SUCCESS:
                return self.after_login_func(openid_response.identity_url)
            elif openid_response.status == CANCEL:
                self.signal_error(u'The request was cancelled')
                return redirect(self.get_current_url())
            self.signal_error(u'OpenID authentication error')
            return redirect(self.get_current_url())
        return decorated
    def try_login(self, identity_url):
        must be called from the login_handler.
        try:
            consumer = Consumer(session, self.create_store())
            auth_request = consumer.begin(identity_url)
        except discover.DiscoveryFailure:
            self.signal_error(u'The OpenID was invalid')
            return redirect(self.get_current_url())
        trust_root = request.host_url
        return redirect(auth_request.redirectURL(request.host_url,
                                                 self.get_success_url()))
# -*- coding: utf-8 -*-
    jQuery Example
    ~~~~~~~~~~~~~~
    A simple application that shows how Flask and jQuery get along.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run()
# -*- coding: utf-8 -*-
    Flaskr
    ~~~~~~
    A microblog example application written as Flask tutorial with
    Flask and sqlite3.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from __future__ import with_statement
import time
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug import secure_filename
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# create our little application :)
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG
def connect_db():
    return sqlite3.connect(DATABASE)
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
@app.request_init
def before_request():
    set `g.logged_in` to `True` if we are logged in.
    g.db = connect_db()
    g.logged_in = session.get('logged_in', False)
@app.request_shutdown
def after_request(response):
    g.db.close()
    return response
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)
@app.route('/add', methods=['POST'])
def add_entry():
    if not g.logged_in:
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != PASSWORD:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
if __name__ == '__main__':
    app.run()
# -*- coding: utf-8 -*-
    Flaskr Tests
    ~~~~~~~~~~~~
    Tests the Flaskr application.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import flaskr
import unittest
import tempfile
class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db = tempfile.NamedTemporaryFile()
        self.app = flaskr.app.test_client()
        flaskr.DATABASE = self.db.name
        flaskr.init_db()
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    # testing functions
    def test_login_logout(self):
        rv = self.login(flaskr.USERNAME, flaskr.PASSWORD)
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login(flaskr.USERNAME + 'x', flaskr.PASSWORD)
        assert 'Invalid username' in rv.data
        rv = self.login(flaskr.USERNAME, flaskr.PASSWORD + 'x')
        assert 'Invalid password' in rv.data
    def test_messages(self):
        # start with a blank state
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data
        self.login(flaskr.USERNAME, flaskr.PASSWORD)
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        self.login(flaskr.USERNAME, flaskr.PASSWORD)
        assert '&lt;Hello&gt' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
if __name__ == '__main__':
    unittest.main()
# -*- coding: utf-8 -*-
    Flask Tests
    ~~~~~~~~~~~
    Tests Flask itself.  The majority of Flask is already tested
    as part of Werkzeug.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from __future__ import with_statement
import flask
import unittest
import tempfile
class ContextTestCase(unittest.TestCase):
    def test_context_binding(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return 'Hello %s!' % flask.request.args['name']
        @app.route('/meh')
        def meh():
            return flask.request.url
        with app.test_request_context('/?name=World'):
            assert index() == 'Hello World!'
        with app.test_request_context('/meh'):
            assert meh() == 'http://localhost/meh'
class BasicFunctionality(unittest.TestCase):
    def test_request_dispatching(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return flask.request.method
        @app.route('/more', methods=['GET', 'POST'])
        def more():
            return flask.request.method
        c = app.test_client()
        assert c.get('/').data == 'GET'
        rv = c.post('/')
        assert rv.status_code == 405
        assert sorted(rv.allow) == ['GET', 'HEAD']
        rv = c.head('/')
        assert rv.status_code == 200
        assert not rv.data # head truncates
        assert c.post('/more').data == 'POST'
        assert c.get('/more').data == 'GET'
        rv = c.delete('/more')
        assert rv.status_code == 405
        assert sorted(rv.allow) == ['GET', 'HEAD', 'POST']
    def test_session(self):
        app = flask.Flask(__name__)
        app.secret_key = 'testkey'
        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'
        @app.route('/get')
        def get():
            return flask.session['value']
        c = app.test_client()
        assert c.post('/set', data={'value': '42'}).data == 'value set'
        assert c.get('/get').data == '42'
    def test_request_processing(self):
        app = flask.Flask(__name__)
        evts = []
        @app.request_init
        def before_request():
            evts.append('before')
        @app.request_shutdown
        def after_request(response):
            response.data += '|after'
            evts.append('after')
            return response
        @app.route('/')
        def index():
            assert 'before' in evts
            assert 'after' not in evts
            return 'request'
        assert 'after' not in evts
        rv = app.test_client().get('/').data
        assert 'after' in evts
        assert rv == 'request|after'
    def test_error_handling(self):
        app = flask.Flask(__name__)
        @app.errorhandler(404)
        def not_found(e):
            return 'not found', 404
        @app.errorhandler(500)
        def internal_server_error(e):
            return 'internal server error', 500
        @app.route('/')
        def index():
            flask.abort(404)
        @app.route('/error')
        def error():
            1/0
        c = app.test_client()
        rv = c.get('/')
        assert rv.status_code == 404
        assert rv.data == 'not found'
        rv = c.get('/error')
        assert rv.status_code == 500
        assert 'internal server error' in rv.data
    def test_response_creation(self):
        app = flask.Flask(__name__)
        @app.route('/unicode')
        def from_unicode():
            return u'Hällo Wörld'
        @app.route('/string')
        def from_string():
            return u'Hällo Wörld'.encode('utf-8')
        @app.route('/args')
        def from_tuple():
            return 'Meh', 400, {'X-Foo': 'Testing'}, 'text/plain'
        c = app.test_client()
        assert c.get('/unicode').data == u'Hällo Wörld'.encode('utf-8')
        assert c.get('/string').data == u'Hällo Wörld'.encode('utf-8')
        rv = c.get('/args')
        assert rv.data == 'Meh'
        assert rv.headers['X-Foo'] == 'Testing'
        assert rv.status_code == 400
        assert rv.mimetype == 'text/plain'
    def test_url_generation(self):
        app = flask.Flask(__name__)
        @app.route('/hello/<name>', methods=['POST'])
        def hello():
            pass
        with app.test_request_context():
            assert flask.url_for('hello', name='test x') == '/hello/test%20x'
class Templating(unittest.TestCase):
    def test_context_processing(self):
        app = flask.Flask(__name__)
        @app.context_processor
        def context_processor():
            return {'injected_value': 42}
        @app.route('/')
        def index():
            return flask.render_template('context_template.html', value=23)
        rv = app.test_client().get('/')
        assert rv.data == '<p>23|42'
    def test_escaping(self):
        text = '<p>Hello World!'
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return flask.render_template('escaping_template.html', text=text,
                                         html=flask.Markup(text))
        lines = app.test_client().get('/').data.splitlines()
        assert lines == [
            '&lt;p&gt;Hello World!',
            '<p>Hello World!',
            '<p>Hello World!',
            '<p>Hello World!',
            '&lt;p&gt;Hello World!',
            '<p>Hello World!'
        ]
if __name__ == '__main__':
    unittest.main()
# -*- coding: utf-8 -*-
    Flask Tests
    ~~~~~~~~~~~
    Tests Flask itself.  The majority of Flask is already tested
    as part of Werkzeug.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
from __future__ import with_statement
import flask
import unittest
import tempfile
class ContextTestCase(unittest.TestCase):
    def test_context_binding(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return 'Hello %s!' % flask.request.args['name']
        @app.route('/meh')
        def meh():
            return flask.request.url
        with app.test_request_context('/?name=World'):
            assert index() == 'Hello World!'
        with app.test_request_context('/meh'):
            assert meh() == 'http://localhost/meh'
    def test_request_dispatching(self):
        app = flask.Flask(__name__)
        @app.route('/')
        def index():
            return flask.request.method
        @app.route('/more', methods=['GET', 'POST'])
        def more():
            return flask.request.method
        c = app.test_client()
        assert c.get('/').data == 'GET'
        rv = c.post('/')
        assert rv.status_code == 405
        assert sorted(rv.allow) == ['GET', 'HEAD']
        rv = c.head('/')
        assert rv.status_code == 200
        assert not rv.data # head truncates
        assert c.post('/more').data == 'POST'
        assert c.get('/more').data == 'GET'
        rv = c.delete('/more')
        assert rv.status_code == 405
        assert sorted(rv.allow) == ['GET', 'HEAD', 'POST']
    def test_session(self):
        app = flask.Flask(__name__)
        app.secret_key = 'testkey'
        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'
        @app.route('/get')
        def get():
            return flask.session['value']
        c = app.test_client()
        assert c.post('/set', data={'value': '42'}).data == 'value set'
        assert c.get('/get').data == '42'
if __name__ == '__main__':
    unittest.main()
# -*- coding: utf-8 -*-
    MiniTwit Tests
    ~~~~~~~~~~~~~~
    Tests the MiniTwit application.
    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
import minitwit
import unittest
import tempfile
from contextlib import closing
class MiniTwitTestCase(unittest.TestCase):
    def setUp(self):
        self.db = tempfile.NamedTemporaryFile()
        self.app = minitwit.app.test_client()
        minitwit.DATABASE = self.db.name
        minitwit.init_db()
    # helper functions
    def register(self, username, password, password2=None, email=None):
        if password2 is None:
            password2 = password
        if email is None:
            email = username + '@example.com'
        return self.app.post('/register', data={
            'username':     username,
            'password':     password,
            'password2':    password2,
            'email':        email,
        }, follow_redirects=True)
    def login(self, username, password):
        return self.app.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)
    def register_and_login(self, username, password):
        self.register(username, password)
        return self.login(username, password)
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    def add_message(self, text):
        rv = self.app.post('/add_message', data={'text': text},
                                    follow_redirects=True)
        if text:
            assert 'Your message was recorded' in rv.data
        return rv
    # testing functions
    def test_register(self):
        rv = self.register('user1', 'default')
        assert 'You were successfully registered ' \
               'and can login now' in rv.data
        rv = self.register('user1', 'default')
        assert 'The username is already taken' in rv.data
        rv = self.register('', 'default')
        assert 'You have to enter a username' in rv.data
        rv = self.register('meh', '')
        assert 'You have to enter a password' in rv.data
        rv = self.register('meh', 'x', 'y')
        assert 'The two passwords do not match' in rv.data
        rv = self.register('meh', 'foo', email='broken')
        assert 'You have to enter a valid email address' in rv.data
    def test_login_logout(self):
        rv = self.register_and_login('user1', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('user1', 'wrongpassword')
        assert 'Invalid password' in rv.data
        rv = self.login('user2', 'wrongpassword')
        assert 'Invalid username' in rv.data
    def test_message_recording(self):
        self.register_and_login('foo', 'default')
        self.add_message('test message 1')
        self.add_message('<test message 2>')
        rv = self.app.get('/')
        assert 'test message 1' in rv.data
        assert '&lt;test message 2&gt;' in rv.data
    def test_timelines(self):
        self.register_and_login('foo', 'default')
        self.add_message('the message by foo')
        self.logout()
        self.register_and_login('bar', 'default')
        self.add_message('the message by bar')
        rv = self.app.get('/public')
        assert 'the message by foo' in rv.data
        assert 'the message by bar' in rv.data
        # bar's timeline should just show bar's message
        rv = self.app.get('/')
        assert 'the message by foo' not in rv.data
        assert 'the message by bar' in rv.data
        # now let's follow foo
        rv = self.app.get('/foo/follow', follow_redirects=True)
        assert 'You are now following &#34;foo&#34;' in rv.data
        # we should now see foo's message
        rv = self.app.get('/')
        assert 'the message by foo' in rv.data
        assert 'the message by bar' in rv.data
        # but on the user's page we only want the user's message
        rv = self.app.get('/bar')
        assert 'the message by foo' not in rv.data
        assert 'the message by bar' in rv.data
        rv = self.app.get('/foo')
        assert 'the message by foo' in rv.data
        assert 'the message by bar' not in rv.data
        # now unfollow and check if that worked
        rv = self.app.get('/foo/unfollow', follow_redirects=True)
        assert 'You are no longer following &#34;foo&#34;' in rv.data
        rv = self.app.get('/')
        assert 'the message by foo' not in rv.data
        assert 'the message by bar' in rv.data
if __name__ == '__main__':
    unittest.main()
# flasky extensions.  flasky pygments style based on tango style
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal
class FlaskyStyle(Style):
    background_color = "#f8f8f8"
    default_style = ""
    styles = {
        # No corresponding class for the following:
        #Text:                     "", # class:  ''
        Whitespace:                "underline #f8f8f8",      # class: 'w'
        Error:                     "#a40000 border:#ef2929", # class: 'err'
        Other:                     "#000000",                # class 'x'
        Comment:                   "italic #8f5902", # class: 'c'
        Comment.Multiline:         "italic #8f5902", # class: 'cm'
        Comment.Preproc:           "italic #8f5902", # class: 'cp'
        Comment.Single:            "italic #8f5902", # class: 'c1'
        Comment.Special:           "italic #8f5902", # class: 'cs'
        Keyword:                   "bold #004461",   # class: 'k'
        Keyword.Constant:          "bold #004461",   # class: 'kc'
        Keyword.Declaration:       "bold #004461",   # class: 'kd'
        Keyword.Namespace:         "bold #004461",   # class: 'kn'
        Keyword.Pseudo:            "bold #004461",   # class: 'kp'
        Keyword.Reserved:          "bold #004461",   # class: 'kr'
        Keyword.Type:              "bold #004461",   # class: 'kt'
        Operator:                  "#582800",   # class: 'o'
        Operator.Word:             "bold #004461",   # class: 'ow' - like keywords
        Punctuation:               "bold #000000",   # class: 'p'
        # because special names such as Name.Class, Name.Function, etc.
        # are not recognized as such later in the parsing, we choose them
        # to look the same as ordinary variables.
        Name:                      "#000000",        # class: 'n'
        Name.Attribute:            "#c4a000",        # class: 'na' - to be revised
        Name.Builtin:              "#004461",        # class: 'nb'
        Name.Builtin.Pseudo:       "#3465a4",        # class: 'bp'
        Name.Class:                "#000000",        # class: 'nc' - to be revised
        Name.Constant:             "#000000",        # class: 'no' - to be revised
        Name.Decorator:            "#999",           # class: 'nd' - to be revised
        Name.Entity:               "#ce5c00",        # class: 'ni'
        Name.Exception:            "bold #cc0000",   # class: 'ne'
        Name.Function:             "#000000",        # class: 'nf'
        Name.Property:             "#000000",        # class: 'py'
        Name.Label:                "#f57900",        # class: 'nl'
        Name.Namespace:            "#000000",        # class: 'nn' - to be revised
        Name.Other:                "#000000",        # class: 'nx'
        Name.Tag:                  "bold #004461",   # class: 'nt' - like a keyword
        Name.Variable:             "#000000",        # class: 'nv' - to be revised
        Name.Variable.Class:       "#000000",        # class: 'vc' - to be revised
        Name.Variable.Global:      "#000000",        # class: 'vg' - to be revised
        Name.Variable.Instance:    "#000000",        # class: 'vi' - to be revised
        # since the tango light blue does not show up well in text, we choose
        # a pure blue instead.
        Number:                    "bold #0000cf",   # class: 'm'
        Number.Float:              "bold #0000cf",   # class: 'mf'
        Number.Hex:                "bold #0000cf",   # class: 'mh'
        Number.Integer:            "bold #0000cf",   # class: 'mi'
        Number.Integer.Long:       "bold #0000cf",   # class: 'il'
        Number.Oct:                "bold #0000cf",   # class: 'mo'
        Literal:                   "#000000",        # class: 'l'
        Literal.Date:              "#000000",        # class: 'ld'
        String:                    "#4e9a06",        # class: 's'
        String.Backtick:           "#4e9a06",        # class: 'sb'
        String.Char:               "#4e9a06",        # class: 'sc'
        String.Doc:                "italic #8f5902", # class: 'sd' - like a comment
        String.Double:             "#4e9a06",        # class: 's2'
        String.Escape:             "#4e9a06",        # class: 'se'
        String.Heredoc:            "#4e9a06",        # class: 'sh'
        String.Interpol:           "#4e9a06",        # class: 'si'
        String.Other:              "#4e9a06",        # class: 'sx'
        String.Regex:              "#4e9a06",        # class: 'sr'
        String.Single:             "#4e9a06",        # class: 's1'
        String.Symbol:             "#4e9a06",        # class: 'ss'
        Generic:                   "#000000",        # class: 'g'
        Generic.Deleted:           "#a40000",        # class: 'gd'
        Generic.Emph:              "italic #000000", # class: 'ge'
        Generic.Error:             "#ef2929",        # class: 'gr'
        Generic.Heading:           "bold #000080",   # class: 'gh'
        Generic.Inserted:          "#00A000",        # class: 'gi'
        Generic.Output:            "italic #000000", # class: 'go'
        Generic.Prompt:            "#8f5902",        # class: 'gp'
        Generic.Strong:            "bold #000000",   # class: 'gs'
        Generic.Subheading:        "bold #800080",   # class: 'gu'
        Generic.Traceback:         "bold #a40000",   # class: 'gt'
    }
# -*- coding: utf-8 -*-
#
# Flask documentation build configuration file, created by
# sphinx-quickstart on Tue Apr  6 15:24:58 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
import sys, os
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))
# -- General configuration -----------------------------------------------------
# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'
# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc']
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# The suffix of source filenames.
source_suffix = '.rst'
# The encoding of source files.
#source_encoding = 'utf-8-sig'
# The master toctree document.
master_doc = 'index'
# General information about the project.
project = u'Flask'
copyright = u'2010, Armin Ronacher'
import pkg_resources
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
release = __import__('pkg_resources').get_distribution('Flask').version
version = '.'.join(release.split('.')[:2])
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None
# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']
# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None
# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True
# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True
# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []
# -- Options for HTML output ---------------------------------------------------
# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'nature'
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}
# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []
# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None
# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None
# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None
# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'
# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True
# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}
# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}
# If false, no module index is generated.
#html_use_modindex = True
# If false, no index is generated.
#html_use_index = True
# If true, the index is split into individual pages for each letter.
#html_split_index = False
# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True
# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True
# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True
# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''
# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''
# Output file base name for HTML help builder.
htmlhelp_basename = 'Flaskdoc'
# -- Options for LaTeX output --------------------------------------------------
# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'
# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Flask.tex', u'Flask Documentation',
   u'Armin Ronacher', 'manual'),
]
# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None
# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False
# Additional stuff for the LaTeX preamble.
#latex_preamble = ''
# Documents to append as an appendix to all manuals.
#latex_appendices = []
# If false, no module index is generated.
#latex_use_modindex = True
# -- Options for Epub output ---------------------------------------------------
# Bibliographic Dublin Core info.
#epub_title = ''
#epub_author = ''
#epub_publisher = ''
#epub_copyright = ''
# The language of the text. It defaults to the language option
# or en if the language is not set.
#epub_language = ''
# The scheme of the identifier. Typical schemes are ISBN or URL.
#epub_scheme = ''
# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#epub_identifier = ''
# A unique identification for the text.
#epub_uid = ''
# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_pre_files = []
# HTML files shat should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_post_files = []
# A list of files that should not be packed into the epub file.
#epub_exclude_files = []
# The depth of the table of contents in toc.ncx.
#epub_tocdepth = 3
from setuptools import setup
setup(
    name='Flask',
    version='0.1',
    url='http://github.com/mitsuhiko/flask/',
    license='BSD',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    description='A microframework based on Werkzeug, Jinja2 and good intentions',
    modules=['flask'],
    zip_safe=False,
    platforms='any',
    install_requires=[ # yes, as of now we need the development versions
        'Werkzeug==dev',
        'Jinja2==dev',
    ]
)