import re
from crawler.items import CardSetItem
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector


class ProductsSpider(CrawlSpider):
    name = 'products'
    domain = 'gatherer.wizards.com'
    allowed_domains = [domain]
    start_urls = ['http://gatherer.wizards.com/Pages/Default.aspx']

    def parse(self, response):
        sel = Selector(response)
        id = 'ctl00_ctl00_MainContent_Content_SearchControls_setAddText'
        cs_select = '//select[@id="{}"]/option[@value!=""]/@value'.format(id)
        for name in sel.xpath(cs_select).extract():
            yield CardSetItem(name=name)


class ProductsInfoSpider(CrawlSpider):
    name = 'products_info'
    domain = 'www.wizards.com'
    allowed_domains = [domain]
    start_urls = ['http://magic.wizards.com'
                  '/en/game-info/products/card-set-archive']

    cards_count_re = re.compile(r'(\d+)\s+cards', re.IGNORECASE)
    separator_re = re.compile(r'\s*(?:,|and)\s*', re.IGNORECASE)

    def parse(self, response):
        sel = Selector(response)
        for node in sel.css('table.product td:nth-child(2) a'):
            # Extract card set name
            text = node.xpath('.//text()').extract()
            name = ' '.join(filter(None, [
                re.sub(r'\s+', ' ', t).strip() for t in text]))

            # Up to the parent table cell and follow siblings to extract
            # cards count and release date
            while node.xpath('name()').extract()[0] != 'td':
                node = node.xpath('..')
            siblings = node.xpath('following-sibling::td')
            data = {}

            cards_count = siblings[0].xpath(
                'p/text()').extract()
            if cards_count:
                match_cards = self.cards_count_re.match(
                    cards_count[-1].strip())
                if match_cards:
                    data['cards'] = int(match_cards.group(1))

            released_at = siblings[1].xpath('p/text()').extract()
            if released_at:
                data['released_at'] = released_at[-1].strip()

            if ',' in name:
                # Comma separated editions
                for separated_name in filter(
                    None, self.separator_re.split(name)
                ):
                    yield CardSetItem(name=separated_name, **data)
            else:
                yield CardSetItem(name=name, **data)
