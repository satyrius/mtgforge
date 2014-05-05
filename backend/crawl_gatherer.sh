#!/bin/sh
cd $(dirname $0)
echo "select name from crawler_cardsetalias where domain = 'gatherer.wizards.com'" | \
    ./manage.py dbshell | \
    sed -n -e 's/^ \(.*\)/\1/p' | \
    grep -ve '^ ' | \
    scrapy crawl -s LOG_LEVEL=INFO $@ gatherer
