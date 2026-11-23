# Lignes ajoutees par un contributeur de github.com/django/django (BSD-3-Clause)
# Extraites par experiments/construire_corpus.py — regle et provenance : corpus/devs/PROVENANCE.md
                FieldInfo(*(
                    (col_name,) +
                    line[1:3] +
                    (
                        to_int(field_info[col_name].max_len) or line[3],
                        to_int(field_info[col_name].num_prec) or line[4],
                        to_int(field_info[col_name].num_scale) or line[5],
                        line[6],
                        field_info[col_name].extra,
                        field_info[col_name].column_default,
                    )
                ))
            if (field_type.startswith('varchar') and field.unique and
                    (field.max_length is None or int(field.max_length) > 255)):
            " NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'" +
            (" TIME_ZONE = 'UTC'" if settings.USE_TZ else '')
        )
        do_offset = with_limits and (self.query.high_mark is not None or self.query.low_mark)
        return [
            FieldInfo(*(
                (force_text(line[0]),) +
                line[1:6] +
                (field_map[force_text(line[0])][0] == 'YES', field_map[force_text(line[0])][1])
            )) for line in cursor.description
        ]
                    (isinstance(self.__class__.__dict__.get(field.attname), DeferredAttribute) or
                        field.column is None)):
            if (field and getattr(self, parent._meta.pk.attname) is None and
                    getattr(self, field.attname) is not None):
            if f.db_column is None and column_name is not None and len(column_name) > allowed_len:
                if m2m.db_column is None and rel_name is not None and len(rel_name) > allowed_len:
        if (signals.pre_delete.has_listeners(model) or
                signals.post_delete.has_listeners(model) or
                signals.m2m_changed.has_listeners(model)):
                ((lhs_output and lhs_output.get_internal_type() == 'DurationField') or
                 (rhs_output and rhs_output.get_internal_type() == 'DurationField'))):
        if lookup_type in ('gte', 'lt') and isinstance(value, float):
            (self.width_field and not getattr(instance, self.width_field)) or
            (self.height_field and not getattr(instance, self.height_field))
        if (hasattr(self.rhs, 'get_compiler') or hasattr(self.rhs, 'as_sql') or
                hasattr(self.rhs, '_as_sql') or self.bilateral_transforms):
            (f for f in self._get_fields(reverse=False)
            if is_not_an_m2m_field(f) and is_not_a_generic_relation(f) and
            is_not_a_generic_foreign_key(f))
            if (connection.features.can_combine_inserts_with_and_without_auto_increment_pk and
                    self.model._meta.has_auto_field):
            parent_louter = parent_alias and self.alias_map[parent_alias].join_type == LOUTER
                    if self.alias_map[join].parent_alias == alias and join not in aliases
                )
                names = sorted(list(get_field_names_from_opts(opts)) + list(self.extra) + list(self.annotation_select))
        if connections[DEFAULT_DB_ALIAS].features.interprets_empty_strings_as_nulls and field.empty_strings_allowed:
                if (form.cleaned_data and form.cleaned_data[field] is not None and
                        form.cleaned_data[unique_for] is not None):
                    pk.remote_field and pk.remote_field.parent_link and
                    pk_is_not_editable(pk.remote_field.model._meta.pk)
            if isinstance(f, ForeignKey) and (
                f.remote_field.model == parent_model or
                f.remote_field.model in parent_model._meta.get_parent_list()
            )
                not is_valid_path(request.path_info, urlconf) and
                is_valid_path('%s/' % request.path_info, urlconf)
                    settings.APPEND_SLASH and not language_path.endswith('/') and
                    is_valid_path('%s/' % language_path, urlconf)
        return len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'")
        return len(s) >= 3 and s[0] == 'u' and s[1] == s[-1] and s[1] in ('"', "'")
        if '/' in path and (('\\' in path and path.find('/') < path.find('\\')) or '\\' not in path):
    should_convert = (
        isinstance(value, datetime) and
        (settings.USE_TZ if use_tz is None else use_tz) and
        not is_naive(value) and
        getattr(value, 'convert_to_local_time', True)
    )
        if self.__language == settings.LANGUAGE_CODE and self.domain == 'django' and self._catalog is None:
            if (isinstance(data, Node) and not data.negated and
                    (data.connector == conn_type or len(data) == 1)):
            if (current_frame.f_code.co_name == 'sensitive_variables_wrapper' and
                    'sensitive_variables_wrapper' in current_frame.f_locals):
        if (tb_frame.f_code.co_name == 'sensitive_variables_wrapper' and
                'sensitive_variables_wrapper' in tb_frame.f_locals):
        if (not tried or (                  # empty URLconf
            request.path == '/' and
            len(tried) == 1 and             # default URLconf
            len(tried[0]) == 1 and
            getattr(tried[0][0], 'app_name', '') == getattr(tried[0][0], 'namespace', '') == 'admin'
        )):
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
__all__ = ['A', 'Area', 'D', 'Distance']
from .client import DatabaseClient                          # NOQA isort:skip
from .creation import DatabaseCreation                      # NOQA isort:skip
from .features import DatabaseFeatures                      # NOQA isort:skip
from .introspection import DatabaseIntrospection            # NOQA isort:skip
from .operations import DatabaseOperations                  # NOQA isort:skip
from .schema import DatabaseSchemaEditor                    # NOQA isort:skip
from .utils import Oracle_datetime, convert_unicode         # NOQA isort:skip
from .client import DatabaseClient                          # NOQA isort:skip
from .creation import DatabaseCreation                      # NOQA isort:skip
from .features import DatabaseFeatures                      # NOQA isort:skip
from .introspection import DatabaseIntrospection            # NOQA isort:skip
from .operations import DatabaseOperations                  # NOQA isort:skip
from .schema import DatabaseSchemaEditor                    # NOQA isort:skip
from .utils import utc_tzinfo_factory                       # NOQA isort:skip
from .version import get_version                            # NOQA isort:skip
import math
class IntegerFieldFloatRounding(object):
    """
    Allow floats to work as query values for IntegerField. Without this, the
    decimal portion of the float would always be discarded.
    """
    def get_prep_lookup(self):
        if isinstance(self.rhs, float):
            self.rhs = math.ceil(self.rhs)
        return super(IntegerFieldFloatRounding, self).get_prep_lookup()
class IntegerGreaterThanOrEqual(IntegerFieldFloatRounding, GreaterThanOrEqual):
    pass
IntegerField.register_lookup(IntegerGreaterThanOrEqual)
class IntegerLessThan(IntegerFieldFloatRounding, LessThan):
    pass
IntegerField.register_lookup(IntegerLessThan)
                "Key '%s' not found in '%s'. Choices are: %s." % (
                    name,
                    self.__class__.__name__,
                    ', '.join(sorted(f for f in self.fields)),
                )
            )
    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH):
        return (blank_choice if include_blank else []) + [
            (x._get_pk_val(), smart_text(x)) for x in self.related_model._default_manager.all()
        ]
                if not field.remote_field.parent_link:
                    warnings.warn(
                        'Add parent_link=True to %s as an implicit link is '
                        'deprecated.' % field, RemovedInDjango20Warning
                    )
from django.db.models.query_utils import Q
            value = force_text(self.format_value(value))
from django.utils.deprecation import (
    RemovedInDjango20Warning, RenameMethodsBase,
)
class RenameWidgetMethods(MediaDefiningClass, RenameMethodsBase):
    renamed_methods = (
        ('_format_value', 'format_value', RemovedInDjango20Warning),
    )
class Widget(six.with_metaclass(RenameWidgetMethods)):
    def format_value(self, value):
            final_attrs['value'] = force_text(self.format_value(value))
    def format_value(self, value):
def conditional_content_removal(request, response):
    """
    Simulate the behavior of most Web servers by removing the content of
    responses for HEAD requests, 1xx, 204, and 304 responses. Ensures
    compliance with RFC 2616, section 4.3.
    """
    if 100 <= response.status_code < 200 or response.status_code in (204, 304):
        if response.streaming:
            response.streaming_content = []
        else:
            response.content = b''
        response['Content-Length'] = '0'
    if request.method == 'HEAD':
        if response.streaming:
            response.streaming_content = []
        else:
            response.content = b''
    return response
        # Simulate behaviors of most Web servers.
        conditional_content_removal(request, response)
from django.utils.encoding import force_text
from django.db.models.query_utils import RegisterLookupMixin
        if lookup_type in ('exact', 'gt', 'gte', 'lt', 'lte'):
from django.utils.formats import get_format
    for attr in FORMAT_SETTINGS:
        result[attr] = get_format(attr)
Python API (https://geoip2.readthedocs.io/). This is an alternative to the
    def subwidgets(self, name, value, attrs=None):
        for widget in self.get_renderer(name, value, attrs):
    def get_renderer(self, name, value, attrs=None):
        return self.renderer(name, value, final_attrs, self.choices)
    def render(self, name, value, attrs=None):
        return self.get_renderer(name, value, attrs).render()
from django.utils.six.moves.urllib.parse import urljoin, urlparse, urlsplit
            # Prepend the request path to handle relative path redirects
            path = url.path
            if not path.startswith('/'):
                path = urljoin(response.request['PATH_INFO'], path)
            response = self.get(path, QueryDict(url.query), follow=False, **extra)
        return [value]
            _, params = self.get_db_prep_lookup(rhs, connection)
class FieldGetDbPrepValueMixin(object):
    """
    Some lookups require Field.get_db_prep_value() to be called on their
    inputs.
    """
    get_db_prep_lookup_value_is_iterable = False
    def get_db_prep_lookup(self, value, connection):
        # For relational fields, use the output_field of the 'field' attribute.
        field = getattr(self.lhs.output_field, 'field', None)
        get_db_prep_value = getattr(field, 'get_db_prep_value', None)
        if not get_db_prep_value:
            get_db_prep_value = self.lhs.output_field.get_db_prep_value
        return (
            '%s',
            [get_db_prep_value(v, connection, prepared=True) for v in value]
            if self.get_db_prep_lookup_value_is_iterable else
            [get_db_prep_value(value, connection, prepared=True)]
        )
class FieldGetDbPrepValueIterableMixin(FieldGetDbPrepValueMixin):
    """
    Some lookups require Field.get_db_prep_value() to be called on each value
    in an iterable.
    """
    get_db_prep_lookup_value_is_iterable = True
class Exact(FieldGetDbPrepValueMixin, BuiltinLookup):
class GreaterThan(FieldGetDbPrepValueMixin, BuiltinLookup):
class GreaterThanOrEqual(FieldGetDbPrepValueMixin, BuiltinLookup):
class LessThan(FieldGetDbPrepValueMixin, BuiltinLookup):
class LessThanOrEqual(FieldGetDbPrepValueMixin, BuiltinLookup):
class In(FieldGetDbPrepValueIterableMixin, BuiltinLookup):
class Range(FieldGetDbPrepValueIterableMixin, BuiltinLookup):
    def _get_db_prep_lookup(self, lookup_type, value, connection):
        Only used by the deprecated GeoQuerySet and to be
        RemovedInDjango20Warning.
        # Populating the parameters list, and wrapping the Geometry
        # with the Adapter of the spatial backend.
        if isinstance(value, (tuple, list)):
            params = [connection.ops.Adapter(value[0])]
            # Getting the distance parameter in the units of the field.
            params += self.get_distance(value[1:], lookup_type, connection)
            params = [connection.ops.Adapter(value)]
        return params
            params = geo_field._get_db_prep_lookup('contains', geom, connection=connection)
        # The field's _get_db_prep_lookup() is used to get any
        params = geo_field._get_db_prep_lookup('distance_lte', lookup_params, connection=connection)
            return QueryDict(encoding=self._encoding), MultiValueDict()
        self._post = QueryDict(mutable=True)
        self._post = QueryDict()
            self._post, self._files = QueryDict(encoding=self._encoding), MultiValueDict()
            self._post, self._files = QueryDict(encoding=self._encoding), MultiValueDict()
                >>> q = QueryDict(mutable=True)
from django.utils import six
    if isinstance(cls().is_anonymous, six.types.MethodType):
        errors.append(
            checks.Critical(
                '%s.is_anonymous must be an attribute or property rather than '
                'a method. Ignoring this is a security issue as anonymous '
                'users will be treated as authenticated!' % cls,
                obj=cls,
                id='auth.C009',
            )
        )
    if isinstance(cls().is_authenticated, six.types.MethodType):
        errors.append(
            checks.Critical(
                '%s.is_authenticated must be an attribute or property rather '
                'than a method. Ignoring this is a security issue as anonymous '
                'users will be treated as authenticated!' % cls,
                obj=cls,
                id='auth.C010',
            )
        )
        content_type = META.get('CONTENT_TYPE', '')
            content_length = int(META.get('CONTENT_LENGTH', 0))
    See https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
    for documentation of Python string formatting.
    if context.autoescape or isinstance(value, EscapeData):
import warnings
        escape_isnt_last_filter = True
                with warnings.catch_warnings():
                    # Ignore mark_for_escaping deprecation as this will be
                    # removed in Django 2.0.
                    warnings.simplefilter('ignore', category=RemovedInDjango20Warning)
                    obj = mark_for_escaping(new_obj)
                    escape_isnt_last_filter = False
        if not escape_isnt_last_filter:
            warnings.warn(
                "escape isn't the last filter in %s and will be applied "
                "immediately in Django 2.0 so the output may change."
                % [func.__name__ for func, _ in self.filters],
                RemovedInDjango20Warning, stacklevel=2
            )
import warnings
from django.utils.deprecation import RemovedInDjango20Warning
    with warnings.catch_warnings():
        # Ignore mark_for_escaping deprecation -- this will use
        # conditional_escape() in Django 2.0.
        warnings.simplefilter('ignore', category=RemovedInDjango20Warning)
        return mark_for_escaping(value)
import warnings
from django.utils.deprecation import RemovedInDjango20Warning
    warnings.warn('mark_for_escaping() is deprecated.', RemovedInDjango20Warning)
        qs = getattr(obj, self.attname).all()
        if qs._result_cache is not None:
            return [item.pk for item in qs]
        return list(qs.values_list('pk', flat=True))
        data[f.name] = f.value_from_object(instance)
                not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
                inserted_id = self._insert(item, fields=fields, using=self.db, return_id=True)
                self._insert(item, fields=fields, using=self.db)
            warnings.warn(
                "Old-style middleware using settings.MIDDLEWARE_CLASSES is "
                "deprecated. Update your middleware and use settings.MIDDLEWARE "
                "instead.", RemovedInDjango20Warning
            )
import django.core.checks.compatibility.django_1_10  # NOQA isort:skip
from __future__ import unicode_literals
from django.conf import global_settings, settings
from .. import Tags, Warning, register
@register(Tags.compatibility)
def check_duplicate_middleware_settings(app_configs, **kwargs):
    if settings.MIDDLEWARE is not None and settings.MIDDLEWARE_CLASSES != global_settings.MIDDLEWARE_CLASSES:
        return [Warning(
            "The MIDDLEWARE_CLASSES setting is deprecated in Django 1.10 "
            "and the MIDDLEWARE setting takes precedence. Since you've set "
            "MIDDLEWARE, the value of MIDDLEWARE_CLASSES is ignored.",
            id='1_10.W001',
        )]
    return []
VERSION = (1, 11, 0, 'alpha', 0)
    iterations = 36000
    @cached_property
    def is_mysql_5_5(self):
        return self.connection.mysql_version < (5, 6, 1)
    @cached_property
    def is_mysql_5_6(self):
        return self.connection.mysql_version < (5, 7, 6)
        if self.is_mysql_5_5:
        if self.is_mysql_5_5:
        if self.is_mysql_5_5:
    @cached_property
    def gis_operators(self):
        MBREquals = 'MBREqual' if self.is_mysql_5_6 else 'MBREquals'
        return {
            'bbcontains': SpatialOperator(func='MBRContains'),  # For consistency w/PostGIS API
            'bboverlaps': SpatialOperator(func='MBROverlaps'),  # ...
            'contained': SpatialOperator(func='MBRWithin'),  # ...
            'contains': SpatialOperator(func='MBRContains'),
            'disjoint': SpatialOperator(func='MBRDisjoint'),
            'equals': SpatialOperator(func=MBREquals),
            'exact': SpatialOperator(func=MBREquals),
            'intersects': SpatialOperator(func='MBRIntersects'),
            'overlaps': SpatialOperator(func='MBROverlaps'),
            'same_as': SpatialOperator(func=MBREquals),
            'touches': SpatialOperator(func='MBRTouches'),
            'within': SpatialOperator(func='MBRWithin'),
        }
            'Area': 'Area' if self.is_mysql_5_5 else 'ST_Area',
            'Centroid': 'Centroid' if self.is_mysql_5_5 else 'ST_Centroid',
            'Envelope': 'Envelope' if self.is_mysql_5_5 else 'ST_Envelope',
            'Length': 'GLength' if self.is_mysql_5_5 else 'ST_Length',
            'NumGeometries': 'NumGeometries' if self.is_mysql_5_5 else 'ST_NumGeometries',
            'NumPoints': 'NumPoints' if self.is_mysql_5_5 else 'ST_NumPoints',
        if self.is_mysql_5_5:
        if obj.pk is None:
            return []
class RemovedInDjango20Warning(DeprecationWarning):
class RemovedInDjango21Warning(PendingDeprecationWarning):
RemovedInNextVersionWarning = RemovedInDjango20Warning
    Clean up urlpattern regexes into something more readable by humans. For
    example, turn "^(?P<sport_slug>\w+)/athletes/(?P<athlete_slug>\w+)/$"
    into "/<sport_slug>/athletes/<athlete_slug>/".
            cursor.execute('SELECT coord_dimension, srid, geometry_type '
                           'WHERE f_table_name=%s AND f_geometry_column=%s',
from django.db import models
    type = models.IntegerField(db_column='geometry_type')
    srtext = models.CharField(max_length=2048)
            'Translate': 'ST_Translate',
        if not self.lwgeom_version():
        if version < (4, 0, 0):
            raise ImproperlyConfigured('GeoDjango only supports SpatiaLite versions 4.0.0 and above.')
                    'GeoDjango requires at least PostGIS version 2.1. '
            try:
                value_list.append(getattr(value, source.attname))
            except AttributeError:
                # A case like Restaurant.objects.filter(place=restaurant_instance),
                # where place is a OneToOneField and the primary key of Restaurant.
                return (value.pk,)
        - ``value`` is the ``parent`` instance on the right of the equal sign
        - ``value`` is the ``restaurant`` instance on the right of the equal sign
        - ``cls`` is the ``Parent`` class (unused)
        - ``value`` is the ``children`` sequence on the right of the equal sign
                except Exception as e:
                    msg = e
                except Exception as e:
                    msg = e
            ModelState.from_model(apps.get_model(*model)) for model in model_keys
    from_text = 'SDO_GEOMETRY'
        return '%s(%%s, %s)' % (connection.ops.from_text, self.srid), [connection.ops.Adapter(self.value)]
    def as_postgresql(self, compiler, connection):
    def _get_file(self):
            self._file = self.storage.open(self.name, 'rb')
        self._require_file()
        self.file.open(mode)
        choice = list(self.choices)[idx]  # Let the IndexError propagate
        self._lazy_method(
            super(ModelSignal, self).connect, apps, receiver, sender,
            weak=weak, dispatch_uid=dispatch_uid,
        )
    def reverse(self, lookup_view, *args, **kwargs):
        return self._reverse_with_prefix(lookup_view, '', *args, **kwargs)
    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))
    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', force_text(username))
        username = self.model.normalize_username(username)
        if self.field.name in instance.__dict__:
            file = instance.__dict__[self.field.name]
        else:
            instance.refresh_from_db(fields=[self.field.name])
            file = getattr(instance, self.field.name)
        # Nothing to update if the field doesn't have dimension fields or if
        # the field is deferred.
        if not has_dimension_fields or self.attname not in instance.__dict__:
      s.textContent = s.textContent == uarr ? darr : uarr;
      link.textContent = link.textContent.trim() == s1 ? s2: s1;
            if field.disabled:
                value = self.initial.get(name, field.initial)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
        value = self.prepare_value(value)
    def _get_set_deprecation_msg_params(self):
        return (  # RemovedInDjango20Warning
            'reverse side of a related set',
            self.rel.get_accessor_name(),
        )
            'Direct assignment to the %s is deprecated due to the implicit '
            'save() that happens. Use %s.set() instead.' % self._get_set_deprecation_msg_params(),
            RemovedInDjango20Warning, stacklevel=2,
    def _get_set_deprecation_msg_params(self):
        return (  # RemovedInDjango20Warning
            '%s side of a many-to-many set' % ('reverse' if self.reverse else 'forward'),
            self.rel.get_accessor_name() if self.reverse else self.field.name,
        )
            connection = connections[db]
            if connection.settings_dict['ENGINE'] != 'django.db.backends.dummy':
                loader.check_consistent_history(connection)
            result = cursor.fetchone()
            return result and result[0] == 1
    def __eq__(self, other):
        return self.value == other
    def __ne__(self, other):
        return self.value != other
                    int(self.META.get('CONTENT_LENGTH') or 0) > settings.DATA_UPLOAD_MAX_MEMORY_SIZE):
        return self.algorithm + data.decode('ascii')
        t = Engine(libraries={'i18n': 'django.templatetags.i18n'}).from_string(DEFAULT_DIRECTORY_INDEX_TEMPLATE)
                    ct_info.append('    - %s %s object(s)' % (
                        obj_type._meta.label,
                    ))
