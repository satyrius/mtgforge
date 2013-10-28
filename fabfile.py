import re
from os.path import join
from fabric.api import task, sudo, cd, prefix, get, local, prompt


APP_DIR = '/var/www/mtgforge'
ETC_DIR = join(APP_DIR, 'package', 'etc')
VIRTUALENV_BIN = '/var/virtualenv/mtgforge/bin'
ACTIVATE = join(VIRTUALENV_BIN, 'activate')
PY = join(VIRTUALENV_BIN, 'python')
VERSION_FILE = '/etc/mtgforge/version'
DOWNLOADS = '~/Downloads'
DATABASE = 'mtgforge'
DUMP_SCHEMA = 'mtgforge.dump.schema.sql'
DUMP_DATA = 'mtgforge.dump.data'


def manage(command):
    with cd(APP_DIR):
        with prefix('export DJANGO_SETTINGS_MODULE=settings.prod'):
            sudo('./py ./backend/manage.py %s' % command, user='www-data')


@task(alias='deploy', default=True)
def full_deploy():
    update()
    backend()
    frontend()
    build_fts()


@task
def update():
    with cd(APP_DIR):
        sudo('git reset --hard')
        sudo('git pull')
        sudo('git log -1 --format="%H" > /etc/mtgforge/version')


@task
def backend():
    with cd(APP_DIR):
        sudo('find . -name "*.pyc" -delete')
        sudo('rm -f ./py')
        sudo('ln -s %s ./py' % PY)
        with prefix('source %s' % ACTIVATE):
            sudo('pip install -r requirements.txt')
    manage('syncdb --noinput')
    manage('migrate --merge --delete-ghost-migrations')
    restart(update_config=True)


@task
def frontend():
    with cd(join(APP_DIR, 'frontend')):
        sudo('rm -rf node_modules bower_components public')
        sudo('npm install')
        sudo('bower install --allow-root')
        sudo('brunch build --production')
    with cd('/var/www/mtgforge-static'):
        sudo('rm -rf *')
        sudo('mkdir $(cat %s)' % VERSION_FILE)
        sudo('chown www-data:www-data $(cat %s)' % VERSION_FILE)

    manage('collectstatic --clear --noinput')


@task
def build_fts():
    manage('build_fts_index')
    manage('build_sim_index')
    manage('build_suggest')


@task
def restart(update_config=False):
    if update_config:
        with cd('/etc/uwsgi/apps-enabled'):
            sudo('rm -rf mtgforge.ini')
            sudo('ln -s %s/uwsgi/apps-available/mtgforge.ini .' % ETC_DIR)
        with cd('/etc/nginx'):
            sudo('rm -rf mtgforge sites-enabled/mtgforge.conf')
            sudo('ln -s %s/nginx/mtgforge' % ETC_DIR)
            with cd('sites-enabled'):
                sudo('ln -s %s/nginx/mtgforge/_.conf mtgforge.conf' % ETC_DIR)
    sudo('service uwsgi restart')
    sudo('service nginx reload')


@task
def pg_dump():
    schema_dump = join('/tmp', DUMP_SCHEMA)
    data_dump = join('/tmp', DUMP_DATA)

    sudo(' '.join([
        'sudo -u mtgforge pg_dump -h localhost ',
        '--schema-only',
        '--no-owner',
        '--no-privileges',
        '--format=plain',
        '%s > %s']) % (DATABASE, schema_dump))

    sudo(' '.join([
        'sudo -u mtgforge pg_dump -h localhost',
        '--data-only',
        '--disable-triggers',
        '--no-owner',
        '--format=custom',
        '-T oracle_dataproviderpage -T django_session',
        '%s > %s']) % (DATABASE, data_dump))

    get('/tmp/mtgforge.dump.*', DOWNLOADS)


def are_you_sure(ask_message, default='no'):
    yes = r'y(e(p|a[h]*)?)?|true|1'
    no = r'n(o(pe)?)?|false|0'

    def yes_no(value):
        value = value.strip().lower()
        if not re.match(r'^%s|%s$' % (yes, no), value):
            raise Exception('It is a yes/no question.')
        return bool(re.match(yes, value))

    return prompt(u'%s Are you sure? [yes/no]' % ask_message, default=default,
                  validate=yes_no)


@task
def pg_restore():
    if are_you_sure('This will destroy current database.'):
        local('dropdb %s' % DATABASE)
        local('createdb %s' % DATABASE)
        local('psql %s < %s' % (DATABASE, join(DOWNLOADS, DUMP_SCHEMA)))
        local('pg_restore -d mtgforge --format=c %s' % join(
            DOWNLOADS, DUMP_DATA))


@task
def reset_images():
    if are_you_sure('This will remove all image and thumbnails data.'):
        local('psql %s -c "truncate oracle_cardimagethumb"' % DATABASE)
        local('psql %s -c "update oracle_cardimage set file = null"' % DATABASE)
        local('rm -rf media/*')
