# Lignes ajoutees par un contributeur de github.com/django/django (BSD-3-Clause)
# Extraites par experiments/construire_corpus.py — regle et provenance : corpus/devs/PROVENANCE.md
from django.db.migrations.state import ModelState, ProjectState
        pre_migrate_apps = executor._create_project_state().apps
        emit_pre_migrate_signal(
            self.verbosity, self.interactive, connection.alias, apps=pre_migrate_apps, plan=plan,
        )
            post_migrate_apps = pre_migrate_apps
            post_migrate_project_state = executor.migrate(
                targets, plan, fake=fake, fake_initial=fake_initial
            )
            post_migrate_apps = post_migrate_project_state.apps
        # Re-render models of real apps to include relationships now that
        # we've got a final state. This wouldn't be necessary if real apps
        # models were rendered with relationships in the first place.
        with post_migrate_apps.bulk_update():
            model_keys = []
            for model_state in post_migrate_apps.real_models:
                model_key = model_state.app_label, model_state.name_lower
                model_keys.append(model_key)
                post_migrate_apps.unregister_model(*model_key)
        post_migrate_apps.render_multiple([
            ModelState.from_model(apps.get_model(*model_key)) for model_key in model_keys
        ])
        emit_post_migrate_signal(
            self.verbosity, self.interactive, connection.alias, apps=post_migrate_apps, plan=plan,
        )
def emit_pre_migrate_signal(verbosity, interactive, db, **kwargs):
            using=db,
            **kwargs
        )
def emit_post_migrate_signal(verbosity, interactive, db, **kwargs):
            using=db,
            **kwargs
        )
