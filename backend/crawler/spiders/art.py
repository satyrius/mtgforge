from scrapy.contrib.spiders import CrawlSpider

from crawler.items import CardImageItem
from oracle.models import CardImage


class DefaultArtSpider(CrawlSpider):
    name = 'default_art'
    allowed_domains = ['gatherer.wizards.com']
    start_urls = ['http://gatherer.wizards.com/Pages/Default.aspx']

    def parse(self, response):
        for ci in CardImage.objects.filter(file='').exclude(scan=''):
            yield CardImageItem(mvid=ci.mvid, art=ci.scan)
