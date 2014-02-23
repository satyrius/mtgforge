from os.path import dirname, join

BOT_NAME = 'mtgru'

SPIDER_MODULES = ['mtgru.spiders']
NEWSPIDER_MODULE = 'mtgru.spiders'

FILES_STORE = join(dirname(dirname(__file__)), 'files')

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.files.FilesPipeline': 1
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mtgru (+http://www.yourdomain.com)'
