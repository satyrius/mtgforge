#!/bin/sh
# Parse card by multiverse id using gatherer crawler with pipelines applied
cd $(dirname $0)

URL="http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=$1"
echo "Parse $URL"

scrapy parse --spider gatherer --pipeline --depth 4 --callback parse_card $URL
