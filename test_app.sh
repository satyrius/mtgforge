#!/bin/sh
DIR=$(dirname $0)
REUSE_DB=1 $DIR/backend/manage.py test $@