pre_migrate = Signal(providing_args=["app_config", "verbosity", "interactive", "using", "apps", "plan"])
post_migrate = Signal(providing_args=["app_config", "verbosity", "interactive", "using", "apps", "plan"])
from django.apps import apps as global_apps
def create_permissions(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    app_label = app_config.label
        app_config = apps.get_app_config(app_label)
        ContentType = apps.get_model('contenttypes', 'ContentType')
from django.apps import apps as global_apps
def update_contenttypes(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    app_label = app_config.label
        app_config = apps.get_app_config(app_label)
    # Always clear the global content types cache.
    if apps is not global_apps:
        global_apps.get_model('contenttypes', 'ContentType').objects.clear_cache()
            # Start with get() and not get_or_create() in order to use
            # the db_for_read (see #20401).
            ct = self.get(app_label=opts.app_label, model=opts.model_name)
        except self.model.DoesNotExist:
            # Not found in the database; we proceed to create it. This time
            # use get_or_create to take care of any race conditions.
            ct, created = self.get_or_create(
                app_label=opts.app_label,
                model=opts.model_name,
from django.apps import apps as global_apps
def create_default_site(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
from django.db.models.signals import post_migrate, pre_migrate
from .management import (
    inject_rename_contenttypes_operations, update_contenttypes,
)
        pre_migrate.connect(inject_rename_contenttypes_operations, sender=self)
from django.db import DEFAULT_DB_ALIAS, migrations, router, transaction
from django.db.utils import IntegrityError
class RenameContentType(migrations.RunPython):
    def __init__(self, app_label, old_model, new_model):
        self.app_label = app_label
        self.old_model = old_model
        self.new_model = new_model
        super(RenameContentType, self).__init__(self.rename_forward, self.rename_backward)
    def _rename(self, apps, schema_editor, old_model, new_model):
        ContentType = apps.get_model('contenttypes', 'ContentType')
        db = schema_editor.connection.alias
        if not router.allow_migrate_model(db, ContentType):
            return
        try:
            content_type = ContentType.objects.db_manager(db).get_by_natural_key(self.app_label, old_model)
        except ContentType.DoesNotExist:
            pass
        else:
            content_type.model = new_model
            try:
                with transaction.atomic(using=db):
                    content_type.save(update_fields={'model'})
            except IntegrityError:
                # Gracefully fallback if a stale content type causes a
                # conflict as update_contenttypes will take care of asking the
                # user what should be done next.
                content_type.model = old_model
            else:
                # Clear the cache as the `get_by_natual_key()` call will cache
                # the renamed ContentType instance by its old model name.
                ContentType.objects.clear_cache()
    def rename_forward(self, apps, schema_editor):
        self._rename(apps, schema_editor, self.old_model, self.new_model)
    def rename_backward(self, apps, schema_editor):
        self._rename(apps, schema_editor, self.new_model, self.old_model)
def inject_rename_contenttypes_operations(plan=None, apps=global_apps, using=DEFAULT_DB_ALIAS, **kwargs):
    """
    Insert a `RenameContentType` operation after every planned `RenameModel`
    operation.
    """
    if plan is None:
        return
    # Determine whether or not the ContentType model is available.
    try:
        ContentType = apps.get_model('contenttypes', 'ContentType')
    except LookupError:
        available = False
    else:
        if not router.allow_migrate_model(using, ContentType):
            return
        available = True
    for migration, backward in plan:
        if ((migration.app_label, migration.name) == ('contenttypes', '0001_initial')):
            # There's no point in going forward if the initial contenttypes
            # migration is unapplied as the ContentType model will be
            # unavailable from this point.
            if backward:
                break
            else:
                available = True
                continue
        # The ContentType model is not available yet.
        if not available:
            continue
        inserts = []
        for index, operation in enumerate(migration.operations):
            if isinstance(operation, migrations.RenameModel):
                operation = RenameContentType(
                    migration.app_label, operation.old_name_lower, operation.new_name_lower
                )
                inserts.append((index + 1, operation))
        for inserted, (index, operation) in enumerate(inserts):
            migration.operations.insert(inserted + index, operation)
from django.apps import apps
@receiver(setting_changed)
def user_model_swapped(**kwargs):
    if kwargs['setting'] == 'AUTH_USER_MODEL':
        apps.clear_cache()
    @property
    def closed(self):
        return not self.file or self.file.closed
    def readable(self):
        if self.closed:
            return False
        if hasattr(self.file, 'readable'):
            return self.file.readable()
        return True
    def writable(self):
        if self.closed:
            return False
        if hasattr(self.file, 'writable'):
            return self.file.writable()
        return 'w' in getattr(self.file, 'mode', '')
    def seekable(self):
        if self.closed:
            return False
        if hasattr(self.file, 'seekable'):
            return self.file.seekable()
        return True
            to_attr = lookup.get_current_to_attr(level)[0]
            prefetcher, descriptor, attr_found, is_fetched = get_prefetcher(first_obj, through_attr, to_attr)
def get_prefetcher(instance, through_attr, to_attr):
    For the attribute 'through_attr' on the given instance, finds
    rel_obj_descriptor = getattr(instance.__class__, through_attr, None)
        attr_found = hasattr(instance, through_attr)
                rel_obj = getattr(instance, through_attr)
                if through_attr != to_attr:
                    is_fetched = hasattr(instance, to_attr)
                else:
                    is_fetched = through_attr in instance._prefetched_objects_cache
    def ensure_timezone(self):
        """
        Ensure the connection's timezone is set to `self.timezone_name` and
        return whether it changed or not.
        """
        return False
    def ensure_timezone(self):
        self.ensure_connection()
        conn_timezone_name = self.connection.get_parameter_status('TimeZone')
        timezone_name = self.timezone_name
        if timezone_name and conn_timezone_name != timezone_name:
            with self.connection.cursor() as cursor:
                cursor.execute(self.ops.set_time_zone_sql(), [timezone_name])
            return True
        return False
        timezone_changed = self.ensure_timezone()
        if timezone_changed:
            conn.ensure_timezone()
    # Does the backend consider quoted identifiers with different casing to
    # be equal?
    ignores_quoted_identifier_case = False
        if (old_db_table == new_db_table or
            (self.connection.features.ignores_quoted_identifier_case and
                old_db_table.lower() == new_db_table.lower())):
    # Oracle doesn't ignore quoted identifiers case but the current backend
    # does by uppercasing all identifiers.
    ignores_quoted_identifier_case = True
    ignores_quoted_identifier_case = True
        if not settings.USE_TZ:
            return field_name
        if not self._tzname_re.match(tzname):
            raise ValueError("Invalid time zone name: %s" % tzname)
        # Convert from UTC to local time, returning TIMESTAMP WITH TIME ZONE
        # and cast it back to TIMESTAMP to strip the TIME ZONE details.
        return "CAST((FROM_TZ(%s, '0:00') AT TIME ZONE '%s') AS TIMESTAMP)" % (field_name, tzname)
            sql = "CAST(%s AS DATE)" % field_name  # Cast to DATE removes sub-second precision.
    def time_trunc_sql(self, lookup_type, field_name):
        """
        Given a lookup_type of 'hour', 'minute' or 'second', returns the SQL
        that truncates the given time field field_name to a time object with
        only the given specificity.
        """
        raise NotImplementedError('subclasses of BaseDatabaseOperations may require a time_trunc_sql() method')
    def time_trunc_sql(self, lookup_type, field_name):
        fields = {
            'hour': '%%H:00:00',
            'minute': '%%H:%%i:00',
            'second': '%%H:%%i:%%s',
        }  # Use double percents to escape.
        if lookup_type in fields:
            format_str = fields[lookup_type]
            return "CAST(DATE_FORMAT(%s, '%s') AS TIME)" % (field_name, format_str)
        else:
            return "TIME(%s)" % (field_name)
    def time_trunc_sql(self, lookup_type, field_name):
        # The implementation is similar to `datetime_trunc_sql` as both
        # `DateTimeField` and `TimeField` are stored as TIMESTAMP where
        # the date part of the later is ignored.
        if lookup_type == 'hour':
            sql = "TRUNC(%s, 'HH24')" % field_name
        elif lookup_type == 'minute':
            sql = "TRUNC(%s, 'MI')" % field_name
        elif lookup_type == 'second':
            sql = "CAST(%s AS DATE)" % field_name  # Cast to DATE removes sub-second precision.
        return sql
    def time_trunc_sql(self, lookup_type, field_name):
        return "DATE_TRUNC('%s', %s)::time" % (lookup_type, field_name)
        conn.create_function("django_time_trunc", 2, _sqlite_time_trunc)
def _sqlite_time_trunc(lookup_type, dt):
    try:
        dt = backend_utils.typecast_time(dt)
    except (ValueError, TypeError):
        return None
    if lookup_type == 'hour':
        return "%02i:00:00" % dt.hour
    elif lookup_type == 'minute':
        return "%02i:%02i:00" % (dt.hour, dt.minute)
    elif lookup_type == 'second':
        return "%02i:%02i:%02i" % (dt.hour, dt.minute, dt.second)
    def time_trunc_sql(self, lookup_type, field_name):
        # sqlite doesn't support DATE_TRUNC, so we fake it with a user-defined
        # function django_date_trunc that's registered in connect(). Note that
        # single quotes are used because this is a string (and could otherwise
        # cause a collision with a field name).
        return "django_time_trunc('%s', %s)" % (lookup_type.lower(), field_name)
        elif isinstance(self.output_field, TimeField):
            sql = connection.ops.time_trunc_sql(self.kind, inner_sql)
            params = []
            raise ValueError('Trunc only valid on DateField, TimeField, or DateTimeField.')
        assert isinstance(field, (DateField, TimeField)), (
            "%r isn't a DateField, TimeField, or DateTimeField." % field.name
        if not isinstance(copy.output_field, (DateField, DateTimeField, TimeField)):
            raise ValueError('output_field must be either DateField, TimeField, or DateTimeField')
        # Passing dates or times to functions expecting datetimes is most
        # likely a mistake.
        output_field = copy.output_field
        explicit_output_field = field.__class__ != copy.output_field.__class__
                isinstance(output_field, DateTimeField) or copy.kind in ('hour', 'minute', 'second', 'time')):
            raise ValueError("Cannot truncate DateField '%s' to %s. " % (
                field.name, output_field.__class__.__name__ if explicit_output_field else 'DateTimeField'
            ))
        elif isinstance(field, TimeField) and (
                isinstance(output_field, DateTimeField) or copy.kind in ('year', 'month', 'day', 'date')):
            raise ValueError("Cannot truncate TimeField '%s' to %s. " % (
                field.name, output_field.__class__.__name__ if explicit_output_field else 'DateTimeField'
            ))
            if isinstance(self.output_field, DateField):
                value = value.date()
            elif isinstance(self.output_field, TimeField):
                value = value.time()
    kind = 'date'
    def datetime_cast_time_sql(self, field_name, tzname):
        """
        Returns the SQL necessary to cast a datetime value to time value.
        """
        raise NotImplementedError('subclasses of BaseDatabaseOperations may require a datetime_cast_time_sql() method')
    def datetime_cast_time_sql(self, field_name, tzname):
        field_name, params = self._convert_field_to_tz(field_name, tzname)
        sql = "TIME(%s)" % field_name
        return sql, params
    def datetime_cast_time_sql(self, field_name, tzname):
        # Since `TimeField` values are stored as TIMESTAMP where only the date
        # part is ignored, convert the field to the specified timezone.
        field_name = self._convert_field_to_tz(field_name, tzname)
        return field_name, []
    def datetime_cast_time_sql(self, field_name, tzname):
        field_name, params = self._convert_field_to_tz(field_name, tzname)
        sql = '(%s)::time' % field_name
        return sql, params
        conn.create_function("django_datetime_cast_time", 2, _sqlite_datetime_cast_time)
def _sqlite_datetime_cast_time(dt, tzname):
    dt = _sqlite_datetime_parse(dt, tzname)
    if dt is None:
        return None
    return dt.time().isoformat()
    def datetime_cast_time_sql(self, field_name, tzname):
        self._require_pytz()
        return "django_datetime_cast_time(%s, %%s)" % field_name, [tzname]
    TruncHour, TruncMinute, TruncMonth, TruncSecond, TruncTime, TruncYear,
    'TruncSecond', 'TruncTime', 'TruncYear',
class TruncTime(TruncBase):
    kind = 'time'
    lookup_name = 'time'
    @cached_property
    def output_field(self):
        return TimeField()
    def as_sql(self, compiler, connection):
        # Cast to date rather than truncate to date.
        lhs, lhs_params = compiler.compile(self.lhs)
        tzname = timezone.get_current_timezone_name() if settings.USE_TZ else None
        sql, tz_params = connection.ops.datetime_cast_time_sql(lhs, tzname)
        lhs_params.extend(tz_params)
        return sql, lhs_params
DateTimeField.register_lookup(TruncTime)
from django.utils.functional import cached_property, partition
                    # Special case cached_property instances because hasattr
                    # triggers attribute computation and assignment.
                    if isinstance(getattr(instance.__class__, to_attr, None), cached_property):
                        is_fetched = to_attr in instance.__dict__
                    else:
                        is_fetched = hasattr(instance, to_attr)
    has_select_for_update_skip_locked = False
    def for_update_sql(self, nowait=False, skip_locked=False):
        elif skip_locked:
            return 'FOR UPDATE SKIP LOCKED'
    has_select_for_update_skip_locked = True
from django.utils.functional import cached_property
    @cached_property
    def has_select_for_update_skip_locked(self):
        return self.connection.pg_version >= 90500
    def select_for_update(self, nowait=False, skip_locked=False):
        if nowait and skip_locked:
            raise ValueError('The nowait option cannot be used with skip_locked.')
        obj.query.select_for_update_skip_locked = skip_locked
                skip_locked = self.query.select_for_update_skip_locked
                # If we've been asked for a NOWAIT/SKIP LOCKED query but the
                # backend does not support it, raise a DatabaseError otherwise
                # we could get an unexpected deadlock.
                elif skip_locked and not self.connection.features.has_select_for_update_skip_locked:
                    raise DatabaseError('SKIP LOCKED is not supported on this database backend.')
                result.append(self.connection.ops.for_update_sql(nowait=nowait, skip_locked=skip_locked))
        self.select_for_update_skip_locked = False
        obj.select_for_update_skip_locked = self.select_for_update_skip_locked
            fake = False
            fake_initial = False
        post_migrate_project_state = executor.migrate(
            targets, plan, fake=fake, fake_initial=fake_initial
        )
        post_migrate_apps = post_migrate_project_state.apps
        pre_migrate_state = executor._create_project_state(with_applied_migrations=True)
        pre_migrate_apps = pre_migrate_state.apps
        post_migrate_state = executor.migrate(
            targets, plan=plan, state=pre_migrate_state.clone(), fake=fake,
            fake_initial=fake_initial,
        post_migrate_apps = post_migrate_state.apps
        if not self.skip_default(field) and self.effective_default(field) is not None:
    @cached_property
    def has_jsonb_datatype(self):
        return self.connection.pg_version >= 90400
            elif internal_type in ('CharField', 'TextField'):
                lookup = '%s'
from django.db.models import (
    Field, TextField, Transform, lookups as builtin_lookups,
)
    operator = '->'
    nested_operator = '#>'
            return "(%s %s %%s)" % (lhs, self.nested_operator), [key_transforms] + params
        return "(%s %s %s)" % (lhs, self.operator, lookup), params
class KeyTextTransform(KeyTransform):
    operator = '->>'
    nested_operator = '#>>'
    _output_field = TextField()
class KeyTransformTextLookupMixin(object):
    """
    Mixin for combining with a lookup expecting a text lhs from a JSONField
    key lookup. Make use of the ->> operator instead of casting key values to
    text and performing the lookup on the resulting representation.
    """
    def __init__(self, key_transform, *args, **kwargs):
        assert isinstance(key_transform, KeyTransform)
        key_text_transform = KeyTextTransform(
            key_transform.key_name, *key_transform.source_expressions, **key_transform.extra
        )
        super(KeyTransformTextLookupMixin, self).__init__(key_text_transform, *args, **kwargs)
class KeyTransformIContains(KeyTransformTextLookupMixin, builtin_lookups.IContains):
    pass
class KeyTransformStartsWith(KeyTransformTextLookupMixin, builtin_lookups.StartsWith):
    pass
class KeyTransformIStartsWith(KeyTransformTextLookupMixin, builtin_lookups.IStartsWith):
    pass
class KeyTransformEndsWith(KeyTransformTextLookupMixin, builtin_lookups.EndsWith):
    pass
class KeyTransformIEndsWith(KeyTransformTextLookupMixin, builtin_lookups.IEndsWith):
    pass
class KeyTransformRegex(KeyTransformTextLookupMixin, builtin_lookups.Regex):
    pass
class KeyTransformIRegex(KeyTransformTextLookupMixin, builtin_lookups.IRegex):
    pass
KeyTransform.register_lookup(KeyTransformIContains)
KeyTransform.register_lookup(KeyTransformStartsWith)
KeyTransform.register_lookup(KeyTransformIStartsWith)
KeyTransform.register_lookup(KeyTransformEndsWith)
KeyTransform.register_lookup(KeyTransformIEndsWith)
KeyTransform.register_lookup(KeyTransformRegex)
KeyTransform.register_lookup(KeyTransformIRegex)
            parents = model._meta.parents
                # Preserve parent reverse relationships if keep_parents=True.
                if keep_parents and related.model in parents:
                    continue
    # Setting the constraint to IMMEDIATE runs any deferred checks to allow
    # dropping it in the same transaction.
    sql_delete_fk = "SET CONSTRAINTS %(name)s IMMEDIATE; ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
from django.db import DEFAULT_DB_ALIAS, connections, router
        """Run the old syncdb-style operation on a list of app_labels."""
        with connection.cursor() as cursor:
        # Build the manifest of apps and models that are to be synchronized.
        all_models = [
            (
                app_config.label,
                router.get_migratable_models(app_config, connection.alias, include_auto_created=False),
            )
            for app_config in apps.get_app_configs()
            if app_config.models_module is not None and app_config.label in app_labels
        ]
        def model_installed(model):
            opts = model._meta
            converter = connection.introspection.table_name_converter
            return not (
                (converter(opts.db_table) in tables) or
                (opts.auto_created and converter(opts.auto_created._meta.db_table) in tables)
        manifest = OrderedDict(
            (app_name, list(filter(model_installed, model_list)))
            for app_name, model_list in all_models
        )
        # Create the tables for each model
        if self.verbosity >= 1:
            self.stdout.write("  Creating tables...\n")
        with connection.schema_editor() as editor:
            for app_name, model_list in manifest.items():
                for model in model_list:
                    # Never install unmanaged models, etc.
                    if not model._meta.can_migrate(connection):
                        continue
                    if self.verbosity >= 3:
                        self.stdout.write(
                            "    Processing %s.%s model\n" % (app_name, model._meta.object_name)
                        )
                    if self.verbosity >= 1:
                        self.stdout.write("    Creating table %s\n" % model._meta.db_table)
                    editor.create_model(model)
            # Deferred SQL is executed when exiting the editor's context.
            if self.verbosity >= 1:
                self.stdout.write("    Running deferred SQL...\n")
from django.db.transaction import TransactionManagementError, atomic
        # Don't perform the transactional DDL check if SQL is being collected
        # as it's not going to be executed anyway.
        if not self.collect_sql and self.connection.in_atomic_block and not self.connection.features.can_rollback_ddl:
            raise TransactionManagementError(
                "Executing DDL statements while in a transaction on databases "
                "that can't perform a rollback is prohibited."
            )
class KeyTransformIExact(KeyTransformTextLookupMixin, builtin_lookups.IExact):
    pass
KeyTransform.register_lookup(KeyTransformIExact)
    def _foreign_key_constraints(self, table_name, recursive=False):
        with self.connection.cursor() as cursor:
            if recursive:
                cursor.execute("""
                    SELECT
                        user_tables.table_name, rcons.constraint_name, MAX(level)
                    FROM
                        user_tables
                    JOIN
                        user_constraints cons
                        ON (user_tables.table_name = cons.table_name AND cons.constraint_type = ANY('P', 'U'))
                    LEFT JOIN
                        user_constraints rcons
                        ON (user_tables.table_name = rcons.table_name AND rcons.constraint_type = 'R')
                    START WITH user_tables.table_name = UPPER(%s)
                    CONNECT BY NOCYCLE PRIOR cons.constraint_name = rcons.r_constraint_name
                    GROUP BY
                        user_tables.table_name, rcons.constraint_name
                    HAVING user_tables.table_name != UPPER(%s)
                    ORDER BY MAX(level) DESC
                """, (table_name, table_name))
            else:
                cursor.execute("""
                    SELECT
                        cons.table_name, cons.constraint_name, 1
                    FROM
                        user_constraints cons
                    WHERE
                        cons.constraint_type = 'R'
                        AND cons.table_name = UPPER(%s)
                """, (table_name,))
            return [
                (foreign_table, constraint) for foreign_table, constraint, _ in cursor.fetchall()
            ]
            truncated_tables = {table.upper() for table in tables}
            constraints = set()
            # Oracle's TRUNCATE CASCADE only works with ON DELETE CASCADE
            # foreign keys which Django doesn't define. Emulate the
            # PostgreSQL behavior which truncates all dependent tables by
            # manually retrieving all foreign key constraints and resolving
            # dependencies.
            for table in tables:
                for foreign_table, constraint in self._foreign_key_constraints(table, recursive=allow_cascade):
                    if allow_cascade:
                        truncated_tables.add(foreign_table)
                    constraints.add((foreign_table, constraint))
            sql = [
                "%s %s %s %s %s %s %s %s;" % (
                    style.SQL_KEYWORD('ALTER'),
                    style.SQL_KEYWORD('TABLE'),
                    style.SQL_FIELD(self.quote_name(table)),
                    style.SQL_KEYWORD('DISABLE'),
                    style.SQL_KEYWORD('CONSTRAINT'),
                    style.SQL_FIELD(self.quote_name(constraint)),
                    style.SQL_KEYWORD('KEEP'),
                    style.SQL_KEYWORD('INDEX'),
                ) for table, constraint in constraints
            ] + [
                "%s %s %s;" % (
                    style.SQL_KEYWORD('TRUNCATE'),
                    style.SQL_KEYWORD('TABLE'),
                    style.SQL_FIELD(self.quote_name(table)),
                ) for table in truncated_tables
            ] + [
                "%s %s %s %s %s %s;" % (
                    style.SQL_KEYWORD('ALTER'),
                    style.SQL_KEYWORD('TABLE'),
                    style.SQL_FIELD(self.quote_name(table)),
                    style.SQL_KEYWORD('ENABLE'),
                    style.SQL_KEYWORD('CONSTRAINT'),
                    style.SQL_FIELD(self.quote_name(constraint)),
                ) for table, constraint in constraints
            ]
from collections import defaultdict
        # Models that aren't already in the cache.
        # Mapping of opts to the list of models requiring it.
        needed_opts = defaultdict(list)
                needed_opts[opts].append(model)
            # Lookup required content types from the DB.
                opts_models = needed_opts.pop(ct.model_class()._meta, [])
                for model in opts_models:
        # Create content types that weren't in the cache or DB.
        for opts, opts_models in needed_opts.items():
            for model in opts_models:
                results[model] = ct
            'base_field': self.base_field.clone(),
        httpd_cls = type('WSGIServer', (socketserver.ThreadingMixIn, server_cls), {})
    meta = type('Meta', (), {
    return type(name, (models.Model,), {
            'RelatedObjectDoesNotExist',
            'RelatedObjectDoesNotExist',
    return type(form.__name__ + 'FormSet', (formset,), attrs)
    Meta = type('Meta', bases, attrs)
    class_name = model.__name__ + 'Form'
            old_field.null and
            not new_field.null and
                UnorderedObjectListWarning,
                stacklevel=3
        obj._forced_pk = getattr(self, '_forced_pk', False)
            if not getattr(self.rhs, 'has_select_fields', True):
            if not getattr(self.rhs, 'has_select_fields', True):
                self.rhs.clear_select_clause()
                self.rhs.add_fields(['pk'])
        if self._fields and len(self._fields) > 1:
        queryset = self._clone()
    @property
    def has_select_fields(self):
        return bool(self.select or self.annotation_select_mask or self.extra_select_mask)
            if (isinstance(value, Query) and not value.has_select_fields and
    def resolve_expression(self, *args, **kwargs):
        query = self.query.resolve_expression(*args, **kwargs)
        query._db = self._db
        return query
    resolve_expression.queryset_only = True
    def resolve_expression(self, query, *args, **kwargs):
        clone = self.clone()
        # Subqueries need to use a different set of aliases than the outer query.
        clone.bump_prefix(query)
        clone.subquery = True
        # It's safe to drop ordering if the queryset isn't using slicing,
        # distinct(*fields) or select_for_update().
        if (self.low_mark == 0 and self.high_mark is None and
                not self.distinct_fields and
                not self.select_for_update):
            clone.clear_ordering(True)
        return clone
            from django.db.models.sql.query import Query  # avoid circular import
            if isinstance(self.rhs, Query):
                query = self.rhs
                # It's safe to drop ordering if the queryset isn't using
                # slicing, distinct(*fields), or select_for_update().
                if (query.low_mark == 0 and query.high_mark is None and
                        not query.distinct_fields and
                        not query.select_for_update):
                    query.clear_ordering(True)
                if not query.has_select_fields:
                    query.clear_select_clause()
                    query.add_fields(['pk'])
            if not getattr(self.rhs, 'has_select_fields', True):
                self.rhs.clear_select_clause()
                self.rhs.add_fields(['pk'])
        # It's safe to drop ordering if the queryset isn't using slicing,
        # distinct(*fields) or select_for_update().
        if (self.low_mark == 0 and self.high_mark is None and
                not self.distinct_fields and
                not self.select_for_update):
            clone.clear_ordering(True)
    def as_sql(self, compiler, connection):
        return self.get_compiler(connection=connection).as_sql()
from .signals import register_type_handlers
                register_type_handlers(conn)
        connection_created.connect(register_type_handlers)
from django.contrib.postgres.signals import register_type_handlers
        # Registering new type handlers cannot be done before the extension is
        # installed, otherwise a subsequent data migration would use the same
        # connection.
        register_type_handlers(schema_editor.connection)
import psycopg2
def register_type_handlers(connection, **kwargs):
    try:
        with connection.cursor() as cursor:
            # Retrieve oids of citext arrays.
            cursor.execute("SELECT typarray FROM pg_type WHERE typname = 'citext'")
            oids = tuple(row[0] for row in cursor)
        array_type = psycopg2.extensions.new_array_type(oids, 'citext[]', psycopg2.STRING)
        psycopg2.extensions.register_type(array_type, None)
    except ProgrammingError:
        # citext is not available on the database.
        #
        # The same comments in the except block of the above call to
        # register_hstore() also apply here.
        pass
            # Unmanaged models are excluded because they could be representing
            # database views on which the optimization might not be allowed.
            pks = {
                expr for expr in expressions
                if hasattr(expr, 'target') and expr.target.primary_key and expr.target.model._meta.managed
            }
            if self.query.subquery and extra_select:
                # If the query is used as a subquery, the extra selects would
                # result in more columns than the left-hand side expression is
                # expecting. This can happen when a subquery uses a combination
                # of order_by() and distinct(), forcing the ordering expressions
                # to be selected as well. Wrap the query in another subquery
                # to exclude extraneous selects.
                sub_selects = []
                sub_params = []
                for select, _, alias in self.select:
                    if alias:
                        sub_selects.append("%s.%s" % (
                            self.connection.ops.quote_name('subquery'),
                            self.connection.ops.quote_name(alias),
                        ))
                    else:
                        select_clone = select.relabeled_clone({select.alias: 'subquery'})
                        subselect, subparams = select_clone.as_sql(self, self.connection)
                        sub_selects.append(subselect)
                        sub_params.extend(subparams)
                return 'SELECT %s FROM (%s) AS subquery' % (
                    ', '.join(sub_selects),
                    ' '.join(result),
                ), sub_params + params
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
                    "name": self.quote_name(
                        self._create_index_name(model._meta.db_table, [new_field.column], suffix="_pk")
                    ),
                    "name": self.quote_name(
                        self._create_index_name(model._meta.db_table, [new_field.column], suffix="_check")
                    ),
    def _create_index_name(self, table_name, column_names, suffix=""):
        table_name = strip_quotes(table_name)
            "name": self.quote_name(self._create_index_name(model._meta.db_table, columns, suffix=suffix)),
            "name": self.quote_name(self._create_index_name(model._meta.db_table, [from_column], suffix=suffix)),
            "name": self.quote_name(self._create_index_name(model._meta.db_table, columns, suffix="_uniq")),
            index_name = self._create_index_name(model._meta.db_table, [old_field.column], suffix='_like')
            index_to_remove = self._create_index_name(model._meta.db_table, [old_field.column], suffix='_like')
        # Rename all references to the old table name.
        for sql in self.deferred_sql:
            if isinstance(sql, Statement):
                sql.rename_table_references(old_db_table, new_db_table)
            # Rename all references to the renamed column.
            for sql in self.deferred_sql:
                if isinstance(sql, Statement):
                    sql.rename_column_references(model._meta.db_table, old_field.column, new_field.column)
    def rename_table_references(self, old_table, new_table):
        """
        Rename all references to the old_name to the new_table.
        """
        pass
    def rename_column_references(self, table, old_column, new_column):
        """
        Rename all references to the old_column to the new_column.
        """
        pass
    def rename_table_references(self, old_table, new_table):
        if self.table == old_table:
            self.table = new_table
    def rename_column_references(self, table, old_column, new_column):
        if self.table == table:
            for index, column in enumerate(self.columns):
                if column == old_column:
                    self.columns[index] = new_column
    def rename_table_references(self, old_table, new_table):
        super().rename_table_references(old_table, new_table)
        self.to_reference.rename_table_references(old_table, new_table)
    def rename_column_references(self, table, old_column, new_column):
        super().rename_column_references(table, old_column, new_column)
        self.to_reference.rename_column_references(table, old_column, new_column)
    def rename_table_references(self, old_table, new_table):
        for part in self.parts.values():
            if hasattr(part, 'rename_table_references'):
                part.rename_table_references(old_table, new_table)
    def rename_column_references(self, table, old_column, new_column):
        for part in self.parts.values():
            if hasattr(part, 'rename_column_references'):
                part.rename_column_references(table, old_column, new_column)
        # Remove all deferred statements referencing the deleted table.
        for sql in list(self.deferred_sql):
            if isinstance(sql, Statement) and sql.references_table(model._meta.db_table):
                self.deferred_sql.remove(sql)
        # Remove all deferred statements referencing the deleted table.
        for sql in list(self.deferred_sql):
            if isinstance(sql, Statement) and sql.references_column(model._meta.db_table, field.column):
                self.deferred_sql.remove(sql)
            # Remove all deferred statements referencing the deleted table.
            for sql in list(self.deferred_sql):
                if isinstance(sql, Statement) and sql.references_table(model._meta.db_table):
                    self.deferred_sql.remove(sql)
        return copy.copy(self)
        self._db_tablespace = db_tablespace
            "db_tablespace": None,
            "db_tablespace": "_db_tablespace",
        equals_comparison = {"choices", "validators"}
    @property
    def db_tablespace(self):
        return self._db_tablespace or settings.DEFAULT_INDEX_TABLESPACE
    output_field = FloatField()
    output_field = TextField()
    output_field = TextField()
    output_field = TextField()
    output_field = TextField()
    output_field = FloatField()
    output_field = IntegerField()
    output_field = IntegerField()
    output_field = IntegerField()
    output_field = FloatField()
    def __init__(self, y, x, output_field=None, filter=None):
    output_field = IntegerField()
    output_field = UUIDField()
    output_field = DateTimeField()
    output_field = FloatField()
        super().__init__(expression, string, **extra)
    output_field = fields.DurationField()
        super().__init__(lhs, self.SUB, rhs)
    output_field = fields.FloatField()
    output_field = fields.BooleanField()
    output_field = fields.IntegerField()
    output_field = fields.DateTimeField()
    output_field = fields.IntegerField()
    DateField, DateTimeField, DurationField, Field, IntegerField, TimeField,
    output_field = IntegerField()
        class_output_field = self.__class__.output_field if isinstance(self.__class__.output_field, Field) else None
        output_field = class_output_field or copy.output_field
        has_explicit_output_field = class_output_field or field.__class__ is not copy.output_field.__class__
                field.name, output_field.__class__.__name__ if has_explicit_output_field else 'DateTimeField'
                field.name, output_field.__class__.__name__ if has_explicit_output_field else 'DateTimeField'
    output_field = DateField()
    output_field = TimeField()
    output_field = IntegerField()
            filter=filter, **extra
    output_field = FloatField()
        super().__init__(expression, **extra)
    output_field = FloatField()
        super().__init__(expression, **extra)
from django.db.utils import NotSupportedError
            raise NotSupportedError(
            raise NotSupportedError("This backend doesn't support the %s function." % func_name)
from django.db.utils import NotSupportedError, ProgrammingError
                raise NotSupportedError('PostGIS only supports geography columns with an SRID of 4326.')
from django.db.utils import NotSupportedError
            raise NotSupportedError('Area on geodetic coordinate systems not supported.')
            raise NotSupportedError("This backend doesn't support Length on geodetic fields")
            raise NotSupportedError("ST_Perimeter cannot use a non-projected non-geography field.")
            raise NotSupportedError("Perimeter cannot use a non-projected field.")
from django.db.utils import NotSupportedError, ProgrammingError
        except NotSupportedError:
        return True
        NotSupportedError.
                        raise utils.NotSupportedError(
                raise NotImplementedError("Bilateral transformations on nested querysets are not implemented.")
def subclass_exception(name, bases, module, attached_to):
    The exception is created in a way that allows it to be pickled, assuming
    that the returned exception class will be added as an attribute to the
    'attached_to' class.
    return type(name, bases, {
        '__module__': module,
        '__qualname__': '%s.%s' % (attached_to.__qualname__, name),
    })
    ``Child.parent`` is a ``ForwardManyToOneDescriptor`` instance.
    ``Restaurant.place`` is a ``ForwardOneToOneDescriptor`` instance.
    ``Place.restaurant`` is a ``ReverseOneToOneDescriptor`` instance.
    ``Parent.children`` is a ``ReverseManyToOneDescriptor`` instance.
    ``Pizza.toppings`` and ``Topping.pizzas`` are ``ManyToManyDescriptor``
        # related model might not be resolved yet; `self.field.model` might
        # still be a string model reference.
            (self.field.remote_field.model.DoesNotExist, AttributeError), {
                '__module__': self.field.model.__module__,
                '__qualname__': '%s.%s.RelatedObjectDoesNotExist' % (
                    self.field.model.__qualname__,
                    self.field.name,
                ),
            }
    def __reduce__(self):
        """
        Pickling should return the instance attached by self.field on the
        model, not a new copy of that descriptor. Use getattr() to retrieve
        the instance directly from the model.
        """
        return getattr, (self.field.model, self.field.name)
            (self.related.related_model.DoesNotExist, AttributeError), {
                '__module__': self.related.model.__module__,
                '__qualname__': '%s.%s.RelatedObjectDoesNotExist' % (
                    self.related.model.__qualname__,
                    self.related.name,
                )
            },
    def __reduce__(self):
        # Same purpose as ForwardManyToOneDescriptor.__reduce__().
        return getattr, (self.related.model, self.related.name)
from django.db.backends.utils import split_identifier
        _, table_name = split_identifier(table_name)
def split_identifier(identifier):
    Split a SQL identifier into a two element tuple of (namespace, name).
    The identifier could be a table, column, or sequence name might be prefixed
    by a namespace.
    """
    try:
        namespace, name = identifier.split('"."')
    except ValueError:
        namespace, name = '', identifier
    return namespace.strip('"'), name.strip('"')
def truncate_name(identifier, length=None, hash_len=4):
    """
    Shorten a SQL identifier to a repeatable mangled version with the given
    length.
    If a quote stripped name contains a namespace, e.g. USERNAME"."TABLE,
    namespace, name = split_identifier(identifier)
    if length is None or len(name) <= length:
        return identifier
    digest = hashlib.md5(force_bytes(name)).hexdigest()[:hash_len]
    return '%s%s%s' % ('%s"."' % namespace if namespace else '', name[:length - hash_len], digest)
            # An ancestor link will exist if this field is defined on a
            # multi-table inheritance parent of the instance's class.
            ancestor_link = instance._meta.get_ancestor_link(self.model)
            if ancestor_link:
                try:
                    # The value might be cached on an ancestor if the instance
                    # originated from walking down the inheritance chain.
                    ancestor = ancestor_link.get_cached_value(instance)
                except KeyError:
                    pass
                else:
                    value = self.get_cached_value(ancestor)
                    # Cache the ancestor value locally to speed up future
                    # lookups.
                    self.set_cached_value(instance, value)
                    return value
    def to_python(self, value):
        return self.target_field.to_python(value)
    def alter_db_table(self, model, old_db_table, new_db_table, disable_constraints=True):
        super().alter_db_table(model, old_db_table, new_db_table, disable_constraints)
    # Does it support operations requiring references rename in a transaction?
    supports_atomic_references_rename = True
    supports_atomic_references_rename = False
from django.db.transaction import atomic
from django.db.utils import NotSupportedError
    def alter_db_table(self, model, old_db_table, new_db_table, disable_constraints=True):
        if model._meta.related_objects and disable_constraints:
            if self.connection.in_atomic_block:
                raise NotSupportedError((
                    'Renaming the %r table while in a transaction is not '
                    'supported on SQLite because it would break referential '
                    'integrity. Try adding `atomic = False` to the Migration class.'
                ) % old_db_table)
            self.connection.enable_constraint_checking()
            super().alter_db_table(model, old_db_table, new_db_table)
            self.connection.disable_constraint_checking()
        else:
            super().alter_db_table(model, old_db_table, new_db_table)
    def alter_field(self, model, old_field, new_field, strict=False):
        old_field_name = old_field.name
        if (new_field.name != old_field_name and
                any(r.field_name == old_field.name for r in model._meta.related_objects)):
            if self.connection.in_atomic_block:
                raise NotSupportedError((
                    'Renaming the %r.%r column while in a transaction is not '
                    'supported on SQLite because it would break referential '
                    'integrity. Try adding `atomic = False` to the Migration class.'
                ) % (model._meta.db_table, old_field_name))
            with atomic(self.connection.alias):
                super().alter_field(model, old_field, new_field, strict=strict)
                # Follow SQLite's documented procedure for performing changes
                # that don't affect the on-disk content.
                # https://sqlite.org/lang_altertable.html#otheralter
                with self.connection.cursor() as cursor:
                    schema_version = cursor.execute('PRAGMA schema_version').fetchone()[0]
                    cursor.execute('PRAGMA writable_schema = 1')
                    table_name = model._meta.db_table
                    references_template = ' REFERENCES "%s" ("%%s") ' % table_name
                    old_column_name = old_field.get_attname_column()[1]
                    new_column_name = new_field.get_attname_column()[1]
                    search = references_template % old_column_name
                    replacement = references_template % new_column_name
                    cursor.execute('UPDATE sqlite_master SET sql = replace(sql, %s, %s)', (search, replacement))
                    cursor.execute('PRAGMA schema_version = %d' % (schema_version + 1))
                    cursor.execute('PRAGMA writable_schema = 0')
                    # The integrity check will raise an exception and rollback
                    # the transaction if the sqlite_master updates corrupt the
                    # database.
                    cursor.execute('PRAGMA integrity_check')
            # Perform a VACUUM to refresh the database representation from
            # the sqlite_master table.
            with self.connection.cursor() as cursor:
                cursor.execute('VACUUM')
        else:
            super().alter_field(model, old_field, new_field, strict=strict)
            self.alter_db_table(
                model, temp_model._meta.db_table, model._meta.db_table,
                disable_constraints=False,
            )
                condition = When(self.filter, then=source_expressions[0])
        if condition is None or not getattr(condition, 'conditional', False) or lookups:
    conditional = True
    conditional = True
    def _get_foreign_key_constraints(self, cursor, table_name):
        constraints = {}
        cursor.execute('PRAGMA foreign_key_list(%s)' % self.connection.ops.quote_name(table_name))
        for row in cursor.fetchall():
            # Remaining on_update/on_delete/match values are of no interest.
            id_, _, table, from_, to = row[:5]
            constraints['fk_%d' % id_] = {
                'columns': [from_],
                'primary_key': False,
                'unique': False,
                'foreign_key': (table, to),
                'check': False,
                'index': False,
            }
        return constraints
        constraints.update(self._get_foreign_key_constraints(cursor, table_name))
    def _is_referenced_by_fk_constraint(self, table_name, column_name=None, ignore_self=False):
        """
        Return whether or not the provided table name is referenced by another
        one. If `column_name` is specified, only references pointing to that
        column are considered. If `ignore_self` is True, self-referential
        constraints are ignored.
        """
        with self.connection.cursor() as cursor:
            for other_table in self.connection.introspection.get_table_list(cursor):
                if ignore_self and other_table.name == table_name:
                    continue
                constraints = self.connection.introspection._get_foreign_key_constraints(cursor, other_table.name)
                for constraint in constraints.values():
                    constraint_table, constraint_column = constraint['foreign_key']
                    if (constraint_table == table_name and
                            (column_name is None or constraint_column == column_name)):
                        return True
        return False
        if disable_constraints and self._is_referenced_by_fk_constraint(old_db_table):
        table_name = model._meta.db_table
        _, old_column_name = old_field.get_attname_column()
                self._is_referenced_by_fk_constraint(table_name, old_column_name, ignore_self=True)):
        hints = {'instance': self}
        db_instance_qs = self.__class__._base_manager.db_manager(using, hints=hints).filter(pk=self.pk)
                for index, (select, _, alias) in enumerate(self.select, start=1):
                    if not alias and with_col_aliases:
                        alias = 'col%d' % index
                ), tuple(sub_params + params)
    def _resolve_output_field(self):
        if len(self.queryset.query.select) == 1:
            return self.queryset.query.select[0].field
        return super()._resolve_output_field()
    prepare_rhs = False
    def _write_content(self, file, timeout, value):
        expiry = self.get_backend_timeout(timeout)
        file.write(pickle.dumps(expiry, pickle.HIGHEST_PROTOCOL))
        file.write(zlib.compress(pickle.dumps(value, pickle.HIGHEST_PROTOCOL)))
                self._write_content(f, timeout, value)
                        self._write_content(f, timeout, previous_value)
    protocol = pickle.HIGHEST_PROTOCOL
        return pickle.dumps(obj, self.protocol)
    pickle_protocol = pickle.HIGHEST_PROTOCOL
            pickled = pickle.dumps(value, self.pickle_protocol)
    pickle_protocol = pickle.HIGHEST_PROTOCOL
        file.write(pickle.dumps(expiry, self.pickle_protocol))
        file.write(zlib.compress(pickle.dumps(value, self.pickle_protocol)))
    pickle_protocol = pickle.HIGHEST_PROTOCOL
        pickled = pickle.dumps(value, self.pickle_protocol)
        pickled = pickle.dumps(value, self.pickle_protocol)
            pickled = pickle.dumps(new_value, self.pickle_protocol)
    arg_joiner = ", ' ',"
    template = '%(function)s(concat(%(expressions)s))'
                template = "%(function)s({}::regconfig, concat(%(expressions)s))".format(config_sql.replace('%', '%%'))
    def __init__(self, *, check, name):
        self.check = check
        where = query.build_where(self.check)
        return "<%s: check='%s' name=%r>" % (self.__class__.__name__, self.check, self.name)
            self.check == other.check
        return (path, (), {'check': self.check, 'name': self.name})
class BaseConstraint:
    def __init__(self, name):
        raise NotImplementedError('This method must be implemented by a subclass.')
    def deconstruct(self):
        path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        path = path.replace('django.db.models.constraints', 'django.db.models')
        return (path, (), {'name': self.name})
    def clone(self):
        _, args, kwargs = self.deconstruct()
        return self.__class__(*args, **kwargs)
class CheckConstraint(BaseConstraint):
    def __init__(self, *, check, name):
        self.check = check
        super().__init__(name)
    def constraint_sql(self, model, schema_editor):
        query = Query(model)
        where = query.build_where(self.check)
        connection = schema_editor.connection
        compiler = connection.ops.compiler('SQLCompiler')(query, connection, 'default')
        sql, params = where.as_sql(compiler, connection)
        params = tuple(schema_editor.quote_value(p) for p in params)
        return schema_editor.sql_check % {
            'name': schema_editor.quote_name(self.name),
            'check': sql % params,
        }
        path, args, kwargs = super().deconstruct()
        kwargs['check'] = self.check
        return path, args, kwargs
import inspect
def make_hashable(value):
    if isinstance(value, list):
        return tuple(map(make_hashable, value))
    if isinstance(value, dict):
        return tuple([
            (key, make_hashable(nested_value)) for key, nested_value in value.items()
        ])
    return value
    @cached_property
    def identity(self):
        constructor_signature = inspect.signature(self.__init__)
        args, kwargs = self._constructor_args
        signature = constructor_signature.bind_partial(*args, **kwargs)
        signature.apply_defaults()
        arguments = signature.arguments.items()
        identity = [self.__class__]
        for arg, value in arguments:
            if isinstance(value, fields.Field):
                value = type(value)
            else:
                value = make_hashable(value)
            identity.append((arg, value))
        return tuple(identity)
        return isinstance(other, BaseExpression) and other.identity == self.identity
        return hash(self.identity)
        if output_field is None:
            output_field = self.target_field
            while isinstance(output_field, ForeignKey):
                output_field = output_field.target_field
                if output_field is self:
                    raise ValueError('Cannot resolve output_field.')
        return super().get_col(alias, output_field)
    def _remake_table(self, model, create_field=None, delete_field=None, alter_field=None):
        self._remake_table(model)
        self._remake_table(model)
            if self.field.many_to_one:
                # Guard against field-like objects such as GenericRelation
                # that abuse create_reverse_many_to_one_manager() with reverse
                # one-to-many relationships instead and break known related
                # objects assignment.
                rel_obj_id = tuple([
                    getattr(self.instance, target_field.attname)
                    for target_field in self.field.get_path_info()[-1].target_fields
                ])
                queryset._known_related_objects = {self.field: {rel_obj_id: self.instance}}
        known_related_objects = [
            (field, related_objs, [
                operator.attrgetter(
                    field.attname
                    if from_field == 'self' else
                    queryset.model._meta.get_field(from_field).attname
                )
                for from_field in field.from_fields
            ]) for field, related_objs in queryset._known_related_objects.items()
        ]
            # Add the known related objects to the model.
            for field, rel_objs, rel_getters in known_related_objects:
                # Avoid overwriting objects loaded by, e.g., select_related().
                if field.is_cached(obj):
                    continue
                rel_obj_id = tuple([rel_getter(obj) for rel_getter in rel_getters])
                try:
                    rel_obj = rel_objs[rel_obj_id]
                except KeyError:
                    pass  # May happen in qs1 | qs2 scenarios.
                else:
                    setattr(obj, field.name, rel_obj)
from django.test.signals import setting_changed
def uninstall_if_needed(setting, value, enter, **kwargs):
    """
    Undo the effects of PostgresConfig.ready() when django.contrib.postgres
    is "uninstalled" by override_settings().
    """
    if not enter and setting == 'INSTALLED_APPS' and 'django.contrib.postgres' not in set(value):
        connection_created.disconnect(register_type_handlers)
        CharField._unregister_lookup(Unaccent)
        TextField._unregister_lookup(Unaccent)
        CharField._unregister_lookup(SearchLookup)
        TextField._unregister_lookup(SearchLookup)
        CharField._unregister_lookup(TrigramSimilar)
        TextField._unregister_lookup(TrigramSimilar)
        # Disconnect this receiver until the next time this app is installed
        # and ready() connects it again to prevent unnecessary processing on
        # each setting change.
        setting_changed.disconnect(uninstall_if_needed)
        setting_changed.connect(uninstall_if_needed)
    sql_foreign_key_constraint = "FOREIGN KEY (%(column)s) REFERENCES %(to_table)s (%(to_column)s)%(deferrable)s"
    sql_unique_constraint = "UNIQUE (%(columns)s)"
    sql_check_constraint = "CHECK (%(check)s)"
    sql_create_constraint = "ALTER TABLE %(table)s ADD %(constraint)s"
    sql_delete_constraint = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    sql_constraint = "CONSTRAINT %(name)s %(constraint)s"
    sql_create_unique = None
    sql_delete_unique = sql_delete_constraint
    sql_delete_fk = sql_delete_constraint
    sql_delete_pk = sql_delete_constraint
                definition += " " + self.sql_check_constraint % db_params
        constraints = [check.full_constraint_sql(model, self) for check in model._meta.constraints]
                self.execute(self._delete_constraint_sql(self.sql_delete_constraint, model, constraint_name))
            constraint = self.sql_constraint % {
                'name': self.quote_name(
                    self._create_index_name(model._meta.db_table, [new_field.column], suffix='_check'),
                ),
                'constraint': self.sql_check_constraint % new_db_params,
            }
                self.sql_create_constraint % {
                    'table': self.quote_name(model._meta.db_table),
                    'constraint': constraint,
    def _create_constraint_sql(self, table, name, constraint):
        constraint = Statement(self.sql_constraint, name=name, constraint=constraint)
        return Statement(self.sql_create_constraint, table=table, constraint=constraint)
    def _create_fk_sql(self, model, field, suffix):
        table = Table(model._meta.db_table, self.quote_name)
        name = ForeignKeyName(
            model._meta.db_table,
            [field.column],
            split_identifier(field.target_field.model._meta.db_table)[1],
            [field.target_field.column],
            suffix,
            create_fk_name,
        )
        column = Columns(model._meta.db_table, [field.column], self.quote_name)
        to_table = Table(field.target_field.model._meta.db_table, self.quote_name)
        to_column = Columns(field.target_field.model._meta.db_table, [field.target_field.column], self.quote_name)
        deferrable = self.connection.ops.deferrable_sql()
        constraint = Statement(
            self.sql_foreign_key_constraint,
            column=column,
            to_table=to_table,
            to_column=to_column,
            deferrable=deferrable,
        return self._create_constraint_sql(table, name, constraint)
    def _create_unique_sql(self, model, columns, name=None):
        table = Table(model._meta.db_table, self.quote_name)
        if name is None:
            name = IndexName(model._meta.db_table, columns, '_uniq', create_unique_name)
        else:
            name = self.quote_name(name)
        columns = Columns(table, columns, self.quote_name)
        if self.sql_create_unique:
            # Some databases use a different syntax for unique constraint
            # creation.
            return Statement(
                self.sql_create_unique,
                table=table,
                name=name,
                columns=columns,
            )
        constraint = Statement(self.sql_unique_constraint, columns=columns)
        return self._create_constraint_sql(table, name, constraint)
import sqlparse
            # Check constraint parsing is based of SQLite syntax diagram.
            # https://www.sqlite.org/syntaxdiagrams.html#table-constraint
            def next_ttype(ttype):
                for token in tokens:
                    if token.ttype == ttype:
                        return token
            statement = sqlparse.parse(table_schema)[0]
            tokens = statement.flatten()
            for token in tokens:
                name = None
                if token.match(sqlparse.tokens.Keyword, 'CONSTRAINT'):
                    # Table constraint
                    name_token = next_ttype(sqlparse.tokens.Literal.String.Symbol)
                    name = name_token.value[1:-1]
                    token = next_ttype(sqlparse.tokens.Keyword)
                if token.match(sqlparse.tokens.Keyword, 'CHECK'):
                    # Column check constraint
                    if name is None:
                        column_token = next_ttype(sqlparse.tokens.Literal.String.Symbol)
                        column = column_token.value[1:-1]
                        name = '__check__%s' % column
                        columns = [column]
                    else:
                        columns = []
                    constraints[name] = {
                        'check': True,
                        'columns': columns,
                        'primary_key': False,
                        'unique': False,
                        'foreign_key': False,
                        'index': False,
                    }
    sql_foreign_key_constraint = None
    def full_constraint_sql(self, model, schema_editor):
        return schema_editor.sql_constraint % {
            'name': schema_editor.quote_name(self.name),
            'constraint': self.constraint_sql(model, schema_editor),
        }
        sql = self.full_constraint_sql(model, schema_editor)
        return schema_editor.sql_create_constraint % {
            'constraint': sql,
        return schema_editor.sql_delete_constraint % {
        return schema_editor.sql_check_constraint % {'check': sql % params}
                if token.match(sqlparse.tokens.Keyword, 'UNIQUE'):
                    constraints[name] = {
                        'unique': True,
                        'columns': [],
                        'primary_key': False,
                        'foreign_key': False,
                        'check': False,
                        'index': False,
                    }
from django.db.models.constraints import CheckConstraint, UniqueConstraint
        constraints = [(self.__class__, self._meta.constraints)]
            if parent_class._meta.constraints:
                constraints.append((parent_class, parent_class._meta.constraints))
        for model_class, model_constraints in constraints:
            for constraint in model_constraints:
                if (isinstance(constraint, UniqueConstraint) and
                        not any(name in exclude for name in constraint.fields)):
                    unique_checks.append((model_class, constraint.fields))
__all__ = ['CheckConstraint', 'UniqueConstraint']
class UniqueConstraint(BaseConstraint):
    def __init__(self, *, fields, name):
        if not fields:
            raise ValueError('At least one field is required to define a unique constraint.')
        self.fields = tuple(fields)
        super().__init__(name)
    def constraint_sql(self, model, schema_editor):
        columns = (
            model._meta.get_field(field_name).column
            for field_name in self.fields
        )
        return schema_editor.sql_unique_constraint % {
            'columns': ', '.join(map(schema_editor.quote_name, columns)),
        }
    def create_sql(self, model, schema_editor):
        columns = [model._meta.get_field(field_name).column for field_name in self.fields]
        return schema_editor._create_unique_sql(model, columns, self.name)
    def __repr__(self):
        return '<%s: fields=%r name=%r>' % (self.__class__.__name__, self.fields, self.name)
    def __eq__(self, other):
        return (
            isinstance(other, UniqueConstraint) and
            self.name == other.name and
            self.fields == other.fields
        )
    def deconstruct(self):
        path, args, kwargs = super().deconstruct()
        kwargs['fields'] = self.fields
        return path, args, kwargs
from django.core.exceptions import FieldError
                try:
                    target_field = self.field.target_field
                except FieldError:
                    # The relationship has multiple target fields. Use a tuple
                    # for related object id.
                    rel_obj_id = tuple([
                        getattr(self.instance, target_field.attname)
                        for target_field in self.field.get_path_info()[-1].target_fields
                    ])
                else:
                    rel_obj_id = getattr(self.instance, target_field.attname)
            (field, related_objs, operator.attrgetter(*[
                field.attname
                if from_field == 'self' else
                queryset.model._meta.get_field(from_field).attname
            ])) for field, related_objs in queryset._known_related_objects.items()
            for field, rel_objs, rel_getter in known_related_objects:
                rel_obj_id = rel_getter(obj)
            return source_expressions + [self.filter]
        self.connection.cursor().execute('PRAGMA legacy_alter_table = ON')
        self.connection.cursor().execute('PRAGMA legacy_alter_table = OFF')
        with self.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = OFF')
            # Foreign key constraints cannot be turned off while in a multi-
            # statement transaction. Fetch the current state of the pragma
            # to determine if constraints are effectively disabled.
            enabled = cursor.execute('PRAGMA foreign_keys').fetchone()[0]
        return not bool(enabled)
        # disabled. Enforce it here for the duration of the schema edition.
        if not self.connection.disable_constraint_checking():
            raise NotSupportedError(
                'SQLite schema editor cannot be used while foreign key '
                'constraint checks are enabled. Make sure to disable them '
                'before entering a transaction.atomic() context because '
                'SQLite3 does not support disabling them in the middle of '
                'a multi-statement transaction.'
            )
from itertools import chain
        if Database.sqlite_version_info >= (3, 20, 0):
            with self.cursor() as cursor:
                if table_names is None:
                    violations = self.cursor().execute('PRAGMA foreign_key_check').fetchall()
                else:
                    violations = chain.from_iterable(
                        cursor.execute('PRAGMA foreign_key_check(%s)' % table_name).fetchall()
                        for table_name in table_names
                    )
                # See https://www.sqlite.org/pragma.html#pragma_foreign_key_check
                for table_name, rowid, referenced_table_name, foreign_key_index in violations:
                    foreign_key = cursor.execute(
                        'PRAGMA foreign_key_list(%s)' % table_name
                    ).fetchall()[foreign_key_index]
                    column_name, referenced_column_name = foreign_key[3:5]
                    primary_key_column_name = self.introspection.get_primary_key_column(cursor, table_name)
                    primary_key_value, bad_value = cursor.execute(
                        'SELECT %s, %s FROM %s WHERE rowid = %%s' % (
                            primary_key_column_name, column_name, table_name
                        ),
                        (rowid,),
                    ).fetchone()
                    raise utils.IntegrityError(
                        "The row in table '%s' with primary key '%s' has an "
                        "invalid foreign key: %s.%s contains a value '%s' that "
                        "does not have a corresponding value in %s.%s." % (
                            table_name, primary_key_value, table_name, column_name,
                            bad_value, referenced_table_name, referenced_column_name
        else:
            with self.cursor() as cursor:
                if table_names is None:
                    table_names = self.introspection.table_names(cursor)
                for table_name in table_names:
                    primary_key_column_name = self.introspection.get_primary_key_column(cursor, table_name)
                    if not primary_key_column_name:
                        continue
                    key_columns = self.introspection.get_key_columns(cursor, table_name)
                    for column_name, referenced_table_name, referenced_column_name in key_columns:
                        cursor.execute(
                            """
                            SELECT REFERRING.`%s`, REFERRING.`%s` FROM `%s` as REFERRING
                            LEFT JOIN `%s` as REFERRED
                            ON (REFERRING.`%s` = REFERRED.`%s`)
                            WHERE REFERRING.`%s` IS NOT NULL AND REFERRED.`%s` IS NULL
                            """
                            % (
                                primary_key_column_name, column_name, table_name,
                                referenced_table_name, column_name, referenced_column_name,
                                column_name, referenced_column_name,
                        for bad_row in cursor.fetchall():
                            raise utils.IntegrityError(
                                "The row in table '%s' with primary key '%s' has an "
                                "invalid foreign key: %s.%s contains a value '%s' that "
                                "does not have a corresponding value in %s.%s." % (
                                    table_name, bad_row[0], table_name, column_name,
                                    bad_row[1], referenced_table_name, referenced_column_name,
                                )
                            )
        self.connection.check_constraints()
        This follows the correct procedure to perform non-rename or column
        addition operations based on SQLite's documentation
        https://www.sqlite.org/lang_altertable.html#caution
          1. Create a table with the updated definition called "new__app_model"
          2. Copy the data from the existing "app_model" table to the new table
          3. Drop the "app_model" table
          4. Rename the "new__app_model" table to "app_model"
          5. Restore any index of the previous "app_model" table.
        # Provide isolated instances of the fields to the new model body so
        # that the existing model's internals aren't interfered with when
        # the dummy model is constructed.
        body_copy = copy.deepcopy(body)
        # Construct a new model with the new fields to allow self referential
        # primary key to resolve to. This model won't ever be materialized as a
        # table and solely exists for foreign key reference resolution purposes.
        # This wouldn't be required if the schema editor was operating on model
        # states instead of rendered models.
        body_copy['Meta'] = meta
        body_copy['__module__'] = model.__module__
        type(model._meta.object_name, model.__bases__, body_copy)
        # Construct a model with a renamed table name.
        body_copy = copy.deepcopy(body)
        meta_contents = {
            'app_label': model._meta.app_label,
            'db_table': 'new__%s' % model._meta.db_table,
            'unique_together': unique_together,
            'index_together': index_together,
            'indexes': indexes,
            'constraints': constraints,
            'apps': apps,
        }
        meta = type("Meta", (), meta_contents)
        body_copy['Meta'] = meta
        body_copy['__module__'] = model.__module__
        new_model = type('New%s' % model._meta.object_name, model.__bases__, body_copy)
        # Create a new table with the updated schema.
        self.create_model(new_model)
        # Copy data from the old table into the new table
        self.execute("INSERT INTO %s (%s) SELECT %s FROM %s" % (
            self.quote_name(new_model._meta.db_table),
            ', '.join(self.quote_name(x) for x in mapping),
            ', '.join(mapping.values()),
            self.quote_name(model._meta.db_table),
        ))
        # Delete the old table to make way for the new
        self.delete_model(model, handle_autom2m=False)
        # Rename the new table to take way for the old
        self.alter_db_table(
            new_model, new_model._meta.db_table, model._meta.db_table,
            disable_constraints=False,
        )
    supports_atomic_references_rename = Database.version_info >= (3, 26, 0)
        if (not self.connection.features.supports_atomic_references_rename and
                disable_constraints and self._is_referenced_by_fk_constraint(old_db_table)):
                    'supported on SQLite < 3.26 because it would break referential '
                not self.connection.features.supports_atomic_references_rename and
                    'supported on SQLite < 3.26 because it would break referential '
    # Deferred constraint checks can be emulated on SQLite < 3.20 but not in a
    # reasonably performant way.
    can_defer_constraint_checks = Database.version_info >= (3, 20, 0)
        # Add any field index and index_together's (deferred as SQLite _remake_table needs it)
SQLite backend for the sqlite3 module in the standard library.
                'SQLite does not support disabling them in the middle of '
    supports_partial_indexes = Database.sqlite_version_info >= (3, 8, 0)
    supports_atomic_references_rename = Database.sqlite_version_info >= (3, 26, 0)
    can_defer_constraint_checks = Database.sqlite_version_info >= (3, 20, 0)
        if self.features.supports_pragma_foreign_key_check:
    supports_pragma_foreign_key_check = Database.sqlite_version_info >= (3, 20, 0)
    can_defer_constraint_checks = supports_pragma_foreign_key_check
        super().__exit__(exc_type, exc_value, traceback)
        if tables and allow_cascade:
            # Simulate TRUNCATE CASCADE by recursively collecting the tables
            # referencing the tables to be flushed.
            query = """
            WITH tables AS (
                %s
                UNION
                SELECT sqlite_master.name
                FROM sqlite_master
                JOIN tables ON (
                    sql REGEXP %%s || tables.name || %%s
                )
            ) SELECT name FROM tables;
            """ % ' UNION '.join("SELECT '%s' name" % table for table in tables)
            params = (
                r'(?i)\s+references\s+("|\')?',
                r'("|\')?\s*\(',
            )
            with self.connection.cursor() as cursor:
                results = cursor.execute(query, params)
                tables = [row[0] for row in results.fetchall()]
from functools import lru_cache
from itertools import chain
from django.utils.functional import cached_property
    def __references_graph(self, table_name):
        query = """
        WITH tables AS (
            SELECT %s name
            UNION
            SELECT sqlite_master.name
            FROM sqlite_master
            JOIN tables ON (sql REGEXP %s || tables.name || %s)
        ) SELECT name FROM tables;
        """
        params = (
            table_name,
            r'(?i)\s+references\s+("|\')?',
            r'("|\')?\s*\(',
        )
        with self.connection.cursor() as cursor:
            results = cursor.execute(query, params)
            return [row[0] for row in results.fetchall()]
    @cached_property
    def _references_graph(self):
        # 512 is large enough to fit the ~330 tables (as of this writing) in
        # Django's test suite.
        return lru_cache(maxsize=512)(self.__references_graph)
            tables = set(chain.from_iterable(self._references_graph(table) for table in tables))
from functools import lru_cache
    def __foreign_key_constraints(self, table_name, recursive):
    @cached_property
    def _foreign_key_constraints(self):
        # 512 is large enough to fit the ~330 tables (as of this writing) in
        # Django's test suite.
        return lru_cache(maxsize=512)(self.__foreign_key_constraints)
    allow_distinct = True
    allow_distinct = True
    def __init__(self, expression, delimiter, **extra):
        super().__init__(expression, delimiter=delimiter, **extra)
        if isinstance(expression, aggregates.Aggregate) and len(expression.source_expressions) > 1:
            raise utils.NotSupportedError(
                "SQLite doesn't support DISTINCT on aggregate functions "
                "accepting multiple arguments."
            )
    template = '%(function)s(%(distinct)s%(expressions)s)'
    allow_distinct = False
    def __init__(self, *expressions, distinct=False, filter=None, **extra):
        if distinct and not self.allow_distinct:
            raise TypeError("%s does not allow distinct." % self.__class__.__name__)
        self.distinct = distinct
        super().__init__(*expressions, **extra)
        extra_context['distinct'] = 'DISTINCT' if self.distinct else ''
        if self.distinct:
            options['distinct'] = self.distinct
            options['filter'] = self.filter
    allow_distinct = True
    def __init__(self, expression, filter=None, **extra):
        super().__init__(expression, filter=filter, **extra)
    def __iter__(self):
        return iter(self.subsuites)
    def _get_databases(self, suite):
        databases = set()
        for test in suite:
            if isinstance(test, unittest.TestCase):
                test_databases = getattr(test, 'databases', None)
                if test_databases == '__all__':
                    return set(connections)
                if test_databases:
                    databases.update(test_databases)
            else:
                databases.update(self._get_databases(test))
        return databases
    def get_databases(self, suite):
        databases = self._get_databases(suite)
        if self.verbosity >= 2:
            unused_databases = [alias for alias in connections if alias not in databases]
            if unused_databases:
                print('Skipping setup of unused database(s): %s.' % ', '.join(sorted(unused_databases)))
        return databases
        databases = self.get_databases(suite)
        old_config = self.setup_databases(aliases=databases)
def setup_databases(verbosity, interactive, keepdb=False, debug_sql=False, parallel=0, aliases=None, **kwargs):
    test_databases, mirrored_aliases = get_unique_databases_and_mirrors(aliases)
def get_unique_databases_and_mirrors(aliases=None):
    if aliases is None:
        aliases = connections
        elif alias in aliases:
        if not self.is_usable():
            return False
        self.ensure_connection()
        if self.connection is None:
            return False
                        self.through(**through_defaults, **{
                        })
            if not allow_joins and len(join_list) > 1:
                raise FieldError('Joined field references are not permitted in this query')
        order is guaranteed by calling _get_deterministic_ordering() with the
        constructed ordering.
        return self._get_deterministic_ordering(ordering)
    def _get_deterministic_ordering(self, ordering):
        """
        Ensure a deterministic order across all database backends. Search for a
        single field or unique together set of fields providing a total
        ordering. If these are missing, augment the ordering with a descendant
        primary key.
        """
        ordering = list(ordering)
        ordering_fields = set()
        total_ordering_fields = {'pk'} | {
            field.attname for field in self.lookup_opts.fields
            if field.unique and not field.null
        }
        for part in ordering:
            # Search for single field providing a total ordering.
            field_name = None
            if isinstance(part, str):
                field_name = part.lstrip('-')
            elif isinstance(part, F):
                field_name = part.name
            elif isinstance(part, OrderBy) and isinstance(part.expression, F):
                field_name = part.expression.name
            if field_name:
                # Normalize attname references by using get_field().
                try:
                    field = self.lookup_opts.get_field(field_name)
                except FieldDoesNotExist:
                    # Could be "?" for random ordering or a related field
                    # lookup. Skip this part of introspection for now.
                    continue
                # Ordering by a related field name orders by the referenced
                # model's ordering. Skip this part of introspection for now.
                if field.remote_field and field_name == field.name:
                    continue
                if field.attname in total_ordering_fields:
                    break
                ordering_fields.add(field.attname)
        else:
            # No single total ordering field, try unique_together.
            for field_names in self.lookup_opts.unique_together:
                # Normalize attname references by using get_field().
                fields = [self.lookup_opts.get_field(field_name) for field_name in field_names]
                # Composite unique constraints containing a nullable column
                # cannot ensure total ordering.
                if any(field.null for field in fields):
                    continue
                if ordering_fields.issuperset(field.attname for field in fields):
                    break
            else:
                # If no set of unique fields is present in the ordering, rely
                # on the primary key to provide total ordering.
                ordering.append('-pk')
        extra_context['distinct'] = 'DISTINCT ' if self.distinct else ''
    ordered_obj.objects.db_manager(using).filter(**filter_args).bulk_update([
        ordered_obj(pk=pk, _order=order) for order, pk in enumerate(id_list)
    ], ['_order'])
    supports_over_clause = Database.sqlite_version_info >= (3, 25, 0)
from django.db.utils import NotSupportedError
        if not connection.features.supports_over_clause:
            raise NotSupportedError('This backend does not support window expressions.')
    supports_frame_range_fixed_distance = False
    supports_frame_range_fixed_distance = True
        if self.connection is None:
        def _get_missing_target_ids(self, source_field_name, target_field_name, db, objs):
            """
            Return the subset of ids of `objs` that aren't already assigned to
            this relationship.
            """
            from django.db.models import Model
            target_ids = set()
            target_field = self.through._meta.get_field(target_field_name)
            for obj in objs:
                if isinstance(obj, self.model):
                    if not router.allow_relation(obj, self.instance):
                        raise ValueError(
                            'Cannot add "%r": instance is on database "%s", '
                            'value is on database "%s"' %
                            (obj, self.instance._state.db, obj._state.db)
                        )
                    target_id = target_field.get_foreign_related_value(obj)[0]
                    if target_id is None:
                        raise ValueError(
                            'Cannot add "%r": the value for field "%s" is None' %
                            (obj, target_field_name)
                        )
                    target_ids.add(target_id)
                elif isinstance(obj, Model):
                    raise TypeError(
                        "'%s' instance expected, got %r" %
                        (self.model._meta.object_name, obj)
                    )
                else:
                    target_ids.add(obj)
            vals = self.through._default_manager.using(db).values_list(
                target_field_name, flat=True
            ).filter(**{
                source_field_name: self.related_val[0],
                '%s__in' % target_field_name: target_ids,
            })
            return target_ids.difference(vals)
                missing_target_ids = self._get_missing_target_ids(source_field_name, target_field_name, db, objs)
                            model=self.model, pk_set=missing_target_ids, using=db,
                            '%s_id' % target_field_name: target_id,
                        for target_id in missing_target_ids
                            model=self.model, pk_set=missing_target_ids, using=db,
                    # Add the ones that aren't there already. Conflicts can be
                    # ignored when the intermediary model is auto-created as
                    # the only possible collision is on the (sid_id, tid_id)
                    # tuple. The same assertion doesn't hold for user-defined
                    # intermediary models as they could have other fields
                    # causing conflicts which must be surfaced.
                    ignore_conflicts = self.through._meta.auto_created is not False
                    ], ignore_conflicts=ignore_conflicts)
        def _get_target_ids(self, target_field_name, objs):
            Return the set of ids of `objs` that the target field references.
            return target_ids
        def _get_missing_target_ids(self, source_field_name, target_field_name, db, target_ids):
            """
            Return the subset of ids of `objs` that aren't already assigned to
            this relationship.
            """
        def _get_add_plan(self, db, source_field_name):
            """
            Return a boolean triple of the way the add should be performed.
            The first element is whether or not bulk_create(ignore_conflicts)
            can be used, the second whether or not signals must be sent, and
            the third element is whether or not the immediate bulk insertion
            with conflicts ignored can be performed.
            """
            # Conflicts can be ignored when the intermediary model is
            # auto-created as the only possible collision is on the
            # (source_id, target_id) tuple. The same assertion doesn't hold for
            # user-defined intermediary models as they could have other fields
            # causing conflicts which must be surfaced.
            can_ignore_conflicts = (
                connections[db].features.supports_ignore_conflicts and
                self.through._meta.auto_created is not False
            )
            # Don't send the signal when inserting duplicate data row
            # for symmetrical reverse entries.
            must_send_signals = (self.reverse or source_field_name == self.source_field_name) and (
                signals.m2m_changed.has_listeners(self.through)
            )
            # Fast addition through bulk insertion can only be performed
            # if no m2m_changed listeners are connected for self.through
            # as they require the added set of ids to be provided via
            # pk_set.
            return can_ignore_conflicts, must_send_signals, (can_ignore_conflicts and not must_send_signals)
                target_ids = self._get_target_ids(target_field_name, objs)
                can_ignore_conflicts, must_send_signals, can_fast_add = self._get_add_plan(db, source_field_name)
                if can_fast_add:
                    self.through._default_manager.using(db).bulk_create([
                        self.through(**{
                            '%s_id' % source_field_name: self.related_val[0],
                            '%s_id' % target_field_name: target_id,
                        })
                        for target_id in target_ids
                    ], ignore_conflicts=True)
                    return
                missing_target_ids = self._get_missing_target_ids(
                    source_field_name, target_field_name, db, target_ids
                )
                    if must_send_signals:
                    # Add the ones that aren't there already.
                    ], ignore_conflicts=can_ignore_conflicts)
                    if must_send_signals:
        # getquoted() returns a quoted byte string of the adapted value.
        return psycopg2.extensions.adapt(value).getquoted().decode()
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
import inspect
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
            for alias, annotation in self.annotation_select.items():
                try:
                    inspect.getcallargs(annotation.get_group_by_cols, alias=alias)
                except TypeError:
                    annotation_class = annotation.__class__
                    msg = (
                        '`alias=None` must be added to the signature of '
                        '%s.%s.get_group_by_cols().'
                    ) % (annotation_class.__module__, annotation_class.__qualname__)
                    warnings.warn(msg, category=RemovedInDjango40Warning)
                    group_by_cols = annotation.get_group_by_cols()
                else:
                    group_by_cols = annotation.get_group_by_cols(alias=alias)
                group_by.extend(group_by_cols)
    def get_group_by_cols(self, alias=None):
    def get_group_by_cols(self, alias=None):
        if alias:
            return [Ref(alias, self)]
        return []
        self.query = queryset.query
        if len(self.query.select) == 1:
            return self.query.select[0].field
        clone.query = clone.query.clone()
        clone.query.bump_prefix(query)
                    clone.query.external_aliases.add(resolved.alias)
        resolve_all(clone.query.where)
        for key, value in clone.query.annotations.items():
                clone.query.annotations[key] = resolve(value)
                for expr in self.query.where.children
        clone.query = clone.query.relabeled_clone(change_map)
        clone.query.external_aliases.update(
            if alias not in clone.query.alias_map
        template_params['subquery'], sql_params = self.query.get_compiler(connection=connection).as_sql()
    def __init__(self, queryset, negated=False, **kwargs):
        # As a performance optimization, remove ordering since EXISTS doesn't
        # care about it, just whether or not a row matches.
        queryset = queryset.order_by()
        super().__init__(queryset, **kwargs)
        clone = self.copy()
        clone.negated = not self.negated
        return clone
    def get_source_expressions(self):
        return [self.query]
    def set_source_expressions(self, exprs):
        self.query = exprs[0]
        return self.query.output_field
    @property
    def external_aliases(self):
        return self.query.external_aliases
        template_params['subquery'], sql_params = self.query.as_sql(compiler, connection)
from django.db.models.expressions import BaseExpression, Col, F, Ref, SimpleCol
class Query(BaseExpression):
    @property
    def output_field(self):
        if len(self.select) == 1:
            return self.select[0].field
        elif len(self.annotation_select) == 1:
            return next(iter(self.annotation_select.values())).output_field
        local_recursion_limit = 67  # explicitly avoid infinite loop
        clone.where.resolve_expression(query, *args, **kwargs)
        for key, value in clone.annotations.items():
            resolved = value.resolve_expression(query, *args, **kwargs)
            if hasattr(resolved, 'external_aliases'):
                resolved.external_aliases.update(clone.alias_map)
            clone.annotations[key] = resolved
        # Outer query's aliases are considered external.
        clone.external_aliases.update(
            alias for alias, table in query.alias_map.items()
            if (
                isinstance(table, Join) and table.join_field.related_model._meta.db_table != alias
            ) or (
                isinstance(table, BaseTable) and table.table_name != table.table_alias
            )
        )
    @staticmethod
    def _resolve_rhs(rhs, query, *args, **kwargs):
        if hasattr(rhs, 'resolve_expression'):
            rhs = rhs.resolve_expression(query, *args, **kwargs)
        return rhs
    @classmethod
    def _resolve_node(cls, node, query, *args, **kwargs):
        if hasattr(node, 'children'):
            for child in node.children:
                cls._resolve_node(child, query, *args, **kwargs)
        if hasattr(node, 'rhs'):
            node.rhs = cls._resolve_rhs(node.rhs, query, *args, **kwargs)
        clone._resolve_node(clone, *args, **kwargs)
        subquery_sql, sql_params = self.query.as_sql(compiler, connection)
        template_params['subquery'] = subquery_sql[1:-1]
            return compiler.compile(value)
from django.db.models.expressions import OrderBy, Random, RawSQL, Ref
        sql, params = self.get_compiler(connection=connection).as_sql()
        if self.subquery:
            sql = '(%s)' % sql
        return sql, params
        if hasattr(values, 'resolve_expression'):
        if hasattr(self.rhs, 'resolve_expression'):
            return self.rhs
        if hasattr(self.rhs, 'resolve_expression'):
            return self.rhs
from django.db.models.expressions import (
    BaseExpression, Col, F, OuterRef, Ref, SimpleCol,
)
        filter_lhs, filter_rhs = filter_expr
        if isinstance(filter_rhs, F):
            filter_expr = (filter_lhs, OuterRef(filter_rhs.name))
    BaseExpression, Col, F, OuterRef, Ref, SimpleCol, Subquery,
            elif isinstance(expr, (Col, Subquery)) or (expr.contains_aggregate and not expr.is_summary):
                # Reference to column, subquery, or another aggregate. Make
                # sure the expression is selected and reuse its alias if so.
                for col_alias, selected_annotation in self.annotation_select.items():
                    if selected_annotation == expr:
                        break
                else:
                    col_cnt += 1
                    col_alias = '__col%d' % col_cnt
                    self.annotations[col_alias] = expr
                    self.append_annotation_mask([col_alias])
        existing_annotations = [
        ]
        if (isinstance(self.group_by, tuple) or has_limit or existing_annotations or
            inner_query.set_annotation_mask(self.annotation_select)
                has_existing_aggregate_annotations = any(
                    annotation for annotation in existing_annotations
                    if getattr(annotation, 'contains_aggregate', True)
                )
                if inner_query.default_cols and has_existing_aggregate_annotations:
                annotation_select_mask = inner_query.annotation_select_mask
                    annotation_select_mask.remove(alias)
    BaseExpression, Col, F, OuterRef, Ref, SimpleCol,
            else:
                # Reuse aliases of expressions already selected in subquery.
                        new_expr = Ref(col_alias, expr)
                    # An expression that is not selected the subquery.
                    if isinstance(expr, Col) or (expr.contains_aggregate and not expr.is_summary):
                        # Reference column or another aggregate. Select it
                        # under a non-conflicting alias.
                        col_cnt += 1
                        col_alias = '__col%d' % col_cnt
                        self.annotations[col_alias] = expr
                        self.append_annotation_mask([col_alias])
                        new_expr = Ref(col_alias, expr)
                    else:
                        # Some other expression not referencing database values
                        # directly. Its subexpression might contain Cols.
                        new_expr, col_cnt = self.rewrite_cols(expr, col_cnt)
import sys
        # Explicitly avoid infinite loop. The constant divider is based on how
        # much depth recursive subquery references add to the stack. This value
        # might need to be adjusted when adding or removing function calls from
        # the code path in charge of performing these operations.
        local_recursion_limit = sys.getrecursionlimit() // 16
                raise RecursionError(
                signals.post_delete.has_listeners(model)):
from itertools import chain
    def _has_signal_listeners(self, model):
        return (
            signals.pre_delete.has_listeners(model) or
            signals.post_delete.has_listeners(model)
        )
        if self._has_signal_listeners(model):
                    else:
                        related_model = related.related_model
                        # Non-referenced fields can be deferred if no signal
                        # receivers are connected for the related model as
                        # they'll never be exposed to the user. Skip field
                        # deferring when some relationships are select_related
                        # as interactions between both features are hard to
                        # get right. This should only happen in the rare
                        # cases where .related_objects is overridden anyway.
                        if not (sub_objs.query.select_related or self._has_signal_listeners(related_model)):
                            referenced_fields = set(chain.from_iterable(
                                (rf.attname for rf in rel.field.foreign_related_fields)
                                for rel in get_candidate_relations_to_delete(related_model._meta)
                            ))
                            sub_objs = sub_objs.only(*tuple(referenced_fields))
                        if sub_objs:
                            field.remote_field.on_delete(self, field, sub_objs, self.using)
from django.db.models import CharField, Field, FloatField, TextField
from django.db.models.functions import Cast, Coalesce
    arg_joiner = " || ' ' || "
        resolved.set_source_expressions([
            Coalesce(
                expression
                if isinstance(expression.output_field, (CharField, TextField))
                else Cast(expression, TextField()),
                Value('')
            ) for expression in resolved.get_source_expressions()
        ])
                template = '%(function)s({}::regconfig, %(expressions)s)'.format(config_sql.replace('%', '%%'))
            return "'%s'" % value.replace("\'", "\'\'").replace('%', '%%')
        if isinstance(value, str):
            value = value.replace('%', '%%')
        # Avoid the extract operation if the rhs is a direct value to allow
        # indexes to be used.
        if self.rhs_is_direct_value():
            # Skip the extract part by directly using the originating field,
            # that is self.lhs.lhs.
            lhs_sql, params = self.process_lhs(compiler, connection, self.lhs.lhs)
            bounds = self.year_lookup_bounds(connection, self.rhs)
            params.extend(bounds)
            return '%s BETWEEN %%s AND %%s' % lhs_sql, params
        return super().as_sql(compiler, connection)
        # Avoid the extract operation if the rhs is a direct value to allow
        # indexes to be used.
        if self.rhs_is_direct_value():
            # Skip the extract part by directly using the originating field,
            # that is self.lhs.lhs.
            lhs_sql, params = self.process_lhs(compiler, connection, self.lhs.lhs)
            rhs_sql, _ = self.process_rhs(compiler, connection)
            rhs_sql = self.get_rhs_op(connection, rhs_sql)
            start, finish = self.year_lookup_bounds(connection, self.rhs)
            params.append(self.get_bound(start, finish))
            return '%s %s' % (lhs_sql, rhs_sql), params
        return super().as_sql(compiler, connection)
class YearGt(YearComparisonLookup, GreaterThan):
class YearGte(YearComparisonLookup, GreaterThanOrEqual):
class YearLt(YearComparisonLookup, LessThan):
class YearLte(YearComparisonLookup, LessThanOrEqual):
            rhs_sql = self.get_direct_rhs_sql(connection, rhs_sql)
            params.extend(self.get_bound_params(start, finish))
    def get_direct_rhs_sql(self, connection, rhs):
    def get_bound_params(self, start, finish):
            'subclasses of YearLookup must provide a get_bound_params() method'
    def get_direct_rhs_sql(self, connection, rhs):
        return 'BETWEEN %s AND %s'
    def get_bound_params(self, start, finish):
        return (start, finish)
class YearGt(YearLookup, GreaterThan):
    def get_bound_params(self, start, finish):
        return (finish,)
class YearGte(YearLookup, GreaterThanOrEqual):
    def get_bound_params(self, start, finish):
        return (start,)
class YearLt(YearLookup, LessThan):
    def get_bound_params(self, start, finish):
        return (start,)
class YearLte(YearLookup, LessThanOrEqual):
    def get_bound_params(self, start, finish):
        return (finish,)
        elif not doseq or isinstance(value, (str, bytes)):
                if value.name and value.model:
                    value = (value.model._meta.label, value.name)
                else:
                    value = type(value)
    def get_migratable_models(self):
        from django.apps import apps
        from django.db import router
        return (
            model
            for app_config in apps.get_app_configs()
            for model in router.get_migratable_models(app_config, self.connection.alias)
            if model._meta.can_migrate(self.connection)
        )
        for model in self.get_migratable_models():
            if not model._meta.managed:
                continue
            tables.add(model._meta.db_table)
            tables.update(
                f.m2m_db_table() for f in model._meta.local_many_to_many
                if f.remote_field.through._meta.managed
            )
            m for m in self.get_migratable_models()
            for model in self.get_migratable_models():
                if not model._meta.managed:
                    continue
                if model._meta.swapped:
                    continue
                sequence_list.extend(self.get_sequences(cursor, model._meta.db_table, model._meta.local_fields))
                for f in model._meta.local_many_to_many:
                    # If this is an m2m using an intermediate table,
                    # we don't need to reset the sequence.
                    if f.remote_field.through._meta.auto_created:
                        sequence = self.get_sequences(cursor, f.m2m_db_table())
                        sequence_list.extend(sequence or [{'table': f.m2m_db_table(), 'column': None}])
            if (
                connection.features.supports_table_check_constraints or
                'supports_table_check_constraints' in cls._meta.required_db_features
            ):
        lhs = compiler.compile(self.lhs)
        rhs = compiler.compile(self.rhs)
        if not compiler.query.subquery:
            return compiler.connection.ops.select % sql, params
        return sql, params
    def select_format(self, compiler, sql, params):
        """
        Custom format for select clauses. For example, EXISTS expressions need
        to be wrapped in CASE WHEN on Oracle.
        """
        return self.output_field.select_format(compiler, sql, params)
                sql, params = self.compile(col)
            else:
                sql, params = col.select_format(self, sql, params)
    def compile(self, node):
            ann_sql, ann_params = self.compile(annotation)
            ann_sql, ann_params = annotation.select_format(self, ann_sql, ann_params)
    # Does the backend support boolean expressions in the SELECT clause?
    supports_boolean_expr_in_select_clause = True
    supports_boolean_expr_in_select_clause = False
    def select_format(self, compiler, sql, params):
        # Wrap EXISTS() with a CASE WHEN expression if a database backend
        # (e.g. Oracle) doesn't support boolean expression in the SELECT list.
        if not compiler.connection.features.supports_boolean_expr_in_select_clause:
            sql = 'CASE WHEN {} THEN 1 ELSE 0 END'.format(sql)
    def as_oracle(self, compiler, connection):
        # Oracle doesn't allow ORDER BY EXISTS() unless it's wrapped in
        # a CASE WHEN.
        if isinstance(self.expression, Exists):
            copy = self.copy()
            # XXX: Use Case(When(self.lhs)) once support for boolean
            # expressions is added to When.
            exists_sql, params = compiler.compile(self.expression)
            case_sql = 'CASE WHEN %s THEN 1 ELSE 0 END' % exists_sql
            copy.expression = RawSQL(case_sql, params)
            return copy.as_sql(compiler, connection)
        return self.as_sql(compiler, connection)
from django.db.models.expressions import Exists, Func, RawSQL, Value
    def as_oracle(self, compiler, connection):
        # Oracle doesn't allow EXISTS() to be compared to another expression
        # unless it's wrapped in a CASE WHEN.
        wrapped = False
        exprs = []
        for expr in (self.lhs, self.rhs):
            if isinstance(expr, Exists):
                # XXX: Use Case(When(self.lhs)) once support for boolean
                # expressions is added to When.
                sql, params = compiler.compile(expr)
                sql = 'CASE WHEN %s THEN 1 ELSE 0 END' % sql
                expr = RawSQL(sql, params)
                wrapped = True
            exprs.append(expr)
        lookup = type(self)(*exprs) if wrapped else self
        return lookup.as_sql(compiler, connection)
    def _resolve_leaf(expr, query, *args, **kwargs):
        if hasattr(expr, 'resolve_expression'):
            expr = expr.resolve_expression(query, *args, **kwargs)
        return expr
        if hasattr(node, 'lhs'):
            node.lhs = cls._resolve_leaf(node.lhs, query, *args, **kwargs)
            node.rhs = cls._resolve_leaf(node.rhs, query, *args, **kwargs)
    # Does the backend support expressions for specifying distance in the
    # dwithin lookup?
    supports_dwithin_distance_expr = True
    supports_dwithin_distance_expr = False
from django.contrib.gis.measure import Distance
from django.db import NotSupportedError
    sql_template = '%(func)s(%(lhs)s, %(rhs)s, %(value)s)'
    def process_distance(self, compiler, connection):
        dist_param = self.rhs_params[0]
        if (
            not connection.features.supports_dwithin_distance_expr and
            hasattr(dist_param, 'resolve_expression') and
            not isinstance(dist_param, Distance)
        ):
            raise NotSupportedError(
                'This backend does not support expressions for specifying '
                'distance in the dwithin lookup.'
            )
        return super().process_distance(compiler, connection)
        if not isinstance(self.lhs, MultiColSource) and not hasattr(self.rhs, 'resolve_expression'):
        if isinstance(filter_rhs, OuterRef):
            filter_expr = (filter_lhs, OuterRef(filter_rhs))
        elif isinstance(filter_rhs, F):
        where = query.build_where(self.condition)
        sql, params = where.as_sql(compiler, schema_editor.connection)
        return sql % tuple(schema_editor.quote_value(p) for p in params)
        return '(%s -> %%s)' % lhs, tuple(params) + (self.key_name,)
        return '(%s %s %%s)' % (lhs, self.operator), tuple(params) + (lookup,)
import copy
        if self.select_related is not False:
            # Use deepcopy because select_related stores fields in nested
            # dicts.
            obj.select_related = copy.deepcopy(obj.select_related)
from collections import Counter, defaultdict
from functools import partial
        self.data = defaultdict(set)
        # {model: {(field, value): {instances}}}
        self.field_updates = defaultdict(partial(defaultdict, set))
        self.dependencies = defaultdict(set)  # {model: {models}}
        instances = self.data[model]
            self.dependencies[source._meta.concrete_model].add(model._meta.concrete_model)
        self.field_updates[model][field, value].update(objs)
        if not collect_related:
            return
        if keep_parents:
            parents = set(model._meta.get_parent_list())
        for related in get_candidate_relations_to_delete(model._meta):
            # Preserve parent reverse relationships if keep_parents=True.
            if keep_parents and related.model in parents:
                continue
            field = related.field
            if field.remote_field.on_delete == DO_NOTHING:
                continue
            batches = self.get_del_batches(new_objs, field)
            for batch in batches:
                sub_objs = self.related_objects(related, batch)
                if self.can_fast_delete(sub_objs, from_field=field):
                    self.fast_deletes.append(sub_objs)
                else:
                    related_model = related.related_model
                    # Non-referenced fields can be deferred if no signal
                    # receivers are connected for the related model as
                    # they'll never be exposed to the user. Skip field
                    # deferring when some relationships are select_related
                    # as interactions between both features are hard to
                    # get right. This should only happen in the rare
                    # cases where .related_objects is overridden anyway.
                    if not (sub_objs.query.select_related or self._has_signal_listeners(related_model)):
                        referenced_fields = set(chain.from_iterable(
                            (rf.attname for rf in rel.field.foreign_related_fields)
                            for rel in get_candidate_relations_to_delete(related_model._meta)
                        ))
                        sub_objs = sub_objs.only(*tuple(referenced_fields))
                    if sub_objs:
                        field.remote_field.on_delete(self, field, sub_objs, self.using)
        for field in model._meta.private_fields:
            if hasattr(field, 'bulk_related_objects'):
                # It's something like generic foreign key.
                sub_objs = field.bulk_related_objects(new_objs, self.using)
                self.collect(sub_objs, source=model, nullable=True)
    def related_objects(self, related_model, related_fields, objs):
        qs = super().related_objects(related_model, related_fields, objs)
        return qs.select_related(*[related_field.name for related_field in related_fields])
import operator
from functools import partial, reduce
from django.db.models import query_utils, signals, sql
            model = objs._meta.model
    def get_del_batches(self, objs, fields):
        field_names = [field.name for field in fields]
            connections[self.using].ops.bulk_batch_size(field_names, objs), 1)
        model_fast_deletes = defaultdict(list)
            related_model = related.related_model
            if self.can_fast_delete(related_model, from_field=field):
                model_fast_deletes[related_model].append(field)
                continue
            batches = self.get_del_batches(new_objs, [field])
                sub_objs = self.related_objects(related_model, [field], batch)
                # Non-referenced fields can be deferred if no signal receivers
                # are connected for the related model as they'll never be
                # exposed to the user. Skip field deferring when some
                # relationships are select_related as interactions between both
                # features are hard to get right. This should only happen in
                # the rare cases where .related_objects is overridden anyway.
                if not (sub_objs.query.select_related or self._has_signal_listeners(related_model)):
                    referenced_fields = set(chain.from_iterable(
                        (rf.attname for rf in rel.field.foreign_related_fields)
                        for rel in get_candidate_relations_to_delete(related_model._meta)
                    ))
                    sub_objs = sub_objs.only(*tuple(referenced_fields))
                if sub_objs:
                    field.remote_field.on_delete(self, field, sub_objs, self.using)
        for related_model, related_fields in model_fast_deletes.items():
            batches = self.get_del_batches(new_objs, related_fields)
            for batch in batches:
                sub_objs = self.related_objects(related_model, related_fields, batch)
                self.fast_deletes.append(sub_objs)
    def related_objects(self, related_model, related_fields, objs):
        Get a QuerySet of the related model to objs via related fields.
        predicate = reduce(operator.or_, (
            query_utils.Q(**{'%s__in' % related_field.name: objs})
            for related_field in related_fields
        ))
        return related_model._base_manager.using(self.using).filter(predicate)
        if connection.Database.sqlite_version_info < (3, 30, 0):
            if self.nulls_last:
                template = '%(expression)s IS NULL, %(expression)s %(ordering)s'
            elif self.nulls_first:
                template = '%(expression)s IS NOT NULL, %(expression)s %(ordering)s'
    def as_sql(self):
        if self.single_alias:
            return super().as_sql()
        # MySQL and MariaDB < 10.3.2 doesn't support deletion with a subquery
        # which is what the default implementation of SQLDeleteCompiler uses
        # when multiple tables are involved. Use the MySQL/MariaDB specific
        # DELETE table FROM table syntax instead to avoid performing the
        # operation in two queries.
        result = [
            'DELETE %s FROM' % self.quote_name_unless_alias(
                self.query.get_initial_alias()
            )
        ]
        from_sql, from_params = self.get_from_clause()
        result.extend(from_sql)
        where, params = self.compile(self.query.where)
        if where:
            result.append('WHERE %s' % where)
        return ' '.join(result), tuple(from_params) + tuple(params)
        query = self.query.clone()
        query.__class__ = sql.DeleteQuery
        cursor = query.get_compiler(using).execute_sql(CURSOR)
        return cursor.rowcount if cursor else 0
from django.db.models.query_utils import (
    Q, QueryWrapper, select_related_descend,
)
from django.utils.functional import cached_property
    @cached_property
    def single_alias(self):
        return sum(self.query.alias_refcount[t] > 0 for t in self.query.alias_map) == 1
    def _as_sql(self, query):
        result = [
            'DELETE FROM %s' % self.quote_name_unless_alias(query.base_table)
        ]
        where, params = self.compile(query.where)
        if where:
            result.append('WHERE %s' % where)
        return ' '.join(result), tuple(params)
        if self.single_alias:
            return self._as_sql(self.query)
        innerq = self.query.clone()
        innerq.__class__ = Query
        innerq.clear_select_clause()
        pk = self.query.model._meta.pk
        innerq.select = [
            pk.get_col(self.query.get_initial_alias())
        ]
        outerq = Query(self.query.model)
        outerq.where = self.query.where_class()
        outerq.add_q(Q(pk__in=innerq))
        return self._as_sql(outerq)
        if self.connection.features.update_can_self_select or self.single_alias:
            template = 'ISNULL(%(expression)s), %(expression)s %(ordering)s '
from django.db.models.query_utils import Q, select_related_descend
                RawSQL('%s = %s' % (lhs_sql, rhs), lhs_params), 'AND')
from django.db.models.query_utils import FilteredRelation, Q
                raise exceptions.FieldDoesNotExist(
                    'Raw query must include the primary key'
                )
import warnings
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.utils.deprecation import RemovedInDjango40Warning
class InvalidQueryType(type):
    @property
    def _subclasses(self):
        return (FieldDoesNotExist, FieldError)
    def __warn(self):
        warnings.warn(
            'The InvalidQuery exception class is deprecated. Use '
            'FieldDoesNotExist or FieldError instead.',
            category=RemovedInDjango40Warning,
            stacklevel=4,
        )
    def __instancecheck__(self, instance):
        self.__warn()
        return isinstance(instance, self._subclasses) or super().__instancecheck__(instance)
    def __subclasscheck__(self, subclass):
        self.__warn()
        return issubclass(subclass, self._subclasses) or super().__subclasscheck__(subclass)
class InvalidQuery(Exception, metaclass=InvalidQueryType):
                msg = (
                    'Field %s.%s cannot be both deferred and traversed using '
                    'select_related at the same time.'
                ) % (field.model._meta.object_name, field.name)
                raise FieldError(msg)
            expression = expression.resolve_expression(query=query)
        query = Query(model, alias_cols=False)
        query = Query(model=model, alias_cols=False)
        query = Query(model=model, alias_cols=False)
                           summarize=False, for_save=False):
        return query.resolve_ref(self.name, allow_joins, reuse, summarize)
    def resolve_expression(self, *args, **kwargs):
        alias, target = self.alias, self.target
        identifiers = (alias, str(target)) if alias else (str(target),)
        return '{}({})'.format(self.__class__.__name__, ', '.join(identifiers))
        alias, column = self.alias, self.target.column
        identifiers = (alias, column) if alias else (column,)
        sql = '.'.join(map(compiler.quote_name_unless_alias, identifiers))
        return sql, []
        if self.alias is None:
            return self
        query = Query(model=model, alias_cols=False)
from django.db.models.expressions import BaseExpression, Col, F, OuterRef, Ref
    def __init__(self, model, where=WhereNode, alias_cols=True):
        # Whether to provide alias to columns during reference resolving.
        self.alias_cols = alias_cols
    def _get_col(self, target, field, alias):
        if not self.alias_cols:
            alias = None
        return target.get_col(alias, field)
    def resolve_lookup_value(self, value, can_reuse, allow_joins):
            value = value.resolve_expression(
                self, reuse=can_reuse, allow_joins=allow_joins,
            )
                self.resolve_lookup_value(sub_value, can_reuse, allow_joins)
                     reuse_with_filtered_relation=False):
        value = self.resolve_lookup_value(value, can_reuse, allow_joins)
                col = self._get_col(targets[0], join_info.final_field, alias)
            col = self._get_col(targets[0], join_info.final_field, alias)
                col = self._get_col(targets[0], join_info.targets[0], alias)
        return self._add_q(q_object, used_aliases=set(), allow_joins=False)[0]
               current_negated=False, allow_joins=True, split_subq=True):
                    current_negated, allow_joins, split_subq)
                    split_subq=split_subq,
    def resolve_ref(self, name, allow_joins=True, reuse=None, summarize=False):
            return self._get_col(targets[0], join_info.targets[0], join_list[-1])
from django.db.models.sql.where import WhereNode
        if isinstance(expression, (Exists, WhereNode)):
        if isinstance(expression, ExpressionWrapper) and expression.conditional:
            return self.conditional_expression_supported_in_where_clause(expression.expression)
    def as_sql(self, compiler, connection):
        # Avoid comparison against direct rhs if lhs is a boolean value. That
        # turns "boolfield__exact=True" into "WHERE boolean_field" instead of
        # "WHERE boolean_field = True" when allowed.
        if (
            isinstance(self.rhs, bool) and
            getattr(self.lhs, 'conditional', False) and
            connection.ops.conditional_expression_supported_in_where_clause(self.lhs)
        ):
            lhs_sql, params = self.process_lhs(compiler, connection)
            template = '%s' if self.rhs else 'NOT %s'
            return template % lhs_sql, params
        return super().as_sql(compiler, connection)
            condition = self.build_lookup(['exact'], filter_expr.resolve_expression(self), True)
        if not getattr(check, 'conditional', False):
            raise TypeError(
                'CheckConstraint.check must be a Q instance or boolean '
                'expression.'
            )
        if isinstance(filter_expr, Q):
            return self._add_q(
                filter_expr,
                branch_negated=branch_negated,
                current_negated=current_negated,
                used_aliases=can_reuse,
                allow_joins=allow_joins,
                split_subq=split_subq,
            )
            condition = self.build_lookup(
                ['exact'], filter_expr.resolve_expression(self, allow_joins=allow_joins), True
            )
    def build_where(self, filter_expr):
        return self.build_filter(filter_expr, allow_joins=False)[0]
            child_clause, needed_inner = self.build_filter(
                child, can_reuse=used_aliases, branch_negated=branch_negated,
                current_negated=current_negated, allow_joins=allow_joins,
                split_subq=split_subq,
            )
            joinpromoter.add_votes(needed_inner)
        if hasattr(filter_expr, 'resolve_expression'):
            if not getattr(filter_expr, 'conditional', False):
                raise TypeError('Cannot filter against a non-conditional expression.')
                    target_ids.add(target_field.get_prep_value(obj))
        template_params['mask'] = sql_params[-1]
        return super().as_sql(connection, lookup, template_params, sql_params[:-1])
        lhs_sql, lhs_params = self.process_lhs(compiler, connection)
        sql_params = (*lhs_params, *rhs_params)
def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()
        email_field_name = UserModel.get_email_field_name()
            '%s__iexact' % email_field_name: email,
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )
        email_field_name = UserModel.get_email_field_name()
            user_email = getattr(user, email_field_name)
                'email': user_email,
                user_email, html_email_template_name=html_email_template_name,
        return self.query.get_external_cols()
        ref_sources = {
            expr.source for expr in expressions if isinstance(expr, Ref)
        }
            # Skip members of the select clause that are already included
            # by reference.
            if expr in ref_sources:
                continue
                    self.query.external_aliases.get(name) and name not in self.query.table_map)):
        # Map external tables to whether they are aliased.
        self.external_aliases = {}
        self.external_aliases = {
            # Table is aliased or it's being changed and thus is aliased.
            change_map.get(alias, alias): (aliased or alias in change_map)
            for alias, aliased in self.external_aliases.items()
        }
                resolved.external_aliases.update(clone.external_aliases)
        for alias, table in query.alias_map.items():
            clone.external_aliases[alias] = (
                (isinstance(table, Join) and table.join_field.related_model._meta.db_table != alias) or
                (isinstance(table, BaseTable) and table.table_name != table.table_alias)
    def get_external_cols(self):
        exprs = chain(self.annotations.values(), self.where.children)
        return [
            col for col in self._gen_cols(exprs)
            if col.alias in self.external_aliases
        ]
    def _gen_cols(cls, exprs):
                yield expr
                yield from cls._gen_cols(expr.get_source_expressions())
    @classmethod
    def _gen_col_aliases(cls, exprs):
        yield from (expr.alias for expr in cls._gen_cols(exprs))
            query.external_aliases[alias] = True
                # Disable GROUP BY aliases to avoid orphaning references to the
                # SELECT clause which is about to be cleared.
                q.set_group_by(allow_aliases=False)
    def set_group_by(self, allow_aliases=True):
                    if not allow_aliases:
                        alias = None
            not raw and
            return '(%s - %s)' % (lhs_sql, rhs_sql), (*lhs_params, *rhs_params)
                }, (*lhs_params, *rhs_params)
            ) % {'lhs': lhs_sql, 'rhs': rhs_sql}, tuple(lhs_params) * 2 + tuple(rhs_params) * 2
        params = (*lhs_params, *rhs_params)
        return "TIMESTAMPDIFF(MICROSECOND, %s, %s)" % (rhs_sql, lhs_sql), params
            params = (*lhs_params, *rhs_params)
            return "NUMTODSINTERVAL(TO_NUMBER(%s - %s), 'DAY')" % (lhs_sql, rhs_sql), params
            params = (*lhs_params, *rhs_params)
            return "(interval '1 day' * (%s - %s))" % (lhs_sql, rhs_sql), params
        params = (*lhs_params, *rhs_params)
            return 'django_time_diff(%s, %s)' % (lhs_sql, rhs_sql), params
        return 'django_timestamp_diff(%s, %s)' % (lhs_sql, rhs_sql), params
from django.db.models import Value
    template = '%(function)s(%(distinct)s%(expressions)s %(ordering)s)'
        delimiter_expr = Value(str(delimiter))
        super().__init__(expression, delimiter_expr, **extra)
    def __init__(self, *expressions, ordering=(), **extra):
        super().__init__(*expressions, **extra)
def check_database_backends(databases=None, **kwargs):
    if databases is None:
        return []
    for alias in databases:
        conn = connections[alias]
    def run_checks(self, app_configs=None, tags=None, include_deployment_checks=False, databases=None):
            new_errors = check(app_configs=app_configs, databases=databases)
              include_deployment_checks=False, fail_level=checks.ERROR,
              databases=None):
        all_issues = checks.run_checks(
            databases=databases,
        parser.add_argument(
            '--database', action='append', dest='databases',
            help='Run database related checks against these aliases.',
        )
            databases=options['databases'],
    requires_system_checks = False
        parser.add_argument(
            '--skip-checks', action='store_true',
            help='Skip system checks.',
        )
        database = options['database']
        if not options['skip_checks']:
            self.check(databases=[database])
        connection = connections[database]
    def run_checks(self, databases):
        call_command('check', verbosity=self.verbosity, databases=databases)
            self.run_checks(databases)
            databases = kwargs.get('databases') or []
                *cls._check_constraints(databases),
    def _check_constraints(cls, databases):
        for db in databases:
        return '%s @@ %s' % (lhs, rhs), params
    @classmethod
    def from_parameter(cls, config):
        if config is None or isinstance(config, cls):
            return config
        return cls(config)
        self.config = SearchConfig.from_parameter(config)
        self.config = SearchConfig.from_parameter(config)
    def __init__(self, *expressions, config=None, weight=None):
        super().__init__(*expressions)
    def __init__(self, vector, query, weights=None):
        super().__init__(vector, query)
        if template is None and self.weights:
            template = '%(function)s(%(weights)s, %(expressions)s)'
            weight_sql, extra_params = compiler.compile(self.weights)
            extra_context['weights'] = weight_sql
        expressions = (vector, query)
        if weights is not None:
            if not hasattr(weights, 'resolve_expression'):
                weights = Value(weights)
            expressions = (weights,) + expressions
        super().__init__(*expressions)
        params = (*rhs_params, *lhs_params)
            config = getattr(self.rhs, 'config', None)
            self.lhs = SearchVector(self.lhs, config=config)
    # Does the backend orders NULLS FIRST by default?
    order_by_nulls_first = False
    order_by_nulls_first = True
    order_by_nulls_first = True
            if self.nulls_last and not (
                self.descending and connection.features.order_by_nulls_first
            ):
            elif self.nulls_first and not (
                not self.descending and connection.features.order_by_nulls_first
            ):
            if isinstance(item, str) and ORDER_PATTERN.match(item):
                if '.' in item:
                    warnings.warn(
                        'Passing column raw column aliases to order_by() is '
                        'deprecated. Wrap %r in a RawSQL expression before '
                        'passing it to order_by().' % item,
                        category=RemovedInDjango40Warning,
                        stacklevel=3,
                    )
            elif not hasattr(item, 'resolve_expression'):
from django.db.models.sql.constants import INNER, LOUTER, ORDER_DIR, SINGLE
            if isinstance(item, str):
                    continue
                if item == '?':
                    continue
                if item.startswith('-'):
                    item = item[1:]
                if item in self.annotations:
                    continue
                if self.extra and item in self.extra:
                    continue
                # names_to_path() validates the lookup. A descriptive
                # FieldError will be raise if it's not.
                self.names_to_path(item.split(LOOKUP_SEP), self.model._meta)
                    remote_label = f.remote_field.model._meta.concrete_model._meta.label
                    related_objects_graph[remote_label].append(f)
            related_objects = related_objects_graph[model._meta.concrete_model._meta.label]
            related_models = set()
            for remote_field in new_field.model._meta.related_objects:
                # Ignore self-relationship since the table was already rebuilt.
                if remote_field.related_model == model:
                    continue
                if not remote_field.many_to_many:
                    related_models.add(remote_field.related_model)
            for related_model in related_models:
                self._remake_table(related_model)
            opts = new_field.model._meta
            for remote_field in opts.related_objects:
                elif remote_field.through._meta.auto_created:
                    related_models.add(remote_field.through)
            for many_to_many in opts.many_to_many:
                # Ignore self-relationship since the table was already rebuilt.
                if many_to_many.related_model == model:
                    continue
                if many_to_many.remote_field.through._meta.auto_created:
                    related_models.add(many_to_many.remote_field.through)
        # Rebuild tables with FKs pointing to this field.
        if new_field.unique and old_type != new_type:
                    if remote_field.field_name == new_field.name:
                        related_models.add(remote_field.related_model)
                elif new_field.primary_key and remote_field.through._meta.auto_created:
            if new_field.primary_key:
                for many_to_many in opts.many_to_many:
                    # Ignore self-relationship since the table was already rebuilt.
                    if many_to_many.related_model == model:
                        continue
                    if many_to_many.remote_field.through._meta.auto_created:
                        related_models.add(many_to_many.remote_field.through)
        elif self.group_by:
            # Resolve GROUP BY annotation references if they are not part of
            # the selected fields anymore.
            group_by = []
            for expr in self.group_by:
                if isinstance(expr, Ref) and expr.refs not in field_names:
                    expr = self.annotations[expr.refs]
                group_by.append(expr)
            self.group_by = tuple(group_by)
                    if selected_annotation is expr:
        # Ensure base table is in aliases.
        self.query.get_initial_alias()
                with transaction.mark_for_rollback_on_error(self.using):
from django.db.models.fields import CharField, IntegerField
    output_field = CharField()
    output_field = CharField()
    output_field = CharField()
    output_field = CharField()
                namespace, _ = split_identifier(model._meta.db_table)
                    'namespace': '%s.' % self.quote_name(namespace) if namespace else '',
        '; SET CONSTRAINTS %(namespace)s%(name)s IMMEDIATE'
    @cached_property
    def has_select_for_update_of(self):
        return not self.connection.mysql_is_mariadb and self.connection.mysql_version >= (8, 0, 1)
    # Provide a default value for `for_save` in order to allow unresolved
    # instances to be compiled until a decision is taken in #25425.
    for_save = False
    def adapt_decimalfield_value(self, value, max_digits=None, decimal_places=None):
        return value
class BoundingCircle(OracleToleranceMixin, GeomOutputGeoFunc):
        copy = self.copy()
        copy.set_source_expressions([
            Value(float(expr.value)) if hasattr(expr, 'value') and isinstance(expr.value, Decimal)
            else expr
            for expr in copy.get_source_expressions()
        ])
        return copy.as_sql(compiler, connection, **extra_context)
            value = models.Value(self.rhs)
import functools
from uuid import UUID
            other = Value(other)
_connector_combinators = {
    connector: [
        (fields.IntegerField, fields.DecimalField, fields.DecimalField),
        (fields.DecimalField, fields.IntegerField, fields.DecimalField),
        (fields.IntegerField, fields.FloatField, fields.FloatField),
        (fields.FloatField, fields.IntegerField, fields.FloatField),
    ]
    for connector in (Combinable.ADD, Combinable.SUB, Combinable.MUL, Combinable.DIV)
}
@functools.lru_cache(maxsize=128)
def _resolve_combined_type(connector, lhs_type, rhs_type):
    combinators = _connector_combinators.get(connector, ())
    for combinator_lhs_type, combinator_rhs_type, combined_type in combinators:
        if issubclass(lhs_type, combinator_lhs_type) and issubclass(rhs_type, combinator_rhs_type):
            return combined_type
    def _resolve_output_field(self):
        try:
            return super()._resolve_output_field()
        except FieldError:
            combined_type = _resolve_combined_type(
                self.connector,
                type(self.lhs.output_field),
                type(self.rhs.output_field),
            )
            if combined_type is None:
                raise
            return combined_type()
    def _resolve_output_field(self):
        if isinstance(self.value, str):
            return fields.CharField()
        if isinstance(self.value, bool):
            return fields.BooleanField()
        if isinstance(self.value, int):
            return fields.IntegerField()
        if isinstance(self.value, float):
            return fields.FloatField()
        if isinstance(self.value, datetime.datetime):
            return fields.DateTimeField()
        if isinstance(self.value, datetime.date):
            return fields.DateField()
        if isinstance(self.value, datetime.time):
            return fields.TimeField()
        if isinstance(self.value, datetime.timedelta):
            return fields.DurationField()
        if isinstance(self.value, Decimal):
            return fields.DecimalField()
        if isinstance(self.value, bytes):
            return fields.BinaryField()
        if isinstance(self.value, UUID):
            return fields.UUIDField()
    CharField, DateTimeField, Field, IntegerField, UUIDField,
                expr = Case(When(expr, then=True), default=False)
        self.query = self.query.exists()
    def exists(self):
        q.add_extra({'a': 1}, None, None, None, None, None)
        q.set_extra_mask(['a'])
        return q
    def has_results(self, using):
        q = self.exists()
        (fields.IntegerField, fields.IntegerField, fields.IntegerField),
        # Prefer the non-standard DELETE FROM syntax over the SQL generated by
        # the SQLDeleteCompiler's default implementation when multiple tables
        # are involved since MySQL/MariaDB will generate a more efficient query
        # plan than when using a subquery.
        where, having = self.query.where.split_having()
        if self.single_alias or having:
            # DELETE FROM cannot be used when filtering against aggregates
            # since it doesn't allow for GROUP BY and HAVING clauses.
        where_sql, where_params = self.compile(where)
        if where_sql:
            result.append('WHERE %s' % where_sql)
        return ' '.join(result), tuple(from_params) + tuple(where_params)
        if not self.connection.features.update_can_self_select:
            # Force the materialization of the inner query to allow reference
            # to the target table on MySQL.
            sql, params = innerq.get_compiler(connection=self.connection).as_sql()
            innerq = RawSQL('SELECT * FROM (%s) subquery' % sql, params)
                make_hashable(self.params),
            return hash(make_hashable(self.error_dict))
    """
    Attempt to make value hashable or raise a TypeError if it fails.
    The returned value should generate the same hash for equal values.
    """
            for key, nested_value in sorted(value.items())
            make_hashable(self.limit_choices_to),
from django.utils.hashable import make_hashable
    @property
    def identity(self):
        return self.__class__, self.lhs, self.rhs
    def __eq__(self, other):
        if not isinstance(other, Lookup):
            return NotImplemented
        return self.identity == other.identity
    def __hash__(self):
        return hash(make_hashable(self.identity))
    @property
    def identity(self):
            self.__class__,
            self.table_name,
            self.parent_alias,
            self.join_field,
            self.filtered_relation,
        if not isinstance(other, Join):
            return NotImplemented
        return self.identity == other.identity
    def __hash__(self):
        return hash(self.identity)
    def equals(self, other, with_filtered_relation):
        if with_filtered_relation:
            return self == other
        return self.identity[:-1] == other.identity[:-1]
    @property
    def identity(self):
        return self.__class__, self.table_name, self.table_alias
    def __eq__(self, other):
        if not isinstance(other, BaseTable):
            return NotImplemented
        return self.identity == other.identity
    def __hash__(self):
        return hash(self.identity)
        return self.identity == other.identity
from django.utils.hashable import make_hashable
    @property
    def identity(self):
        identity = (
            (arg, make_hashable(value))
            for arg, value in self.__dict__.items()
        )
        return (self.__class__, *identity)
        # Allow the usage of both QuerySet and sql.Query objects.
        self.query = getattr(queryset, 'query', queryset)
            args = (self.query, *args[1:])
            kwargs['queryset'] = self.query
from django.db.models.expressions import (
    BaseExpression, Col, Exists, F, OuterRef, Ref, ResolvedOuterRef,
)
            WHERE NOT EXISTS(
                SELECT 1
                FROM child
                WHERE name = 'foo' AND child.parent_id = parent.id
                LIMIT 1
            )
        lookup_class = select_field.get_lookup('exact')
        lookup = lookup_class(col, ResolvedOuterRef(trimmed_prefix))
        query.where.add(lookup, AND)
        condition, needed_inner = self.build_filter(Exists(query))
import os
import subprocess
    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        raise NotImplementedError(
            'subclasses of BaseDatabaseClient must provide a '
            'settings_to_cmd_args_env() method or override a runshell().'
        )
        args, env = self.settings_to_cmd_args_env(self.connection.settings_dict, parameters)
        if env:
            env = {**os.environ, **env}
        subprocess.run(args, env=env, check=True)
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        return args, None
import os
        cmd_args, cmd_env = DatabaseClient.settings_to_cmd_args_env(self.connection.settings_dict, [])
        dump_cmd = ['mysqldump', *cmd_args[1:-1], '--routines', '--events', source_database_name]
        dump_env = load_env = {**os.environ, **cmd_env} if cmd_env else None
        load_cmd = cmd_args
        with subprocess.Popen(dump_cmd, stdout=subprocess.PIPE, env=dump_env) as dump_proc:
            with subprocess.Popen(load_cmd, stdin=dump_proc.stdout, stdout=subprocess.DEVNULL, env=load_env):
from .utils import dsn, Oracle_datetime                     # NOQA isort:skip
            dsn=dsn(self.settings_dict),
    @staticmethod
    def connect_string(settings_dict):
        from django.db.backends.oracle.utils import dsn
        return '%s/"%s"@%s' % (
            settings_dict['USER'],
            settings_dict['PASSWORD'],
            dsn(settings_dict),
        )
    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        args = [cls.executable_name, '-L', cls.connect_string(settings_dict)]
        wrapper_path = shutil.which(cls.wrapper_name)
        return args, None
def dsn(settings_dict):
    if settings_dict['PORT']:
        host = settings_dict['HOST'].strip() or 'localhost'
        return Database.makedsn(host, int(settings_dict['PORT']), settings_dict['NAME'])
    return settings_dict['NAME']
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        options = settings_dict.get('OPTIONS', {})
        host = settings_dict.get('HOST')
        port = settings_dict.get('PORT')
        dbname = settings_dict.get('NAME') or 'postgres'
        user = settings_dict.get('USER')
        passwd = settings_dict.get('PASSWORD')
        sslmode = options.get('sslmode')
        sslrootcert = options.get('sslrootcert')
        sslcert = options.get('sslcert')
        sslkey = options.get('sslkey')
        env = {}
            env['PGPASSWORD'] = str(passwd)
            env['PGSSLMODE'] = str(sslmode)
            env['PGSSLROOTCERT'] = str(sslrootcert)
            env['PGSSLCERT'] = str(sslcert)
            env['PGSSLKEY'] = str(sslkey)
        return args, env
    def runshell(self, parameters):
        sigint_handler = signal.getsignal(signal.SIGINT)
            super().runshell(parameters)
    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        args = [
            cls.executable_name,
            # TODO: Remove str() when dropping support for PY37. args
            # parameter accepts path-like objects on Windows since Python 3.8.
            str(settings_dict['NAME']),
            *parameters,
        ]
        return args, None
        env = None
            # The MYSQL_PWD environment variable usage is discouraged per
            # MySQL's documentation due to the possibility of exposure through
            # `ps` on old Unix flavors but --password suffers from the same
            # flaw on even more systems. Usage of an environment variable also
            # prevents password exposure if the subprocess.run(check=True) call
            # raises a CalledProcessError since the string representation of
            # the latter includes all of the provided `args`.
            env = {'MYSQL_PWD': password}
        return args, env
        inner_query_sql, inner_query_params = self.query.inner_query.get_compiler(
            self.using
        ).as_sql(with_col_aliases=True)
        sql = 'SELECT %s FROM (%s) subquery' % (sql, inner_query_sql)
        params = params + inner_query_params
from django.core.exceptions import FieldDoesNotExist, FieldError
            inner_query.subquery = True
            outer_query = AggregateQuery(self.model, inner_query)
    def __init__(self, model, inner_query):
        self.inner_query = inner_query
        super().__init__(model)
        # Index.create_sql returns interpolated SQL which makes params=None a
        # necessity to avoid escaping attempts on execution.
            # Constraint.create_sql returns interpolated SQL which makes
            # params=None a necessity to avoid escaping attempts on execution.
            self.execute(sql, params=None)
            self.verbosity, self.interactive, connection.alias, stdout=self.stdout, apps=pre_migrate_apps, plan=plan,
            self.verbosity, self.interactive, connection.alias, stdout=self.stdout, apps=post_migrate_apps, plan=plan,
import sys
            stdout = kwargs.get('stdout', sys.stdout)
            stdout.write('Running pre-migrate handlers for application %s' % app_config.label)
            stdout = kwargs.get('stdout', sys.stdout)
            stdout.write('Running post-migrate handlers for application %s' % app_config.label)
    def get_external_cols(self):
        return self.query.get_external_cols()
        external_cols = self.get_external_cols()
            col for col in self._gen_cols(exprs, include_external=True)
    def _gen_cols(cls, exprs, include_external=False):
            elif include_external and callable(getattr(expr, 'get_external_cols', None)):
                yield from expr.get_external_cols()
                yield from cls._gen_cols(
                    expr.get_source_expressions(),
                    include_external=include_external,
                )
        databases = {}
                    test_databases = connections
                    serialized_rollback = getattr(test, 'serialized_rollback', False)
                    databases.update(
                        (alias, serialized_rollback or databases.get(alias, False))
                        for alias in test_databases
                    )
        serialized_aliases = set(
            alias
            for alias, serialize in databases.items() if serialize
        )
            old_config = self.setup_databases(
                aliases=databases,
                serialized_aliases=serialized_aliases,
            )
from django.utils.deprecation import RemovedInDjango50Warning
def setup_databases(
    verbosity,
    interactive,
    *,
    time_keeper=None,
    keepdb=False,
    debug_sql=False,
    parallel=0,
    aliases=None,
    serialized_aliases=None,
    **kwargs,
):
                    # RemovedInDjango50Warning: when the deprecation ends,
                    # replace with:
                    # serialize_alias = serialized_aliases is None or alias in serialized_aliases
                    try:
                        serialize_alias = connection.settings_dict['TEST']['SERIALIZE']
                    except KeyError:
                        serialize_alias = (
                            serialized_aliases is None or
                            alias in serialized_aliases
                        )
                    else:
                        warnings.warn(
                            'The SERIALIZE test database setting is '
                            'deprecated as it can be inferred from the '
                            'TestCase/TransactionTestCase.databases that '
                            'enable the serialized_rollback feature.',
                            category=RemovedInDjango50Warning,
                        )
                        serialize=serialize_alias,
        # Combine subqueries aliases to ensure aliases relabelling properly
        # handle subqueries when combining where and select clauses.
        self.subq_aliases |= rhs.subq_aliases
        "Oracle doesn't allow filters to be compared to another expression in "
        "the WHERE clause.": {
            'lookup.tests.LookupTests.test_lookup_rhs',
        },
            sql, params = compiler.compile(value)
            # Ensure expression is wrapped in parentheses to respect operator
            # precedence but avoid double wrapping as it can be misinterpreted
            # on some backends (e.g. subqueries on SQLite).
            if sql and sql[0] != '(':
                sql = '(%s)' % sql
            return sql, params
@deconstructible
class Expression(BaseExpression, Combinable):
    """An expression that can be combined with other expressions."""
        if not isinstance(other, Expression):
class Subquery(BaseExpression, Combinable):
@deconstructible
import copy
        if not self:
            return other.copy() if hasattr(other, 'copy') else copy.copy(other)
        elif isinstance(other, Q) and not other:
class OrderBy(Expression):
    def get_group_by_cols(self, alias=None):
        cols = self.lhs.get_group_by_cols()
        if hasattr(self.rhs, 'get_group_by_cols'):
            if not getattr(self.rhs, 'has_select_fields', True):
                self.rhs.clear_select_clause()
                self.rhs.add_fields(['pk'])
            cols.extend(self.rhs.get_group_by_cols())
        return cols
        if self.connector == conn_type and data in self.children:
