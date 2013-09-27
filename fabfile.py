from os.path import join
from fabric.api import task, sudo, cd, prefix


APP_DIR = '/var/www/mtgforge'
ETC_DIR = join(APP_DIR, 'package', 'etc')
VIRTUALENV_BIN = '/var/virtualenv/mtgforge/bin'
ACTIVATE = join(VIRTUALENV_BIN, 'activate')
PY = join(VIRTUALENV_BIN, 'python')
VERSION_FILE = '/etc/mtgforge/version'


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
