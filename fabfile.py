from fabric.api import env, cd, sudo, prefix

env.hosts = ['evindor.com']


def deploy():
    with cd('/var/www/mtgforge'):
        sudo('git pull')
        sudo('find . -name "*.pyc" -delete')
        sudo('rm -rf _generated_media*')
        sudo('rm -rf ../mtgforge-static/*')
        with prefix('source /var/virtualenv/mtgforge/bin/activate'):
            sudo('./manage.py migrate')
            sudo('./manage.py generatemedia')
            sudo('./manage.py compressmedia')
            sudo('./manage.py collectstatic')
        sudo('service uwsgi restart')
        sudo('service nginx restart')
