#!/bin/sh
cd $(dirname $0)
scrapy check -s SPIDER_MODULES=crawler.tests $@
