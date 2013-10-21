from scrapy.selector import HtmlXPathSelector
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest, Request
from urlparse import urljoin
from planeswalker.items import CardSetItem, CardItem


class GathererSpider(CrawlSpider):
    name = 'gatherer'
    allowed_domains = ['gatherer.wizards.com']
    search_url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx'

    def __init__(self, card_set=None, *args, **kwargs):
        self.card_sets = [card_set or 'Theros']

    def card_set_names(self):
        for name in self.card_sets:
            yield name

    def start_requests(self):
        for name in self.card_set_names():
            yield FormRequest(
                url=self.search_url, method='GET',
                callback=self.parse_paginagor,
                formdata={'set': '[%s]' % name, 'output': 'compact'},
                meta={'card_set': CardSetItem(name=name)})
            return

    def parse_paginagor(self, response):
        card_set = response.request.meta.get('card_set', CardSetItem())

        hxs = HtmlXPathSelector(response)
        page_select = '//div[contains(@class, "pagingControls")]//a'
        for page_link in hxs.select(page_select):
            page_url = page_link.select('@href').extract()[0]
            page_num = page_link.select('text()').extract()[0].strip()
            if page_url and page_num.isdigit():
                yield Request(
                    urljoin(response.request.url, page_url),
                    callback=self.parse_list,
                    meta={'card_set': card_set})

    def parse_list(self, response):
        '''Parse compact card list and follow card details for each printing.

        @url http://gatherer.wizards.com/Pages/Search/Default.aspx?output=compact&set=%5BTheros%5D
        @returns items 0 0
        @scrapes slug
        @returns requests 100 106
        '''
        card_set = response.request.meta.get('card_set', CardSetItem())
        hxs = HtmlXPathSelector(response)
        for card_row in hxs.select('//tr[contains(@class, "cardItem")]'):
            a = card_row.select('.//td[contains(@class, "name")]//a')
            card_url = a.select('@href').extract()[0]
            card_name = a.select('text()').extract()[0].strip()

            # Next we should parse 'printings' block. It contains card links
            # for all card releases in all sets. We will get all links for
            # current set. We should use these links because some cards might
            # have several printing in one set (e.g. Forest, High Tide)
            get_href = lambda a: a.select('@href').extract()[0]
            get_alt = lambda a: a.select('.//img/@alt').extract()[0]
            printings = {get_href(a): get_alt(a) for a in card_row.select(
                './/td[contains(@class, "printings")]//a')}
            slug = printings[card_url]

            # Fill card set slug and return an item if not returned yet
            if 'slug' not in card_set:
                card_set['slug'] = slug

            for url, cs in printings.items():
                if cs == slug:
                    card = CardItem(name=card_name)
                    yield Request(
                        urljoin(response.request.url, url),
                        meta={'card': card, 'card_set': card_set},
                        callback=self.parse_card)

    def parse_card(self, response):
        r = response.request
        card = r.meta.get('card', CardItem())
        yield card
