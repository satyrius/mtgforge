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
    'planeswalker.pipelines.DupsHandlePipeline': 100,
    'planeswalker.pipelines.CardsPipeline': 110,
}

SPIDER_CONTRACTS = {
    'planeswalker.contracts.QueryContract': 98,
    'planeswalker.contracts.MetaContract': 99,
    'planeswalker.contracts.FieldContract': 100,
    'planeswalker.contracts.PartialContract': 101,
    'planeswalker.contracts.ItemContract': 102,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = '/tmp/planeswalker'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Forger (+http://topdeck.pro)'
