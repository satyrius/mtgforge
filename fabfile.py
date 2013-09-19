from fabric.api import local, lcd, task, prefix
import deploy


def lmanage(command):
    with lcd('backend'):
        local('./manage.py %s' % command)


@task(alias='runs')
def runserver():
    with lcd('frontend'):
        local('brunch watch &')
    lmanage('runserver')


@task
def test():
    with prefix('export REUSE_DB=1'):
        lmanage('test')
