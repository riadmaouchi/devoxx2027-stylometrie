# Lignes ajoutees par un contributeur de github.com/django/django (BSD-3-Clause)
# Extraites par experiments/construire_corpus.py — regle et provenance : corpus/devs/PROVENANCE.md
    @property
    def page_range(self):
    @property
    def outdim(self):
    @outdim.setter
    def outdim(self, new_dim):
    @property
    def srid(self):
    @srid.setter
    def srid(self, include):
        if bool(flag) != self._trim:
            self._trim = bool(flag)
            wkt_writer_set_trim(self.ptr, b'\x01' if flag else b'\x00')
        if (not isinstance(precision, int) or precision < 0) and precision is not None:
            raise AttributeError('WKT output rounding precision must be non-negative integer or None.')
        if precision != self._precision:
        return wkt_w(dim=3 if self.hasz else 2).write(self).decode()
        return wkb_w(dim=3 if self.hasz else 2).write_hex(self)
        return ewkb_w(dim=3 if self.hasz else 2).write_hex(self)
    def __init__(self, dim=2, trim=False, precision=None):
        super(WKTWriter, self).__init__()
        if bool(trim) != self._trim:
            self.trim = trim
        if precision is not None:
            self.precision = precision
        self.outdim = dim
    def __init__(self, dim=2):
        super(WKBWriter, self).__init__()
        self.outdim = dim
def wkt_w(dim=2, trim=False, precision=None):
        thread_context.wkt_w = WKTWriter(dim=dim, trim=trim, precision=precision)
    else:
        thread_context.wkt_w.outdim = dim
        thread_context.wkt_w.trim = trim
        thread_context.wkt_w.precision = precision
        thread_context.wkb_w = WKBWriter(dim=dim)
    else:
        thread_context.wkb_w.outdim = dim
        thread_context.ewkb_w = WKBWriter(dim=dim)
    else:
        thread_context.ewkb_w.outdim = dim
        return wkt_w(dim=3 if self.hasz else 2, trim=True).write(self).decode()
utf8_charset_qp = Charset.Charset('utf-8')
utf8_charset_qp.body_encoding = Charset.QP
RFC5322_EMAIL_LINE_LENGTH_LIMIT = 998
            has_long_lines = any(len(l) > RFC5322_EMAIL_LINE_LENGTH_LIMIT for l in _text.splitlines())
            # Quoted-Printable encoding has the side effect of shortening long
            # lines, if any (#22561).
            self.set_payload(_text, utf8_charset_qp if has_long_lines else utf8_charset)
    ignore_patterns = ['CVS', '.*', '*~']
from django.apps import apps
            help="Don't ignore the common private glob-style patterns (defaults to 'CVS', '.*' and '*~').",
            ignore_patterns += apps.get_app_config('staticfiles').ignore_patterns
        return sorted(
            s for s in list(self.__dict__) + dir(self.default_settings)
            if s not in self._deleted
        )
            old_path = self.work_path
            new_path = self.path
            old_path = self.work_path[2:]
            new_path = self.path[2:]
        return re.sub(
            r'^(#: .*)(' + re.escape(old_path) + r')',
            r'\1' + new_path,
            msgs,
            flags=re.MULTILINE
        )
            lambda match: match.group().replace(old_path, new_path),
        if (self.used_parameters and self.lookup_kwarg in self.used_parameters and
                self.used_parameters[self.lookup_kwarg] in ('1', '0')):
            self.used_parameters[self.lookup_kwarg] = bool(int(self.used_parameters[self.lookup_kwarg]))
        return RangeField().get_prep_value(self.rhs)
from django.utils.encoding import force_text
    prepare_rhs = False
    def get_prep_lookup(self):
        return [force_text(item) for item in self.rhs]
class HasAnyKeys(HasKeys):
        Hook used by Lookup.get_prep_lookup() to do custom preparation.
        Used by the default implementations of get_db_prep_save().
        return self.to_python(value)
        return self.to_python(value)
            # We need to run the related field's get_prep_value(). Consider case
                # Run the target field's get_prep_value. We can safely assume there is
                target_field = self.lhs.output_field.get_path_info()[-1].target_fields[-1]
                self.rhs = [target_field.get_prep_value(v) for v in self.rhs]
            # We need to run the related field's get_prep_value(). Consider case
                target_field = self.lhs.output_field.get_path_info()[-1].target_fields[-1]
                self.rhs = target_field.get_prep_value(self.rhs)
    prepare_rhs = True
        if hasattr(self.rhs, '_prepare'):
            return self.rhs._prepare(self.lhs.output_field)
        if self.prepare_rhs and hasattr(self.lhs.output_field, 'get_prep_value'):
            return self.lhs.output_field.get_prep_value(self.rhs)
        return self.rhs
        return ('%s', [value])
    prepare_rhs = False
    def get_prep_lookup(self):
        if hasattr(self.rhs, '_prepare'):
            return self.rhs._prepare(self.lhs.output_field)
        if hasattr(self.lhs.output_field, 'get_prep_value'):
            return [self.lhs.output_field.get_prep_value(v) for v in self.rhs]
        return self.rhs
    prepare_rhs = False
    prepare_rhs = False
    prepare_rhs = False
    prepare_rhs = False
    prepare_rhs = False
    prepare_rhs = False
    def get_prep_lookup(self):
        if hasattr(self.rhs, '_prepare'):
            return self.rhs._prepare(self.lhs.output_field)
        return [self.lhs.output_field.get_prep_value(v) for v in self.rhs]
    prepare_rhs = False
    prepare_rhs = False
    prepare_rhs = False
from django.utils import six
from django.utils.functional import lazy
from django.utils.six import string_types, text_type
def _password_validators_help_text_html(password_validators=None):
password_validators_help_text_html = lazy(_password_validators_help_text_html, text_type)
        Escape CR and LF characters.
        return subject.replace('\n', '\\n').replace('\r', '\\r')
from .validators import ASCIIUsernameValidator, UnicodeUsernameValidator
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
        validators=[username_validator],
import re
from django.core import validators
from django.utils import six
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = re.ASCII if six.PY3 else 0
@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = re.UNICODE if six.PY2 else 0
import unicodedata
from django.utils.encoding import force_text, python_2_unicode_compatible
    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', force_text(username))
import unicodedata
class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))
        field_classes = {'username': UsernameField}
        field_classes = {'username': UsernameField}
    username = UsernameField(
        username = self.normalize_username(username)
from django.contrib.gis.gdal import OGRGeomType
        Returns a GDAL SpatialReference object.
        # TODO: Is caching really necessary here?  Is complexity worth it?
        if hasattr(self, '_srs'):
            # Returning a clone of the cached SpatialReference object.
            return self._srs.clone()
            # Attempting to cache a SpatialReference object.
            # Trying to get from WKT first.
            try:
                self._srs = gdal.SpatialReference(self.wkt)
                return self.srs
            except Exception as e:
                msg = e
            try:
                self._srs = gdal.SpatialReference(self.proj4text)
                return self.srs
            except Exception as e:
                msg = e
            raise Exception('Could not get OSR SpatialReference from WKT: %s\nError:\n%s' % (self.wkt, msg))
        return self.srs.ellipsoid
        return self.srs.projected
        return self.srs.local
        return self.srs.geographic
        return self.srs.linear_name
        return self.srs.linear_units
        return self.srs.angular_name
        return self.srs.angular_units
        return gdal.SpatialReference(wkt).units
        srs = gdal.SpatialReference(wkt)
        sphere_params = srs.ellipsoid
        sphere_name = srs['spheroid']
        Returns the string representation, a 'pretty' OGC WKT.
        return six.text_type(self.srs)
from django.contrib.gis import forms, gdal
        if isinstance(value, gdal.GDALRaster):
                return gdal.GDALRaster(value)
                return gdal.GDALRaster(value)
            # Try to convert the input to raster.
            raster = self.get_raster_prep_value(obj, is_candidate)
        setattr(cls, self.attname, SpatialProxy(gdal.GDALRaster, self))
    map_srid = 3857
from django.core.serializers.base import SerializerDoesNotExist
        # Type-based geometries.
        # TODO: Support 'M' extension.
        if f.dim == 3:
            geom_type = f.geom_type + 'Z'
        else:
            geom_type = f.geom_type
        if f.geography:
            return 'geography(%s,%d)' % (geom_type, f.srid)
              102: 'PointZ',
        elif s == 'PointZ':
            s = 'Point'
    # Force a TemplateResponse to be rendered.
    if not getattr(response, 'is_rendered', True) and callable(getattr(response, 'render', None)):
        response = response.render()
        from django.contrib.auth.views import LogoutView
        return LogoutView.as_view(**defaults)(request)
        from django.contrib.auth.views import LoginView
        return LoginView.as_view(**defaults)(request)
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
from django.utils.decorators import method_decorator
from django.utils.deprecation import (
    RemovedInDjango20Warning, RemovedInDjango21Warning,
)
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
class LoginView(FormView):
    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    redirect_authenticated_user = False
    extra_context = None
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)
    def get_success_url(self):
        """Ensure the user-originating redirection URL is safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            return resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to
    def get_form_class(self):
        return self.authentication_form or self.form_class
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_success_url(),
            'site': current_site,
            'site_name': current_site.name,
        })
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context
@deprecate_current_app
def login(request, *args, **kwargs):
    warnings.warn(
        'The login() view is superseded by the class-based LoginView().',
        RemovedInDjango21Warning, stacklevel=2
    )
    return LoginView.as_view(**kwargs)(request, *args, **kwargs)
class LogoutView(TemplateView):
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/logged_out.html'
    extra_context = None
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)
    def get_next_page(self):
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            next_page = resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            next_page = self.next_page
        if (self.redirect_field_name in self.request.POST or
                self.redirect_field_name in self.request.GET):
            next_page = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name)
            )
            # Security check -- don't allow redirection to a different host.
            if not is_safe_url(url=next_page, host=self.request.get_host()):
                next_page = self.request.path
        return next_page
    def get_context_data(self, **kwargs):
        context = super(LogoutView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            'site': current_site,
            'site_name': current_site.name,
            'title': _('Logged out'),
        })
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context
@deprecate_current_app
def logout(request, *args, **kwargs):
    warnings.warn(
        'The logout() view is superseded by the class-based LogoutView().',
        RemovedInDjango21Warning, stacklevel=2
    )
    return LogoutView.as_view(**kwargs)(request, *args, **kwargs)
        # Add the Content-Length header to non-streaming responses if not
        # already set.
        if not response.streaming and not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))
    ('dsb', gettext_noop('Lower Sorbian')),
    ('hsb', gettext_noop('Upper Sorbian')),
            # Unfortunately, Python doesn't yet pass a Charset instance as
            # MIMEText init parameter to set_payload().
            # http://bugs.python.org/issue27445
            if six.PY3 and isinstance(_text, bytes):
                # Sniffing encoding would fail with bytes content in MIMEText.__init__.
                _text = _text.decode('utf-8')
            input_files_list.write(force_str('\n'.join(input_files), encoding=DEFAULT_LOCALE_ENCODING))
            primary_keys = [pk.strip() for pk in pks.split(',')]
        2950: 'UUIDField',
from django.db import connections
        # Connections may already exist before we are called.
        for conn in connections.all():
            if conn.connection is not None:
                register_hstore_handler(conn)
            if self.prepare_rhs and hasattr(self.lhs.output_field, 'get_path_info'):
        if self.max_length is not None and not widget.is_hidden:
        if self.min_length is not None and not widget.is_hidden:
        if value and isinstance(value, six.string_types):
        if value and isinstance(value, six.string_types):
            'startapp', 'startproject', 'compilemessages',
                # SpatiaLite versions >= 4 use the new SFSQL 1.2 offsets
        Convert the polygon data received from SpatiaLite to min/max values.
            raise TypeError("SpatiaLite NumPoints can only operate on LineString content")
        # SpatiaLite specific
from django.utils.translation import templatize
    from .template import templatize
    return templatize(src, origin)
from __future__ import unicode_literals
import re
import warnings
from django.conf import settings
from django.template.base import (
    TOKEN_BLOCK, TOKEN_COMMENT, TOKEN_TEXT, TOKEN_VAR, TRANSLATOR_COMMENT_MARK,
    Lexer,
)
from django.utils import six
from django.utils.encoding import force_text
from django.utils.six import StringIO
from . import TranslatorCommentWarning, trim_whitespace
dot_re = re.compile(r'\S')
def blankout(src, char):
    """
    Change every non-whitespace character to the given char.
    Used in the templatize function.
    """
    return dot_re.sub(char, src)
context_re = re.compile(r"""^\s+.*context\s+((?:"[^"]*?")|(?:'[^']*?'))\s*""")
inline_re = re.compile(
    # Match the trans 'some text' part
    r"""^\s*trans\s+((?:"[^"]*?")|(?:'[^']*?'))"""
    # Match and ignore optional filters
    r"""(?:\s*\|\s*[^\s:]+(?::(?:[^\s'":]+|(?:"[^"]*?")|(?:'[^']*?')))?)*"""
    # Match the optional context part
    r"""(\s+.*context\s+((?:"[^"]*?")|(?:'[^']*?')))?\s*"""
)
block_re = re.compile(r"""^\s*blocktrans(\s+.*context\s+((?:"[^"]*?")|(?:'[^']*?')))?(?:\s+|$)""")
endblock_re = re.compile(r"""^\s*endblocktrans$""")
plural_re = re.compile(r"""^\s*plural$""")
constant_re = re.compile(r"""_\(((?:".*?")|(?:'.*?'))\)""")
def templatize(src, origin=None):
    """
    Turn a Django template into something that is understood by xgettext. It
    does so by translating the Django translation tags into standard gettext
    function invocations.
    """
    src = force_text(src, settings.FILE_CHARSET)
    out = StringIO('')
    message_context = None
    intrans = False
    inplural = False
    trimmed = False
    singular = []
    plural = []
    incomment = False
    comment = []
    lineno_comment_map = {}
    comment_lineno_cache = None
    # Adding the u prefix allows gettext to recognize the Unicode string
    # (#26093).
    raw_prefix = 'u' if six.PY3 else ''
    def join_tokens(tokens, trim=False):
        message = ''.join(tokens)
        if trim:
            message = trim_whitespace(message)
        return message
    for t in Lexer(src).tokenize():
        if incomment:
            if t.token_type == TOKEN_BLOCK and t.contents == 'endcomment':
                content = ''.join(comment)
                translators_comment_start = None
                for lineno, line in enumerate(content.splitlines(True)):
                    if line.lstrip().startswith(TRANSLATOR_COMMENT_MARK):
                        translators_comment_start = lineno
                for lineno, line in enumerate(content.splitlines(True)):
                    if translators_comment_start is not None and lineno >= translators_comment_start:
                        out.write(' # %s' % line)
                    else:
                        out.write(' #\n')
                incomment = False
                comment = []
            else:
                comment.append(t.contents)
        elif intrans:
            if t.token_type == TOKEN_BLOCK:
                endbmatch = endblock_re.match(t.contents)
                pluralmatch = plural_re.match(t.contents)
                if endbmatch:
                    if inplural:
                        if message_context:
                            out.write(' npgettext({p}{!r}, {p}{!r}, {p}{!r},count) '.format(
                                message_context,
                                join_tokens(singular, trimmed),
                                join_tokens(plural, trimmed),
                                p=raw_prefix,
                            ))
                        else:
                            out.write(' ngettext({p}{!r}, {p}{!r}, count) '.format(
                                join_tokens(singular, trimmed),
                                join_tokens(plural, trimmed),
                                p=raw_prefix,
                            ))
                        for part in singular:
                            out.write(blankout(part, 'S'))
                        for part in plural:
                            out.write(blankout(part, 'P'))
                    else:
                        if message_context:
                            out.write(' pgettext({p}{!r}, {p}{!r}) '.format(
                                message_context,
                                join_tokens(singular, trimmed),
                                p=raw_prefix,
                            ))
                        else:
                            out.write(' gettext({p}{!r}) '.format(
                                join_tokens(singular, trimmed),
                                p=raw_prefix,
                            ))
                        for part in singular:
                            out.write(blankout(part, 'S'))
                    message_context = None
                    intrans = False
                    inplural = False
                    singular = []
                    plural = []
                elif pluralmatch:
                    inplural = True
                else:
                    filemsg = ''
                    if origin:
                        filemsg = 'file %s, ' % origin
                    raise SyntaxError(
                        "Translation blocks must not include other block tags: "
                        "%s (%sline %d)" % (t.contents, filemsg, t.lineno)
                    )
            elif t.token_type == TOKEN_VAR:
                if inplural:
                    plural.append('%%(%s)s' % t.contents)
                else:
                    singular.append('%%(%s)s' % t.contents)
            elif t.token_type == TOKEN_TEXT:
                contents = t.contents.replace('%', '%%')
                if inplural:
                    plural.append(contents)
                else:
                    singular.append(contents)
        else:
            # Handle comment tokens (`{# ... #}`) plus other constructs on
            # the same line:
            if comment_lineno_cache is not None:
                cur_lineno = t.lineno + t.contents.count('\n')
                if comment_lineno_cache == cur_lineno:
                    if t.token_type != TOKEN_COMMENT:
                        for c in lineno_comment_map[comment_lineno_cache]:
                            filemsg = ''
                            if origin:
                                filemsg = 'file %s, ' % origin
                            warn_msg = (
                                "The translator-targeted comment '%s' "
                                "(%sline %d) was ignored, because it wasn't "
                                "the last item on the line."
                            ) % (c, filemsg, comment_lineno_cache)
                            warnings.warn(warn_msg, TranslatorCommentWarning)
                        lineno_comment_map[comment_lineno_cache] = []
                else:
                    out.write('# %s' % ' | '.join(lineno_comment_map[comment_lineno_cache]))
                comment_lineno_cache = None
            if t.token_type == TOKEN_BLOCK:
                imatch = inline_re.match(t.contents)
                bmatch = block_re.match(t.contents)
                cmatches = constant_re.findall(t.contents)
                if imatch:
                    g = imatch.group(1)
                    if g[0] == '"':
                        g = g.strip('"')
                    elif g[0] == "'":
                        g = g.strip("'")
                    g = g.replace('%', '%%')
                    if imatch.group(2):
                        # A context is provided
                        context_match = context_re.match(imatch.group(2))
                        message_context = context_match.group(1)
                        if message_context[0] == '"':
                            message_context = message_context.strip('"')
                        elif message_context[0] == "'":
                            message_context = message_context.strip("'")
                        out.write(' pgettext({p}{!r}, {p}{!r}) '.format(
                            message_context, g, p=raw_prefix
                        ))
                        message_context = None
                    else:
                        out.write(' gettext({p}{!r}) '.format(g, p=raw_prefix))
                elif bmatch:
                    for fmatch in constant_re.findall(t.contents):
                        out.write(' _(%s) ' % fmatch)
                    if bmatch.group(1):
                        # A context is provided
                        context_match = context_re.match(bmatch.group(1))
                        message_context = context_match.group(1)
                        if message_context[0] == '"':
                            message_context = message_context.strip('"')
                        elif message_context[0] == "'":
                            message_context = message_context.strip("'")
                    intrans = True
                    inplural = False
                    trimmed = 'trimmed' in t.split_contents()
                    singular = []
                    plural = []
                elif cmatches:
                    for cmatch in cmatches:
                        out.write(' _(%s) ' % cmatch)
                elif t.contents == 'comment':
                    incomment = True
                else:
                    out.write(blankout(t.contents, 'B'))
            elif t.token_type == TOKEN_VAR:
                parts = t.contents.split('|')
                cmatch = constant_re.match(parts[0])
                if cmatch:
                    out.write(' _(%s) ' % cmatch.group(1))
                for p in parts[1:]:
                    if p.find(':_(') >= 0:
                        out.write(' %s ' % p.split(':', 1)[1])
                    else:
                        out.write(blankout(p, 'F'))
            elif t.token_type == TOKEN_COMMENT:
                if t.contents.lstrip().startswith(TRANSLATOR_COMMENT_MARK):
                    lineno_comment_map.setdefault(t.lineno, []).append(t.contents)
                    comment_lineno_cache = t.lineno
            else:
                out.write(blankout(t.contents, 'X'))
    return out.getvalue()
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils import six
if six.PY2:
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
            m = re.search('"(.*)".*PRIMARY KEY( AUTOINCREMENT)?', field_desc)
