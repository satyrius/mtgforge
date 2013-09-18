from fabric.api import local, lcd, task
import deploy


@task(alias='runs')
def runserver():
    with lcd('frontend'):
        local('brunch watch &')
    with lcd('backend'):
        local('./manage.py runserver')
