import os
import sys
from os.path import abspath, dirname, join

# Setup Django environment
DJANGO_PROJECT = abspath(join(dirname(__file__), '..'))
sys.path.append(DJANGO_PROJECT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
from django.conf import settings

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

IMAGES_STORE = settings.MEDIA_ROOT

ITEM_PIPELINES = {
    'crawler.pipelines.art.ArtPipeline': 1,
    'crawler.pipelines.art.CardImagePipeline': 90,
    'crawler.pipelines.cards.DupsHandlePipeline': 100,
    'crawler.pipelines.cards.CardsPipeline': 110,
    'crawler.pipelines.sets.CardSetsPipeline': 200,
    'crawler.pipelines.sets.InfoPipeline': 210,
}

FEED_EXPORTERS = {
    'name': 'crawler.exporters.ItemNameExporter',
}

SPIDER_CONTRACTS = {
    'crawler.contracts.QueryContract': 98,
    'crawler.contracts.MetaContract': 99,
    'crawler.contracts.FieldContract': 100,
    'crawler.contracts.PartialContract': 101,
    'crawler.contracts.ItemContract': 102,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = '/tmp/crawler'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Forger (+http://topdeck.pro)'
