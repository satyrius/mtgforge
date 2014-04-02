from os.path import join
from fabric.api import task, sudo, get, local
from fabfile.helpers import are_you_sure


DUMP_SCHEMA = 'mtgforge.dump.schema.sql'
DUMP_DATA = 'mtgforge.dump.data'


@task
def dump(db='mtgforge', downloads='.'):
    schema_dump = join('/tmp', DUMP_SCHEMA)
    data_dump = join('/tmp', DUMP_DATA)

    sudo(' '.join([
        'sudo -u postgres pg_dump',
        '--schema-only',
        '--no-owner',
        '--no-privileges',
        '--format=plain',
        '%s > %s']) % (db, schema_dump))

    sudo(' '.join([
        'sudo -u postgres pg_dump',
        '--data-only',
        '--disable-triggers',
        '--no-owner',
        '--format=custom',
        '-T django_session',
        '%s > %s']) % (db, data_dump))

    get('/tmp/mtgforge.dump.*', downloads)


@task
def restore(db, downloads='.'):
    if are_you_sure('This will destroy current database.'):
        local('dropdb %s' % db)
        local('createdb %s' % db)
        local('psql %s < %s' % (db, join(downloads, DUMP_SCHEMA)))
        local('pg_restore -d %s --format=c %s' % (db, join(downloads, DUMP_DATA)))
