#!/bin/sh
DIR=$(dirname $0)

cd $DIR/frontend
brunch watch &

../backend/manage.py runserver $@
