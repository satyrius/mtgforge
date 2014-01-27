from os.path import join
from fabric.api import task, sudo, get, local, env
from fabfile.helpers import are_you_sure


DUMP_SCHEMA = 'mtgforge.dump.schema.sql'
DUMP_DATA = 'mtgforge.dump.data'


@task
def dump():
    db = env['database']
    schema_dump = join('/tmp', DUMP_SCHEMA)
    data_dump = join('/tmp', DUMP_DATA)

    sudo(' '.join([
        'sudo -u mtgforge pg_dump -h localhost ',
        '--schema-only',
        '--no-owner',
        '--no-privileges',
        '--format=plain',
        '%s > %s']) % (db, schema_dump))

    sudo(' '.join([
        'sudo -u mtgforge pg_dump -h localhost',
        '--data-only',
        '--disable-triggers',
        '--no-owner',
        '--format=custom',
        '-T django_session',
        '%s > %s']) % (db, data_dump))

    get('/tmp/mtgforge.dump.*', env['downloads'])


@task
def restore():
    db = env['database']
    dl = env['downloads']
    if are_you_sure('This will destroy current database.'):
        local('dropdb %s' % db)
        local('createdb %s' % db)
        local('psql %s < %s' % (db, join(dl, DUMP_SCHEMA)))
        local('pg_restore -d mtgforge --format=c %s' % join(dl, DUMP_DATA))