from django.utils.encoding import (
    force_str, force_text, repercent_broken_unicode,
)
from django.utils.functional import cached_property
        request = self.request_class(environ)
        response = self.get_response(request)
    return repercent_broken_unicode(path_info).decode(UTF_8)
        return super(WSGIRequestHandler, self).get_environ()
class JsonAdapter(Json):
    """
    Customized psycopg2.extras.Json to allow for a custom encoder.
    """
    def __init__(self, adapted, dumps=None, encoder=None):
        self.encoder = encoder
        super(JsonAdapter, self).__init__(adapted, dumps=dumps)
    def dumps(self, obj):
        options = {'cls': self.encoder} if self.encoder else {}
        return json.dumps(obj, **options)
    def __init__(self, verbose_name=None, name=None, encoder=None, **kwargs):
        if encoder and not callable(encoder):
            raise ValueError("The encoder parameter must be a callable object.")
        self.encoder = encoder
        super(JSONField, self).__init__(verbose_name, name, **kwargs)
    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        if self.encoder is not None:
            kwargs['encoder'] = self.encoder
        return name, path, args, kwargs
            return JsonAdapter(value, encoder=self.encoder)
        options = {'cls': self.encoder} if self.encoder else {}
            json.dumps(value, **options)
from django.utils.encoding import force_text, python_2_unicode_compatible
        return "%s.%s" % (self.app_label, self.model_name)
            GROUP BY indexname, indisunique, indisprimary, amname;
from django.utils.encoding import force_str
    @property
    def connection_class(self):
        return smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
            self.connection = self.connection_class(self.host, self.port, **connection_params)
                self.connection.login(force_str(self.username), force_str(self.password))
from django.utils.encoding import force_text
                'selected': self.lookup_val == force_text(pk_val),
                'selected': force_text(lookup) == self.lookup_val,
            val = force_text(val)
from django.utils.encoding import force_text
                        result_repr = force_text(value)
from django.utils.encoding import force_text, python_2_unicode_compatible
            object_id=force_text(object_id),
        return force_text(self.action_time)
        return force_text(value)
from django.utils.encoding import force_text, python_2_unicode_compatible
        return force_text([instance._get_pk_val() for instance in qs])
from django.utils.encoding import force_text
                self.log("Pretending to delete '%s'" % force_text(fpath), level=1)
                self.log("Deleting '%s'" % force_text(fpath), level=1)
from django.utils.encoding import force_text, iri_to_uri
                url=force_text(enc_url),
                length=force_text(self._get_dynamic_attr('item_enclosure_length', item)),
                mime_type=force_text(self._get_dynamic_attr('item_enclosure_mime_type', item)),
    force_bytes, force_str, force_text, python_2_unicode_compatible,
        return force_text(self.name or '')
from django.utils.encoding import force_text
        attrs = OrderedDict([("model", force_text(obj._meta))])
                attrs['pk'] = force_text(obj_pk)
                    self.xml.characters(force_text(key_value))
                self.xml.characters(force_text(related_att))
                        self.xml.characters(force_text(key_value))
                        'pk': force_text(value._get_pk_val())
            ("to", force_text(field.remote_field.model._meta)),
        return force_text(self.value_from_object(obj))
        return force_text(value)
        return force_text(value)
from django.utils.encoding import force_text
            (x._get_pk_val(), force_text(x)) for x in self.related_model._default_manager.all()
from django.utils.encoding import force_text, python_2_unicode_compatible
        if auto_id and '%s' in force_text(auto_id):
            return force_text(auto_id) % self.html_name
from django.utils.encoding import force_str, force_text
        value = force_text(value).strip()
        return force_text(value)
        return [force_text(val) for val in value]
from django.utils.encoding import force_text
        return force_text(obj)
# django.utils.encoding.force_text for parsing URLs and form inputs. Thus,
from django.utils.encoding import force_text
            return force_text(token)
from django.utils.encoding import force_text
            force_text(k, 'ascii'): v.resolve(context)
from django.utils.encoding import force_bytes, force_text
                unicode_hint = force_text(
            c['exception_value'] = force_text(self.exc_value, errors='replace')
from django.utils.encoding import force_text
            formats[k] = force_text(v)
            formats[k] = [force_text(value) for value in v]
    def get_constraints(self, cursor, table_name):
        constraints = super(SpatiaLiteIntrospection, self).get_constraints(cursor, table_name)
            constraints['%s__spatial__index' % row[0]] = {
                "columns": [row[0]],
                "primary_key": False,
                "unique": False,
                "foreign_key": None,
                "check": False,
                "index": True,
            }
        return constraints
                    primary_key_column = connection.introspection.get_primary_key_column(cursor, table_name)
                    unique_columns = [
                        c['columns'][0] for c in constraints.values()
                        if c['unique'] and len(c['columns']) == 1
                    ]
                    if column_name == primary_key_column:
                        extra_params['primary_key'] = True
                    elif column_name in unique_columns:
                        extra_params['unique'] = True
        for constraint in self.get_constraints(cursor, table_name).values():
            if constraint['primary_key']:
                return constraint['columns'][0]
        Deprecated in Django 1.11, use get_constraints instead.
import warnings
from django.utils.deprecation import RemovedInDjango21Warning
        warnings.warn(
            "get_indexes() is deprecated in favor of get_constraints().",
            RemovedInDjango21Warning, stacklevel=2
        )
import warnings
from django.utils.deprecation import RemovedInDjango21Warning
        warnings.warn(
            "get_indexes() is deprecated in favor of get_constraints().",
            RemovedInDjango21Warning, stacklevel=2
        )
import warnings
from django.utils.deprecation import RemovedInDjango21Warning
        warnings.warn(
            "get_indexes() is deprecated in favor of get_constraints().",
            RemovedInDjango21Warning, stacklevel=2
        )
import warnings
from django.utils.deprecation import RemovedInDjango21Warning
        warnings.warn(
            "get_indexes() is deprecated in favor of get_constraints().",
            RemovedInDjango21Warning, stacklevel=2
        )
                ) idx
                LEFT JOIN pg_class c ON idx.indrelid = c.oid
                LEFT JOIN pg_class c2 ON idx.indexrelid = c2.oid
                LEFT JOIN pg_am am ON c2.relam = am.oid
                LEFT JOIN pg_attribute attr ON attr.attrelid = c.oid AND attr.attnum = idx.key
                WHERE c.relname = %s
        Retrieve any constraints or keys (unique, pk, fk, check, index) across
        one or more columns. Also retrieve the definition of expression-based
        indexes.
                "definition": None,
                array_agg(ordering), amname, exprdef
                    CASE
                        WHEN idx.indexprs IS NOT NULL THEN
                            pg_get_indexdef(idx.indexrelid)
                    END AS exprdef,
            GROUP BY indexname, indisunique, indisprimary, amname, exprdef;
        for index, columns, unique, primary, orders, type_, definition in cursor.fetchall():
                    "columns": columns if columns != [None] else [],
                    "orders": orders if orders != [None] else [],
                    "definition": definition,
    The 'geometry_columns' view from PostGIS. See the PostGIS
    def _field_should_be_indexed(self, model, field):
        if getattr(field, 'spatial_index', False):
            return True
        return super(PostGISSchemaEditor, self)._field_should_be_indexed(model, field)
    def _create_index_sql(self, model, fields, suffix="", sql=None):
        if len(fields) != 1 or not hasattr(fields[0], 'geodetic'):
            return super(PostGISSchemaEditor, self)._create_index_sql(model, fields, suffix=suffix, sql=sql)
        field = fields[0]
        field_column = self.quote_name(field.column)
        if field.geom_type == 'RASTER':
            # For raster fields, wrap index creation SQL statement with ST_ConvexHull.
            # Indexes on raster columns are based on the convex hull of the raster.
            field_column = self.rast_index_wrapper % field_column
        elif field.dim > 2 and not field.geography:
            # Use "nd" ops which are fast on multidimensional cases
            field_column = "%s %s" % (field_column, self.geom_index_ops_nd)
        return self.sql_create_index % {
            "name": self.quote_name('%s_%s_id' % (model._meta.db_table, field.column)),
            "table": self.quote_name(model._meta.db_table),
            "using": "USING %s" % self.geom_index_type,
            "columns": field_column,
            "extra": '',
        }
    sql_alter_column_to_3d = "ALTER COLUMN %(column)s TYPE %(type)s USING ST_Force3D(%(column)s)::%(type)s"
    sql_alter_column_to_2d = "ALTER COLUMN %(column)s TYPE %(type)s USING ST_Force2D(%(column)s)::%(type)s"
    def _alter_column_type_sql(self, table, old_field, new_field, new_type):
        """
        Special case when dimension changed.
        """
        if not hasattr(old_field, 'dim') or not hasattr(new_field, 'dim'):
            return super(PostGISSchemaEditor, self)._alter_column_type_sql(
                table, old_field, new_field, new_type
            )
        if old_field.dim == 2 and new_field.dim == 3:
            sql_alter = self.sql_alter_column_to_3d
        elif old_field.dim == 3 and new_field.dim == 2:
            sql_alter = self.sql_alter_column_to_2d
        else:
            sql_alter = self.sql_alter_column_type
        return (
            (
                sql_alter % {
                    "column": self.quote_name(new_field.column),
                    "type": new_type,
                },
                [],
            ),
            [],
        )
            try:
                connections.close_all()
            except ImproperlyConfigured:
                # Ignore if connections aren't setup at this point (e.g. no
                # configured settings).
                pass
from django.conf import settings
            django.setup()
from django.core.exceptions import ImproperlyConfigured
        encoding = settings.FILE_CHARSET if self.command.settings_available else 'utf-8'
        with io.open(self.path, 'r', encoding=encoding) as fp:
            content = templatize(src_data, origin=self.path[2:], charset=encoding)
            if self.settings_available:
                self.locale_paths.extend(settings.LOCALE_PATHS)
    @cached_property
    def settings_available(self):
        try:
            settings.LOCALE_PATHS
        except ImproperlyConfigured:
            if self.verbosity > 1:
                self.stderr.write("Running without configured settings.")
            return False
        return True
        ignored_roots = []
        if self.settings_available:
            ignored_roots = [os.path.normpath(p) for p in (settings.MEDIA_ROOT, settings.STATIC_ROOT) if p]
