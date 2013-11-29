#!/bin/sh
PYTHONPATH=$(dirname $0) py.test --ds=settings.test $@
