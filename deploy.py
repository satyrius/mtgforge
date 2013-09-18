import os
from fabric.api import task, sudo, cd, prefix


APP_DIR = '/var/www/mtgforge'
VIRTUALENV_BIN = '/var/virtualenv/mtgforge/bin'
ACTIVATE = os.path.join(VIRTUALENV_BIN, 'activate')
PY = os.path.join(VIRTUALENV_BIN, 'python')


def manage(command):
    with cd(APP_DIR):
        with prefix('export DJANGO_SETTINGS_MODULE=settings.prod'):
            sudo('./py ./backend/manage.py %s' % command, user='www-data')


@task(default=True)
def full_deploy():
    update()
    backend()
    restart()
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


@task
def frontend():
    with cd(os.path.join(APP_DIR, 'frontend')):
        sudo('rm -rf node_modules bower_components public')
        sudo('npm install')
        sudo('bower install --allow-root')
        sudo('brunch build --production')
    manage('collectstatic --clear --noinput')


@task
def build_fts():
    manage('build_fts_index')
    manage('build_sim_index')
    manage('build_suggest')


@task
def restart():
    # TODO update configs
    sudo('service uwsgi restart')
    sudo('service nginx reload')