def templatize(src, **kwargs):
    return templatize(src, **kwargs)
def templatize(src, origin=None, charset='utf-8'):
    src = force_text(src, charset)
            with translation_override(None):
                for formset in formsets:
                    for added_object in formset.new_objects:
                        change_message.append({
                            'added': {
                                'name': force_text(added_object._meta.verbose_name),
                                'object': force_text(added_object),
                            }
                        })
                    for changed_object, changed_fields in formset.changed_objects:
                        change_message.append({
                            'changed': {
                                'name': force_text(changed_object._meta.verbose_name),
                                'object': force_text(changed_object),
                                'fields': changed_fields,
                            }
                        })
                    for deleted_object in formset.deleted_objects:
                        change_message.append({
                            'deleted': {
                                'name': force_text(deleted_object._meta.verbose_name),
                                'object': force_text(deleted_object),
                            }
                        })
import io
                    with io.open(writer.path, "w", encoding='utf-8') as fh:
                    with io.open(writer.path, "w", encoding='utf-8') as fh:
import io
        with io.open(writer.path, "w", encoding='utf-8') as fh:
        MIMEText.__init__(self, _text, _subtype=_subtype, _charset=_charset)
    def set_payload(self, payload, charset=None):
        if charset == 'utf-8':
            has_long_lines = any(len(l) > RFC5322_EMAIL_LINE_LENGTH_LIMIT for l in payload.splitlines())
            # Quoted-Printable encoding has the side effect of shortening long
            # lines, if any (#22561).
            charset = utf8_charset_qp if has_long_lines else utf8_charset
        MIMEText.set_payload(self, payload, charset=charset)
        members = self._archive.getmembers()
import io
                    with io.open(old_path, 'r', encoding='utf-8') as template_file:
                        content = template_file.read()
                    with io.open(new_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(content)
                else:
                    shutil.copyfile(old_path, new_path)
        return [email for email in (self.to + self.cc + self.bcc) if email]
        if type(self) == GEOSGeometry:
            if GEOSGeometry._GEOS_CLASSES is None:
                # Lazy-loaded variable to avoid import conflicts with GEOSGeometry.
                from .linestring import LineString, LinearRing
                from .point import Point
                from .polygon import Polygon
                from .collections import (
                    GeometryCollection, MultiPoint, MultiLineString, MultiPolygon,
                )
                GEOSGeometry._GEOS_CLASSES = {
                    0: Point,
                    1: LineString,
                    2: LinearRing,
                    3: Polygon,
                    4: MultiPoint,
                    5: MultiLineString,
                    6: MultiPolygon,
                    7: GeometryCollection,
                }
            self.__class__ = GEOSGeometry._GEOS_CLASSES[self.geom_typeid]
    @cached_property
from django.utils.formats import FORMAT_SETTINGS, reset_format_cache
@receiver(setting_changed)
def localize_settings_changed(**kwargs):
    if kwargs['setting'] in FORMAT_SETTINGS or kwargs['setting'] == 'USE_THOUSAND_SEPARATOR':
        reset_format_cache()
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/ol3/3.20.1/ol.css',
                'gis/css/ol3.css',
            )
        }
            'https://cdnjs.cloudflare.com/ajax/libs/ol3/3.20.1/ol.js',
    def serialize(self, value):
        return value.json if value else ''
class OSMWidget(OpenLayersWidget):
            has_long_lines = any(
                len(l.encode('utf-8')) > RFC5322_EMAIL_LINE_LENGTH_LIMIT
                for l in payload.splitlines()
            )
from django.utils.encoding import force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_text
from django.utils.encoding import iri_to_uri
from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes, force_str, force_text
from django.utils.encoding import force_str, force_text
from django.utils.encoding import force_bytes, force_text, smart_text
from django.utils.encoding import force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_str, force_text
from django.utils.encoding import force_str, force_text
from django.utils.encoding import force_text
from django.utils.encoding import force_text, smart_text
        if name == "__str__":
from django.utils.encoding import force_bytes, force_text
        data = crypt.crypt(password, salt)
        return constant_time_compare(data, crypt.crypt(password, data))
        p = getpass.getpass(prompt=prompt)
                    input_msg = '%s%s: ' % (
                        ) if username_rel else ''
                        message = '%s%s: ' % (
                        )
                    password2 = getpass.getpass('Password (again): ')
from django.utils.encoding import force_text
            obj = force_text(self.obj)
from django.utils.encoding import force_text
        return "<%s: %s>" % (self.__class__.__name__, self or "None")
        return "<%s: %s (%s)>" % (self.__class__.__name__, self.name, self.content_type)
from django.utils.encoding import force_text, repercent_broken_unicode
ISO_8859_1, UTF_8 = 'iso-8859-1', 'utf-8'
        start_response(status, response_headers)
                self.connection.login(self.username, self.password)
from io import TextIOBase
class OutputWrapper(TextIOBase):
        self._out.write(style_func(msg))
                        self.style.ERROR(str(e))
                        else self.style.WARNING(str(e))
from django.utils.encoding import DEFAULT_LOCALE_ENCODING
            input_files_list.write(('\n'.join(input_files)))
                    plural_form_line = m.group('value')
from django.utils.encoding import force_bytes, force_text
        self.sep = sep
        self.salt = salt or '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        return force_text(base64_hmac(self.salt + 'signer', value, self.key))
        return '%s%s%s' % (value, self.sep, self.signature(value))
        value = '%s%s%s' % (force_text(value), self.sep, self.timestamp())
            kwargs['passwd'] = settings_dict['PASSWORD']
            conn_params['password'] = settings_dict['PASSWORD']
from django.utils.encoding import force_text
        return '<%s: %s>' % (self.__class__.__name__, u)
from django.utils.encoding import force_text
            dirname = force_text(datetime.datetime.now().strftime(self.upload_to))
from django.utils.encoding import force_text
        return datetime.datetime.strptime(value, format).date()
        return datetime.datetime.strptime(value, format).time()
        return datetime.datetime.strptime(value, format)
from django.utils.encoding import force_text
                    d = datetime.datetime.strptime(value, input_format)
from django.utils.encoding import escape_uri_path, force_bytes, iri_to_uri
            return '<%s>' % self.__class__.__name__
        return '<%s: %s %r>' % (self.__class__.__name__, self.method, self.get_full_path())
from django.utils.encoding import force_bytes, force_text, iri_to_uri
from django.utils.encoding import force_text
        return "<%s: %r>" % (self.__class__.__name__, self.s[:25])
from django.utils.encoding import force_bytes, uri_to_iri
        path = parsed.path
        if parsed.params:
            path += ";" + parsed.params
        parsed = urlparse(str(path))  # path can be lazy
    test_module = __import__(test_module_name, {}, {}, test_path[-1])
from django.utils.encoding import force_text
        return '<%s %s %s>' % (self.__class__.__name__, self.name, self.regex.pattern)
        format = default or get_format('DATETIME_INPUT_FORMATS')[0]
        format = default or get_format('DATE_INPUT_FORMATS')[0]
        format = default or get_format('TIME_INPUT_FORMATS')[0]
from django.utils.encoding import force_text
        segment = unquote(segment)
        query_parts = [(unquote(q[0]), unquote(q[1]))
from django.utils.encoding import force_text
        return template % (self.connector, ', '.join(force_text(c) for c in self.children))
        return "<%s: %s>" % (self.__class__.__name__, self)
from django.utils.encoding import force_text
        'reason': str(exception),
from django.utils.encoding import force_text
        return datetime.datetime.strptime(datestr, format).date()
            return 'new OpenLayers.Bounds(%s)' % extent
            return '%s(%s)' % (
                self._adapter.getquoted().decode()
                        param_name, check_types)
        return '%s (%s)' % (self.name, self.driver)
            raise GDALException('Unrecognized input type for GDAL/OGR Driver: %s' % type(dr_input))
            raise GDALException('Could not initialize GDAL/OGR Driver on input: %s' % dr_input)
                raise TypeError('Incorrect type of argument: %s' % type(args[0]))
                raise TypeError('Incorrect type of argument: %s' % type(args[0]))
            raise GDALException('Cannot create OGR Geometry from input: %s' % geom_input)
            raise OGRIndexError('index out of range: %s' % index)
            raise IndexError('invalid GEOS Geometry index: %s' % index)
            raise TypeError('Improper geometry input type: %s' % type(geo_input))
        raise ValueError('%s not found in object' % val)
        raise IndexError('invalid index: %s' % index)
            raise TypeError('Invalid point dimension: %s' % ndim)
        response_headers = list(response.items())
            response_headers.append(('Set-Cookie', c.output(header='')))
    key and default should be strings.
    value = environ.get(key, default)
    return name, val
            potfile = os.path.join(path, '%s.pot' % self.domain)
            pot_path = os.path.join(path, '%s.pot' % self.domain)
            potfile = os.path.join(locale_dir, '%s.pot' % self.domain)
        pofile = os.path.join(basedir, '%s.po' % self.domain)
            os.environ["DJANGO_COLORS"] = "nocolor"
            if args[0].startswith('\x16\x03'):
Database.register_converter("bool", decoder(lambda s: s == '1'))
Database.register_converter("time", decoder(parse_time))
Database.register_converter("date", decoder(parse_date))
Database.register_converter("datetime", decoder(parse_datetime))
Database.register_converter("timestamp", decoder(parse_datetime))
Database.register_converter("TIMESTAMP", decoder(parse_datetime))
Database.register_converter("decimal", decoder(backend_utils.typecast_decimal))
        return '<Deferred field>'
        return '<Deferred field>'
                    'DoesNotExist',
                    'MultipleObjectsReturned',
__all__ = [
]
        # Need to convert File objects provided via a form to string for database insertion
__all__ = ['Index']
    for chunk in cookie.split(';'):
        if '=' in chunk:
            key, val = chunk.split('=', 1)
            key, val = '', chunk
    Convert bytes objects to strings, using the given encoding. Illegally
    Return any non-bytes objects without change.
                value = Header(value, 'utf-8', maxlinelen=sys.maxsize).encode()
            'PATH_INFO': '/',
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.url_scheme': 'http',
            'REQUEST_METHOD': method,
            'SERVER_PORT': '443' if secure else '80',
            'wsgi.url_scheme': 'https' if secure else 'http',
                'CONTENT_TYPE': content_type,
                    "%s%s" % (capfirst(browser), name),
        return '<%s %s (%s:%s) %s>' % (
        segment = quote(segment, safe=RFC3986_SUBDELIMS + RFC3986_GENDELIMS + '~')
RFC3986_GENDELIMS = ":/?#[]@"
RFC3986_SUBDELIMS = "!$&'()*+,;="
        nv = name_value.split('=', 1)
    object can be used everywhere a string is appropriate.
    eol_message = message.replace('\r\n', '\n').replace('\r', '\n')
    return main + sub
            raise IncorrectLookupParameters(e) from e
            except Exception as exc:
                raise Exception(
                    'corresponding to "%s"."%s"' % (table_name, geo_col)
                ) from exc
        except Exception as exc:
            raise ImproperlyConfigured(
                'Unable to load the SpatiaLite library extension "%s"' % self.spatialite_lib
            ) from exc
        except Exception as exc:
            raise ImproperlyConfigured(
                'Cannot determine the SpatiaLite version for the "%s" database. '
                'Was the SpatiaLite initialization SQL loaded on this database?' % (
                    self.connection.settings_dict['NAME'],
                )
            ) from exc
        except Exception as exc:
            raise LayerMapError(
                'Could not translate between the data source and model geometry.'
            ) from exc
            except Exception as exc:
                raise CommandError(
                    "That's the SQL this command wasn't able to run.\n" % (
                        connection.settings_dict['NAME'],
                    )
                ) from exc
    except OSError as err:
        raise os_err_exc_type('Error executing %s' % args[0]) from err
    except (GeneratorExit, DeserializationError):
    except Exception as exc:
        raise DeserializationError() from exc
    except (GeneratorExit, DeserializationError):
    except Exception as exc:
        raise DeserializationError() from exc
    except ImportError as err:
        raise ImproperlyConfigured(
            "WSGI application '%s' could not be loaded; "
            "Error importing module." % app_path
        ) from err
except ImportError as err:
        'Error loading MySQLdb module.\n'
        'Did you install mysqlclient or MySQL-python?'
    ) from err
                raise utils.IntegrityError(*tuple(e.args))
                raise utils.IntegrityError(*tuple(e.args))
                    raise utils.IntegrityError(*tuple(e.args))
from django.utils import timezone
            raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
                raise dj_exc_value.with_traceback(traceback)
from django.utils import formats
        except Exception as exc:
            raise ValidationError(
            ) from exc
from django.utils import timezone
        except Exception as exc:
            raise ValidationError(
                _('%(datetime)s couldn\'t be interpreted '
                  'in time zone %(current_timezone)s; it '
                  'may be ambiguous or it may not exist.'),
                params={'datetime': value, 'current_timezone': current_timezone}
            ) from exc
                                except Exception as exc:
                                    raise MultiPartParserError("Could not decode base64 data.") from exc
                raise UnreadablePostError(*e.args) from e
            raise UnreadablePostError(*e.args) from e
            raise UnreadablePostError(*e.args) from e
    raise new from exc
            raise TemplateDoesNotExist(exc.name, backend=self) from exc
            raise new from exc
from django.utils import translation
                raise TemplateSyntaxError(
                    "No argument provided to the '%s' tag for the context option." % bits[0]
                )
                raise TemplateSyntaxError(
                    "No argument provided to the '%s' tag for the as option." % bits[0]
                )
                raise TemplateSyntaxError(
                    '"context" in %r tag expected exactly one argument.' % bits[0]
                )
                raise TemplateSyntaxError(
                    "No argument provided to the '%s' tag for the asvar option." % bits[0]
                )
                raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
        raise _exception[0](_exception[1]).with_traceback(_exception[2])
    except Exception as exc:
        raise ValueError("%r is not a valid date" % date) from exc
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
        ) from err
    return iri_to_uri(value)
from django.utils.encoding import iri_to_uri
    return iri_to_uri(resolver._reverse_with_prefix(view, prefix, *args, **kwargs))
    This is the algorithm from section 3.1 of RFC 3987, slightly simplified
    since the input is assumed to be a string rather than an arbitrary byte
    stream.
    Take an IRI (string or UTF-8 bytes, e.g. '/I ♥ Django/' or
    b'/I \xe2\x99\xa5 Django/') and return a string containing the encoded
    result with ASCII chars only (e.g. '/I%20%E2%99%A5%20Django/').
    elif isinstance(iri, Promise):
        iri = str(iri)
    return quote(iri, safe="/#%[]=:;$&()+,!?*@'~")
from urllib.parse import quote as urlquote
from django.utils.http import urlencode
from urllib.parse import quote
    key = ':'.join(quote(str(var)) for var in vary_on)
from urllib.parse import quote
    should not be escaped by Python's quote() function. If not provided, the
    return quote(value, **kwargs)
from urllib.parse import quote
from django.utils.http import RFC3986_SUBDELIMS
                    url = quote(candidate_pat % candidate_subs, safe=RFC3986_SUBDELIMS + '/~:@')
