#!/bin/bash -xe

# Ensure that nginx configs are ok
nginx -t

# Validates all installed models and prints validation errors to standard output
setuser www-data /var/www/extrota/manage.py validate
