from crawler.items import CardSetItem
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['gatherer.wizards.com']
    start_urls = ['http://gatherer.wizards.com/Pages/Default.aspx']

    def parse(self, response):
        sel = Selector(response)
        id = 'ctl00_ctl00_MainContent_Content_SearchControls_setAddText'
        cs_select = '//select[@id="{}"]/option[@value!=""]/@value'.format(id)
        for name in sel.xpath(cs_select).extract():
            yield CardSetItem(name=name)
