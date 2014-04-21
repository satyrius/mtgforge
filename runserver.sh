#!/bin/sh
DIR=$(dirname $0)

cd $DIR/client
gulp watch &

../backend/manage.py runserver $@
