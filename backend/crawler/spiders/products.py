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
            yield CardSetItem(name=name, is_gatherer=True)


class ProductsInfoSpider(CrawlSpider):
    name = 'products_info'
    domain = 'www.wizards.com'
    allowed_domains = [domain]
    start_urls = [
        'http://www.wizards.com/magic/TCG/Article.aspx?'
        'x=mtg/tcg/products/allproducts']

    product_link_re = re.compile(
        r'x=mtg[/_]tcg[/_](?:products[/_]([^/_#]+)|'
        r'([^/_]+)[/_]productinfo)$')
    cards_count_re = re.compile(r'(\d+)\s+cards', re.IGNORECASE)
    separator_re = re.compile(r'\s*(?:,|and)\s*')

    def parse(self, response):
        sel = Selector(response)
        for node in sel.css('div.article-content a'):
            href = node.xpath('@href').extract()
            if not href:
                continue
            href = href[0]

            match = self.product_link_re.search(href)
            if match:
                # Extract card set name
                text = node.xpath('.//text()').extract()
                name = ' '.join(filter(None, [
                    re.sub(r'\s+', ' ', t).strip() for t in text]))

                # Up to the parent table cell and follow siblings to extract
                # cards count and release date
                while node.xpath('name()').extract()[0] != 'td':
                    node = node.xpath('..')
                siblings = node.xpath('following-sibling::td')
                data = {
                    'released_at': siblings[1].xpath(
                        './/text()').extract()[1].strip()
                }
                cards_count = siblings[0].xpath('text()').extract()[0].strip()
                match_cards = self.cards_count_re.match(cards_count)
                if match_cards:
                    data['cards'] = int(match_cards.group(1))
                if ',' in name:
                    # Comma separated editions
                    for separated_name in filter(
                        None, self.separator_re.split(name)
                    ):
                        yield CardSetItem(name=separated_name, **data)
                else:
                    yield CardSetItem(name=name, **data)
