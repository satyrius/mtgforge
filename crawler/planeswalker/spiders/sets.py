from planeswalker.items import CardSetItem
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector


class SetsSpider(CrawlSpider):
    name = 'sets'
    allowed_domains = ['gatherer.wizards.com']
    start_urls = ['http://gatherer.wizards.com/Pages/Default.aspx']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        cs_select = '//select[@id="ctl00_ctl00_MainContent_Content_SearchControls_setAddText"]/option[@value!=""]/@value'
        return [CardSetItem(name=name) for name in hxs.select(cs_select).extract()]