Any objects that depend on these content types will also be deleted.
The content types and dependent objects that would be deleted are:
This list doesn't include any cascade deletions to data outside of Django's
models (uncommon).
        Always load related objects to display them when showing confirmation.
host_validation_re = re.compile(r"^([a-z0-9.-]+|\[[a-f0-9]*:[a-f0-9\.:]+\])(:\d+)?$")
                    unpacked_vars = dict(zip(self.loopvars, item))
                    pop_context = True
                    context.update(unpacked_vars)
                    try:
                    except TypeError:  # not an iterable
                        len_item = 1
    request.session.cycle_key()
    sql_recover_geometry_metadata = (
        "SELECT RecoverGeometryColumn(%(table)s, %(column)s, %(srid)s, "
        "%(geom_type)s, %(dim)s)"
    )
                self.execute(self.sql_recover_geometry_metadata % {
        # Leave defaults for fields that aren't in POST data, except for
        # checkbox inputs because they don't appear in POST data if not checked.
        if (f.has_default() and f.name not in form.data and
                not getattr(form[f.name].field.widget, 'dont_use_model_field_default_for_empty_data', False)):
            continue
    # Don't use model field defaults for fields that aren't in POST data,
    # because checkboxes don't appear in POST data if not checked.
    dont_use_model_field_default_for_empty_data = True
                        # Reraise if the exception was raised by a @property
                        if not isinstance(current, BaseContext) and bit in dir(current):
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS, connections, router
        consistency_check_labels = set(config.label for config in apps.get_app_configs())
        # Non-default databases are only checked if database routers used.
        aliases_to_check = connections if settings.DATABASE_ROUTERS else [DEFAULT_DB_ALIAS]
        for alias in sorted(aliases_to_check):
            connection = connections[alias]
            if (connection.settings_dict['ENGINE'] != 'django.db.backends.dummy' and
                    # At least one app must be migrated to the database.
                    any(router.allow_migrate(connection.alias, label) for label in consistency_check_labels)):
            if not debug:
                loaders = [('django.template.loaders.cached.Loader', loaders)]
    create_contenttypes, inject_rename_contenttypes_operations,
        post_migrate.connect(create_contenttypes)
                # conflict as remove_stale_contenttypes will take care of
                # asking the user what should be done next.
def get_contenttypes_and_models(app_config, using, ContentType):
    if not router.allow_migrate_model(using, ContentType):
        return None, None
    ContentType.objects.clear_cache()
    content_types = {
        ct.model: ct
        for ct in ContentType.objects.using(using).filter(app_label=app_config.label)
    }
    app_models = {
        model._meta.model_name: model
        for model in app_config.get_models()
    }
    return content_types, app_models
def create_contenttypes(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    Creates content types for models in the given app.
    content_types, app_models = get_contenttypes_and_models(app_config, using, ContentType)
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, router
from django.db.models.deletion import Collector
from django.utils import six
from django.utils.six.moves import input
from ...management import get_contenttypes_and_models
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
            help='Nominates the database to use. Defaults to the "default" database.',
        )
    def handle(self, **options):
        db = options['database']
        interactive = options['interactive']
        verbosity = options['verbosity']
        for app_config in apps.get_app_configs():
            content_types, app_models = get_contenttypes_and_models(app_config, db, ContentType)
            if not app_models:
                continue
            to_remove = [
                ct for (model_name, ct) in six.iteritems(content_types)
                if model_name not in app_models
            ]
            # Confirm that the content type is stale before deletion.
            using = router.db_for_write(ContentType)
            if to_remove:
                if interactive:
                    ct_info = []
                    for ct in to_remove:
                        ct_info.append('    - Content type for %s.%s' % (ct.app_label, ct.model))
                        collector = NoFastDeleteCollector(using=using)
                        collector.collect([ct])
                        for obj_type, objs in collector.data.items():
                            if objs == {ct}:
                                continue
                            ct_info.append('    - %s %s object(s)' % (
                                len(objs),
                                obj_type._meta.label,
                            ))
                        content_type_display = '\n'.join(ct_info)
                    self.stdout.write("""Some content types in your database are stale and can be deleted.
Any objects that depend on these content types will also be deleted.
The content types and dependent objects that would be deleted are:
%s
This list doesn't include any cascade deletions to data outside of Django's
models (uncommon).
Are you sure you want to delete these content types?
If you're unsure, answer 'no'.\n""" % content_type_display)
                    ok_to_delete = input("Type 'yes' to continue, or 'no' to cancel: ")
                else:
                    ok_to_delete = False
                if ok_to_delete == 'yes':
                    for ct in to_remove:
                        if verbosity >= 2:
                            self.stdout.write("Deleting stale content type '%s | %s'" % (ct.app_label, ct.model))
                        ct.delete()
                else:
                    if verbosity >= 2:
                        self.stdout.write("Stale content types remain.")
class NoFastDeleteCollector(Collector):
    def can_fast_delete(self, *args, **kwargs):
        """
        Always load related objects to display them when showing confirmation.
        """
        return False
        Clear out the content-type cache.
        return "(%s -> %s)" % (lhs, lookup), params
# Whether to use the "ETag" header. This saves bandwidth but slows down performance.
    parameters as the view itself. The ETag function should return a string (or
        if isinstance(self.remote_field.through, six.string_types) or not self.remote_field.through._meta.managed:
            if model != self.remote_field.through and model._meta.managed
    url(r'^$',
    url(r'^bookmarklets/$',
    url(r'^tags/$',
    url(r'^filters/$',
    url(r'^views/$',
    url(r'^views/(?P<view>[^/]+)/$',
    url(r'^models/$',
    url(r'^models/(?P<app_label>[^\.]+)\.(?P<model_name>[^/]+)/$',
    url(r'^templates/(?P<template>.*)/$',
    r"""
            value_parts = re.split(r'\W+', value) + [value]
    new = re.sub(r"^(-?\d+)(\d{3})", r'\g<1>,\g<2>', orig)
    if regex_pattern.endswith('$') and not regex_pattern.endswith(r'\$'):
        r'\.'                                # dot
        r'(?!-)'                             # can't start with a dash
        r'(?:[a-z' + ul + '-]{2,63}'         # domain label
        r'|xn--[a-z0-9]{1,59})'              # or punycode label
        r'(?<!-)'                            # can't end with a dash
        r'\.?'                               # may have a trailing dot
    _lazy_re_compile(r'^-?\d+\Z'),
    regexp = _lazy_re_compile(r'^%(neg)s\d+(?:%(sep)s%(neg)s\d+)*\Z' % {
        return force_text(x).replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
            m = re.search(r'references (\S*) ?\(["|]?(.*)["|]?\)', field_desc, re.I)
                m = re.match(r'FOREIGN KEY\(([^\)]*)\).*', field_desc, re.I)
            m = re.search(r'"(.*)".*references (.*) \(["|](.*)["|]\)', field_desc, re.I)
    'var_chars': r'\w\.',
    return re.sub(r"\d([A-Z])", lambda m: m.group(0).lower(), t)
    r"""
CONTENT_TYPE_RE = re.compile(r'.*; charset=([\w\d-]+);?')
WHITESPACE = re.compile(r'\s+')
    r'<\/?smallcaps>|<\/?uppercase>)', re.IGNORECASE)
    r"""
    r"""
        value = re.sub(r'[^\w\s-]', '', value, flags=re.U).strip().lower()
        return mark_safe(re.sub(r'[-\s]+', '-', value, flags=re.U))
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return mark_safe(re.sub(r'[-\s]+', '-', value))
trim_whitespace_re = re.compile(r'\s*\n\s*')
r"""{% if request %} at {{ request.path_info|escape }}{% endif %}</title>
        if '_' not in name:
            try:
                index = int(name)
            except ValueError:
                pass
            else:
                index += 1  # postgres uses 1-indexing
                return IndexTransformFactory(index, self.base_field)
class BtreeGinExtension(CreateExtension):
    def __init__(self):
        self.name = 'btree_gin'
class UnaccentExtension(CreateExtension):
        self.name = 'unaccent'
    def value_omitted_from_data(self, data, files, name):
        return all(
            self.widget.value_omitted_from_data(data, files, '%s_%s' % (name, index))
            for index in range(self.size)
        )
        if (f.has_default() and
                form[f.name].field.widget.value_omitted_from_data(form.data, form.files, form.add_prefix(f.name))):
    def value_omitted_from_data(self, data, files, name):
        return name not in data
    def value_omitted_from_data(self, data, files, name):
        return name not in files
    def value_omitted_from_data(self, data, files, name):
        # HTML checkboxes don't appear in POST data if not checked, so it's
        # never known if the value is actually omitted.
        return False
    def value_omitted_from_data(self, data, files, name):
        return all(
            widget.value_omitted_from_data(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)
        )
    def value_omitted_from_data(self, data, files, name):
        return not any(
            ('{}_{}'.format(name, interval) in data)
            for interval in ('year', 'month', 'day')
        )
            val = self._check_parent_chain(instance, self.field_name)
    @property
    def errors(self):
        return self.form.errors
    @property
    def non_field_errors(self):
        return self.form.non_field_errors
    @property
    def forms(self):
        return self.formset.forms
    @property
    def non_form_errors(self):
        return self.formset.non_form_errors
    # https://dev.mysql.com/doc/refman/en/spatial-function-argument-handling.html
# versions like 5.0.24 and 5.0.24a as the same).
    def value_omitted_from_data(self, data, files, name):
        # HTML checkboxes don't appear in POST data if not checked, so it's
        # never known if the value is actually omitted.
        return False
    import warnings
    from functools import wraps
    from django.utils.deprecation import RemovedInDjango21Warning
    warnings.warn(
        'permalink() is deprecated in favor of calling django.urls.reverse() '
        'in the decorated method.',
        RemovedInDjango21Warning
    )
    NestedObjects, construct_change_message, flatten_fieldsets,
    get_deleted_objects, lookup_needs_distinct, model_format_dict, quote,
    unquote,
from django.utils.translation import ugettext as _, ungettext
        """
        return construct_change_message(form, formsets, add)
from django.utils.translation import (
    override as translation_override, ungettext,
)
def construct_change_message(form, formsets, add):
    """
    Construct a JSON structure describing changes from a changed object.
    Translations are deactivated so that strings are stored untranslated.
    Translation happens later on LogEntry access.
    """
    change_message = []
    if add:
        change_message.append({'added': {}})
    elif form.changed_data:
        change_message.append({'changed': {'fields': form.changed_data}})
    if formsets:
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
    return change_message
        except (smtplib.SMTPException, socket.error):
from django.db.models import __all__ as models_all  # isort:skip
from django.contrib.gis.db.models.aggregates import __all__ as aggregates_all
from django.contrib.gis.db.models.fields import (
from django.contrib.gis.db.models.manager import GeoManager
__all__ = models_all + aggregates_all
__all__ += [
    'GeometryCollectionField', 'GeometryField', 'LineStringField',
    'MultiLineStringField', 'MultiPointField', 'MultiPolygonField', 'PointField',
    'PolygonField', 'RasterField', 'GeoManager',
]
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
from django.db.models.aggregates import __all__ as aggregates_all
from django.db.models.deletion import (
from django.db.models.expressions import (
from django.db.models.fields import __all__ as fields_all
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.proxy import OrderWrt
from django.db.models.indexes import __all__ as indexes_all
from django.db.models.lookups import Lookup, Transform
from django.db.models.manager import Manager
from django.db.models.query import (
from django.db.models.base import DEFERRED, Model  # isort:skip
from django.db.models.fields.related import (  # isort:skip
__all__ = aggregates_all + fields_all + indexes_all
__all__ += [
    'ObjectDoesNotExist', 'signals',
    'CASCADE', 'DO_NOTHING', 'PROTECT', 'SET', 'SET_DEFAULT', 'SET_NULL',
    'ProtectedError',
    'Case', 'Expression', 'ExpressionWrapper', 'F', 'Func', 'Value', 'When',
    'FileField', 'ImageField', 'OrderWrt', 'Lookup', 'Transform', 'Manager',
    'Prefetch', 'Q', 'QuerySet', 'prefetch_related_objects', 'DEFERRED', 'Model',
    'ForeignKey', 'ForeignObject', 'OneToOneField', 'ManyToManyField',
    'ManyToOneRel', 'ManyToManyRel', 'OneToOneRel', 'permalink',
]
__all__ = [str('Index')]
            if (connection.settings_dict['ENGINE'] != 'django.db.backends.dummy' and any(
                    # At least one model must be migrated to the database.
                    router.allow_migrate(connection.alias, app_label, model_name=model._meta.object_name)
                    for app_label in consistency_check_labels
                    for model in apps.get_models(app_label)
            )):
        return obj.get_compiler(connection=self.connection).as_sql(subquery=True)
            self.group_by = [col.relabeled_clone(change_map) for col in self.group_by]
                (key, col.relabeled_clone(change_map)) for key, col in self._annotations.items())
                model = field.model._meta.concrete_model
                        (value.model._meta.object_name, opts.object_name)
from django.utils.http import parse_http_date_safe
    Also sets the Content-Length response-header.
            objs_with_pk, objs_without_pk = partition(lambda o: o.pk is None, objs)
            if objs_with_pk:
                self._batched_insert(objs_with_pk, fields, batch_size)
            if objs_without_pk:
                fields = [f for f in fields if not isinstance(f, AutoField)]
                ids = self._batched_insert(objs_without_pk, fields, batch_size)
                if connection.features.can_return_ids_from_bulk_insert:
                    assert len(ids) == len(objs_without_pk)
                for obj_without_pk, pk in zip(objs_without_pk, ids):
                    obj_without_pk.pk = pk
                    obj_without_pk._state.adding = False
                    obj_without_pk._state.db = self.db
    def delete_batch(self, pk_list, using):
        field = self.get_meta().pk
import pytz
import pytz
from django.core.exceptions import FieldError
                        "Are time zone definitions for your database installed?"
import pytz
    elif isinstance(arg, six.string_types):
    time zone name, or ``None``. If it is ``None``, the default time zone is
    used within the block.
import pytz
utc = pytz.utc
    return pytz.timezone(settings.TIME_ZONE)
    time zone name.
    elif isinstance(timezone, six.string_types):
    time zone name, or ``None``. If it is ``None``, Django enables the default
    time zone.
from django.db.models.sql.query import Query
        if isinstance(self.rhs, Query):
            # If rhs is some Query, don't touch it.
    def as_sql(self, with_limits=True, with_col_aliases=False):
            if getattr(self.rhs, '_forced_pk', False):
                self.rhs.clear_select_clause()
                if getattr(self.lhs.output_field, 'primary_key', False):
                    # A case like Restaurant.objects.filter(place__in=restaurant_qs),
                    # where place is a OneToOneField and the primary key of
                    # Restaurant.
                    target_field = self.lhs.field.name
                else:
                    target_field = self.lhs.field.target_field.name
                self.rhs.add_fields([target_field], True)
            from django.db.models.sql.query import Query  # avoid circular import
            if isinstance(rhs, Query):
        # instance and as_sql just something with as_sql. Finally the value
        # can of course be just plain Python value.
        if hasattr(self.rhs, 'get_compiler') or hasattr(self.rhs, 'as_sql') or self.bilateral_transforms:
from django.db.models.query_utils import InvalidQuery, Q
    def _prepare_as_filter_value(self):
        if self._fields is None:
            queryset = self.values('pk')
            queryset.query._forced_pk = True
        else:
            if len(self._fields) > 1:
            queryset = self._clone()
        return queryset.query.as_subquery_filter(queryset._db)
FORCE = object()
        if select_format is FORCE or (select_format and not self.query.subquery):
    def as_sql(self, with_limits=True, with_col_aliases=False):
            ann_sql, ann_params = self.compile(annotation, select_format=FORCE)
        self.subquery = False
        obj.subquery = self.subquery
    def _prepare_as_filter_value(self):
        return self.clone()
            return True, ['isnull'], used_joins
        if hasattr(value, '_prepare_as_filter_value'):
            value = value._prepare_as_filter_value()
            # Check that the field and the queryset use the same model in a
            # query like .filter(author=Author.objects.all()). For example, the
            # opts would be Author's (from the author field) and value.model
            # would be Author.objects.all() queryset's .model (Author also).
            # The field is the related field on the lhs side.
            # If _forced_pk isn't set, this isn't a queryset query or values()
            # or values_list() was specified by the developer in which case
            # that choice is trusted.
            if (getattr(value, '_forced_pk', False) and
                    not check_rel_lookup_compatibility(value.model, opts, field)):
                raise ValueError(
                    'Cannot use QuerySet for "%s": Use a QuerySet for "%s".' %
                    (value.model._meta.object_name, opts.object_name)
                )
    def as_subquery_filter(self, db):
        self._db = db
        self.subquery = True
        # It's safe to drop ordering if the queryset isn't using slicing,
        # distinct(*fields) or select_for_update().
        if (self.low_mark == 0 and self.high_mark is None and
                not self.distinct_fields and
                not self.select_for_update):
            self.clear_ordering(True)
        return self
        query.subquery = True
        self.subquery, self.sub_params = query.get_compiler(using).as_sql(with_col_aliases=True)
        query.set_values(self.targets)
            value = self.to_python(value)
        if not isinstance(value, uuid.UUID):
            except (AttributeError, ValueError):
        # Allow variants of localhost if ALLOWED_HOSTS is empty and DEBUG=True.
        allowed_hosts = settings.ALLOWED_HOSTS
        if settings.DEBUG and not allowed_hosts:
            allowed_hosts = ['localhost', '127.0.0.1', '[::1]']
        if domain and validate_host(domain, allowed_hosts):
@keep_lazy_text
    """Capitalize the first letter of a string."""
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
        """
        Raise an exception if trying to pickle an unrendered response. Pickle
        only rendered data, not the data used to construct the response.
        """
        Prevent older versions of pickle from trying to pickle the __dict__
        (which in the case of a SimpleLazyObject may contain a lambda). The
        value will be ignored by __reduce__() and the custom unpickler.
        """
        new_attrs = {'__module__': module}
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        new_class = super_new(cls, name, bases, new_attrs)
                    self.stdout.write("  %s\n" % (self.style.MIGRATE_LABEL(migration_string),))
    def __init__(self, engine, dirs=None):
        super(Loader, self).__init__(engine)
        self.dirs = dirs
        return self.dirs if self.dirs is not None else self.engine.dirs
    from django.contrib.gis.gdal import SpatialReference
from django.utils.six.moves.urllib.parse import urljoin
        url = self.url(context)
from django.utils.six.moves.urllib.parse import quote, urljoin
            return urljoin(PrefixNode.handle_simple("STATIC_URL"), quote(path))
        defaults = {'form_class': forms.NullBooleanField}
import warnings
from django.utils.deprecation import RemovedInDjango21Warning
    (4) Ignore look-ahead and look-behind assertions.
                    if ch in '!=<':
                    elif ch in 'iLmsu#':
                        warnings.warn(
                            'Using (?%s) in url() patterns is deprecated.' % ch,
                            RemovedInDjango21Warning
                        )
                        walk_to_end(ch, pattern_iter)
        model = registered_tables.get(m2m_db_table)
        # The second condition allows multiple m2m relations on a model if
        # some point to a through model that proxies another through model.
        if model and model._meta.concrete_model != self.remote_field.through._meta.concrete_model:
from .utils import Oracle_datetime                          # NOQA isort:skip
        return Database.connect(self._connect_string(), **conn_params)
        self.connection.stmtcachesize = 20
                # cx_Oracle raises a cx_Oracle.DatabaseError exception
            self.force_bytes = force_text(param, cursor.charset, strings_only)
            query = query
            query = query % args
            query = query % tuple(args)
            query = query % tuple(args)
        return force_text(query, self.charset), self._format_params(params)
        return self.cursor.execute(query, self._param_generator(params))
        return self.cursor.executemany(query, [self._param_generator(p) for p in formatted])
from .utils import InsertIdVar, Oracle_datetime
        return "SAVEPOINT " + self.quote_name(sid)
        return "ROLLBACK TO SAVEPOINT " + self.quote_name(sid)
    # Is the aggregate supported by the database?
    @property
    def supports_union_aggr(self):
        return aggregates.Union not in self.connection.ops.disallowed_aggregates
from django.utils.html import format_html
        msg = _("""%(name)s with ID "%(key)s" doesn't exist. Perhaps it was deleted?""") % {
            'key': unquote(object_id),
                        # If it's --link mode and the path isn't a link (i.e.
                        # the previous collectstatic wasn't with --link) or if
                        # it's non-link mode and the path is a link (i.e. the
                        # previous collectstatic was with --link), the old
                        # links/files must be deleted so it's not safe to skip
                        # unmodified files.
                        can_skip_unmodified_files = not (self.symlink ^ os.path.islink(full_path))
                        # In remote storages, skipping is only based on the
                        # modified times since symlinks aren't relevant.
                        can_skip_unmodified_files = True
                    file_is_unmodified = (
                        target_last_modified.replace(microsecond=0) >=
                        source_last_modified.replace(microsecond=0)
                    )
                    if file_is_unmodified and can_skip_unmodified_files:
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
    def ipython(self, options):
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ImproperlyConfigured
    isolation_levels = {
        'read uncommitted',
        'read committed',
        'repeatable read',
        'serializable',
    }
        # Validate the transaction isolation level, if specified.
        options = settings_dict['OPTIONS'].copy()
        isolation_level = options.pop('isolation_level', None)
        if isolation_level:
            isolation_level = isolation_level.lower()
            if isolation_level not in self.isolation_levels:
                raise ImproperlyConfigured(
                    "Invalid transaction isolation level '%s' specified.\n"
                    "Use one of %s, or None." % (
                        isolation_level,
                        ', '.join("'%s'" % s for s in sorted(self.isolation_levels))
                    ))
            # The variable assignment form of setting transaction isolation
            # levels will be used, e.g. "set tx_isolation='repeatable-read'".
            isolation_level = isolation_level.replace(' ', '-')
        self.isolation_level = isolation_level
        kwargs.update(options)
        assignments = []
            # SQL_AUTO_IS_NULL controls whether an AUTO_INCREMENT column on
            # a recently inserted row will return when the field is tested
            # for NULL. Disabling this brings this aspect of MySQL in line
            # with SQL standards.
            assignments.append('SQL_AUTO_IS_NULL = 0')
        if self.isolation_level:
            assignments.append("TX_ISOLATION = '%s'" % self.isolation_level)
        if assignments:
                cursor.execute('SET ' + ', '.join(assignments))
VERSION = (2, 0, 0, 'alpha', 0)
    def disconnect(self, receiver=None, sender=None, dispatch_uid=None, apps=None):
    def disconnect(self, receiver=None, sender=None, dispatch_uid=None):
    def __init__(self, to, on_delete, related_name=None, related_query_name=None,
    def __init__(self, to, on_delete, to_field=None, **kwargs):
from django.utils import six
from MySQLdb.converters import conversions                      # isort:skip
from django.utils import six
    'PolygonField', 'RasterField',
            try:
                template = loader.get_template(name, skip=skip)
                return template, template.origin
            except TemplateDoesNotExist as e:
                tried.extend(e.tried)
from django.template import Template, TemplateDoesNotExist
    def get_template(self, template_name, skip=None):
        for origin in self.get_template_sources(template_name):
from django.template import TemplateDoesNotExist
    def get_template(self, template_name, skip=None):
        key = self.cache_key(template_name, skip)
            template = super(Loader, self).get_template(template_name, skip)
    def get_template_sources(self, template_name):
            for origin in loader.get_template_sources(template_name):
    def cache_key(self, template_name, skip=None):
    def get_template_sources(self, template_name):
        for template_dir in self.get_dirs():
        response = callback(request, **dict(param_dict, exception=exception))
def include(arg, namespace=None):
    app_name = None
            raise ImproperlyConfigured(
                'Passing a 3-tuple to django.conf.urls.include() is not supported. '
        raise ImproperlyConfigured(
            'providing an app_name is not supported. Set the app_name attribute '
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.deprecation import RemovedInDjango21Warning
                        result_repr = linebreaksbr(force_text(value))
                 unique_id=None, unique_id_is_permalink=None, categories=(),
                 item_copyright=None, ttl=None, updateddate=None, enclosures=None, **kwargs):
    Context, Node, NodeList, Origin, RequestContext, Template, Variable,
from django.utils.deprecation import RemovedInDjango20Warning
        return (
        raise TypeError(
            'Direct assignment to the %s is prohibited. Use %s.set() instead.'
            % self._get_set_deprecation_msg_params(),
        return (
    system_check_removed_details = {
            'CommaSeparatedIntegerField is removed except for support in '
            'historical migrations.'
            'Use CharField(validators=[validate_comma_separated_integer_list]) '
            'instead.'
        'id': 'fields.E901',
        raise NotImplementedError('subclasses of Storage must provide a get_accessed_time() method')
        raise NotImplementedError('subclasses of Storage must provide a get_created_time() method')
        raise NotImplementedError('subclasses of Storage must provide a get_modified_time() method')
                    qs = manager._apply_rel_filters(lookup.queryset)
        return False
        return True
        return True
        return False
    def contribute_to_class(self, cls, name, private_only=False):
    def add_field(self, field, private=False):
    LANGUAGE_SESSION_KEY, check_for_language, get_language,
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
                    raise ImproperlyConfigured(
                        'Add parent_link=True to %s.' % field,
class Widget(six.with_metaclass(MediaDefiningClass)):
from django.utils.safestring import SafeData, mark_safe
    if context.autoescape:
from django.utils.safestring import SafeData, mark_safe
    return conditional_escape(value)
        if not opts.managers:
        return self.field.remote_field.model._base_manager.db_manager(hints=hints).all()
        return self.related.related_model._base_manager.db_manager(hints=hints).all()
from django.utils.deprecation import RemovedInDjango21Warning
    'indexes',
MIDDLEWARE = []
        if (settings.APPEND_SLASH and
                'django.middleware.common.CommonMiddleware' in settings.MIDDLEWARE and
from django.conf import settings
    if settings.MIDDLEWARE is not None and hasattr(settings, 'MIDDLEWARE_CLASSES'):
    return 'django.middleware.security.SecurityMiddleware' in settings.MIDDLEWARE
    return 'django.middleware.clickjacking.XFrameOptionsMiddleware' in settings.MIDDLEWARE
    return [] if passed_check else [W001]
    return [] if passed_check else [W002]
    return [] if passed_check else [W019]
    return 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE
    return [] if passed_check else [W003]
    return [] if passed_check else [W016]
            errors.append(W011)
            errors.append(W014)
    return 'django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE
from django.urls import get_resolver, set_urlconf
from .exception import convert_exception_to_response, get_exception_response
        Populate middleware lists from settings.MIDDLEWARE.
        handler = convert_exception_to_response(self._get_response)
        for middleware_path in reversed(settings.MIDDLEWARE):
            middleware = import_string(middleware_path)
            try:
                mw_instance = middleware(handler)
            except MiddlewareNotUsed as exc:
                if settings.DEBUG:
                    if six.text_type(exc):
                        logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                    else:
                        logger.debug('MiddlewareNotUsed: %r', middleware_path)
                continue
            if mw_instance is None:
                raise ImproperlyConfigured(
                    'Middleware factory %s returned None.' % middleware_path
                )
            if hasattr(mw_instance, 'process_view'):
                self._view_middleware.insert(0, mw_instance.process_view)
            if hasattr(mw_instance, 'process_template_response'):
                self._template_response_middleware.append(mw_instance.process_template_response)
            if hasattr(mw_instance, 'process_exception'):
                self._exception_middleware.append(mw_instance.process_exception)
            handler = convert_exception_to_response(mw_instance)
{{ settings.MIDDLEWARE|pprint }}"""
"""
{{ settings.MIDDLEWARE|pprint }}"""
"""
class RemovedInDjango30Warning(PendingDeprecationWarning):
class RemovedInDjango21Warning(DeprecationWarning):
RemovedInNextVersionWarning = RemovedInDjango21Warning
    iterations = 100000
def constant_time_compare(val1, val2):
    """Return True if the two strings are equal, False otherwise."""
    return hmac.compare_digest(force_bytes(val1), force_bytes(val2))
def pbkdf2(password, salt, iterations, dklen=0, digest=None):
    """Return the hash of password using pbkdf2."""
    if digest is None:
        digest = hashlib.sha256
    if not dklen:
        dklen = None
    password = force_bytes(password)
    salt = force_bytes(salt)
    return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)
from email.utils import formatdate, getaddresses, make_msgid, parseaddr
                # Problem cases are non-ASCII strings.
    # base36 string that is longer than 13 base36 digits (13 digits
# Cookie pickling bug is fixed in Python 3.4.3+
if sys.version_info >= (3, 4, 3):
        def __setitem__(self, key, value):
            if isinstance(value, Morsel):
                # allow assignment of constructed Morsels (e.g. for pickling)
                dict.__setitem__(self, key, value)
            else:
                super(SimpleCookie, self).__setitem__(key, value)
        return paths[0]
        os.path.dirname(os.path.realpath(__file__)), 'common-passwords.txt.gz'
from django.utils._os import safe_join
        return os.path.abspath(self.base_location)
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
    commands = {name: 'django.core' for name in find_commands(__path__[0])}
            basedirs.extend(settings.LOCALE_PATHS)
            if i == 0 and not is_writable(base_path + '.mo'):
                '-o', base_path + '.mo', base_path + '.po'
        dirs = [os.path.abspath(os.path.realpath(d)) for d in dirs]
        django_dir = os.path.normpath(os.path.join(os.path.dirname(django.__file__)))
        backend_dir = os.path.join(os.path.dirname(__file__), 'backends')
                name for _, name, ispkg in pkgutil.iter_modules([backend_dir])
ROOT = os.path.dirname(__file__)
            template_dirs.append(template_dir)
# For backwards-compatibility in Django 2.0
    """Always return a unicode path (did something for Python 2)."""
    Python 2. Noop for Python 3.
    final_path = abspath(join(base, *paths))
    base_path = abspath(base)
            basedirs.append(os.path.join(app_config.path, 'locale'))
        settingsfile = sys.modules[settings.__module__].__file__
        os.path.dirname(sys.modules[settings.__module__].__file__), 'locale')
    DatabaseWrapper as SQLiteDatabaseWrapper, SQLiteCursorWrapper,
                'SpatiaLite requires SQLite to be configured to allow '
                'extension loading.'
            )
SQLite3 backend for the sqlite3 module in the standard library.
from sqlite3 import dbapi2 as Database
        @wraps(view_func)
    @wraps(get_response)
        @wraps(func)
        update_wrapper(_dec, decorator)
# Unused, for backwards compatibility in Django 2.0.
            @wraps(view_func)
from django.utils.decorators import decorator_from_middleware_with_args
        @wraps(viewfunc)
    @wraps(view_func)
    return wraps(view_func)(wrapped_view)
    return wraps(view_func)(wrapped_view)
    return wraps(view_func)(wrapped_view)
from django.utils.decorators import decorator_from_middleware
    return wraps(view_func)(wrapped_view)
from django.utils.decorators import decorator_from_middleware
        @wraps(func)
        @wraps(func)
        @wraps(func)
    @wraps(func)
        except (ValueError, InvalidOperation, TypeError):
    # Set the precision high enough to avoid an exception (#15789).
    tupl = d.as_tuple()
    units = len(tupl[1])
    units += -tupl[2] if m else tupl[2]
    prec = abs(p) + units + 1
    # Avoid conversion to scientific notation by accessing `sign`, `digits`,
    # and `exponent` from Decimal.as_tuple() directly.
    sign, digits, exponent = d.quantize(exp, ROUND_HALF_UP, Context(prec=prec)).as_tuple()
    digits = [str(digit) for digit in reversed(digits)]
    while len(digits) <= abs(exponent):
        digits.append('0')
    digits.insert(-exponent, '.')
    if sign:
        digits.append('-')
    number = ''.join(reversed(digits))
    return mark_safe(formats.number_format(number, abs(p)))
        # from 'django/contrib/admin/__init__.py'>.
        # '/path/to/django/contrib/admin'.
        # from 'django/contrib/admin/models.py'>. Set by import_models().
            # functools.partial in Python <= 3.5.1.
The custom version of NamedTemporaryFile doesn't support the same keyword
arguments available in tempfile.NamedTemporaryFile.
        Unlike tempfile.NamedTemporaryFile from the standard library,
        __init__() doesn't support the 'delete', 'buffering', 'encoding', or
        'newline' keyword arguments.
            name = force_text(desc[0])  # cx_Oracle always returns a 'str'
        yield from subclasses(subclass)
            # Might fail for server-side cursors (e.g. connection closed)
            cursor.close()
from collections import UserList
    # Allow for relative paths
            # Fallback version
            # _strip_once was not able to detect more tags
    This silences a deprecation warning on Python 3.4.
    """Return a string of the translation of the message."""
        receiver.
        # listing all built-in database backends.
        builtin_backends = [
            name for _, name, ispkg in pkgutil.iter_modules([backend_dir])
            if ispkg and name not in {'base', 'dummy', 'postgresql_psycopg2'}
        ]
        if backend_name not in ['django.db.backends.%s' % b for b in builtin_backends]:
            raise ImproperlyConfigured(
                "%r isn't an available database backend.\n"
                "Try using 'django.db.backends.XXX', where XXX is one of:\n"
                "    %s" % (backend_name, ", ".join(backend_reprs))
            ) from e_user
# and Django expects time.
        return Database.connect(**conn_params)
import warnings
from django.utils.deprecation import RemovedInDjango30Warning
warnings.warn(
    "The django.db.backends.postgresql_psycopg2 module is deprecated in "
    "favor of django.db.backends.postgresql.",
    RemovedInDjango30Warning, stacklevel=2
)
        except FileNotFoundError:
            if not must_create:
        except FileExistsError:
            if must_create:
                raise CreateError
        except FileNotFoundError:
            pass
        except FileNotFoundError:
            # The file may have been removed by another process.
            pass
            except FileExistsError:
                pass
    except PermissionError as e:
        if getattr(e, 'winerror', 0) != 32:
            except FileNotFoundError:
                # There's a race between os.path.exists() and os.makedirs().
                # If os.makedirs() fails with FileNotFoundError, the directory
                # was created concurrently.
                pass
            except FileExistsError:
                # A new name is needed if the file exists.
                name = self.get_available_name(name)
                full_path = self.path(name)
        except FileNotFoundError:
            # If os.remove() fails with FileNotFoundError, the file may have
            # been removed concurrently.
            pass
        except FileNotFoundError:
            # The file was moved or deleted before the tempfile could unlink
            # it. Still sets self.file.close_called and calls
            # self.file.file.close() before the exception.
            pass
            except FileExistsError:
                raise CommandError("'%s' already exists" % top_dir)
                raise CommandError(e)
            except FileNotFoundError:
                tried.append((
                    Origin(template_file, template_name, self),
                    'Source does not exist',
                ))
                continue
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)
        'Did you install mysqlclient?'
if version < (1, 3, 3):
    raise ImproperlyConfigured("mysqlclient 1.3.3 or newer is required; you have %s" % Database.__version__)
# MySQLdb returns TIME columns as timedelta -- they are more like timedelta in
# terms of actual behavior as they are signed and include days -- and Django
# expects time.
        return self.connection.mysql_version >= (5, 6, 4)
    """Exhaust an iterator or stream."""
        # Convert paths to list because Python's _NamespacePath doesn't support
        # indexing.
            # Use binascii.hexlify() because a hex encoded bytestring is str.
        # urlsafe_base64_decode() decodes to bytestring
            # urlsafe_base64_decode() decodes to bytestring
                        # If mimetype suggests the file is text but it's
                        # actually binary, read() raises a UnicodeDecodeError.
            # These lines are copied from Python's Lib/site.py.
        # Oracle doesn't recognize True and False correctly.
    if multiprocessing.get_start_method() != 'fork':
        value = value.strip()
        # Try to strptime against each input format.
        for format in self.input_formats:
            try:
                return self.strptime(value, format)
            except (ValueError, TypeError):
                continue
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        # Remember the order in which form fields are defined.
        return OrderedDict()
    unsupported_functions = {
        'AsGeoJSON', 'AsKML', 'AsSVG', 'Envelope', 'ForceRHR', 'GeoHash',
        'MakeValid', 'MemSize', 'Scale', 'SnapToGrid', 'Translate',
    }
    def introspected_boolean_field_type(self, field=None):
        The `field` argument may be used to give further details of the field
        to be introspected.
        The return value from this function is compared by tests against actual
        introspection results; it should provide expectations, not run an
        introspection itself.
        isolation_level = options.pop('isolation_level', 'read committed')
                # Lookups on nonexistent fields are ok, since they're ignored
            # difference between an existing and a nonexistent user (#20760).
                    "The GenericForeignKey object ID references the "
                    "nonexistent field '%s'." % self.fk_field,
                    "The GenericForeignKey content type references the "
                    "nonexistent field '%s.%s'." % (
        # python-memcache responds to incr on nonexistent keys by
        # python-memcache responds to incr on nonexistent keys by
                        "'%s' refers to the nonexistent field '%s'." % (
        # Check for invalid or nonexistent fields in ordering.
                    "'ordering' refers to the nonexistent field '%s'." % invalid_field,
                # Ignore translations for nonexistent column names
        super().__init__(*args)
        return '%s. You passed in %r (%s)' % (super().__str__(), self.obj, type(self.obj))
    if isinstance(s, Promise) or not isinstance(s, str):
        raise DjangoUnicodeDecodeError(s, *e.args)
    def value_omitted_from_data(self, data, files, name):
        return (
            super().value_omitted_from_data(data, files, name) and
            self.clear_checkbox_name(name) not in data
        )
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
                common_passwords_lines = f.read().decode().splitlines()
                return manifest.read().decode()
        contents = json.dumps(payload).encode()
    return repercent_broken_unicode(path_info).decode()
    return script_name.decode()
    return value.encode('iso-8859-1')
    return value.decode(errors='replace')
                len(l.encode()) > RFC5322_EMAIL_LINE_LENGTH_LIMIT
                        content = content.decode()
        stream_or_string = stream_or_string.decode()
        stream_or_string = stream_or_string.decode()
            return cursor.query.decode()
    return lambda s: conv_func(s.decode())
from django.core.handlers.wsgi import WSGIRequest
        path = uri_to_iri(path).encode()
        return path.decode('iso-8859-1')
                ('%s%s%s' % (random.getstate(), time.time(), settings.SECRET_KEY)).encode()
            ).digest()
        )
    return repercent_broken_unicode(iri).decode()
        path.decode()
            return func(*self.__args, **self.__kw).encode()
    def get_distance(self, f, value, lookup_type):
    def get_distance(self, f, dist_val, lookup_type):
        return [dist_param]
    def get_distance(self, f, value, lookup_type):
                self.lookup_name,
import warnings
from django.utils.deprecation import RemovedInDjango30Warning
    warnings.warn(
        'render_to_response() is deprecated in favor render(). It has the '
        'same signature except that it also requires a request.',
        RemovedInDjango30Warning, stacklevel=2,
    )
                        if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
            field.serialize = False
            # Use the base.Template of a backends.django.Template.
            elif hasattr(template, 'template'):
                template = template.template
from django.db.models.indexes import Index
            constraints[index]['type'] = Index.suffix if type_ == 'BTREE' else type_.lower()
                    "type": 'idx' if type_ == 'normal' else type_,
from django.db.models.indexes import Index
                    "type": Index.suffix if type_ == 'btree' else type_,
from django.db.models.indexes import Index
                constraints[index]['type'] = Index.suffix
import warnings
from django.utils.deprecation import RemovedInDjango30Warning
        if self.is_overridden('DEFAULT_CONTENT_TYPE'):
            warnings.warn('The DEFAULT_CONTENT_TYPE setting is deprecated.', RemovedInDjango30Warning)
        if name == 'DEFAULT_CONTENT_TYPE':
            warnings.warn('The DEFAULT_CONTENT_TYPE setting is deprecated.', RemovedInDjango30Warning)
            raise MultiPartParserError('Invalid boundary in multipart: %s' % boundary.decode())
    def __init__(self, regex, max_length=None, min_length=None, *args, **kwargs):
        # Does the backend accept a request argument?
            args = ()
            # Does the backend accept a request keyword argument?
                inspect.getcallargs(backend.authenticate, request=request, **credentials)
                # Does the backend accept credentials without request?
                try:
                    inspect.getcallargs(backend.authenticate, **credentials)
                except TypeError:
                    # This backend doesn't accept these credentials as arguments. Try the next one.
                    continue
                else:
                    warnings.warn(
                        "Update %s.authenticate() to accept a positional "
                        "`request` argument." % backend_path,
                        RemovedInDjango21Warning
                    )
                credentials['request'] = request
                    "In %s.authenticate(), move the `request` keyword argument "
                    "to the first positional argument." % backend_path,
    match = re.match(r'([^"]+)"\."([^"]+)', name)
        Given a lookup_type of 'year', 'month', 'day', 'hour', 'minute', or
        'second', return the SQL that extracts a value from the given
        datetime field field_name.
        Given a lookup_type of 'year', 'month', 'day', 'hour', 'minute', or
        'second', return the SQL that truncates the given datetime field
        field_name to a datetime object with only the given specificity.
        raise NotImplementedError('subclasses of BaseDatabaseOperations may require a datetime_trunc_sql() method')
            return self.connection.server_version
        namespace = getattr(pattern, 'namespace', None)
        current = parents
        if namespace is not None:
            current += (namespace,)
    ord('`'): '\\u0060',
#!/usr/bin/env python
#!/usr/bin/env python
        result.queryset = self.queryset.all()
    # https://postgis.net/docs/PostGIS_Special_Functions_Index.html#PostGIS_3D_Functions
https://web.archive.org/web/20130407175746/https://www.gaia-gis.it/gaia-sins/spatialite-sql-4.0.0.html
https://www.gaia-gis.it/gaia-sins/spatialite-sql-4.2.1.html
    normalized_path = posixpath.normpath(path).lstrip('/')
    path = posixpath.normpath(path)
    map_srid = 3857
                    name, subvalue, sublabel, selected, index,
                    subindex=subindex, attrs=attrs,
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
    def get_context(self, name, value, attrs):
        if base_meta and base_meta.abstract and not abstract:
            new_class._meta.indexes = [copy.deepcopy(idx) for idx in new_class._meta.indexes]
            # Set the name of _meta.indexes. This can't be done in
            # Options.contribute_to_class() because fields haven't been added
            # to the model at that point.
            for index in new_class._meta.indexes:
                if not index.name:
                    index.set_name_with_model(new_class)
    def clone(self):
        """Create a copy of this Index."""
        path, args, kwargs = self.deconstruct()
        return self.__class__(*args, **kwargs)
    def push_state(self, template, isolated_context=True):
        if isolated_context:
            self.push()
            if isolated_context:
                self.pop()
        with context.render_context.push_state(compiled_parent, isolated_context=False):
            return compiled_parent._render(context)
        # The default for cx_Oracle < 5.3 is 50.
        RemovedInDjango21Warning,
        stacklevel=2,
from django.utils._os import safe_join
    path = posixpath.normpath(path).lstrip('/')
    fullpath = safe_join(document_root, path)
            return directory_index(path, fullpath)
    ParseResult, SplitResult, _coerce_args, _splitnetloc, _splitparams, quote,
    quote_plus, scheme_chars, unquote, unquote_plus,
    urlencode as original_urlencode, uses_params,
# Copied from urllib.parse.urlparse() but uses fixed urlsplit() function.
def _urlparse(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    splitresult = _urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = splitresult
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    result = ParseResult(scheme, netloc, url, params, query, fragment)
    return _coerce_result(result)
# Copied from urllib.parse.urlsplit() with
# https://github.com/python/cpython/pull/661 applied.
def _urlsplit(url, scheme='', allow_fragments=True):
    """Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>
    Return a 5-tuple: (scheme, netloc, path, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    allow_fragments = bool(allow_fragments)
    netloc = query = fragment = ''
    i = url.find(':')
    if i > 0:
        for c in url[:i]:
            if c not in scheme_chars:
                break
        else:
            scheme, url = url[:i].lower(), url[i + 1:]
    if url[:2] == '//':
        netloc, url = _splitnetloc(url, 2)
        if (('[' in netloc and ']' not in netloc) or
                (']' in netloc and '[' not in netloc)):
            raise ValueError("Invalid IPv6 URL")
    if allow_fragments and '#' in url:
        url, fragment = url.split('#', 1)
    if '?' in url:
        url, query = url.split('?', 1)
    v = SplitResult(scheme, netloc, url, query, fragment)
    return _coerce_result(v)
    url_info = _urlparse(url)
                if (getattr(self.lhs.output_field, 'primary_key', False) and
                        self.lhs.output_field.model == self.rhs.model):
            'filtered_POST_items': list(self.filter.get_post_parameters(self.request).items()),
    def __bool__(self):
        # BoundField evaluates to True even if it doesn't have subwidgets.
        return True
        context = super().get_context(name, value, attrs)
        context.update(self.build_attrs(self.attrs, dict(
        )))
        c = Context()
    else:
        c = {}
    c.update({
from django.utils.encoding import force_text
            # Empty forms are unchanged forms beyond those with initial data.
            if not form.has_changed() and i >= self.initial_form_count():
    template_name = 'postgres/widgets/split_array.html'
    def get_context(self, name, value, attrs=None):
        attrs = {} if attrs is None else attrs
        context = super().get_context(name, value, attrs)
        context['widget']['subwidgets'] = []
            context['widget']['subwidgets'].append(
                self.widget.get_context(name + '_%s' % i, widget_value, final_attrs)['widget']
            )
        return context
                    # The only way to check if an index was created with
        groups = []
        for index, (option_value, option_label) in enumerate(chain(self.choices)):
            subgroup = []
                group_name = option_value
                group_name = None
            groups.append((group_name, subgroup, index))
                obj = rel_model(**kwargs)
                obj._state.db = instance._state.db
                return obj
        return bool(session_key) and (self.cache_key_prefix + session_key) in self._cache
from django.contrib.gis.gdal.datasource import DataSource
from django.contrib.gis.gdal.driver import Driver
from django.contrib.gis.gdal.error import (
from django.contrib.gis.gdal.geometries import OGRGeometry
from django.contrib.gis.gdal.geomtype import OGRGeomType
from django.contrib.gis.gdal.libgdal import (
    GDAL_VERSION, gdal_full_version, gdal_version,
)
from django.contrib.gis.gdal.raster.source import GDALRaster
from django.contrib.gis.gdal.srs import CoordTransform, SpatialReference
__all__ = (
    'Driver', 'DataSource', 'CoordTransform', 'Envelope', 'GDALException',
    'GDALRaster', 'GDAL_VERSION', 'OGRException', 'OGRGeometry', 'OGRGeomType',
    'OGRIndexError', 'SpatialReference', 'SRSException',
    'check_err', 'gdal_version', 'gdal_full_version',
)
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.contrib.gis.utils.ogrinfo import ogrinfo  # NOQA
from django.contrib.gis.utils.ogrinspect import mapping, ogrinspect  # NOQA
from django.contrib.gis.utils.srs import add_srs_entry  # NOQA
try:
    # LayerMapping requires DJANGO_SETTINGS_MODULE to be set,
    # so this needs to be in try/except.
    from django.contrib.gis.utils.layermapping import LayerMapping, LayerMapError  # NOQA
except ImproperlyConfigured:
    pass
            if (not getattr(self.rhs, 'has_select_fields', True) and
                    not getattr(self.lhs.field.target_field, 'primary_key', False)):
    lib_names = ['gdal21', 'gdal20', 'gdal111', 'gdal110', 'gdal19']
    lib_names = ['gdal', 'GDAL', 'gdal2.1.0', 'gdal2.0.0', 'gdal1.11.0', 'gdal1.10.0', 'gdal1.9.0']
    raise ImproperlyConfigured('GDAL is unsupported on OS "%s".' % os.name)
    raise ImproperlyConfigured(
        'Could not find the GDAL library (tried "%s"). Is GDAL installed? '
        'If it is, try setting GDAL_LIBRARY_PATH in your settings.'
        % '", "'.join(lib_names)
            state = self.__dict__.copy()
            # The _get_default cached_property can't be pickled due to lambda
            # usage.
            state.pop('_get_default', None)
            return _empty, (self.__class__,), state
                obj._state.adding = instance._state.adding
    lib_names = ['gdal201', 'gdal20', 'gdal111', 'gdal110', 'gdal19']
from django.db.backends.mysql.base import (
    DatabaseWrapper as MySQLDatabaseWrapper,
)
from django.db.backends.mysql.features import (
    DatabaseFeatures as MySQLDatabaseFeatures,
)
from django.contrib.gis.db.backends.base.operations import (
    BaseSpatialOperations,
)
from django.db.backends.oracle.base import (
    DatabaseWrapper as OracleDatabaseWrapper,
)
from django.db.backends.oracle.features import (
    DatabaseFeatures as OracleDatabaseFeatures,
)
from django.contrib.gis.db.backends.base.operations import (
    BaseSpatialOperations,
)
from django.db.backends.postgresql.base import (
    DatabaseWrapper as Psycopg2DatabaseWrapper,
)
from django.db.backends.postgresql.features import (
    DatabaseFeatures as Psycopg2DatabaseFeatures,
)
from django.contrib.gis.db.backends.base.operations import (
    BaseSpatialOperations,
)
from django.db.backends.sqlite3.features import (
    DatabaseFeatures as SQLiteDatabaseFeatures,
)
from django.contrib.gis.db.backends.base.operations import (
    BaseSpatialOperations,
)
from django.core.management.commands.inspectdb import (
    Command as InspectDBCommand,
)
from django.core.management.commands.runserver import (
    Command as RunserverCommand,
)
from django.core.mail.backends.console import (
    EmailBackend as ConsoleEmailBackend,
)
        if not issubclass(obj.form, BaseModelForm):
        if not isinstance(obj.filter_vertical, (list, tuple)):
        if not isinstance(obj.filter_horizontal, (list, tuple)):
        if not isinstance(obj.radio_fields, dict):
        if not callable(obj.view_on_site) and not isinstance(obj.view_on_site, bool):
            return [
                checks.Error(
                    "The value of 'view_on_site' must be a callable or a boolean value.",
                    obj=obj.__class__,
                    id='admin.E025',
                )
            ]
        if not isinstance(obj.prepopulated_fields, dict):
    def __init__(self, fields, *args, **kwargs):
    def __init__(self, fields, *args, require_all_fields=True, **kwargs):
            args=(quote(obj.pk),),
                                   args=(obj.pk,),
                                    None, (quote(obj.pk),))
                lambda obj: (obj.pk, obj.__class__),
                            rel_obj._meta.pk.to_python(pk_val) != rel_obj.pk):
            fk = value.pk
        return str([instance.pk for instance in qs])
            self.pk_val = instance.pk
                '%s__in' % self.object_id_field_name: {obj.pk for obj in instances}
                    lambda obj: obj.pk,
            obj_pk = obj.pk
                    obj.__class__.__name__, field.name, obj.pk))
                        'pk': str(value.pk)
        my_pk = self.pk
        return my_pk == other.pk
        if self.pk is None:
        return hash(self.pk)
        assert self.pk is not None, (
            lst = [(x.pk, smart_text(x))
            defaults['initial'] = [i.pk for i in initial]
            return obj.pk
            related_pk = instance.pk
            (x.pk, str(x)) for x in self.related_model._default_manager.all()
        return {obj.pk: obj for obj in qs}
        if self.fields:
            return self.fields
        # _get_form_for_get_fields() is implemented in subclasses.
        form = self._get_form_for_get_fields(request, obj)
        return list(form.base_fields) + list(self.get_readonly_fields(request, obj))
    def _get_form_for_get_fields(self, request, obj):
        return self.get_form(request, obj, fields=None)
    def _get_form_for_get_fields(self, request, obj=None):
        return self.get_formset(request, obj, fields=None).form
        return '<%s: %s>' % (self.__class__.__name__, self)
        Return an alias for the 'join', either reusing an existing alias for
        that join or creating a new one. 'join' is either a
        sql.datastructures.BaseTable or Join.
        The 'reuse' parameter can be either None which means all joins are
        reusable, or it can be a set containing the aliases that can be reused.
        sure chains like t1 LOUTER t2 INNER t3 aren't generated. All new
        joins are created as LOUTER if the join is nullable.
            'value': value,
    return value.astimezone(timezone)
    return value.astimezone(timezone).replace(tzinfo=None)
        """Limit the amount of work when a Query is deepcopied."""
        result = self.clone()
    def clone(self, klass=None, **kwargs):
        self.related_updates = {}
from django.core.exceptions import ImproperlyConfigured
class CacheKeyWarning(RuntimeWarning):
from .pgraster import from_pgraster
        """Convert a PostGIS HEX String into a dict readable by GDALRaster."""
    def convert_invalid_empty_geometry_collection(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def from_db_value(self, value, expression, connection):
    def from_db_value(self, value, expression, connection):
    def from_db_value(self, value, expression, connection):
    def from_db_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
from django.utils.inspect import func_supports_parameter
    def _from_db_value(self, value, expression, connection):
            self.base_field.from_db_value(item, expression, connection, {})
            if func_supports_parameter(self.base_field.from_db_value, 'context')  # RemovedInDjango30Warning
            else self.base_field.from_db_value(item, expression, connection)
from django.utils.inspect import func_supports_parameter
            if func_supports_parameter(converter, 'context'):  # RemovedInDjango30Warning
                expires = converter(expires, expression, connection, {})
            else:
                expires = converter(expires, expression, connection)
                            if func_supports_parameter(converter, 'context'):  # RemovedInDjango30Warning
                                current_expires = converter(current_expires, expression, connection, {})
                            else:
                                current_expires = converter(current_expires, expression, connection)
    def convert_durationfield_value(self, value, expression, connection):
    def convert_textfield_value(self, value, expression, connection):
    def convert_booleanfield_value(self, value, expression, connection):
    def convert_datetimefield_value(self, value, expression, connection):
    def convert_uuidfield_value(self, value, expression, connection):
    def convert_textfield_value(self, value, expression, connection):
    def convert_binaryfield_value(self, value, expression, connection):
    def convert_booleanfield_value(self, value, expression, connection):
    def convert_datetimefield_value(self, value, expression, connection):
    def convert_datefield_value(self, value, expression, connection):
    def convert_timefield_value(self, value, expression, connection):
    def convert_uuidfield_value(self, value, expression, connection):
    def convert_empty_values(self, value, expression, connection):
    def convert_datetimefield_value(self, value, expression, connection):
    def convert_datefield_value(self, value, expression, connection):
    def convert_timefield_value(self, value, expression, connection):
    def convert_decimalfield_value(self, value, expression, connection):
    def convert_uuidfield_value(self, value, expression, connection):
    def convert_booleanfield_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
    def convert_empty_strings(self, value, expression, connection):
    def convert_value(self, value, expression, connection):
import warnings
from django.utils.deprecation import RemovedInDjango30Warning
from django.utils.inspect import func_supports_parameter
                if func_supports_parameter(converter, 'context'):
                    warnings.warn(
                        'Remove the context parameter from %s.%s(). Support for it '
                        'will be removed in Django 3.0.' % (
                            converter.__self__.__class__.__name__,
                            converter.__name__,
                        ),
                        RemovedInDjango30Warning,
                    )
                    value = converter(value, expression, self.connection, {})
                else:
                    value = converter(value, expression, self.connection)
    def __init__(self, sql, using, params=None):
        return RawQuery(self.sql, using, params=self.params)
from .libgeos import geos_version  # NOQA
    return get_version_tuple(geos_version().decode())
        return [] if obj.pk is None else list(getattr(obj, self.attname).all())
from django.template.defaultfilters import pprint
                    frame_vars.append((k, v))
def to_locale(language):
    """Turn a language name (en-us) into a locale name (en_US)."""
        # Get correct locale for sr-latn
        if len(language[p + 1:]) > 2:
            return language[:p].lower() + '_' + language[p + 1].upper() + language[p + 2:].lower()
        return language[:p].lower() + '_' + language[p + 1:].upper()
    language = language.lower()
    parts = language.split('-')
    try:
        country = parts[1]
    except IndexError:
        return language
        # A language with > 2 characters after the dash only has its first
        # character after the dash capitalized; e.g. sr-latn becomes sr_Latn.
        # A language with 2 characters after the dash has both characters
        # capitalized; e.g. en-us becomes en_US.
        parts[1] = country.title() if len(country) > 2 else country.upper()
    return parts[0] + '_' + '-'.join(parts[1:])
from django.contrib.gis.geos.geometry import GEOSGeometry, GEOSGeometryBase
            ext_geom = GEOSGeometry(memoryview(clob.read()))
from django.contrib.gis.geos import GEOSGeometry
        self.is_geometry = isinstance(obj, (GEOSGeometry, PostGISAdapter))
from django.contrib.gis.geos.geometry import GEOSGeometry, GEOSGeometryBase
        shell = GEOSGeometry(box).shell
    GeometryCollection, GEOSException, GEOSGeometry, LineString,
    MultiLineString, MultiPoint, MultiPolygon, Point, Polygon,
        if isinstance(obj, GEOSGeometry):
                    obj = GEOSGeometry(obj)
                except (GEOSException, GDALException):
        setattr(cls, self.attname, SpatialProxy(GEOSGeometry, self))
from django.contrib.gis.geos import GEOSGeometry
            if not isinstance(geom, GEOSGeometry) or output_field and not isinstance(output_field, GeometryField):
from django.contrib.gis.geometry import hex_regex, json_regex, wkt_regex
from django.contrib.gis.geometry import json_regex
from django.contrib.gis.geometry import hex_regex, json_regex, wkt_regex
from django.urls import RegexURLPattern, RegexURLResolver, include
from .conf import include
    'include', 'is_valid_path', 'resolve', 'reverse', 'reverse_lazy',
    'set_script_prefix', 'set_urlconf', 'translate_url',
"""Functions for use in URLsconfs."""
from importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from .resolvers import LocaleRegexURLResolver
def include(arg, namespace=None):
    app_name = None
    if isinstance(arg, tuple):
        # Callable returning a namespace hint.
        try:
            urlconf_module, app_name = arg
        except ValueError:
            if namespace:
                raise ImproperlyConfigured(
                    'Cannot override the namespace for a dynamic module that '
                    'provides a namespace.'
                )
            raise ImproperlyConfigured(
                'Passing a %d-tuple to include() is not supported. Pass a '
                '2-tuple containing the list of patterns and app_name, and '
                'provide the namespace argument to include() instead.' % len(arg)
            )
    else:
        # No namespace hint - use manually provided namespace.
        urlconf_module = arg
    if isinstance(urlconf_module, str):
        urlconf_module = import_module(urlconf_module)
    patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
    app_name = getattr(urlconf_module, 'app_name', app_name)
    if namespace and not app_name:
        raise ImproperlyConfigured(
            'Specifying a namespace in include() without providing an app_name '
            'is not supported. Set the app_name attribute in the included '
            'module, or pass a 2-tuple containing the list of patterns and '
            'app_name instead.',
        )
    namespace = namespace or app_name
    # Make sure the patterns can be iterated through (without this, some
    # testcases will break).
    if isinstance(patterns, (list, tuple)):
        for url_pattern in patterns:
            if isinstance(url_pattern, LocaleRegexURLResolver):
                raise ImproperlyConfigured(
                    'Using i18n_patterns in an included URLconf is not allowed.'
                )
    return (urlconf_module, app_name, namespace)
        if not restricted and cur_depth > self.query.max_depth:
from django.db.backends.base.base import NO_DB_ALIAS
    if connection.vendor != 'postgresql' or connection.alias == NO_DB_ALIAS:
VERSION = (2, 1, 0, 'alpha', 0)
from django.urls import reverse_lazy
def logout_then_login(request, login_url=None):
def is_safe_url(url, allowed_hosts=None, require_https=False):
        template = self.template.resolve(context)
        # Does this quack like a Template?
        if not callable(getattr(template, 'render', None)):
            # If not, try the cache and get_template().
            template_name = template
            cache = context.render_context.dicts[0].setdefault(self, {})
            template = cache.get(template_name)
            if template is None:
                template = context.template.engine.get_template(template_name)
                cache[template_name] = template
        # Use the base.Template of a backends.django.Template.
        elif hasattr(template, 'template'):
            template = template.template
        values = {
            name: var.resolve(context)
            for name, var in self.extra_context.items()
        }
        if self.isolated_context:
            return template.render(context.new(values))
        with context.push(**values):
            return template.render(context)
            inspect.getcallargs(backend.authenticate, request, **credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue
        try:
            user = backend.authenticate(request, **credentials)
    'ManyToOneRel', 'ManyToManyRel', 'OneToOneRel',
from django.utils.deprecation import MiddlewareMixin
            renderer=self.form.renderer,
class RemovedInNextVersionWarning(DeprecationWarning):
        if (self._num_days(self._today()) - ts) > settings.PASSWORD_RESET_TIMEOUT_DAYS:
    geom_func_prefix = 'ST_'
    data_types = {
        'DateTimeField': 'datetime(6)',
        'TimeField': 'time(6)',
        return 'INTERVAL %s MICROSECOND' % sql
        if internal_type == 'TimeField':
                "((TIME_TO_SEC(%(lhs)s) * POW(10, 6) + MICROSECOND(%(lhs)s)) -"
                " (TIME_TO_SEC(%(rhs)s) * POW(10, 6) + MICROSECOND(%(rhs)s)))"
            ) % {'lhs': lhs_sql, 'rhs': rhs_sql}, lhs_params * 2 + rhs_params * 2
            return "TIMESTAMPDIFF(MICROSECOND, %s, %s)" % (rhs_sql, lhs_sql), rhs_params + lhs_params
# For backwards compatibility in Django 2.1.
SimpleCookie = cookies.SimpleCookie
from html.parser import HTMLParser
class HTMLParseError(Exception):
    pass
        HTMLParser.__init__(self, convert_charrefs=False)
    return {**DEFAULT_CONVERTERS, **REGISTERED_CONVERTERS}
        if isinstance(callback, functools.partial):
from html.parser import HTMLParser
        HTMLParser.__init__(self, convert_charrefs=False)
    s.feed(value)
    s.close()
    return s.get_data()
            except json.JSONDecodeError:
                except json.JSONDecodeError:
            except json.JSONDecodeError:
        except json.JSONDecodeError:
        except json.JSONDecodeError:
        except json.JSONDecodeError:
    supports_aggregate_filter_clause = True
                    FROM unnest(c.conkey) WITH ORDINALITY cols(colid, arridx)
                indexname, array_agg(attname ORDER BY arridx), indisunique, indisprimary,
                array_agg(ordering ORDER BY arridx), amname, exprdef, s2.attoptions
                    c2.relname as indexname, idx.*, attr.attname, am.amname,
                    SELECT *
                    FROM pg_index i, unnest(i.indkey, i.indoption) WITH ORDINALITY koi(key, option, arridx)
    Issues a temporary redirect by default; pass permanent=True to issue a
    permanent redirect.
    codes_for_integrityerror = (
        1048,  # Column cannot be null
        1690,  # BIGINT UNSIGNED value is out of range
    )
                cursor.execute("SELECT InitSpatialMetaData(1)")
                # SpatiaLite uses SFSQL 1.2 offsets 1000 (Z), 2000 (M), and
                # 3000 (ZM) to indicate the presence of higher dimensional
                # coordinates (M not yet supported by Django).
        if version < (4, 1, 0):
            raise ImproperlyConfigured('GeoDjango only supports SpatiaLite versions 4.1.0 and above.')
            if not return_id:
    uses_savepoints = True
    can_release_savepoints = True
    can_share_in_memory_db = True
        Helper method for bulk_create() to insert objs one batch at a time.
        kwargs.update({'check_same_thread': False, 'uri': True})
        if test_database_name == ':memory:':
            return 'file:memorydb_%s?mode=memory&cache=shared' % self.connection.alias
            value = var.resolve(context, ignore_failures=True)
            values = self.sequence.resolve(context, ignore_failures=True)
        if self._varlist:
            # Consider multiple parameters. This behaves like an OR evaluation
            # of the multiple variables.
            compare_to = [var.resolve(context, ignore_failures=True) for var in self._varlist]
        else:
            # The "{% ifchanged %}" syntax (without any variables) compares
            # the rendered output.
            compare_to = nodelist_true_output = self.nodelist_true.render(context)
        val1 = self.var1.resolve(context, ignore_failures=True)
        val2 = self.var2.resolve(context, ignore_failures=True)
        return self.expression.resolve(context, ignore_failures=True)
        obj_list = self.target.resolve(context, ignore_failures=True)
        # Check the timestamp is within limit. Timestamps are rounded to
        # midnight (server time) providing a resolution of only 1 day. If a
        # link is generated 5 minutes before midnight and used 6 minutes later,
        # that counts as 1 day. Therefore, PASSWORD_RESET_TIMEOUT_DAYS = 1 means
        # "at least 1 day, could be up to 2."
        return NodeList(iter(self))
import sys
# Private, stable API for detecting the Python version. PYXY means "Python X.Y
# or later". So that third-party apps can use these values, each constant
# should remain as long as the oldest supported Django version supports that
# Python version.
PY36 = sys.version_info >= (3, 6)
PY37 = sys.version_info >= (3, 7)
PY38 = sys.version_info >= (3, 8)
PY39 = sys.version_info >= (3, 9)
    # Timezone aware formatting. email.utils.formatdate() isn't tz aware.
    # email.utils.parsedate() does the job for RFC1123 dates; unfortunately
    def process_rhs(self, compiler, connection):
        from django.db.models.sql.query import Query
        if isinstance(self.rhs, Query):
            if self.rhs.has_limit_one():
                # The subquery must select only the pk.
                self.rhs.clear_select_clause()
                self.rhs.add_fields(['pk'])
            else:
                raise ValueError(
                    'The QuerySet value for an exact lookup must be limited to '
                    'one result using slicing.'
                )
        return super().process_rhs(compiler, connection)
    def has_limit_one(self):
        return self.high_mark is not None and (self.high_mark - self.low_mark) == 1
# A string like "example.com", or None for standard domain cookie.
                related_url += '?' + '&amp;'.join('%s=%s' % (k, v) for k, v in params.items())
            assignments.append('SET SQL_AUTO_IS_NULL = 0')
            assignments.append('SET SESSION TRANSACTION ISOLATION LEVEL %s' % self.isolation_level.upper())
                cursor.execute('; '.join(assignments))
        # Drop incoming FK constraints if the field is a primary key or unique,
        # which might be a to_field target, and things are going to change.
        drop_foreign_keys = (
            (
                (old_field.primary_key and new_field.primary_key) or
                (old_field.unique and new_field.unique)
            ) and old_type != new_type
        )
        if drop_foreign_keys:
        if drop_foreign_keys:
            kwargs['widget'] = AutocompleteSelect(db_field.remote_field, self.admin_site, using=db)
            kwargs['widget'] = AutocompleteSelectMultiple(db_field.remote_field, self.admin_site, using=db)
    url_name = '%s:%s_%s_autocomplete'
    def __init__(self, rel, admin_site, attrs=None, choices=(), using=None):
        self.admin_site = admin_site
        return reverse(self.url_name % (self.admin_site.name, model._meta.app_label, model._meta.model_name))
        for params in constraints.values():
        for k in self.headers:
        for instances_for_fieldvalues in self.field_updates.values():
            for annotation in self.annotation_select.values():
    for db_name, aliases in test_databases.values():
                    for k in cleansed:
                for name in tb_frame.f_locals:
        for list_filter in self.list_filter:
            if callable(list_filter):
                # This is simply a custom list filter class.
                spec = list_filter(request, lookup_params, self.model, self.model_admin)
            else:
                field_path = None
                if isinstance(list_filter, (tuple, list)):
                    # This is a custom FieldListFilter class for a given field.
                    field, field_list_filter_class = list_filter
                    # This is simply a field name, so use the default
                    # FieldListFilter class that has been registered for the
                    # type of the given field.
                    field, field_list_filter_class = list_filter, FieldListFilter.create
                if not isinstance(field, models.Field):
                    field_path = field
                    field = get_fields_from_path(self.model, field_path)[-1]
                lookup_params_count = len(lookup_params)
                spec = field_list_filter_class(
                    field, request, lookup_params,
                    self.model, self.model_admin, field_path=field_path,
                )
                # field_list_filter_class removes any lookup_params it
                # processes. If that happened, check if distinct() is needed to
                # remove duplicate results.
                if lookup_params_count > len(lookup_params):
                    use_distinct = use_distinct or lookup_needs_distinct(self.lookup_opts, field_path)
            if spec and spec.has_output():
                filter_specs.append(spec)
            for rel_populator in related_populators:
                rel_populator.populate(row, obj)
            for rel_iter in self.related_populators:
                rel_iter.populate(row, obj)
    for bit in bits:
        match = kwarg_re.match(bit)
        if not match:
            raise TemplateSyntaxError("Malformed arguments to url tag")
        name, value = match.groups()
        if name:
            kwargs[name] = parser.compile_filter(value)
        else:
            args.append(parser.compile_filter(value))
            return not self._session_key and not self._session_cache
        regex_matches = self.regex.search(str(value))
        fields = self.query.fields or [opts.pk]
        if self.query.fields:
            is_valid = self.is_bound and not self._errors
        return (isinstance(value, str) and not value) or value is None
        self.app_dirs = params.pop('APP_DIRS')
    stealth_options = ('shutdown_message',)
        db_instance_qs = self.__class__._base_manager.using(db).filter(pk=self.pk)
import warnings
from django.utils.deprecation import RemovedInDjango30Warning
    warnings.warn(
        'cookie_date() is deprecated in favor of http_date(), which follows '
        'the format of the latest RFC.',
        RemovedInDjango30Warning, stacklevel=2,
    )
                if getattr(attr, 'boolean', False):
        return (
            # Auto fields are editable, so check for auto or non-editable pk.
            self.form._meta.model._meta.auto_field or not self.form._meta.model._meta.pk.editable or
            # Also search any parents for an auto field. (The pk info is
            # propagated to child models so that does not need to be checked
            # in parents.)
            any(parent._meta.auto_field or not parent._meta.model._meta.pk.editable
                for parent in self.form._meta.model._meta.get_parent_list())
        return OrderedDict(
                return session_key
            if all(candidate for candidate in ((d not in models or d in model_list) for d in deps)):
        if getattr(self, '_file', None) is None:
            self.receivers = [
                r for r in self.receivers
                if not(isinstance(r[1], weakref.ReferenceType) and r[1]() is None)
            ]
            self.parallel = min(self.parallel, parallel_units)
                self.active_writers = 1
            if self.disabled:
                f.disabled = True
        if self.disabled and not isinstance(value, list):
            value = self.widget.decompress(value)
    def is_postgresql_9_5(self):
    has_select_for_update_skip_locked = is_postgresql_9_5
    has_brin_index_support = is_postgresql_9_5
    has_jsonb_agg = is_postgresql_9_5
    has_gin_pending_list_limit = is_postgresql_9_5
    def create_sql(self, model, schema_editor, using=''):
        statement = super().create_sql(model, schema_editor, using=' USING %s' % self.suffix)
        with_params = self.get_with_params()
        if with_params:
            statement.parts['extra'] = 'WITH (%s) %s' % (
                ', '.join(with_params),
                statement.parts['extra'],
            )
        return statement
    def get_with_params(self):
        return []
    def get_with_params(self):
        with_params = []
            with_params.append('pages_per_range = %d' % self.pages_per_range)
        return with_params
    def get_with_params(self):
            with_params.append('fastupdate = %s' % ('on' if self.fastupdate else 'off'))
        return with_params
    def get_with_params(self):
            with_params.append('buffering = %s' % ('on' if self.buffering else 'off'))
        return with_params
        """
        Return False if set_unusable_password() has been called for this user,
        or if the password is None, or if the password uses a hasher that's not
        in the PASSWORD_HASHERS setting.
        """
            match = self.date_re.match(value)
            if match:
                year, month, day = [int(val) for val in match.groups()]
            elif settings.USE_L10N:
from django.core.exceptions import ValidationError
        except (ValueError, self.rel.model.DoesNotExist, ValidationError):
    OFTDate, OFTDateTime, OFTInteger, OFTInteger64, OFTReal, OFTString,
    OFTTime,
    OFTDate, OFTDateTime, OFTInteger, OFTInteger64, OFTReal, OFTString,
    OFTTime,
    PermissionDenied, RequestDataTooBig, SuspiciousOperation,
    TooManyFieldsSent,
    ManyToManyDescriptor, ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor,
    DJANGO_VERSION_PICKLE_KEY, IntegrityError, connections, router,
    transaction,
    """Validate every formset and return True if all are valid."""
        valid &= formset.is_valid()
from django.utils.encoding import escape_uri_path, iri_to_uri
            safe = safe.encode(self.encoding)
            output.extend(
                encode(k.encode(self.encoding), v.encode(self.encoding))
                for v in list_
            )
from django.utils.encoding import iri_to_uri
        # Handle non-string types.
        return str(value).encode(self.charset)
            return data.encode(charset)
            query_string = parsed[4].encode().decode('iso-8859-1')
        super().__init__(children=list(args) + sorted(kwargs.items()), connector=connector, negated=negated)
        if path.startswith('django.db.models.query_utils'):
            path = path.replace('django.db.models.query_utils', 'django.db.models')
            if self.connector != self.default:
                kwargs = {'_connector': self.connector}
                "The list filter '%s' does not specify a 'title'."
                % self.__class__.__name__
            )
                "The list filter '%s' does not specify a 'parameter_name'."
                % self.__class__.__name__
            )
            'return a list of tuples (value, verbose value).'
        )
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
                'query_string': changelist.get_query_string({self.lookup_kwarg: pk_val}, [self.lookup_kwarg_isnull]),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg2]),
                'query_string': changelist.get_query_string({self.lookup_kwarg2: 'True'}, [self.lookup_kwarg]),
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg_isnull]),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
        self.lookup_choices = queryset.distinct().order_by(field.name).values_list(field.name, flat=True)
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
                'query_string': changelist.get_query_string({self.lookup_kwarg: val}, [self.lookup_kwarg_isnull]),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
        queryset, request.user, modeladmin.admin_site, using,
    )
        deleted_objects, model_count, perms_needed, protected = get_deleted_objects(
            [obj], request.user, self.admin_site, using,
        )
def get_deleted_objects(objs, user, admin_site, using):
        queryset, request.user, modeladmin.admin_site,
            [obj], request.user, self.admin_site,
from django.db import models, router
def get_deleted_objects(objs, user, admin_site):
    try:
        obj = objs[0]
    except IndexError:
        return [], {}, set(), []
    else:
        using = router.db_for_write(obj._meta.model)
    bcrypt's 72 bytes password truncation. Most use cases should prefer the
    BCryptSHA256PasswordHasher.
    """Display the row of change list object tools."""
        func=lambda context: context,
    """Display the row of change form object tools."""
        func=lambda context: context,
    """
    Template tag that allows its template to be overridden per model, per app,
    or globally.
    """
            parser, bits[1:], params, varargs, varkw, defaults, kwonly,
            kwonly_defaults, takes_context, bits[0],
        super().__init__(func, takes_context, args, kwargs, filename=None)
TRAILING_PUNCTUATION_CHARS = '.,:;!'
            stripped = middle.rstrip(TRAILING_PUNCTUATION_CHARS)
            if middle != stripped:
                trail = middle[len(stripped):] + trail
                middle = stripped
    def is_email_simple(value):
        """Return True if value looks like an email address."""
        # An @ must be in the middle of the value.
        if '@' not in value or value.startswith('@') or value.endswith('@'):
            return False
        try:
            p1, p2 = value.split('@')
        except ValueError:
            # value contains more than one @.
            return False
        # Dot must be in p2 (e.g. example.com)
        if '.' not in p2 or p2.startswith('.'):
            return False
        return True
            elif ':' not in middle and is_email_simple(middle):
re_tag = re.compile(r'<(/)?(\S+?)(?:(\s*/)|\s.*?)?>', re.S)
        context = {'widget': {**self.data, 'wrap_label': wrap_label}}
            'wrap_label': True,
        if field and field.null:
        if self.field.null:
    # BooleanField needs special-case null-handling, so it comes before the
    # general null test.
        'BooleanField': NUMBER,
        'invalid_nullable': _("'%(value)s' value must be either True, False, or None."),
        if self.null and value in self.empty_values:
            return None
            self.error_messages['invalid_nullable' if self.null else 'invalid'],
            form_class = forms.NullBooleanField if self.null else forms.BooleanField
            # In HTML checkboxes, 'required' means "must be checked" which is
            # different from the choices case ("must select some value").
            # required=False allows unchecked checkboxes.
            defaults = {'form_class': form_class, 'required': False}
        return super().formfield(**{**defaults, **kwargs})
                        extra_params['blank'] = True
                        extra_params['null'] = True
    # Some backends may not be able to differentiate BooleanField from other
    # fields such as IntegerField.
    introspected_boolean_field_type = 'BooleanField'
    introspected_boolean_field_type = 'IntegerField'
    Store a list of available languages in the context.
    This puts settings.LANGUAGES into the named variable.
    Store the language information dictionary for the given language code in a
    context variable.
    Store a list of language information dictionaries for the given language
    codes in a context variable. The language codes can be specified either as
    a list of strings or a settings.LANGUAGES style list (or any sequence of
    sequences whose first items are language codes).
    Store the current language in the context.
    This fetches the currently active language and puts its value into the
    ``language`` context variable.
    Store the current language layout in the context.
    This fetches the currently active language's layout and puts its value into
    the ``bidi`` context variable. True indicates right-to-left layout,
    otherwise left-to-right.
    Mark a string for translation and translate the string for the current
    language.
    This marks the string for translation so it will be pulled out by
    makemessages into the .po files and runs the string through the translation
    engine.
    This marks the string for translation, but returns the string unchanged.
    Use it when you need to store values into forms that should be translated
    later on.
    This tries to translate the contents of the variable ``variable``. Make
    sure that the string in there is something that is in the .po file.
    Translate a block of text with parameters.
    Enable the given language just for this block.
                    unique_together.append('(' + str(tuple(column_to_field_name[c] for c in columns)) + ')')
                    unique_together.append(str(tuple(column_to_field_name[c] for c in columns)))
        Return False if set_unusable_password() has been called for this user.
    """
    Return True if this password wasn't generated by
    User.set_unusable_password(), i.e. make_password(None).
    """
    return encoded is None or not encoded.startswith(UNUSABLE_PASSWORD_PREFIX)
    try:
        hasher = identify_hasher(encoded)
    except ValueError:
        # encoded is gibberish or uses a hasher that's no longer installed.
        return False
from .mixins import CheckFieldDefaultMixin
class HStoreField(CheckFieldDefaultMixin, Field):
    _default_hint = ('dict', '{}')
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
        """
        Hash the user's primary key and some user state that's sure to change
        after a password reset to produce a token that invalidated when it's
        used:
        1. The password field will change upon a password reset (even if the
           same password is chosen, due to password salting).
        2. The last_login field will usually be updated very shortly after
           a password reset.
        Failing those things, settings.PASSWORD_RESET_TIMEOUT_DAYS eventually
        invalidates the token.
        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.
        """
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
            m = re.match(r'(?:(?:["`\[])(.*)(?:["`\]])|(\w+)).*PRIMARY KEY.*', field_desc)
    """Turn a language name (en-us) into a locale name (en_US)."""
    language = language.lower()
    parts = language.split('-')
    try:
        country = parts[1]
    except IndexError:
        return language
    # A language with > 2 characters after the dash only has its first
    # character after the dash capitalized; e.g. sr-latn becomes sr_Latn.
    # A language with 2 characters after the dash has both characters
    # capitalized; e.g. en-us becomes en_US.
    parts[1] = country.title() if len(country) > 2 else country.upper()
    return parts[0] + '_' + '-'.join(parts[1:])
from . import LANGUAGE_SESSION_KEY, to_locale
    'check_for_language', 'to_language', 'to_locale', 'templatize',
def to_language(locale):
    """Turn a locale name (en_US) into a language name (en-us)."""
    p = locale.find('_')
    if p >= 0:
        return locale[:p].lower() + '-' + locale[p + 1:].lower()
    else:
        return locale.lower()
from . import LANGUAGE_SESSION_KEY, to_language, to_locale
    iterations = 120000
VERSION = (2, 2, 0, 'alpha', 0)
class RemovedInDjango30Warning(DeprecationWarning):
class RemovedInDjango31Warning(PendingDeprecationWarning):
RemovedInNextVersionWarning = RemovedInDjango30Warning
    iterations = 150000
        if not self.SECRET_KEY:
            raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")
# A secret key for this particular Django installation. Used in secret-key
# hashing algorithms. Set this in your settings, or Django will complain
# loudly.
SECRET_KEY = ''
        def is_value(value, accept_promise=True):
            return isinstance(value, (str, Promise) if accept_promise else str) or not is_iterable(value)
        if is_value(self.choices, accept_promise=False):
from django.contrib.gis.geos.libgeos import (
    GEOM_PTR, GEOSFuncFactory, geos_version_tuple,
)
        if geos_version_tuple() < (3, 6, 1) and isinstance(geom, Polygon) and geom.empty:
        if geos_version_tuple() < (3, 6, 1) and isinstance(geom, Polygon) and geom.empty:
        pk_pattern = re.compile(r'{}-\d+-{}$'.format(prefix, self.model._meta.pk.name))
        return super().save_new(form, commit=commit)
            match = re.match(br'SRID=(?P<srid>\-?\d+)', srid_part)
    lib_names = ['gdal202', 'gdal201', 'gdal20', 'gdal111']
    lib_names = ['gdal', 'GDAL', 'gdal2.2.0', 'gdal2.1.0', 'gdal2.0.0', 'gdal1.11.0']
get_ds_metadata_domain_list = chararray_output(std_call('GDALGetMetadataDomainList'), [c_void_p], errcheck=False)
    lib_names = ['gdal203', 'gdal202', 'gdal201', 'gdal20', 'gdal111']
    lib_names = ['gdal', 'GDAL', 'gdal2.3.0', 'gdal2.2.0', 'gdal2.1.0', 'gdal2.0.0', 'gdal1.11.0']
from django.db.models.expressions import Combinable, F, OrderBy
                if isinstance(field, (Combinable, OrderBy)):
                    if not isinstance(field, OrderBy):
                        field = field.asc()
from django.db.models.expressions import Combinable, F, OrderBy
        if isinstance(field_name, (Combinable, OrderBy)):
            if not isinstance(field_name, OrderBy):
                field_name = field_name.asc()
            if isinstance(field_name.expression, F):
                field_name = field_name.expression.name
            else:
                return []
        return HttpResponse(template.render(Context(context)), 'text/javascript; charset="utf-8"')
                raise TypeError("%s() got an unexpected keyword argument '%s'" % (cls.__name__, kwarg))
    data_type_check_constraints = {
        'PositiveIntegerField': '"%(column)s" >= 0',
        'PositiveSmallIntegerField': '"%(column)s" >= 0',
    }
        # Find inline check constraints.
        try:
            table_schema = cursor.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' and name=%s" % (
                    self.connection.ops.quote_name(table_name),
                )
            ).fetchone()[0]
        except TypeError:
            # table_name is a view.
            pass
        else:
            fields_with_check_constraints = [
                schema_row.strip().split(' ')[0][1:-1]
                for schema_row in table_schema.split(',')
                if schema_row.find('CHECK') >= 0
            ]
            for field_name in fields_with_check_constraints:
                # An arbitrary made up name.
                constraints['__check__%s' % field_name] = {
                    'columns': [field_name],
                    'primary_key': False,
                    'unique': False,
                    'foreign_key': False,
                    'check': True,
                    'index': False,
                }
            return force_bytes(data, encoding=charset)
        if settings.USE_TZ:
            modification = datetime.datetime.utcfromtimestamp(modification)
            return modification.replace(tzinfo=timezone.utc)
        return datetime.datetime.fromtimestamp(modification)
        if settings.USE_TZ:
            # Safe to use .replace() because UTC doesn't have DST
            return datetime.utcfromtimestamp(ts).replace(tzinfo=timezone.utc)
        else:
            return datetime.fromtimestamp(ts)
        # datetime.now(tz=utc) is slower, as documented in django.utils.timezone.now
        return latest_date or datetime.datetime.utcnow().replace(tzinfo=utc)
from datetime import datetime, timedelta, tzinfo
utc = pytz.utc
        isinstance(value, datetime) and
    if settings.USE_TZ:
        # timeit shows that datetime.now(tz=utc) is 24% slower
        return datetime.utcnow().replace(tzinfo=utc)
    else:
        return datetime.now()
    context = decimal.getcontext().copy()
    if max_digits is not None:
        context.prec = max_digits
        value = value.quantize(decimal.Decimal(1).scaleb(-decimal_places), context=context)
    else:
        context.traps[decimal.Rounded] = 1
        value = context.create_decimal(value)
from django.contrib.auth.models import User
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
        model = User
        field_classes = {'username': UsernameField}
                'CONTENT_LENGTH': str(len(data)),
                        field_desc += ', '.join('%s=%r' % (k, v) for k, v in extra_params.items())
                    column_name = row.name
                    if row.null_ok:  # If it's NULL...
            field_type = connection.introspection.get_field_type(row.type_code, row)
        if field_type == 'CharField' and row.internal_size:
            field_params['max_length'] = int(row.internal_size)
            if row.precision is None or row.scale is None:
                field_params['max_digits'] = row.precision if row.precision is not None else 10
                field_params['decimal_places'] = row.scale if row.scale is not None else 5
                field_params['max_digits'] = row.precision
                field_params['decimal_places'] = row.scale
        d = ',%s' % date.strftime('%Y-%m-%d')
            # 1/0 are equal to True/False. bool() converts former to latter.
# These classes override date and datetime to ensure that strftime('%Y')
# returns four digits (with leading zeros) on years < 1000.
# https://bugs.python.org/issue13305
# >>> datetime_safe.date(10, 8, 2).strftime("%Y/%m/%d was a %A")
# '0010/08/02 was a Monday'
    if dt.year >= 1000:
        raise TypeError("strftime of dates before 1000 does not handle " + illegal_formatting.group(0))
                encode(k.encode(self.encoding), str(v).encode(self.encoding))
        'overflow': _('The number of days must be between {min_days} and {max_days}.')
            raise ValidationError(self.error_messages['overflow'].format(
                min_days=datetime.timedelta.min.days,
                max_days=datetime.timedelta.max.days,
            ), code='overflow')
            return str(value)
            label = label_for_field(field, form._meta.model, model_admin, form=form)
def label_for_field(name, model, model_admin=None, return_attr=False, form=None):
            elif form and name in form.fields:
                attr = form.fields[name]
                if form:
                    message += " or %s" % form.__class__.__name__
                inline_has_add_permission = inline._has_add_permission(request, obj)
            has_add_permission = inline._has_add_permission(request, obj)
    def _has_add_permission(self, request, obj):
        # RemovedInDjango30Warning: obj will be a required argument.
        args = get_func_args(self.has_add_permission)
        return self.has_add_permission(request, obj) if 'obj' in args else self.has_add_permission(request)
        can_add = self._has_add_permission(request, obj) if request else True
from django.urls import get_mod_func, get_resolver, get_urlconf
            action = str(action).replace('\n', '')
        return self.initial.get('password')
WRAPPING_PUNCTUATION = [('(', ')'), ('[', ']')]
    def unescape(text):
        return text.replace('&amp;', '&').replace('&lt;', '<').replace(
            # Trim trailing punctuation (after trimming wrapping punctuation,
            # as encoded entities contain ';'). Unescape entites to avoid
            # breaking them by removing ';'.
            middle_unescaped = unescape(middle)
            stripped = middle_unescaped.rstrip(TRAILING_PUNCTUATION_CHARS)
            if middle_unescaped != stripped:
                trail = middle[len(stripped):] + trail
                middle = middle[:len(stripped) - len(middle_unescaped)]
                trimmed_something = True
                url = smart_urlquote(unescape(middle))
                url = smart_urlquote('http://%s' % unescape(middle))
__all__ = (
    'Storage', 'FileSystemStorage', 'DefaultStorage', 'default_storage',
    'get_storage_class',
)
    uses_savepoints = True
    uses_savepoints = False
        return self.in_atomic_block
            hasattr(self, '_start_transaction_under_autocommit')
import sys
    autocommits_when_autocommit_is_off = sys.version_info < (3, 6)
                # sqlite3 in Python < 3.6 doesn't handle transactions and
                # savepoints properly when autocommit is off.
import warnings
from django.utils.deprecation import RemovedInDjango31Warning
    def __init__(self, *args, **kwargs):
        warnings.warn(
            'CachedStaticFilesStorage is deprecated in favor of '
            'ManifestStaticFilesStorage.',
            RemovedInDjango31Warning, stacklevel=2,
        )
        super().__init__(*args, **kwargs)
                # If the relationship's pk/to_field was changed, clear the
                # cached relationship.
                if obj and getattr(obj, field.target_field.attname) != getattr(self, field.attname):
            except FileExistsError:
                # If os.makedirs() fails with FileExistsError, the directory
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            from selenium import webdriver
import sqlparse
        return [
            sqlparse.format(statement, strip_comments=True)
            for statement in sqlparse.split(sql) if statement
        ]
                default = default.date()
                default = default.time()
                default = timezone.now()
    @classmethod
    def _effective_default(self, field):
        # This method allows testing its logic without a connection.
        return default
    def effective_default(self, field):
        """Return a field's effective database default value."""
        return field.get_db_prep_save(self._effective_default(field), self.connection)
from .exception import convert_exception_to_response
def get_exception_response(request, resolver, status_code, exception):
        signals.got_request_exception.send(sender=None, request=request)
    @staticmethod
    def _effective_default(field):
        # With MySQLdb, cursor objects have an (undocumented) "_executed"
        query = getattr(cursor, '_executed', None)
        # Unlike Psycopg's `query` and MySQLdb`'s `_executed`, CxOracle's
from django.test import SimpleTestCase, TestCase
    reorder_by = (TestCase, SimpleTestCase)
    return reordered_suite
if version < (1, 3, 13):
    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
    supports_functions_in_partial_indexes = True
    supports_functions_in_partial_indexes = Database.sqlite_version_info >= (3, 15, 0)
    def _earliest(self, *fields, field_name=None):
        Return the earliest object according to fields (if given) or by the
        model's Meta.get_latest_by.
        return self._earliest(*fields, field_name=field_name)
        return self.reverse()._earliest(*fields, field_name=field_name)
            if not inline.has_change_permission(request, obj if change else None):
class SettingsReference(str):
    """
    String subclass which references a current settings value. It's treated as
    the value in memory but serializes to a settings.NAME attribute reference.
    """
    def __new__(self, value, setting_name):
        return str.__new__(self, value)
    def __init__(self, value, setting_name):
        self.setting_name = setting_name
from django.conf import SettingsReference
VERSION = (3, 0, 0, 'alpha', 0)
from django.utils.deprecation import RemovedInDjango31Warning
        if name == 'FILE_CHARSET':
# Default charset to use for all HttpResponse objects, if a MIME type isn't
# manually specified. It's used to construct the Content-Type header.
            content_type = 'text/html; charset=%s' % self.charset
        if self.get('Content-Type', '').startswith('text/html'):
        content_type = None             # Django will use 'text/html'.
            self.base_field.from_db_value(item, expression, connection)
                expires = converter(expires, expression, connection)
                            current_expires = converter(current_expires, expression, connection)
from django.utils.deprecation import RemovedInDjango31Warning
                    converters[i] = (backend_converters + field_converters, expression)
    def _earliest(self, *fields):
        if fields:
    def earliest(self, *fields):
        return self._earliest(*fields)
    def latest(self, *fields):
        return self.reverse()._earliest(*fields)
        'GeoHash', 'Intersection', 'IsValid', 'Length', 'LineLocatePoint',
        'MakeValid', 'MemSize', 'NumGeometries', 'NumPoints', 'Perimeter',
        'PointOnSurface', 'Reverse', 'Scale', 'SnapToGrid', 'SymDifference',
        'Transform', 'Translate', 'Union',
            'ForcePolygonCW', 'LineLocatePoint', 'MakeValid', 'MemSize',
            'Perimeter', 'PointOnSurface', 'Reverse', 'Scale', 'SnapToGrid',
            'Transform', 'Translate',
        'AsGeoJSON', 'AsKML', 'AsSVG', 'Azimuth', 'ForcePolygonCW', 'GeoHash',
        'LineLocatePoint', 'MakeValid', 'MemSize', 'Scale', 'SnapToGrid',
        'Translate',
        unsupported = {'BoundingCircle', 'MemSize'}
                        inline.has_add_permission(request, obj) or
                if not inline.has_add_permission(request, obj):
            has_add_permission = inline.has_add_permission(request, obj)
        can_add = self.has_add_permission(request, obj) if request else True
    def has_add_permission(self, request, obj):
class RemovedInDjango31Warning(DeprecationWarning):
class RemovedInDjango40Warning(PendingDeprecationWarning):
RemovedInNextVersionWarning = RemovedInDjango31Warning
    iterations = 180000
        Generate a cache key for the template name and skip.
        return '-'.join(s for s in (str(template_name), skip_prefix) if s)
def check_sqlite_version():
    if Database.sqlite_version_info < (3, 8, 3):
        raise ImproperlyConfigured('SQLite 3.8.3 or later is required (found %s).' % Database.sqlite_version)
check_sqlite_version()
            args.extend(getattr(operation, 'args', []))
            keywords.update(getattr(operation, 'keywords', {}))
    The optional ``name`` argument is obsolete as of Python 3.6 and will be
    deprecated in Django 4.0 (#30127).
        self.real_func = func
    except (ModuleNotFoundError, AttributeError):
        # When module_name is an invalid dotted path, Python raises
        # ModuleNotFoundError. AttributeError is raised on PY36 (fixed in PY37)
    # Convert to list because _NamespacePath does not support indexing.
https://www.gaia-gis.it/gaia-sins/spatialite-sql-4.3.0.html
from django.contrib.gis.geos.prototypes.io import wkb_r
    select = 'CAST (AsEWKB(%s) AS BLOB)'
        if version < (4, 3, 0):
            raise ImproperlyConfigured('GeoDjango supports SpatiaLite 4.3.0 and above.')
        read = wkb_r().read
        def converter(value, expression, connection):
            return None if value is None else GEOSGeometryBase(read(value), geom_class)
        if not getattr(connection.ops, 'spatialite', False) or connection.ops.spatial_version >= (5, 0, 0):
        # of y / x, but it's ATan2(x, y) on SpatiaLite < 5.0.0.
                    'GeoDjango requires at least PostGIS version 2.2. '
    has_select_for_update_skip_locked = True
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
    warnings.warn(
        'django.utils.http.urlquote() is deprecated in favor of '
        'urllib.parse.quote().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    warnings.warn(
        'django.utils.http.urlquote_plus() is deprecated in favor of '
        'urllib.parse.quote_plus(),',
        RemovedInDjango40Warning, stacklevel=2,
    )
    warnings.warn(
        'django.utils.http.urlunquote() is deprecated in favor of '
        'urllib.parse.unquote().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    warnings.warn(
        'django.utils.http.urlunquote_plus() is deprecated in favor of '
        'urllib.parse.unquote_plus().',
        RemovedInDjango40Warning, stacklevel=2,
    )
from functools import lru_cache
@lru_cache(maxsize=None)
from functools import partial, update_wrapper, wraps
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
def smart_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    warnings.warn(
        'smart_text() is deprecated in favor of smart_str().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return smart_str(s, encoding, strings_only, errors)
def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    warnings.warn(
        'force_text() is deprecated in favor of force_str().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return force_str(s, encoding, strings_only, errors)
from django.utils.safestring import SafeString
psycopg2.extensions.register_adapter(SafeString, psycopg2.extensions.QuotedString)
from django.utils.safestring import SafeString
csrf_input_lazy = lazy(csrf_input, SafeString, str)
from django.utils.safestring import SafeData, SafeString, mark_safe
@keep_lazy(str, SafeString)
@keep_lazy(str, SafeString)
    templates to detect classes whose __str__ methods return SafeString.
class SafeString(str, SafeData):
            return SafeString(t)
SafeText = SafeString  # For backwards compatibility since Django 2.0.
    return SafeString(s)
        return capi.from_json(geom_input)
    lib_names = ['gdal203', 'gdal202', 'gdal201', 'gdal20']
    lib_names = ['gdal', 'GDAL', 'gdal2.3.0', 'gdal2.2.0', 'gdal2.1.0', 'gdal2.0.0']
get_field_as_integer64 = int64_output(lgdal.OGR_F_GetFieldAsInteger64, [c_void_p, c_int])
    lib_names = ['gdal204', 'gdal203', 'gdal202', 'gdal201', 'gdal20']
    lib_names = ['gdal', 'GDAL', 'gdal2.4.0', 'gdal2.3.0', 'gdal2.2.0', 'gdal2.1.0', 'gdal2.0.0']
from django.contrib.gis.geos.libgeos import GEOM_PTR
            raise MultiPartParserError('Invalid boundary in multipart: %s' % force_str(boundary))
        try:
            ctypes, opts = parse_header(content_type.encode('ascii'))
        except UnicodeEncodeError:
            raise MultiPartParserError('Invalid non-ASCII Content-Type in multipart: %s' % force_str(content_type))
    def __init__(self, out, ending='\n'):
            self.stderr = OutputWrapper(options['stderr'])
    def _has_any_perms_for_target_model(self, request, perms):
        """
        This method is called only when the ModelAdmin's model is for an
        ManyToManyField's implicit through model (if self.opts.auto_created).
        Return True if the user has any of the given permissions ('add',
        'change', etc.) for the model that points to the through model.
        """
        opts = self.opts
        # Find the target model of an auto-created many-to-many relationship.
        for field in opts.fields:
            if field.remote_field and field.remote_field.model != self.parent_model:
                opts = field.remote_field.model._meta
                break
        return any(
            request.user.has_perm('%s.%s' % (opts.app_label, get_permission_codename(perm, opts)))
            for perm in perms
        )
            # Auto-created intermediate models don't have their own
            # permissions. The user needs to have the change permission for the
            # related model in order to be able to do anything with the
            # intermediate model.
            return self._has_any_perms_for_target_model(request, ['change'])
            # Same comment as has_add_permission().
            return self._has_any_perms_for_target_model(request, ['change'])
            # Same comment as has_add_permission().
            return self._has_any_perms_for_target_model(request, ['change'])
            # Same comment as has_add_permission(). The 'change' permission
            # also implies the 'view' permission.
            return self._has_any_perms_for_target_model(request, ['view', 'change'])
    only_supports_unbounded_with_preceding_and_following = False
        start_, end_ = self.window_frame_rows_start_end(start, end)
        if (
            self.connection.features.only_supports_unbounded_with_preceding_and_following and
            ((start and start < 0) or (end and end > 0))
        ):
            raise NotSupportedError(
                '%s only supports UNBOUNDED together with PRECEDING and '
                'FOLLOWING.' % self.connection.display_name
            )
        return start_, end_
    only_supports_unbounded_with_preceding_and_following = True
        if (
            self.connection.features.supports_foreign_keys and
            old_field.remote_field and
            old_field.db_constraint
        ):
            self.connection.features.supports_foreign_keys and (
        if (self.connection.features.supports_foreign_keys and new_field.remote_field and
    # Does the backend use PostgreSQL-style JSON operators like '->'?
    has_json_operators = False
    has_json_operators = True
                        elif field_type == connection.features.introspected_field_types['AutoField'] + '(':
        'AutoField': 'AutoField',
        'CharField': 'CharField',
        'IntegerField': 'IntegerField',
    # Does value__d__contains={'f': 'g'} (without a list around the dict) match
    # {'d': [{'f': 'g'}]}?
    json_key_contains_list_matching_requires_list = False
    json_key_contains_list_matching_requires_list = True
    def _alter_column_type_sql(self, model, old_field, new_field, new_type):
        auto_field_types = {'AutoField', 'BigAutoField', 'SmallAutoField'}
        # Drop the identity if migrating away from AutoField.
        if (
            old_field.get_internal_type() in auto_field_types and
            new_field.get_internal_type() not in auto_field_types and
            self._is_identity_column(model._meta.db_table, new_field.column)
        ):
            self._drop_identity(model._meta.db_table, new_field.column)
        return super()._alter_column_type_sql(model, old_field, new_field, new_type)
        elif old_field.db_parameters(connection=self.connection)['type'] in serial_fields_map:
            # Drop the sequence if migrating away from AutoField.
            column = strip_quotes(new_field.column)
            sequence_name = '%s_%s_seq' % (table, column)
            fragment, _ = super()._alter_column_type_sql(model, old_field, new_field, new_type)
            return fragment, [
                (
                    self.sql_delete_sequence % {
                        'sequence': self.quote_name(sequence_name),
                    },
                    [],
                ),
            ]
if not func_supports_parameter(parse_qsl, 'max_num_fields'):
    # A hook for subclasses.
    index_default_access_method = 'btree'
                        WHEN %s THEN
        """, [self.index_default_access_method, table_name])
                basic_index = (
                    type_ == self.index_default_access_method and
                    # '_btree' references
                    # django.contrib.postgres.indexes.BTreeIndex.suffix.
                    not index.endswith('_btree') and options is None
                )
    # Can SchemaEditor alter geometry fields?
    can_alter_geometry_field = True
    can_alter_geometry_field = False  # Not implemented
    # Does it automatically index foreign keys?
    indexes_foreign_keys = True
    # Oracle can't group by LOB (large object) data types.
    allows_group_by_lob = True
    # Oracle crashes with "ORA-00932: inconsistent datatypes: expected - got
    # BLOB" when grouping by LOBs (#24096).
    allows_group_by_lob = False
    @classmethod
    def _fix_polygon(cls, poly):
        # Hook for Oracle.
        return poly
            if self._polygon_must_be_fixed(geom):
                geom = self._fix_polygon(geom)
            if any(isinstance(g, Polygon) and self._polygon_must_be_fixed(g) for g in geom):
                geom = self._fix_geometry_collection(geom)
    @staticmethod
    def _polygon_must_be_fixed(poly):
        return (
            not poly.empty and
            (
                not poly.exterior_ring.is_counterclockwise or
                any(x.is_counterclockwise for x in poly)
            )
        )
    @classmethod
    def _fix_polygon(cls, poly, clone=True):
        if clone:
            poly = poly.clone()
    @classmethod
    def _fix_geometry_collection(cls, coll):
        coll = coll.clone()
                coll[i] = cls._fix_polygon(geom, clone=False)
        return coll
    @classmethod
    def _fix_polygon(cls, poly):
        return poly
    # Does the spatial database have a geography type?
    # Does the database have a geography type?
    supports_geography = False
    supports_geography = True
            **(
                {'geography': True}
                if self.geography and connection.features.supports_geography
                else {}
            )
    # Set of options that AsGeoJSON() doesn't support.
    unsupported_geojson_options = {}
    unsupported_geojson_options = {'crs'}
    unsupported_geojson_options = {'bbox', 'crs', 'precision'}
    # Do the database functions/aggregates support the tolerance parameter?
    supports_tolerance_parameter = False
    supports_tolerance_parameter = True
    # Does Intersection() return None (rather than an empty GeometryCollection)
    # for empty results?
    empty_intersection_returns_none = True
    def empty_intersection_returns_none(self):
        return (
            not self.connection.mysql_is_mariadb and
            self.connection.mysql_version < (5, 7, 5)
        )
    empty_intersection_returns_none = False
    mariadb = False
    @cached_property
    def mariadb(self):
        return self.connection.mysql_is_mariadb
    @cached_property
    def mysql(self):
        return not self.connection.mysql_is_mariadb
import django.core.checks.compatibility.django_4_0  # NOQA isort:skip
from django.conf import settings
from .. import Error, Tags, register
@register(Tags.compatibility)
def check_csrf_trusted_origins(app_configs, **kwargs):
    errors = []
    for origin in settings.CSRF_TRUSTED_ORIGINS:
        if '://' not in origin:
            errors.append(Error(
                'As of Django 4.0, the values in the CSRF_TRUSTED_ORIGINS '
                'setting must start with a scheme (usually http:// or '
                'https://) but found %s. See the release notes for details.'
                % origin,
                id='4_0.E001',
            ))
    return errors
from django.utils.functional import cached_property
    @cached_property
    def csrf_trusted_origins_hosts(self):
        return [
            urlparse(origin).netloc.lstrip('*')
            for origin in settings.CSRF_TRUSTED_ORIGINS
        ]
                good_hosts = list(self.csrf_trusted_origins_hosts)
from collections import defaultdict
REASON_BAD_ORIGIN = "Origin checking failed - %s does not match any trusted origins."
    @cached_property
    def allowed_origins_exact(self):
        return {
            origin for origin in settings.CSRF_TRUSTED_ORIGINS
            if '*' not in origin
        }
    @cached_property
    def allowed_origin_subdomains(self):
        """
        A mapping of allowed schemes to list of allowed netlocs, where all
        subdomains of the netloc are allowed.
        """
        allowed_origin_subdomains = defaultdict(list)
        for parsed in (urlparse(origin) for origin in settings.CSRF_TRUSTED_ORIGINS if '*' in origin):
            allowed_origin_subdomains[parsed.scheme].append(parsed.netloc.lstrip('*'))
        return allowed_origin_subdomains
    def _origin_verified(self, request):
        request_origin = request.META['HTTP_ORIGIN']
        good_origin = '%s://%s' % (
            'https' if request.is_secure() else 'http',
            request.get_host(),
        )
        if request_origin == good_origin:
            return True
        if request_origin in self.allowed_origins_exact:
            return True
        try:
            parsed_origin = urlparse(request_origin)
        except ValueError:
            return False
        request_scheme = parsed_origin.scheme
        request_netloc = parsed_origin.netloc
        return any(
            is_same_domain(request_netloc, host)
            for host in self.allowed_origin_subdomains.get(request_scheme, ())
        )
            # Reject the request if the Origin header doesn't match an allowed
            # value.
            if 'HTTP_ORIGIN' in request.META:
                if not self._origin_verified(request):
                    return self._reject(request, REASON_BAD_ORIGIN % request.META['HTTP_ORIGIN'])
            elif request.is_secure():
                # If the Origin header wasn't provided, reject HTTPS requests
                # if the Referer header doesn't match an allowed value.
                #
    "SECURE_CONTENT_TYPE_NOSNIFF, SECURE_REFERRER_POLICY, "
    "SECURE_CROSS_ORIGIN_OPENER_POLICY, and SECURE_SSL_REDIRECT settings will "
    "have no effect.",