from django.utils.encoding import force_bytes
    A legacy compatibility wrapper to Python's urllib.parse.quote() function.
    (was used for unicode handling on Python 2)
    return quote(url, safe)
    A legacy compatibility wrapper to Python's urllib.parse.quote_plus()
    function. (was used for unicode handling on Python 2)
    return quote_plus(url, safe)
    A legacy compatibility wrapper to Python's urllib.parse.unquote() function.
    (was used for unicode handling on Python 2)
    return unquote(quoted_url)
    A legacy compatibility wrapper to Python's urllib.parse.unquote_plus()
    function. (was used for unicode handling on Python 2)
    return unquote_plus(quoted_url)
def urlencode(query, doseq=False):
    A version of Python's urllib.parse.urlencode() function that can operate on
    MultiValueDict and non-string values.
        [(k, [str(i) for i in v] if isinstance(v, (list, tuple)) else str(v))
         for k, v in query],
        doseq
    )
from urllib.parse import unquote
from django.utils.http import is_safe_url
            next = unquote(next)  # HTTP_REFERER may be encoded.
# An alias since Django 2.0
ugettext = gettext
def ngettext(singular, plural, number):
    return _trans.ngettext(singular, plural, number)
# An alias since Django 2.0
ungettext = ngettext
gettext_lazy = ugettext_lazy = lazy(gettext, str)
# An alias since Django 2.0
ungettext_lazy = ngettext_lazy
def gettext(message):
    return message
gettext_noop = gettext_lazy = _ = gettext
    return gettext(message)
    return ngettext(singular, plural, number)
def gettext(message):
    Translate the 'message' string. It uses the current thread to find the
        result = translation_object.gettext(eol_message)
    result = gettext(msg_with_ctxt)
    result = ngettext(*msgs_with_ctxt)
        result = ngettext(singular, plural, number)
class MIMEMixin:
            referer = request.META.get('HTTP_REFERER', '')
                ua = request.META.get('HTTP_USER_AGENT', '<none>')
    if re.search('[^a-zA-Z0-9]', token):
                referer = request.META.get('HTTP_REFERER')
            return token
import ipaddress
def validate_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise ValidationError(_('Enter a valid IPv4 address.'), code='invalid')
import ipaddress
    Clean an IPv6 address string.
    Raise ValidationError if the address is invalid.
    Replace the longest continuous zero-sequence with "::", remove leading
    zeroes, and make sure all hextets are lowercase.
    Return a compressed IPv6 address or the same value.
    try:
        addr = ipaddress.IPv6Address(int(ipaddress.IPv6Address(ip_str)))
    except ValueError:
    if unpack_ipv4 and addr.ipv4_mapped:
        return str(addr.ipv4_mapped)
    elif addr.ipv4_mapped:
        return '::ffff:%s' % str(addr.ipv4_mapped)
    return str(addr)
    try:
        ipaddress.IPv6Address(ip_str)
    except ValueError:
from django.utils.safestring import SafeText
            str(s, encoding, errors)
    return quote(path, safe="/:@&+$,-_.!~*'()")
    Return a string containing the result.
    return quote(path.replace("\\", "/"), safe="/~!*()'")
from django.utils.functional import Promise, wraps
    Kept in Django 2.0 for usage by apps supporting Python 2. Shouldn't be used
    in Django anymore.
    return SafeText(str(s))
    def __str__(self):
        return self
    objects_name = model_ngettext(queryset)
    get_deleted_objects, lookup_needs_distinct, model_format_dict,
    model_ngettext, quote, unquote,
                        'name': model_ngettext(opts, changecount),
from django.utils.functional import Promise, keep_lazy, keep_lazy_text
    if isinstance(text, Promise):
        text = str(text)
            content = templatize(src_data, origin=self.path[2:])
