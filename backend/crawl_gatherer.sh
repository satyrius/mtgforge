#!/bin/sh
cd $(dirname $0)
scrapy crawl -o - --output-format=name sets | scrapy crawl gatherer
