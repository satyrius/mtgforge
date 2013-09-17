from fabric.api import local, lcd, task


@task
def runserver():
    with lcd('frontend'):
        local('brunch watch &')
    with lcd('backend'):
        local('./manage.py runserver')