def templatize(src, origin=None):
from django.utils.translation import gettext as _, gettext_lazy
delete_selected.short_description = gettext_lazy("Delete selected %(verbose_name_plural)s")
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext, gettext_lazy as _
                'addText': gettext('Add another %(verbose_name)s') % {
                'deleteText': gettext('Remove'),
from django.utils.translation import gettext, gettext_lazy as _
            return gettext('Added "%(object)s".') % {'object': self.object_repr}
            return gettext('Changed "%(object)s" - %(changes)s') % {
            return gettext('Deleted "%(object)s."') % {'object': self.object_repr}
        return gettext('LogEntry Object')
                        sub_message['added']['name'] = gettext(sub_message['added']['name'])
                        messages.append(gettext('Added {name} "{object}".').format(**sub_message['added']))
                        messages.append(gettext('Added.'))
                        sub_message['changed']['fields'], gettext('and')
                        sub_message['changed']['name'] = gettext(sub_message['changed']['name'])
                        messages.append(gettext('Changed {fields} for {name} "{object}".').format(
                        messages.append(gettext('Changed {fields}.').format(**sub_message['changed']))
                    sub_message['deleted']['name'] = gettext(sub_message['deleted']['name'])
                    messages.append(gettext('Deleted {name} "{object}".').format(**sub_message['deleted']))
            return change_message or gettext('No fields changed.')
from django.utils.translation import gettext as _, ngettext
                    msg = ngettext(
        selection_note_all = ngettext(
from django.utils.translation import gettext as _, gettext_lazy
    site_title = gettext_lazy('Django site admin')
    site_header = gettext_lazy('Django administration')
    index_title = gettext_lazy('Site administration')
from django.utils.translation import gettext as _
from django.utils.translation import ngettext, override as translation_override
    return ngettext(singular, plural, n or 0)
from django.utils.translation import gettext
            title = gettext('Select %s')
            title = gettext('Select %s to change')
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from django.utils.translation import gettext, gettext_lazy as _
                msg = gettext('Password changed successfully.')
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext, gettext_lazy as _
            summary.append({'label': gettext("No password set.")})
                summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
                    summary.append({'label': gettext(key), 'value': value_})
from django.utils.translation import gettext_noop as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _, ngettext
                ngettext(
        return ngettext(
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext, gettext_lazy as _
                gettext("URL is missing a leading slash."),
                gettext("URL is missing a trailing slash."),
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _, ngettext, pgettext
        ngettext('%(value).1f million', '%(value).1f million', number),
        ngettext('%(value)s million', '%(value)s million', number),
        ngettext('%(value).1f billion', '%(value).1f billion', number),
        ngettext('%(value)s billion', '%(value)s billion', number),
        ngettext('%(value).1f trillion', '%(value).1f trillion', number),
        ngettext('%(value)s trillion', '%(value)s trillion', number),
        ngettext('%(value).1f quadrillion', '%(value).1f quadrillion', number),
        ngettext('%(value)s quadrillion', '%(value)s quadrillion', number),
        ngettext('%(value).1f quintillion', '%(value).1f quintillion', number),
        ngettext('%(value)s quintillion', '%(value)s quintillion', number),
        ngettext('%(value).1f sextillion', '%(value).1f sextillion', number),
        ngettext('%(value)s sextillion', '%(value)s sextillion', number),
        ngettext('%(value).1f septillion', '%(value).1f septillion', number),
        ngettext('%(value)s septillion', '%(value)s septillion', number),
        ngettext('%(value).1f octillion', '%(value).1f octillion', number),
        ngettext('%(value)s octillion', '%(value)s octillion', number),
        ngettext('%(value).1f nonillion', '%(value).1f nonillion', number),
        ngettext('%(value)s nonillion', '%(value)s nonillion', number),
        ngettext('%(value).1f decillion', '%(value).1f decillion', number),
        ngettext('%(value)s decillion', '%(value)s decillion', number),
        ngettext('%(value).1f googol', '%(value).1f googol', number),
        ngettext('%(value)s googol', '%(value)s googol', number),
            return ngettext(
            return ngettext(
            return ngettext(
            return ngettext(
            return ngettext(
            return ngettext(
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
            # ngettext calls require a count parameter and are converted
from django.utils.translation import gettext_lazy as _, ngettext_lazy
    message = ngettext_lazy(
    message = ngettext_lazy(
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _, ngettext_lazy
    message = ngettext_lazy(
    message = ngettext_lazy(
        'max_digits': ngettext_lazy(
        'max_decimal_places': ngettext_lazy(
        'max_whole_digits': ngettext_lazy(
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _, ngettext_lazy
        'max_length': ngettext_lazy(
from django.utils.translation import gettext as _
from django.utils.translation import gettext as _, ngettext
                raise ValidationError(ngettext(
                raise ValidationError(ngettext(
from django.utils.translation import gettext, gettext_lazy as _
            return gettext("Please correct the duplicate data for %(field)s.") % {
            return gettext("Please correct the duplicate data for %(field)s, which must be unique.") % {
        return gettext(
        return gettext("Please correct the duplicate values below.")
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
    clear_checkbox_label = _('Clear')
    initial_text = _('Currently')
    input_text = _('Change')
            ('1', _('Unknown')),
            ('2', _('Yes')),
            ('3', _('No')),
from django.utils.translation import gettext_lazy, pgettext_lazy
                return gettext_lazy(msgid)
from django.utils.translation import gettext, ngettext
        arg = gettext('yes,no,maybe')
        value = ngettext("%(size)d byte", "%(size)d bytes", 0) % {'size': 0}
        value = ngettext("%(size)d byte", "%(size)d bytes", bytes_) % {'size': bytes_}
        value = gettext("%s KB") % filesize_number_format(bytes_ / KB)
        value = gettext("%s MB") % filesize_number_format(bytes_ / MB)
        value = gettext("%s GB") % filesize_number_format(bytes_ / GB)
        value = gettext("%s TB") % filesize_number_format(bytes_ / TB)
        value = gettext("%s PB") % filesize_number_format(bytes_ / PB)
        context[self.variable] = [(k, translation.gettext(v)) for k, v in settings.LANGUAGES]
                result = translation.ngettext(singular, plural, count)
                result = translation.gettext(singular)
    return translation.gettext(english_name)
        # translatable string (using gettext_lazy) representing a regular
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _, gettext_lazy, pgettext
def get_text_list(list_, last_word=gettext_lazy('or')):
from django.utils.translation import gettext, ngettext_lazy
    (60 * 60 * 24 * 365, ngettext_lazy('%d year', '%d years')),
    (60 * 60 * 24 * 30, ngettext_lazy('%d month', '%d months')),
    (60 * 60 * 24 * 7, ngettext_lazy('%d week', '%d weeks')),
    (60 * 60 * 24, ngettext_lazy('%d day', '%d days')),
    (60 * 60, ngettext_lazy('%d hour', '%d hours')),
    (60, ngettext_lazy('%d minute', '%d minutes'))
        return avoid_wrapping(gettext('0 minutes'))
            result += gettext(', ') + avoid_wrapping(name2 % count2)
        info['name_translated'] = gettext_lazy(info['name'])
from django.utils.translation import gettext as _
from django.utils.translation import gettext as _
from django.utils.translation import gettext as _
from django.utils.translation import gettext as _
from django.utils.translation import gettext as _
from django.utils.translation import gettext as _, gettext_lazy
template_translatable = gettext_lazy("Index of %(directory)s")
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
    orig = str(value)
from django.utils.encoding import force_bytes
    return b64_encode(salted_hmac(salt, value, key).digest()).decode()
    base64d = b64_encode(data).decode()
        base64d = '.' + base64d
        return base64_hmac(self.salt + 'signer', value, self.key)
            return value
        value = '%s%s%s' % (value, self.sep, self.timestamp())
            message = str(exception.args[0])
            bits.append(str(bit))
        if not issubclass(type(value), str):
            value = str(value)
        return str(value)
from django.utils.encoding import iri_to_uri
            args[0] = str(args[0])
            d = Decimal(str(float(text)))
    return [mark_safe(str(obj)) for obj in value]
                indent, escaper(item), sublist))
        return "Error in formatting: %s: %s" % (e.__class__.__name__, e)
        output = [pformat(val) for val in context]
        output.append(pformat(sys.modules))
        return mark_safe(''.join(nodelist))
        kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
from django.utils.encoding import force_bytes
        return '-'.join(filter(bool, [str(template_name), skip_prefix, dirs_prefix]))
    return str(formats.localize(value, use_l10n=True))
    return str(value)
        return template % (self.connector, ', '.join(str(c) for c in self.children))
    http_version = '1.1'
    protocol_version = 'HTTP/1.1'
        """Handle multiple requests if necessary."""
        self.close_connection = 1
        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()
    def handle_one_request(self):
        """Copy of WSGIRequestHandler.handle() but with different ServerHandler"""
        looks_like_locale = re.compile(r'[a-z]{2}')
        all_locales = [
            lang_code for lang_code in map(os.path.basename, locale_dirs)
            if looks_like_locale.match(lang_code)
        ]
            '/' if settings.FORCE_SCRIPT_NAME is None else settings.FORCE_SCRIPT_NAME
        contents = conditional_escape(self.field.label)
        return format_html('<label{}>{}:</label>', flatatt(attrs), capfirst(label))
                        result_repr = linebreaksbr(value)
            'name': opts.verbose_name,
            'name': opts.verbose_name,
                'name': opts.verbose_name,
                'obj': obj_display,
            'name': opts.verbose_name,
            title=(_('Add %s') if add else _('Change %s')) % opts.verbose_name,
            title=_('Change history: %s') % obj,
        yield format_html('<td>{}</td>', form[cl.model._meta.pk.name])
                yield mark_safe(form[cl.model._meta.pk.name])
from django.utils.encoding import force_text
        no_edit_link = '%s: %s' % (capfirst(opts.verbose_name), obj)
        'verbose_name': opts.verbose_name,
        'verbose_name_plural': opts.verbose_name_plural,
    return help_text
        self.title = title % self.opts.verbose_name
                'name': self.model._meta.verbose_name,
        return unicodedata.normalize('NFKC', username) if username else username
        uid = urlsafe_base64_decode(uidb64).decode()
            uid = urlsafe_base64_decode(uidb64).decode()
                self.log("Pretending to delete '%s'" % fpath, level=1)
                self.log("Deleting '%s'" % fpath, level=1)
                "\n  ".join(finders.searched_locations)
            result = (os.path.realpath(path) for path in result)
from django.utils.encoding import force_bytes
                    hashed_name = self.clean_name(saved_name)
                        hashed_name = self.clean_name(saved_name)
        return self.name or ''
from django.utils.encoding import filepath_to_uri
        return name.replace('\\', '/')
from django.utils.encoding import repercent_broken_unicode
        return settings.FORCE_SCRIPT_NAME
                        (tablename, e))
                    yield "# The error was: %s" % e
                                'error_msg': e,
                error_text = e
            col_name = line[0]
            FieldInfo(*(line[0:6] + (field_map[line.name][0] == 'YES', field_map[line.name][1])))
            for line in cursor.description
        return database_name == ':memory:' or 'mode=memory' in database_name
        param = getattr(self, field.attname)
        return (self.name, path, [], keywords)
            dirname = datetime.datetime.now().strftime(self.upload_to)
                related_name = related_name % {
                related_query_name = self.remote_field.related_query_name % {
        return widget.render(
                    help_text = help_text_html % field.help_text
                    'errors': bf_errors,
                    'label': label,
                    'field': bf,
            output.insert(0, error_row % top_errors)
            format_html_join('', '<li>{}{}</li>', self.items())
            format_html_join('', '<li>{}</li>', ((e,) for e in self))
        return error
    return lazy(str, str)(text)
        result = message
                    'verbose_name_plural': qs.model._meta.verbose_name_plural,
            raise Http404(
                _("No %(verbose_name_plural)s available") % {
                    'verbose_name_plural': queryset.model._meta.verbose_name_plural,
                }
            )
JSON_CONTENT_TYPE_RE = re.compile(r'^application\/(vnd\..+\+)?json')
        context['widget']['href'] = smart_urlquote(context['widget']['value']) if value else ''
        if value == '' or value is None:
            return None
        """Return selected values as a list."""
        return [str(v) if v is not None else '' for v in value]
                content = message_from_string(force_text(content))
from pathlib import Path
# regardless of the project's TEMPLATES setting. Templates are
# read directly from the filesystem so that the error handler
# works even if the template loader is broken.
CURRENT_DIR = Path(__file__).parent
        with Path(CURRENT_DIR, 'templates', 'technical_500.html').open() as fh:
            t = DEBUG_ENGINE.from_string(fh.read())
        with Path(CURRENT_DIR, 'templates', 'technical_500.txt').open() as fh:
            t = DEBUG_ENGINE.from_string(fh.read())
    with Path(CURRENT_DIR, 'templates', 'technical_404.html').open() as fh:
        t = DEBUG_ENGINE.from_string(fh.read())
    with Path(CURRENT_DIR, 'templates', 'default_urlconf.html').open() as fh:
        t = DEBUG_ENGINE.from_string(fh.read())
        if queryset is not None and not issubclass(queryset._iterable_class, ModelIterable):
            "<a href=\"{}\">this form</a>."
        self.fields['password'].help_text = self.fields['password'].help_text.format('../password/')
    import geoip2  # NOQA
except ImportError:
    HAS_GEOIP2 = False
else:
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
        try:
            validate_ipv46_address(query)
        except ValidationError:
                obj_display = str(obj)
        objects_name=str(objects_name),
                'selected': self.value() == str(lookup),
                'selected': self.lookup_val == str(pk_val),
                'selected': str(lookup) == self.lookup_val,
            val = str(val)
            object_id=str(object_id),
        return str(self.action_time)
            object_repr=str(object),
            object_repr=str(object),
        return helpers.checkbox.render(helpers.ACTION_CHECKBOX_NAME, str(obj.pk))
            obj_repr = str(obj)
            module_name=str(opts.verbose_name_plural),
            obj_display = str(obj)
        object_name = str(opts.verbose_name)
            module_name=str(capfirst(opts.verbose_name_plural)),
        if str(result_repr) == '':
                result_repr = mark_safe(str(bf.errors) + str(bf))
            label = str(model._meta.verbose_name)
        return ', '.join(str(v) for v in value)
        return str(value)
                            'name': str(added_object._meta.verbose_name),
                            'object': str(added_object),
                            'name': str(changed_object._meta.verbose_name),
                            'object': str(changed_object),
                            'name': str(deleted_object._meta.verbose_name),
                            'object': str(deleted_object),
        return ','.join(str(v) for v in value) if value else ''
        return str(login_url)
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
        return str([instance._get_pk_val() for instance in qs])
        return str(model._meta.verbose_name)
                key = str(key)
                    val = str(val)
            value = [str(item) for item in value]
        return [str(item) for item in self.rhs]
from django.utils.encoding import force_bytes
                logger.warning(str(e))
                    logger.warning(str(e))
                logger.warning(str(e))
                        logger.warning(str(e))
from django.utils.encoding import iri_to_uri
        return escape(str(item))
        return str(item)
                url=str(enc_url),
                length=str(self._get_dynamic_attr('item_enclosure_length', item)),
                mime_type=str(self._get_dynamic_attr('item_enclosure_mime_type', item)),
            obj = str(self.obj)
                yield str(message)
            str(exc),
    val = str(val)  # val may be lazy
        addr = parseaddr(addr)
        msg['To'] = self.extra_headers.get('To', ', '.join(map(str, self.to)))
            msg['Cc'] = ', '.join(map(str, self.cc))
            msg['Reply-To'] = self.extra_headers.get('Reply-To', ', '.join(map(str, self.reply_to)))
        attrs = OrderedDict([("model", str(obj._meta))])
                attrs['pk'] = str(obj_pk)
                    self.xml.characters(str(key_value))
                self.xml.characters(str(related_att))
                        self.xml.characters(str(key_value))
                        'pk': str(value._get_pk_val())
            ("to", str(field.remote_field.model._meta)),
        if not (self.inverse_match is not bool(self.regex.search(str(value)))):
        return str(x).replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
    return bool(re.search(re_pattern, str(re_string))) if re_string is not None else False
from django.utils.encoding import force_bytes, smart_text
        return str(self.value_from_object(obj))
        return str(value)
            value = str(value)
        return str(value)
            (x._get_pk_val(), str(x)) for x in self.related_model._default_manager.all()
            return str(self.verbose_name)
        auto_id = self.form.auto_id  # Boolean or string
        if auto_id and '%s' in str(auto_id):
            return auto_id % self.html_name
        value = str(value)
            value = int(self.re_decimal.sub('', str(value)))
        value = str(value).strip()
        value = parse_duration(str(value))
        return str(value)
        text_value = str(value)
                    if value == k2 or text_value == str(k2):
                if value == k or text_value == str(k):
        return [str(val) for val in value]
        initial_set = set(str(value) for value in initial)
        data_set = set(str(value) for value in data)
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
                    output.append(error_row % str(bf_errors))
                    label = conditional_escape(bf.label)
        if str(value) != str(orig):
        return str(obj)
        return str(self.prepare_value(initial_value)) != str(data_value)
        pks = set(str(getattr(o, key)) for o in qs)
            if str(val) not in pks:
        initial_set = set(str(value) for value in self.prepare_value(initial))
        data_set = set(str(value) for value in data)
        return str(value)
        return str(value)
                    str(subvalue) in value and
from django.utils.encoding import force_bytes, iri_to_uri
        parsed = urlparse(str(redirect_to))
        to = str(to)
            instance._regex_dict[language_code] = self._compile(str(instance._regex))
        path = str(path)  # path may be a reverse_lazy object
        text_args = [str(v) for v in args]
        text_kwargs = {k: str(v) for (k, v) in kwargs.items()}
        for i, piece in enumerate(re_formatchars.split(str(formatstr))):
                pieces.append(str(getattr(self, piece)()))
        str(text).replace('&', '&amp;').replace('<', '&lt;')
    return mark_safe(str(value).translate(_js_escapes))
    value = normalize_newlines(value)
    paras = re.split('\n{2,}', str(value))
    return x and str(x)[0].upper() + str(x)[1:]
        super().__init__(lambda: str(text))
    s = str(s).strip().replace(' ', '_')
        return str(list_[0])
        _(', ').join(str(i) for i in list_[:-1]), str(last_word), str(list_[-1])
    )
    return re_newlines.sub('\n', str(text))
    for bit in smart_split_re.finditer(str(text)):
    return _entity_re.sub(_replace_entity, str(text))
    value = str(value)
    return ''.join(str(s) for s in strings)
                user_str = str(self.request.user)
            c['exception_value'] = str(self.exc_value)
        template.render(request=request, context={'exception': str(exception)})
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy
from django.utils.encoding import iri_to_uri
            return str(s) if s is not None else s
            categories = [str(c) for c in categories]
            'ttl': to_str(ttl),
            return str(s) if s is not None else s
            'ttl': to_str(ttl),
    return {attr: get_format(attr) for attr in FORMAT_SETTINGS}
    @cached_property
    def context(self):
        return decimal.Context(prec=self.max_digits)
        if isinstance(value, float):
            return self.context.create_decimal_from_float(value)
        self.message = str(self.message)
        self.extra_tags = str(self.extra_tags) if self.extra_tags is not None else None
        return str(self.message)
        return ' '.join(tag for tag in [self.extra_tags, self.level_tag] if tag)
        return LEVEL_TAGS.get(self.level, '')
import re
    @property
    def _num_plurals(self):
        """
        Return the number of plurals for this catalog language, or 2 if no
        plural string is available.
        """
        match = re.search(r'nplurals=\s*(\d+)', self._plural_string or '')
        if match:
            return int(match.groups()[0])
        return 2
    @property
    def _plural_string(self):
        """
        Return the plural string (including nplurals) for this catalog language,
        or None if no plural string is available.
        """
                    return line.split(':', 1)[1].strip()
        return None
    def get_plural(self):
        plural = self._plural_string
        num_plurals = self._num_plurals
                msgid, cnt = key
            catalog[k] = [v.get(i, '') for i in range(num_plurals)]
        seen_keys = set()
            if key == '' or key in seen_keys:
            seen_keys.add(key)
    def __init__(self, base_field, *, delimiter=',', max_length=None, min_length=None, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, base_field, size, *, remove_trailing_nulls=False, **kwargs):
    def __init__(self, *, required=True, widget=None, label=None, initial=None,
    def __init__(self, *, max_length=None, min_length=None, strip=True, empty_value='', **kwargs):
        super().__init__(**kwargs)
    def __init__(self, *, max_value=None, min_value=None, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, *, max_value=None, min_value=None, max_digits=None, decimal_places=None, **kwargs):
        super().__init__(max_value=max_value, min_value=min_value, **kwargs)
    def __init__(self, *, input_formats=None, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, regex, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)
    def __init__(self, *, max_length=None, allow_empty_file=False, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)
    def __init__(self, *, choices=(), **kwargs):
        super().__init__(**kwargs)
    def __init__(self, *, coerce=lambda val: val, empty_value='', **kwargs):
        super().__init__(**kwargs)
    def __init__(self, *, coerce=lambda val: val, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, fields, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, fields, *, require_all_fields=True, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, path, *, match=None, recursive=False, allow_files=True,
                 allow_folders=False, **kwargs):
        super().__init__(choices=(), **kwargs)
    def __init__(self, *, input_date_formats=None, input_time_formats=None, **kwargs):
        super().__init__(fields, **kwargs)
    def __init__(self, *, protocol='both', unpack_ipv4=False, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, *, allow_unicode=False, **kwargs):
        super().__init__(**kwargs)
    def __init__(self, queryset, *, empty_label="---------",
                 **kwargs):
        Field.__init__(
            self, required=required, widget=widget, label=label,
            initial=initial, help_text=help_text, **kwargs
        )
    def __init__(self, queryset, **kwargs):
        super().__init__(queryset, empty_label=None, **kwargs)
from django.utils.encoding import is_protected_type
        data = OrderedDict([('model', str(obj._meta))])
            data["pk"] = self._value_from_field(obj, obj._meta.pk)
    def _value_from_field(self, obj, field):
        return value if is_protected_type(value) else field.value_to_string(obj)
    def handle_field(self, obj, field):
        self._current[field.name] = self._value_from_field(obj, field)
            value = self._value_from_field(obj, field)
                    return self._value_from_field(value, value._meta.pk)
                            return model._meta.pk.to_python(value)
                        return model._meta.pk.to_python(v)
        _, ext = os.path.splitext(name)
        file = tempfile.NamedTemporaryFile(suffix='.upload' + ext, dir=settings.FILE_UPLOAD_TEMP_DIR)
        if len(app_configs) < len(packages):
            excluded = [p for p in packages if p not in allowable_packages]
            raise ValueError(
                'Invalid package(s) provided to JavaScriptCatalog: %s' % ','.join(excluded)
            )
    lib_names = ['gdal202', 'gdal201', 'gdal20', 'gdal111', 'gdal110', 'gdal19']
    lib_names = ['gdal', 'GDAL', 'gdal2.2.0', 'gdal2.1.0', 'gdal2.0.0', 'gdal1.11.0', 'gdal1.10.0', 'gdal1.9.0']
    INNER, LOUTER, ORDER_DIR, ORDER_PATTERN, SINGLE,
    elif isinstance(message, SafeData):
        result = mark_safe(result)
    def _create_index_sql(self, model, fields, **kwargs):
            return super()._create_index_sql(model, fields, **kwargs)
    def create_sql(self, model, schema_editor, using=''):
        statement = super().create_sql(model, schema_editor, using=' USING brin')
            statement.parts['extra'] = ' WITH (pages_per_range={})'.format(
                schema_editor.quote_value(self.pages_per_range)
            ) + statement.parts['extra']
        return statement
    def create_sql(self, model, schema_editor, using=''):
        statement = super().create_sql(model, schema_editor, using=' USING gin')
            statement.parts['extra'] = 'WITH ({}) {}'.format(', '.join(with_params), statement.parts['extra'])
        return statement
    def _create_index_sql(self, model, fields, *, name=None, suffix='', using='',
                          db_tablespace=None, col_suffixes=(), sql=None):
        tablespace_sql = self._get_index_tablespace_sql(model, fields, db_tablespace=db_tablespace)
            nonlocal name
            if name is None:
                name = self._create_index_name(*args, **kwargs)
            return self.quote_name(name)
            using=using,
            columns=Columns(table, columns, self.quote_name, col_suffixes=col_suffixes),
    def __init__(self, table, columns, quote_name, col_suffixes=()):
        self.col_suffixes = col_suffixes
        def col_str(column, idx):
            try:
                return self.quote_name(column) + self.col_suffixes[idx]
            except IndexError:
                return self.quote_name(column)
        return ', '.join(col_str(column, idx) for idx, column in enumerate(self.columns))
        fields = [model._meta.get_field(field_name) for field_name, _ in self.fields_orders]
        col_suffixes = [order[1] for order in self.fields_orders]
        return schema_editor._create_index_sql(
            model, fields, name=self.name, using=using, db_tablespace=self.db_tablespace,
            col_suffixes=col_suffixes,
        )
        return [
            force_text(
                capi.get_field_name(capi.get_field_defn(self._layer._ldefn, i)),
                self.encoding,
                strings_only=True
            ) for i in range(self.num_fields)
        ]
    if isinstance(value, tuple):
        value = str(value)
    def load_middleware(self):
        # Middleware are already loaded for self.application; no need to reload
        # them for self.
        pass
            if conn.vendor == 'postgresql':
                conn.introspection.data_types_reverse.update({
                    3802: 'django.contrib.postgresql.fields.JSONField',
                })
                if conn.connection is not None:
                    register_type_handlers(conn)
                    3904: 'django.contrib.postgresql.fields.IntegerRangeField',
                    3906: 'django.contrib.postgresql.fields.FloatRangeField',
                    3910: 'django.contrib.postgresql.fields.DateTimeRangeField',
                    3912: 'django.contrib.postgresql.fields.DateRangeField',
                    3926: 'django.contrib.postgresql.fields.BigIntegerRangeField',
            # Try to interpret values containg a period or an 'e'/'E'
            # (possibly scientific notation) as a float;  otherwise, try int.
            if '.' in var or 'e' in var.lower():
                self.literal = float(var)
                # "2." is invalid
                if var.endswith('.'):
                    raise ValueError
            else:
                self.literal = int(var)
        return str(value)
    return str(formats.localize(value, use_l10n=False))
            'has_file_field': context['adminform'].form.is_multipart() or any(
                admin_formset.formset.form().is_multipart()
                for admin_formset in context['inline_admin_formsets']
            ),
    # Force newlines of POT files to '\n' to work around
    # https://savannah.gnu.org/bugs/index.php?52395
    with open(potfile, 'a', encoding='utf-8', newline='\n') as fp:
    ('kab', gettext_noop('Kabyle')),
    python_reloader(wrapped_main_func, args, kwargs)
    Redirect to a given URL while setting the chosen language in the session
    (if enabled) and in a cookie. The URL and the language code need to be
    specified in the request parameters.
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
            )
        self.connection.ensure_connection()
        quoted = self.connection.connection.escape(value, self.connection.connection.encoders)
        if isinstance(value, str):
            quoted = quoted.decode()
        return quoted
        if value is None and self.allow_multiple_selected:
            return []
            if hasattr(self.widget, 'deserialize'):
                value = self.widget.deserialize(value)
            else:
                try:
                    value = GEOSGeometry(value)
                except (GEOSException, ValueError, TypeError):
                    value = None
            if value is None:
from django.contrib.gis.geometry import json_regex
        except (GEOSException, ValueError, TypeError) as err:
    def deserialize(self, value):
        geom = super().deserialize(value)
        # GeoJSON assumes WGS84 (4326). Use the map's SRID instead.
        if geom and json_regex.match(value) and self.map_srid != 4326:
            geom.srid = self.map_srid
        return geom
            self.log("Linking '%s'" % source_path, level=2)
            self.log("Copying '%s'" % source_path, level=2)
from django.core.handlers.exception import response_for_exception
                return response_for_exception(request, e)
            # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
            return _('%(delta)s ago') % {'delta': defaultfilters.timesince(value, now)}
            # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
            return _('%(delta)s from now') % {'delta': defaultfilters.timeuntil(value, now)}
                'https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.css',
            'https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.js',
The Lexer.tokenize() method converts a template string (i.e., a string
containing markup with custom template tags) to tokens, which can be either
plain text (TokenType.TEXT), variables (TokenType.VAR), or block statements
(TokenType.BLOCK).
from enum import Enum
class TokenType(Enum):
    TEXT = 0
    VAR = 1
    BLOCK = 2
    COMMENT = 3
            A TokenType, either .TEXT, .VAR, .BLOCK, or .COMMENT.
        token_name = self.token_type.name.capitalize()
                return Token(TokenType.VAR, token_string[2:-2].strip(), position, lineno)
                return Token(TokenType.BLOCK, block_content, position, lineno)
                return Token(TokenType.COMMENT, content, position, lineno)
            return Token(TokenType.TEXT, token_string, position, lineno)
            # Use the raw values here for TokenType.* for a tiny performance boost.
            if token.token_type.value == 0:  # TokenType.TEXT
            elif token.token_type.value == 1:  # TokenType.VAR
            elif token.token_type.value == 2:  # TokenType.BLOCK
            if token.token_type == TokenType.BLOCK and token.contents == endtag:
from django.template.base import TokenType, render_value_in_context
            if token.token_type == TokenType.TEXT:
            elif token.token_type == TokenType.VAR:
        if token.token_type in (TokenType.VAR, TokenType.TEXT):
            if token.token_type in (TokenType.VAR, TokenType.TEXT):
from django.template.base import TRANSLATOR_COMMENT_MARK, Lexer, TokenType
            if t.token_type == TokenType.BLOCK and t.contents == 'endcomment':
            if t.token_type == TokenType.BLOCK:
            elif t.token_type == TokenType.VAR:
            elif t.token_type == TokenType.TEXT:
                    if t.token_type != TokenType.COMMENT:
            if t.token_type == TokenType.BLOCK:
            elif t.token_type == TokenType.VAR:
            elif t.token_type == TokenType.COMMENT:
import mimetypes
import os
from urllib.parse import quote, urlparse
    def __init__(self, *args, as_attachment=False, filename='', **kwargs):
        self.as_attachment = as_attachment
        self.filename = filename
        super().__init__(*args, **kwargs)
        if not hasattr(value, 'read'):
            return super()._set_streaming_content(value)
        self.file_to_stream = filelike = value
        if hasattr(filelike, 'close'):
            self._closable_objects.append(filelike)
        value = iter(lambda: filelike.read(self.block_size), b'')
        self.set_headers(filelike)
    def set_headers(self, filelike):
        """
        Set some common response headers (Content-Length, Content-Type, and
        Content-Disposition) based on the `filelike` response content.
        """
        encoding_map = {
            'bzip2': 'application/x-bzip',
            'gzip': 'application/gzip',
            'xz': 'application/x-xz',
        }
        filename = getattr(filelike, 'name', None)
        filename = filename if (isinstance(filename, str) and filename) else self.filename
        if os.path.isabs(filename):
            self['Content-Length'] = os.path.getsize(filelike.name)
        elif hasattr(filelike, 'getbuffer'):
            self['Content-Length'] = filelike.getbuffer().nbytes
        if self.get('Content-Type', '').startswith(settings.DEFAULT_CONTENT_TYPE):
            if filename:
                content_type, encoding = mimetypes.guess_type(filename)
                # Encoding isn't set to prevent browsers from automatically
                # uncompressing files.
                content_type = encoding_map.get(encoding, content_type)
                self['Content-Type'] = content_type or 'application/octet-stream'
            else:
                self['Content-Type'] = 'application/octet-stream'
        if self.as_attachment:
            filename = self.filename or os.path.basename(filename)
            if filename:
                try:
                    filename.encode('ascii')
                    file_expr = 'filename="{}"'.format(filename)
                except UnicodeEncodeError:
                    file_expr = "filename*=utf-8''{}".format(quote(filename))
                self['Content-Disposition'] = 'attachment; {}'.format(file_expr)
from django.contrib.contenttypes.management import create_contenttypes
    # Ensure that contenttypes are created for this app. Needed if
    # 'django.contrib.auth' is in INSTALLED_APPS before
    # 'django.contrib.contenttypes'.
    create_contenttypes(app_config, verbosity=verbosity, interactive=interactive, using=using, apps=apps, **kwargs)
from argparse import ArgumentParser, HelpFormatter
class DjangoHelpFormatter(HelpFormatter):
    """
    Customized formatter so that command-specific arguments appear in the
    --help output before arguments common to all commands.
    """
    show_last = {
        '--version', '--verbosity', '--traceback', '--settings', '--pythonpath',
        '--no-color',
    }
    def _reordered_actions(self, actions):
        return sorted(
            actions,
            key=lambda a: set(a.option_strings) & self.show_last != set()
        )
    def add_usage(self, usage, actions, *args, **kwargs):
        super().add_usage(usage, self._reordered_actions(actions), *args, **kwargs)
    def add_arguments(self, actions):
        super().add_arguments(self._reordered_actions(actions))
            formatter_class=DjangoHelpFormatter,
        self.add_arguments(parser)
    gettext as _, gettext_lazy, ngettext, ngettext_lazy, npgettext_lazy,
    pgettext,
    return NaturalTimeFormatter.string_for(value)
class NaturalTimeFormatter:
    time_strings = {
        # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
        'past-day': gettext_lazy('%(delta)s ago'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'past-hour': ngettext_lazy('an hour ago', '%(count)s hours ago', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'past-minute': ngettext_lazy('a minute ago', '%(count)s minutes ago', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'past-second': ngettext_lazy('a second ago', '%(count)s seconds ago', 'count'),
        'now': gettext_lazy('now'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'future-second': ngettext_lazy('a second from now', '%(count)s seconds from now', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'future-minute': ngettext_lazy('a minute from now', '%(count)s minutes from now', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'future-hour': ngettext_lazy('an hour from now', '%(count)s hours from now', 'count'),
        # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
        'future-day': gettext_lazy('%(delta)s from now'),
    }
    past_substrings = {
        # Translators: 'naturaltime-past' strings will be included in '%(delta)s ago'
        'year': npgettext_lazy('naturaltime-past', '%d year', '%d years'),
        'month': npgettext_lazy('naturaltime-past', '%d month', '%d months'),
        'week': npgettext_lazy('naturaltime-past', '%d week', '%d weeks'),
        'day': npgettext_lazy('naturaltime-past', '%d day', '%d days'),
        'hour': npgettext_lazy('naturaltime-past', '%d hour', '%d hours'),
        'minute': npgettext_lazy('naturaltime-past', '%d minute', '%d minutes'),
    }
    future_substrings = {
        # Translators: 'naturaltime-future' strings will be included in '%(delta)s from now'
        'year': npgettext_lazy('naturaltime-future', '%d year', '%d years'),
        'month': npgettext_lazy('naturaltime-future', '%d month', '%d months'),
        'week': npgettext_lazy('naturaltime-future', '%d week', '%d weeks'),
        'day': npgettext_lazy('naturaltime-future', '%d day', '%d days'),
        'hour': npgettext_lazy('naturaltime-future', '%d hour', '%d hours'),
        'minute': npgettext_lazy('naturaltime-future', '%d minute', '%d minutes'),
    }
    @classmethod
    def string_for(cls, value):
        if not isinstance(value, date):  # datetime is a subclass of date
            return value
        now = datetime.now(utc if is_aware(value) else None)
        if value < now:
            delta = now - value
            if delta.days != 0:
                return cls.time_strings['past-day'] % {
                    'delta': defaultfilters.timesince(value, now, time_strings=cls.past_substrings),
                }
            elif delta.seconds == 0:
                return cls.time_strings['now']
            elif delta.seconds < 60:
                return cls.time_strings['past-second'] % {'count': delta.seconds}
            elif delta.seconds // 60 < 60:
                count = delta.seconds // 60
                return cls.time_strings['past-minute'] % {'count': count}
            else:
                count = delta.seconds // 60 // 60
                return cls.time_strings['past-hour'] % {'count': count}
            delta = value - now
            if delta.days != 0:
                return cls.time_strings['future-day'] % {
                    'delta': defaultfilters.timeuntil(value, now, time_strings=cls.future_substrings),
                }
            elif delta.seconds == 0:
                return cls.time_strings['now']
            elif delta.seconds < 60:
                return cls.time_strings['future-second'] % {'count': delta.seconds}
            elif delta.seconds // 60 < 60:
                count = delta.seconds // 60
                return cls.time_strings['future-minute'] % {'count': count}
            else:
                count = delta.seconds // 60 // 60
                return cls.time_strings['future-hour'] % {'count': count}
        self.lib_spatialite_paths = [name for name in [
            getattr(settings, 'SPATIALITE_LIBRARY_PATH', None),
            'mod_spatialite.so',
            'mod_spatialite',
            find_library('spatialite'),
        ] if name is not None]
        for path in self.lib_spatialite_paths:
            try:
                conn.load_extension(path)
            except Exception:
                if getattr(settings, 'SPATIALITE_LIBRARY_PATH', None):
                    raise ImproperlyConfigured(
                        'Unable to load the SpatiaLite library extension '
                        'as specified in your SPATIALITE_LIBRARY_PATH setting.'
                    )
                continue
            else:
                break
        else:
                'Unable to load the SpatiaLite library extension. '
                'Library names tried: %s' % ', '.join(self.lib_spatialite_paths)
            )
        self.has_errors = False
        if self.has_errors:
            raise CommandError('compilemessages generated one or more errors.')
                self.stderr.write(
                    'The %s file has a BOM (Byte Order Mark). Django only '
                    'supports .po files encoded in UTF-8 and without any BOM.' % po_path
                )
                self.has_errors = True
                continue
                self.stderr.write(
                    'The po files under %s are in a seemingly not writable location. '
                    'mo files will not be updated/created.' % dirpath
                )
                self.has_errors = True
                    self.stderr.write('Execution of %s failed: %s.' % (self.program, errors))
                    self.stderr.write('Execution of %s failed.' % self.program)
                self.has_errors = True
import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i, (dirpath, f) in enumerate(locations):
                if self.verbosity > 0:
                    self.stdout.write('processing file %s in %s\n' % (f, dirpath))
                po_path = os.path.join(dirpath, f)
                if has_bom(po_path):
                    self.stderr.write(
                        'The %s file has a BOM (Byte Order Mark). Django only '
                        'supports .po files encoded in UTF-8 and without any BOM.' % po_path
                    )
                    self.has_errors = True
                    continue
                base_path = os.path.splitext(po_path)[0]
                # Check writability on first location
                if i == 0 and not is_writable(base_path + '.mo'):
                    self.stderr.write(
                        'The po files under %s are in a seemingly not writable location. '
                        'mo files will not be updated/created.' % dirpath
                    )
                    self.has_errors = True
                    return
                args = [self.program] + self.program_options + [
                    '-o', base_path + '.mo', base_path + '.po'
                ]
                futures.append(executor.submit(popen_wrapper, args))
            for future in concurrent.futures.as_completed(futures):
                output, errors, status = future.result()
                if status:
                    if self.verbosity > 0:
                        if errors:
                            self.stderr.write("Execution of %s failed: %s" % (self.program, errors))
                        else:
                            self.stderr.write("Execution of %s failed" % self.program)
                    self.has_errors = True
        has_bad_labels = False
            except LookupError as err:
                self.stderr.write(str(err))
                has_bad_labels = True
        if has_bad_labels:
        if options['app_label']:
            # Validate app_label.
            app_label = options['app_label']
            try:
                apps.get_app_config(app_label)
            except LookupError as err:
                raise CommandError(str(err))
                raise CommandError("App '%s' does not have migrations." % app_label)
        if options['app_label'] and options['migration_name']:
            migration_name = options['migration_name']
from django.apps import apps
        # Validate app_label.
        try:
            apps.get_app_config(app_label)
        except LookupError as err:
            raise CommandError(str(err))
            '--database',
            '--database',
                '--%s' % field,
            '--database', default=DEFAULT_DB_ALIAS,
            '--blank',
            '--decimal',
            '--geom-name', default='geom',
            '--multi-geom', action='store_true',
            '--name-field',
            '--null', action=ListOptionAction, default=False,
            '--srid',
            '--mapping', action='store_true',
        parser.add_argument('sitemap_url', nargs='?')
            '-n', '--dry-run', action='store_true',
            '-c', '--clear', action='store_true',
            '-l', '--link', action='store_true',
            '-v', '--verbosity', default=1,
            '--no-color', action='store_true',
            '--list-tags', action='store_true',
            '--deploy', action='store_true',
            '--locale', '-l', action='append', default=[],
            '--exclude', '-x', action='append', default=[],
            '--database',
            '--dry-run', action='store_true',
            '--database', default=DEFAULT_DB_ALIAS,
            '--all', action='store_true',
            '--default', metavar='MODULE',
            '--output', default='hash', choices=('hash', 'unified'),
            '--format', default='json',
            '--indent', type=int,
            '--database',
            '-e', '--exclude', action='append', default=[],
            '-o', '--output',
            '--database', default=DEFAULT_DB_ALIAS,
            'table', nargs='*', type=str,
            '--database', default=DEFAULT_DB_ALIAS,
            '--database', default=DEFAULT_DB_ALIAS,
            '--app', dest='app_label',
            '-e', '--exclude', action='append', default=[],
            '--format',
            '--locale', '-l', default=[], action='append',
            '--exclude', '-x', default=[], action='append',
            '--domain', '-d', default='django',
            '--all', '-a', action='store_true',
            '--symlinks', '-s', action='store_true',
            '--no-wrap', action='store_true',
            '--no-location', action='store_true',
            '--add-location',
            '--no-obsolete', action='store_true',
            '--keep-pot', action='store_true',
            '--dry-run', action='store_true',
            '--merge', action='store_true',
            '--empty', action='store_true',
            '-n', '--name',
            '--database',
            '--fake', action='store_true',
            '--fake-initial', action='store_true',
            '--run-syncdb', action='store_true',
            '--managers', action='store_true',
            '--admins', action='store_true',
            '--no-startup', action='store_true',
            '-i', '--interface', choices=self.shells,
            '-c', '--command',
            '--database', default=DEFAULT_DB_ALIAS,
            '--backwards', action='store_true',
            'start_migration_name', nargs='?',
            '--no-optimize', action='store_true',
            '--squashed-name',
            '-t', '--top-level-directory', dest='top_level',
            '-p', '--pattern', default="test*.py",
            '-k', '--keepdb', action='store_true',
            '-r', '--reverse', action='store_true',
            '--debug-mode', action='store_true',
            '-d', '--debug-sql', action='store_true',
            '--parallel', nargs='?', default=1, type=int,
        # Supported with MyISAM/Aria, or InnoDB on MySQL 5.7.5+/MariaDB 10.2.2+
        if storage_engine == 'InnoDB':
            return self.connection.mysql_version >= (
                (10, 2, 2) if self.connection.mysql_is_mariadb else (5, 7, 5)
            )
        return storage_engine in ('MyISAM', 'Aria')
        MBREquals = 'MBREqual' if (
            self.connection.mysql_is_mariadb or self.connection.mysql_version < (5, 7, 6)
        ) else 'MBREquals'
        if self.connection.mysql_is_mariadb:
            unsupported.update({'GeoHash', 'IsValid'})
            if self.connection.mysql_version < (10, 2, 4):
                unsupported.add('AsGeoJSON')
        elif self.connection.mysql_version < (5, 7, 5):
        force_grouping=force_grouping,
        use_l10n=use_l10n,
           force_grouping=False, use_l10n=None):
    use_grouping = (use_l10n or (use_l10n is None and settings.USE_L10N)) and settings.USE_THOUSAND_SEPARATOR
import os
    def log(self, msg):
        sys.stderr.write(msg + os.linesep)
            self.log('%s test database for alias %s...' % (
                self.log('Got an error creating the test database: %s' % e)
                            self.log('Destroying old test database for alias %s...' % (
                        self.log('Got an error recreating the test database: %s' % e)
                    self.log('Tests cancelled.')
            self.log('%s for alias %s...' % (
            self.log('%s test database for alias %s...' % (
                self.log('Got an error creating the test database: %s' % e)
                        self.log('Destroying old test database for alias %s...' % (
                    self.log('Got an error recreating the test database: %s' % e)
                        self.log('Got an error creating the test database: %s' % e)
                            self.log("Destroying old test database for alias '%s'..." % self.connection.alias)
                                self.log('Got an error destroying the old test database: %s' % e)
                            self.log('Got an error destroying the old test database: %s' % e)
                            self.log('Got an error recreating the test database: %s' % e)
                        self.log('Tests cancelled.')
                    self.log('Creating test user...')
                        self.log('Got an error creating the test user: %s' % e)
                                self.log('Destroying old test user...')
                                self.log('Creating test user...')
                            self.log('Got an error recreating the test user: %s' % e)
                        self.log('Tests cancelled.')
        self.log(
            'There are objects in the old test database which prevent its destruction.\n'
            'If they belong to the test user, deleting the user will allow the test '
            'database to be recreated.\n'
            'Otherwise, you will need to find and remove each of these objects, '
            'or use a different tablespace.\n'
        )
                        self.log('Destroying old test user...')
                    self.log('Got an error destroying the test user: %s' % e)
                        self.log("Destroying old test database for alias '%s'..." % self.connection.alias)
                    self.log('Got an error destroying the test database: %s' % e)
                self.log('Tests cancelled -- test database cannot be recreated.')
            self.log("Django is configured to use pre-existing test user '%s',"
                     " and will not attempt to delete it." % parameters['user'])
            self.log('Tests cancelled -- test database cannot be recreated.')
                    self.log('Destroying test user...')
                    self.log('Destroying test database tables...')
            self.log('_create_test_db(): dbname = %s' % parameters['user'])
            self.log('_create_test_user(): username = %s' % parameters['user'])
            self.log('Failed to grant CREATE VIEW permission to test user. This may be ok.')
            self.log('_execute_test_db_destruction(): dbname=%s' % parameters['user'])
            self.log('_destroy_test_user(): user=%s' % parameters['user'])
            self.log('Be patient.  This can take some time...')
                    self.log('Failed (%s)' % (err))
                self.log('Got an error creating the test database: %s' % e)
                        self.log('Destroying old test database for alias %s...' % (
                    self.log('Got an error cloning the test database: %s' % e)
                self.log('Destroying old test database for alias %s...' % (
                        self.log('Got an error deleting the old test database: %s' % e)
                    self.log('Tests cancelled.')
                    self.log('Destroying old test database for alias %s...' % (
                    self.log('Got an error deleting the old test database: %s' % e)
                self.log('Got an error cloning the test database: %s' % e)
from django.utils.functional import SimpleLazyObject, keep_lazy_text, lazy
@keep_lazy_text
    return re.sub(r'[-\s]+', '-', value)
            return forms.Media(js=['admin/js/collapse%s.js' % extra])
    class Media:
            'admin/js/calendar.js',
            'admin/js/admin/DateTimeShortcuts.js',
    class Media:
            'admin/js/calendar.js',
            'admin/js/admin/DateTimeShortcuts.js',
from urllib.parse import urlsplit
    elif not settings.DEBUG or urlsplit(prefix).netloc:
        return Truncator(obj).words(14), url
    return Truncator(value).words(length, truncate=' …')
    return Truncator(value).words(length, html=True, truncate=' …')
    than this limit to trim_url_limit - 1 characters and append an ellipsis.
        return '%s…' % x[:max(0, limit - 1)]
                '%(truncated_text)s…')
        been truncated, defaulting to a translatable string of an ellipsis.
        defaulting to ellipsis.
        return '… '
                    stream.write('Processed %d features, saved %d …\n' % (num_feat, num_saved))
            self.stdout.write("Loading '%s' fixtures…" % fixture_name)
                self.stdout.write("Checking %s for fixtures…" % humanize(fixture_dir))
                self.stdout.write("  Applying %s…" % migration, ending="")
                self.stdout.write("  Unapplying %s…" % migration, ending="")
                self.stdout.write("  Rendering model states…", ending="")
            self.stdout.write("  Creating tables…\n")
                self.stdout.write("    Running deferred SQL…\n")
        self.stdout.write("Performing system checks…\n\n")
                return " … (%s)" % ", ".join(out)
                self.stdout.write(self.style.MIGRATE_HEADING("Optimizing…"))
            self.log('%s test database for alias %s…' % (
                            self.log('Destroying old test database for alias %s…' % (
                        self.log('Destroying old test database for alias %s…' % (
                            self.log("Destroying old test database for alias '%s'…" % self.connection.alias)
                    self.log('Creating test user…')
                                self.log('Destroying old test user…')
                                self.log('Creating test user…')
                        self.log('Destroying old test user…')
                        self.log("Destroying old test database for alias '%s'…" % self.connection.alias)
                    self.log('Destroying test user…')
                    self.log('Destroying test database tables…')
            self.log('Be patient. This can take some time…')
                        self.log('Destroying old test database for alias %s…' % (
                self.log('Destroying old test database for alias %s…' % (
                    self.log('Destroying old test database for alias %s…' % (
            data[-1] = "…(remaining elements truncated)…"
                raise ValueError("When merging querysets using 'or', you cannot have extra(select=…) on both sides.")
                        v = '%s… <trimmed %d bytes string>' % (v[0:4096], len(v))
    SEARCH_TYPES = {
        'plain': 'plainto_tsquery',
        'phrase': 'phraseto_tsquery',
        'raw': 'to_tsquery',
    }
    def __init__(self, value, output_field=None, *, config=None, invert=False, search_type='plain'):
        if search_type not in self.SEARCH_TYPES:
            raise ValueError("Unknown search_type argument '%s'." % search_type)
        self.search_type = search_type
        function = self.SEARCH_TYPES[self.search_type]
            template = '{}({}::regconfig, %s)'.format(function, config_sql)
            template = '{}(%s)'.format(function)
    @cached_property
    def is_postgresql_9_6(self):
        return self.connection.pg_version >= 90600
    has_phraseto_tsquery = is_postgresql_9_6
    # How many second decimals does the database return when casting a value to
    # a type with time?
    time_cast_precision = 6
    time_cast_precision = 3
    def as_sqlite(self, compiler, connection, **extra_context):
        db_type = self.output_field.db_type(connection)
        if db_type in {'datetime', 'time'}:
            # Use strftime as datetime/time don't keep fractional seconds.
            template = 'strftime(%%s, %(expressions)s)'
            sql, params = super().as_sql(compiler, connection, template=template, **extra_context)
            format_string = '%H:%M:%f' if db_type == 'time' else '%Y-%m-%d %H:%M:%f'
            params.insert(0, format_string)
            return sql, params
        elif db_type == 'date':
            template = 'date(%(expressions)s)'
            return super().as_sql(compiler, connection, template=template, **extra_context)
        return self.as_sql(compiler, connection, **extra_context)
    geos_version = geos_version_tuple()
        if self.geos_version < (3, 6, 1) and isinstance(geom, Polygon) and geom.empty:
        if self.geos_version < (3, 6, 1) and isinstance(geom, Polygon) and geom.empty:
from django.contrib.gis.gdal import GDALException
                try:
                    value = self.widget.deserialize(value)
                except GDALException:
                    value = None
    ('hy', gettext_noop('Armenian')),
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
            'contains': SpatialOperator(func='ST_Contains'),
            'crosses': SpatialOperator(func='ST_Crosses'),
            'disjoint': SpatialOperator(func='ST_Disjoint'),
            'equals': SpatialOperator(func='ST_Equals'),
            'exact': SpatialOperator(func='ST_Equals'),
            'intersects': SpatialOperator(func='ST_Intersects'),
            'overlaps': SpatialOperator(func='ST_Overlaps'),
            'same_as': SpatialOperator(func='ST_Equals'),
            'touches': SpatialOperator(func='ST_Touches'),
            'within': SpatialOperator(func='ST_Within'),
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.translation import LANGUAGE_SESSION_KEY
        if key == LANGUAGE_SESSION_KEY:
            warnings.warn(
                'The user language will no longer be stored in '
                'request.session in Django 4.0. Read it from '
                'request.COOKIES[settings.LANGUAGE_COOKIE_NAME] instead.',
                RemovedInDjango40Warning, stacklevel=2,
            )
from . import to_language, to_locale
    if lang_code is not None and lang_code in get_languages() and check_for_language(lang_code):
        return lang_code
                # Storing the language in the session is deprecated.
                # (RemovedInDjango40Warning)
        srid = self.srid
            if srid is not None:
                self.srid = srid
            srid = self.srid
            if srid is not None:
                self.srid = srid
from pathlib import Path
def to_path(value):
    """Convert value to a pathlib.Path instance, if not already a Path."""
    if isinstance(value, Path):
        return value
    elif not isinstance(value, str):
        raise TypeError('Invalid path type: %s' % type(value).__name__)
    return Path(value)
from django.utils._os import to_path
        path = to_path(path)
SECURE_CONTENT_TYPE_NOSNIFF = True
            dirname = datetime.datetime.now().strftime(str(self.upload_to))
            subprocess.run(cmd.split())
from subprocess import PIPE, run
        p = run(args, stdout=PIPE, stderr=PIPE, close_fds=os.name != 'nt')
        p.stdout.decode(stdout_encoding),
        p.stderr.decode(DEFAULT_LOCALE_ENCODING, errors='replace'),
        subprocess.run(args, check=True)
        subprocess.run(args, check=True)
        subprocess.run(args, check=True)
        p = subprocess.run(args, env=new_environ, close_fds=False)
        if p.returncode != 3:
            return p.returncode
    git_log = subprocess.run(
    timestamp = git_log.stdout
X_FRAME_OPTIONS = 'DENY'
    "Unless there is a good reason for your site to serve other parts of "
    "itself in a frame, you should change it to 'DENY'.",
        the X_FRAME_OPTIONS setting, or 'DENY' if not set.
        return getattr(settings, 'X_FRAME_OPTIONS', 'DENY').upper()
    ('uz', gettext_noop('Uzbek')),
from django.utils.dateparse import parse_datetime, parse_duration
        try:
            result = parse_datetime(value.strip())
        except ValueError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        if not result:
            result = super().to_python(value)
class DateTimeFormatsIterator:
    def __iter__(self):
        yield from formats.get_format('DATETIME_INPUT_FORMATS')
        yield from formats.get_format('DATE_INPUT_FORMATS')
    input_formats = DateTimeFormatsIterator()
from .multipartparser import parse_header
    @cached_property
    def accepted_types(self):
        """Return a list of MediaType instances."""
        return parse_accept_header(self.headers.get('Accept', '*/*'))
    def accepts(self, media_type):
        return any(
            accepted_type.match(media_type)
            for accepted_type in self.accepted_types
        )
class MediaType:
    def __init__(self, media_type_raw_line):
        full_type, self.params = parse_header(
            media_type_raw_line.encode('ascii') if media_type_raw_line else b''
        )
        self.main_type, _, self.sub_type = full_type.partition('/')
    def __str__(self):
        params_str = ''.join(
            '; %s=%s' % (k, v.decode('ascii'))
            for k, v in self.params.items()
        )
        return '%s%s%s' % (
            self.main_type,
            ('/%s' % self.sub_type) if self.sub_type else '',
            params_str,
        )
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__qualname__, self)
    @property
    def is_all_types(self):
        return self.main_type == '*' and self.sub_type == '*'
    def match(self, other):
        if self.is_all_types:
            return True
        other = MediaType(other)
        if self.main_type == other.main_type and self.sub_type in {'*', other.sub_type}:
            return True
        return False
def parse_accept_header(header):
    return [MediaType(token) for token in header.split(',') if token.strip()]
    if request.accepts('text/html'):
    else:
        text = reporter.get_traceback_text()
        return HttpResponse(text, status=status_code, content_type='text/plain; charset=utf-8')
        (next_url or request.accepts('text/html')) and
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
        warnings.warn(
            'request.is_ajax() is deprecated. See Django 3.1 release notes '
            'for more details about this deprecation.',
            RemovedInDjango40Warning,
        )
class InvalidAlgorithm(ValueError):
    """Algorithm is not supported by hashlib."""
    pass
def salted_hmac(key_salt, value, secret=None, *, algorithm='sha1'):
    Return the HMAC of 'value', using a key generated from key_salt and a
    secret (which defaults to settings.SECRET_KEY). Default algorithm is SHA1,
    but any algorithm name supported by hashlib.new() can be passed.
    try:
        hasher = getattr(hashlib, algorithm)
    except AttributeError as e:
        raise InvalidAlgorithm(
            '%r is not an algorithm accepted by the hashlib module.'
            % algorithm
        ) from e
    # passing the key_salt and our base key through a pseudo-random function.
    key = hasher(key_salt + secret).digest()
    return hmac.new(key, msg=force_bytes(value), digestmod=hasher)
    key_salt = 'django.contrib.messages'
        return salted_hmac(self.key_salt, value).hexdigest()
from django.core import signing
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signer = signing.get_cookie_signer(salt=self.key_salt)
    def _legacy_hash(self, value):
        # RemovedInDjango40Warning: pre-Django 3.1 hashes will be invalid.
            return self.signer.sign(value)
        try:
            decoded = self.signer.unsign(data)
        except signing.BadSignature:
            # RemovedInDjango40Warning: when the deprecation ends, replace
            # with:
            #   decoded = None.
            decoded = self._legacy_decode(data)
        if decoded:
            try:
                return json.loads(decoded, cls=MessageDecoder)
            except json.JSONDecodeError:
                pass
    def _legacy_decode(self, data):
        # RemovedInDjango40Warning: pre-Django 3.1 hashes will be invalid.
        bits = data.split('$', 1)
        if len(bits) == 2:
            hash_, value = bits
            if constant_time_compare(hash_, self._legacy_hash(value)):
                return value
        return None
    algorithm = 'sha256'
            # RemovedInDjango40Warning: when the deprecation ends, replace
            # with:
            #   return False
            if not constant_time_compare(
                self._make_token_with_timestamp(user, ts, legacy=True),
                token,
            ):
                return False
    def _make_token_with_timestamp(self, user, timestamp, legacy=False):
            # RemovedInDjango40Warning: when the deprecation ends, remove the
            # legacy argument and replace with:
            #   algorithm=self.algorithm,
            algorithm='sha1' if legacy else self.algorithm,
from django.core import signing
    @property
    def key_salt(self):
        return 'django.contrib.sessions.' + self.__class__.__qualname__
        # RemovedInDjango40Warning: pre-Django 3.1 format will be invalid.
        return signing.dumps(
            session_dict, salt=self.key_salt, serializer=self.serializer,
            compress=True,
        )
        try:
            return signing.loads(session_data, salt=self.key_salt, serializer=self.serializer)
        # RemovedInDjango40Warning: when the deprecation ends, handle here
        # exceptions similar to what _legacy_decode() does now.
        except Exception:
            return self._legacy_decode(session_data)
    def _legacy_decode(self, session_data):
        # RemovedInDjango40Warning: pre-Django 3.1 format will be invalid.
class TranslationCatalog:
    """
    Simulate a dict for DjangoTranslation._catalog so as multiple catalogs
    with different plural equations are kept separate.
    """
    def __init__(self, trans=None):
        self._catalogs = [trans._catalog.copy()] if trans else [{}]
        self._plurals = [trans.plural] if trans else [lambda n: int(n != 1)]
    def __getitem__(self, key):
        for cat in self._catalogs:
            try:
                return cat[key]
            except KeyError:
                pass
        raise KeyError(key)
    def __setitem__(self, key, value):
        self._catalogs[0][key] = value
    def __contains__(self, key):
        return any(key in cat for cat in self._catalogs)
    def items(self):
        for cat in self._catalogs:
            yield from cat.items()
    def keys(self):
        for cat in self._catalogs:
            yield from cat.keys()
    def update(self, trans):
        # Merge if plural function is the same, else prepend.
        for cat, plural in zip(self._catalogs, self._plurals):
            if trans.plural.__code__ == plural.__code__:
                cat.update(trans._catalog)
                break
        else:
            self._catalogs.insert(0, trans._catalog)
            self._plurals.insert(0, trans.plural)
    def get(self, key, default=None):
        missing = object()
        for cat in self._catalogs:
            result = cat.get(key, missing)
            if result is not missing:
                return result
        return default
    def plural(self, msgid, num):
        for cat, plural in zip(self._catalogs, self._plurals):
            tmsg = cat.get((msgid, plural(num)))
            if tmsg is not None:
                return tmsg
        raise KeyError
            self._catalog = TranslationCatalog()
            self._catalog = TranslationCatalog(other)
            self._catalog.update(other)
    def ngettext(self, msgid1, msgid2, n):
        try:
            tmsg = self._catalog.plural(msgid1, n)
        except KeyError:
            if self._fallback:
                return self._fallback.ngettext(msgid1, msgid2, n)
            if n == 1:
                tmsg = msgid1
            else:
                tmsg = msgid2
        return tmsg
        # 12 returns a 71-bit value, log_2((26+26+10)^12) =~ 71 bits
        return get_random_string(12)
            password = get_random_string(30)
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
NOT_PROVIDED = object()  # RemovedInDjango40Warning.
# RemovedInDjango40Warning: when the deprecation ends, replace with:
#   def get_random_string(self, length, allowed_chars='...'):
def get_random_string(length=NOT_PROVIDED, allowed_chars=(
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)):
    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)
    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    if length is NOT_PROVIDED:
        warnings.warn(
            'Not providing a length argument is deprecated.',
            RemovedInDjango40Warning,
        )
        length = 12
def base64_hmac(salt, value, key, algorithm='sha1'):
    return b64_encode(salted_hmac(salt, value, key, algorithm=algorithm).digest()).decode()
    Return URL-safe, hmac signed base64 compressed JSON string. If key is
    None, use settings.SECRET_KEY instead. The hmac algorithm is the default
    Signer algorithm.
    # RemovedInDjango40Warning.
    legacy_algorithm = 'sha1'
    def __init__(self, key=None, sep=':', salt=None, algorithm='sha256'):
        self.algorithm = algorithm
        return base64_hmac(self.salt + 'signer', value, self.key, algorithm=self.algorithm)
    def _legacy_signature(self, value):
        # RemovedInDjango40Warning.
        return base64_hmac(self.salt + 'signer', value, self.key, algorithm=self.legacy_algorithm)
        if (
            constant_time_compare(sig, self.signature(value)) or (
                self.legacy_algorithm and
                constant_time_compare(sig, self._legacy_signature(value))
            )
        ):
from django.contrib.gis.gdal.srs import (
    AxisOrder, CoordTransform, SpatialReference,
)
    'AxisOrder', 'Driver', 'DataSource', 'CoordTransform', 'Envelope',
    'GDALException', 'GDALRaster', 'GDAL_VERSION', 'OGRGeometry',
    'OGRGeomType', 'SpatialReference', 'SRSException', 'check_err',
    'gdal_version', 'gdal_full_version',
from django.contrib.gis.gdal.libgdal import GDAL_VERSION, lgdal, std_call
if GDAL_VERSION >= (3, 0):
    set_axis_strategy = void_output(lgdal.OSRSetAxisMappingStrategy, [c_void_p, c_int])
from enum import IntEnum
from django.contrib.gis.gdal.libgdal import GDAL_VERSION
class AxisOrder(IntEnum):
    TRADITIONAL = 0
    AUTHORITY = 1
    def __init__(self, srs_input='', srs_type='user', axis_order=None):
        if not isinstance(axis_order, (type(None), AxisOrder)):
            raise ValueError(
                'SpatialReference.axis_order must be an AxisOrder instance.'
            )
        self.axis_order = axis_order or AxisOrder.TRADITIONAL
            if self.axis_order == AxisOrder.TRADITIONAL and GDAL_VERSION >= (3, 0):
                capi.set_axis_strategy(self.ptr, self.axis_order)
            elif self.axis_order != AxisOrder.TRADITIONAL and GDAL_VERSION < (3, 0):
                raise ValueError('%s is not supported in GDAL < 3.0.' % self.axis_order)
        if self.axis_order == AxisOrder.TRADITIONAL and GDAL_VERSION >= (3, 0):
            capi.set_axis_strategy(self.ptr, self.axis_order)
        elif self.axis_order != AxisOrder.TRADITIONAL and GDAL_VERSION < (3, 0):
            raise ValueError('%s is not supported in GDAL < 3.0.' % self.axis_order)
        return SpatialReference(capi.clone_srs(self.ptr), axis_order=self.axis_order)
            except (gdal.GDALException, gdal.SRSException):
        """Return the version of the PROJ library used with PostGIS."""
        Return the version of PROJ used by PostGIS as a tuple of the
            raise Exception('Could not determine PROJ version from PostGIS.')
    def proj_version(self):
        """Return the version of the PROJ library used by SpatiaLite."""
        WKT or PROJ, and/or an integer SRID.  By default, return nothing
# For exporting to WKT, PROJ, "Pretty" WKT, and XML.
        EPSG code, a PROJ string, and/or a projection "well known" shorthand
        """Import the Spatial Reference from a PROJ string."""
        """Return the PROJ representation for this Spatial Reference."""
        PROJ string. By default, transform the geometry in-place and return
    ('ky', gettext_noop('Kyrgyz')),
            m2m_iter = getattr(obj, '_prefetched_objects_cache', {}).get(
                field.name,
                getattr(obj, field.name).iterator(),
            )
            self._current[field.name] = [m2m_value(related) for related in m2m_iter]
            m2m_iter = getattr(obj, '_prefetched_objects_cache', {}).get(
                field.name,
                getattr(obj, field.name).iterator(),
            )
            for relobj in m2m_iter:
    if use_l10n:
            return number_format(value, use_l10n=True, force_grouping=True)
    (6, lambda number: ngettext('%(value)s million', '%(value)s million', number)),
    (9, lambda number: ngettext('%(value)s billion', '%(value)s billion', number)),
    (12, lambda number: ngettext('%(value)s trillion', '%(value)s trillion', number)),
    (15, lambda number: ngettext('%(value)s quadrillion', '%(value)s quadrillion', number)),
    (18, lambda number: ngettext('%(value)s quintillion', '%(value)s quintillion', number)),
    (21, lambda number: ngettext('%(value)s sextillion', '%(value)s sextillion', number)),
    (24, lambda number: ngettext('%(value)s septillion', '%(value)s septillion', number)),
    (27, lambda number: ngettext('%(value)s octillion', '%(value)s octillion', number)),
    (30, lambda number: ngettext('%(value)s nonillion', '%(value)s nonillion', number)),
    (33, lambda number: ngettext('%(value)s decillion', '%(value)s decillion', number)),
    (100, lambda number: ngettext('%(value)s googol', '%(value)s googol', number)),
    for exponent, converter in intword_converters:
            return converter(abs(rounded_value)) % {
                'value': defaultfilters.floatformat(new_value, 1),
            }
        if use_l10n is False:
            return str(value)
    ('tg', gettext_noop('Tajik')),
from pathlib import Path
    with fn.open('rb') as f:
                po_path = Path(dirpath) / f
                mo_path = po_path.with_suffix('.mo')
                if i == 0 and not is_writable(mo_path):
                args = [self.program, *self.program_options, '-o', mo_path, po_path]
                try:
                    if mo_path.stat().st_mtime >= po_path.stat().st_mtime:
                        if self.verbosity > 0:
                            self.stdout.write(
                                'File “%s” is already compiled and up to date.'
                                % po_path
                            )
                        continue
                except FileNotFoundError:
                    pass
                if self.verbosity > 0:
                    self.stdout.write('processing file %s in %s' % (f, dirpath))
    if settings.USE_I18N:
        is_accept_language_redundant = settings.USE_I18N
        # If i18n is used, the generated cache key will be suffixed with the
        # current locale. Adding the raw value of Accept-Language is redundant
        # in that case and would result in storing the same content under
        # multiple keys in the cache. See #18191 for details.
            else:
'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});
    const v = {{ plural }};
    if (typeof v === 'boolean') {
  const newcatalog = {{ catalog_str }};
  for (const key in newcatalog) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return (typeof value === 'string') ? value : value[0];
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
      let value = django.gettext(context + '\x04' + msgid);
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
};
        # Accessing errors triggers a full clean the first time only.
        # List comprehension ensures is_valid() is called for all forms.
        # Forms due to be deleted shouldn't cause the formset to be invalid.
        forms_valid = all([
            form.is_valid() for form in self.forms
            if not (self.can_delete and self._should_delete_form(form))
        ])
    # List comprehension ensures is_valid() is called for all formsets.
    return all([formset.is_valid() for formset in formsets])
    lang, _, country = language.lower().partition('-')
        return language[:3].lower() + language[3:]
    return lang + '_' + country
    lib_names = [
        'gdal302', 'gdal301', 'gdal300',
        'gdal204', 'gdal203', 'gdal202', 'gdal201', 'gdal20',
    ]
        'gdal3.2.0', 'gdal3.1.0', 'gdal3.0.0',
from django.contrib.gis.gdal.libgdal import std_call
get_ds_info = const_string_output(std_call('GDALInfo'), [c_void_p, c_void_p])
delete_band_nodata_value = void_output(std_call('GDALDeleteRasterNoDataValue'), [c_void_p])
                if self.ops.spatial_version < (5,):
                    cursor.execute('SELECT InitSpatialMetaData(1)')
                else:
                    cursor.execute('SELECT InitSpatialMetaDataFull(1)')
        return bool(self.connection.ops.geom_lib_version())
        if not self.geom_lib_version():
    def rttopo_version(self):
        """Return the version of RTTOPO library used by SpatiaLite."""
        return self._get_spatialite_func('rttopo_version()')
    def geom_lib_version(self):
        """
        Return the version of the version-dependant geom library used by
        SpatiaLite.
        """
        if self.spatial_version >= (5,):
            return self.rttopo_version()
        else:
            return self.lwgeom_version()
        'year': npgettext_lazy('naturaltime-past', '%(num)d year', '%(num)d years', 'num'),
        'month': npgettext_lazy('naturaltime-past', '%(num)d month', '%(num)d months', 'num'),
        'week': npgettext_lazy('naturaltime-past', '%(num)d week', '%(num)d weeks', 'num'),
        'day': npgettext_lazy('naturaltime-past', '%(num)d day', '%(num)d days', 'num'),
        'hour': npgettext_lazy('naturaltime-past', '%(num)d hour', '%(num)d hours', 'num'),
        'minute': npgettext_lazy('naturaltime-past', '%(num)d minute', '%(num)d minutes', 'num'),
        'year': npgettext_lazy('naturaltime-future', '%(num)d year', '%(num)d years', 'num'),
        'month': npgettext_lazy('naturaltime-future', '%(num)d month', '%(num)d months', 'num'),
        'week': npgettext_lazy('naturaltime-future', '%(num)d week', '%(num)d weeks', 'num'),
        'day': npgettext_lazy('naturaltime-future', '%(num)d day', '%(num)d days', 'num'),
        'hour': npgettext_lazy('naturaltime-future', '%(num)d hour', '%(num)d hours', 'num'),
        'minute': npgettext_lazy('naturaltime-future', '%(num)d minute', '%(num)d minutes', 'num'),
    'year': ngettext_lazy('%(num)d year', '%(num)d years', 'num'),
    'month': ngettext_lazy('%(num)d month', '%(num)d months', 'num'),
    'week': ngettext_lazy('%(num)d week', '%(num)d weeks', 'num'),
    'day': ngettext_lazy('%(num)d day', '%(num)d days', 'num'),
    'hour': ngettext_lazy('%(num)d hour', '%(num)d hours', 'num'),
    'minute': ngettext_lazy('%(num)d minute', '%(num)d minutes', 'num'),
        return avoid_wrapping(time_strings['minute'] % {'num': 0})
        return avoid_wrapping(time_strings['minute'] % {'num': 0})
        result.append(avoid_wrapping(time_strings[name] % {'num': count}))
import warnings
from django.utils.deprecation import RemovedInDjango50Warning
        if self.USE_TZ is False and not self.is_overridden('USE_TZ'):
            warnings.warn(
                'The default value of USE_TZ will change from False to True '
                'in Django 5.0. Set USE_TZ to False in your project settings '
                'if you want to keep the current default behavior.',
                category=RemovedInDjango50Warning,
            )
