#!/bin/sh
# Parse card by multoverse id using gatherer crawler
cd $(dirname $0)

URL="http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=$1"
echo "Parse $URL"

scrapy parse --spider gatherer --pipeline --depth 3 --callback parse_card $URL
