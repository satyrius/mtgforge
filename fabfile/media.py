from fabric.api import task, local, env
from fabfile.helpers import are_you_sure


@task
def reset():
    db = env['database']
    if are_you_sure('This will remove all image and thumbnails data.'):
        local('psql %s -c "truncate oracle_cardimagethumb"' % db)
        local('psql %s -c "update oracle_cardimage set file = \'\'"' % db)
        local('rm -rf media/*')
