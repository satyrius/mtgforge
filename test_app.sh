#!/bin/sh
DIR=$(dirname $0)
$DIR/backend/manage.py test $@
