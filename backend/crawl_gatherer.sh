#!/bin/sh
cd $(dirname $0)
scrapy crawl -o - --output-format=name products | scrapy crawl gatherer
