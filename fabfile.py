from fabric.api import env, cd, sudo, prefix, task
from functools import wraps


env.hosts = ['evindor.com']
virtualenv = 'source /var/virtualenv/mtgforge/bin/activate'


def project_task(func):
    @task
    @wraps(func)
    def wrapper(*args, **kwargs):
        with cd('/var/www/mtgforge'):
            with prefix(virtualenv):
                with prefix('export DJANGO_SETTINGS_MODULE=settings.prod'):
                    return func(*args, **kwargs)
    return wrapper


@task
def restart():
    sudo('service uwsgi restart')
    sudo('service nginx restart')


@project_task
def recollect_static():
    sudo('rm -rf _generated_media*')
    sudo('./manage.py generatemedia')
    sudo('./manage.py compressmedia')
    sudo('./manage.py collectstatic --clear --noinput')


@project_task
def build_fts():
    sudo('./manage.py build_fts_index')
    sudo('./manage.py build_sim_index')
    sudo('./manage.py build_suggest')


@project_task
def deploy():
    sudo('git reset --hard')
    sudo('git pull')
    sudo('find . -name "*.pyc" -delete')
    sudo('pip install -r requirements.txt')
    sudo('./manage.py migrate --merge --delete-ghost-migrations')
    build_fts()
    recollect_static()
    restart()
