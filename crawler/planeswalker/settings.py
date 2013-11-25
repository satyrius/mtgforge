#import os
#import sys
#from os.path import abspath, dirname, join

## Setup Django environment
#DJANGO_PROJECT = abspath(join(dirname(__file__), '../../backend'))
#sys.path.append(DJANGO_PROJECT)
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

BOT_NAME = 'planeswalker'

SPIDER_MODULES = ['planeswalker.spiders']
NEWSPIDER_MODULE = 'planeswalker.spiders'

ITEM_PIPELINES = {
    'planeswalker.pipelines.CardsPipeline': 100,
}

SPIDER_CONTRACTS = {
    'planeswalker.contracts.ItemContract': 100,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = '/tmp/planeswalker'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Forger (+http://topdeck.pro)'
