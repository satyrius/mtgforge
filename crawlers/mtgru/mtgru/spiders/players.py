import re
from urlparse import urljoin

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector

from mtgru.items import PlayerItem


class PlayersSpider(CrawlSpider):
    name = 'players'
    allowed_domains = ['mtg.ru']
    search_url = 'http://www.mtg.ru/exchange/search.phtml'
    cards_page_re = re.compile(r'window.open\("(?P<url>[^"]+)"')
    exchange_link_fmt = '/player/{username}/mtg_{username}.txt'

    rules = (
        Rule(SgmlLinkExtractor(allow=('card\.phtml', )),
             callback='parse_card'),
    )

    def __init__(self, auth, *args, **kwargs):
        super(PlayersSpider, self).__init__(*args, **kwargs)
        self.auth_cookie = {'MTG': auth}

    def start_requests(self):
        yield Request(
            url=self.search_url,
            cookies=self.auth_cookie,
            callback=self.parse_list)

    def parse_list(self, response):
        sel = Selector(response)

        # Pagination
        for a in sel.css('span.split-pages a[href*="?page="]'):
            href = a.xpath('@href').extract()[0]
            yield Request(
                url=urljoin(response.request.url, href),
                callback=self.parse_list)

        # Card offers
        for details_btn in sel.css('input[type=button]'):
            onclick = details_btn.xpath('@onclick').extract()[0]
            mt = self.cards_page_re.match(onclick)
            yield Request(
                url=urljoin(response.request.url, mt.group('url')),
                callback=self.parse_card)

    def parse_card(self, response):
        for username in Selector(response).css(
            'table.NoteDivWidth th[align=left]::text'
        ):
            name = username.extract()
            txt_url = urljoin(
                response.request.url,
                self.exchange_link_fmt.format(username=name))
            yield PlayerItem(name=name, file_urls=[txt_url])
