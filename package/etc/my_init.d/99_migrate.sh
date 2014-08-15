#!/bin/bash -xe
cd /var/www/extrota
setuser www-data ./manage.py syncdb --noinput
setuser www-data ./manage.py migrate --merge --delete-ghost-migrations --no-initaial-data --noinput -v2 || true