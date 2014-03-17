import itertools as it
import re
import sys
import urlparse as up
from collections import OrderedDict
from urllib import urlencode

from lxml import etree
from lxml.html import document_fromstring
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector

from crawler.items import CardItem, L10nItem


class GathererSpider(CrawlSpider):
    name = 'gatherer'
    allowed_domains = ['gatherer.wizards.com']
    search_url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx'

    def __init__(self, card_set=None, *args, **kwargs):
        '''You should specify card set to parse. Use names from Gatherer
        search form. Otherwise names will be read from stdin.
        '''
        self.card_set = card_set

    def card_set_names(self):
        if self.card_set:
            yield self.card_set
        else:
            for name in sys.stdin.readlines():
                yield name.strip()

    def start_requests(self):
        for name in self.card_set_names():
            yield FormRequest(
                url=self.search_url, method='GET',
                callback=self.parse_list,
                formdata={'set': '[%s]' % name, 'output': 'compact'})

    def parse_list(self, response):
        '''Parse compact card list and follow card details for each printing.
        '''
        # Follow pagination
        sel = Selector(response)
        for page_link in sel.css('div.pagingControls a'):
            page_url = page_link.xpath('@href').extract()[0]
            page_num = page_link.xpath('text()').extract()[0].strip()
            if page_url and page_num.isdigit():
                yield Request(
                    up.urljoin(response.request.url, page_url),
                    callback=self.parse_list)

        sel = Selector(response)
        for card_row in sel.css('tr.cardItem'):
            a = card_row.css('td.name a')
            card_url = a.xpath('@href').extract()[0]

            # Next we should parse 'printings' block. It contains card links
            # for all card releases in all sets. We will get all links for
            # current set. We should use these links because some cards might
            # have several printing in one set (e.g. Forest, High Tide)
            get_href = lambda a: a.xpath('@href').extract()[0]
            get_alt = lambda a: a.xpath('.//img/@alt').extract()[0]
            printings = {get_href(a): get_alt(a) for a in card_row.css(
                'td.printings a')}
            slug = printings[card_url]

            for url, cs in printings.items():
                if cs == slug:
                    yield Request(
                        up.urljoin(response.request.url, url),
                        callback=self.parse_card)

    def extract_mana(self, el_selector):
        # We dont need to use `encode_mana` here, because mana value node
        # contains only mana symbols. It's easy to extract them from
        # img sources params.
        mana = el_selector.xpath('.//img/@src').re(r'name=(.+?)&')
        return ''.join(['{%s}' % s for s in mana])

    def extract_text(self, el_selector):
        blocks = []
        for block in el_selector.css('div.cardtextbox'):
            blocks.append(extract_text(encode_mana(block)))
        return '\n'.join(blocks).strip()

    def extract_rarity(self, el_selector):
        value = extract_text(el_selector)
        # Workaround with Wizards' dummies
        if value == u'Basic Land':
            value = u'Common'
        return value

    def parse_card(self, response):
        '''Parse compact card list and follow card details for each printing.
        '''
        sel = Selector(response)
        page_url = response.request.url
        is_printed = is_printed_url(page_url)
        ignore_fields = ['player_rating', 'other_sets']
        subcontent_re = re.compile('MainContent_SubContent_SubContent')

        # Card title
        title = extract_text(sel.css(
            'div.contentTitle span::text').extract()[0].strip())
        suffixes = number_suffixes(title)

        # Get name for all card face on the card page
        faces = sel.css('table.cardDetails')
        names = [n.strip() for n in faces.css(
            'td.rightCol div[id$="nameRow"] div.value::text').extract()]

        # We have to extract splited card names from the tile, because
        # card's printed vertion name contains both names for each face.
        if len(names) == 2 and '//' in title and is_printed:
            names = suffixes.keys()

        names_set = set(names)
        # Big Fury Monster case. It's page looks like a double faced card page,
        # but phisically it is a one card released twice with the same name
        # (like a basic lands).
        is_bfm = len(names) > len(names_set)

        # Double faced cards has only one name in title, we should use first
        if len(names) > 1 and len(suffixes) == 1:
            title = names[0]

        for i, details in enumerate(faces):
            card = CardItem(title=title)

            # Iterate over card details rows and parse data
            for field_row in details.css('td.rightCol div.row'):
                id = field_row.xpath('@id').extract()[0]
                if subcontent_re.search(id):
                    k = id.split('_')[-1][:-3]
                    # Camel case to underscore
                    k = re.sub('([A-Z]+)', r'_\1', k).lower()
                    if k in ignore_fields:
                        continue
                    value = field_row.css('div.value')
                    extract = 'extract_' + k
                    if hasattr(self, extract):
                        value = getattr(self, extract)(value)
                    else:
                        value = extract_text(value)

                    # Special name processing for multifaces cards
                    if k == 'name' and len(names) > 1 and not is_bfm:
                        # Use name parsed from card totle for splited cards
                        # localization, because name field contains title,
                        # not a spell name.
                        if value == title:
                            value = names[i]
                        # Get sibling name for multifaces cards
                        card['sibling'] = (names_set - {value}).pop()

                    card[k] = value

            # Fix card numner suffix
            if 'number' in card and len(suffixes) > 1:
                card['number'] = re.sub(r'\D+', '', card['number']) + \
                    suffixes[card['name']]

            # Get image url and extract multiverse id
            card['art'] = up.urljoin(page_url, details.css(
                'td.leftCol img::attr(src)').extract()[0])

            if not is_printed:
                # Oracle rules page
                yield card
            else:
                card_l10n = L10nItem()
                # Copy shared fields from card item
                for n, _ in card_l10n.fields.items():
                    card_l10n[n] = card.get(n)
                card_l10n['language'] = response.meta.get('language')
                yield card_l10n

        # Go to Languages
        if not is_printed:
            yield Request(
                url=printed_url(page_url),
                callback=self.parse_card,
                meta={'language': 'English'})

            lid = 'ctl00_ctl00_ctl00_MainContent_SubContent_'\
                  'SubContentAnchors_DetailsAnchors_LanguagesLink'
            langs = sel.css('#{id}::attr("href")'.format(id=lid)).extract()[0]
            yield Request(
                url=up.urljoin(page_url, langs),
                callback=self.parse_languages)

    def parse_languages(self, response):
        sel = Selector(response)
        page_url = response.request.url
        for row in sel.css('table.cardList tr.cardItem'):
            cells = row.xpath('.//td')
            href = cells[0].xpath('.//a/@href').extract()[0]
            print_url = printed_url(up.urljoin(page_url, href))
            lang = cells[1].xpath('text()').extract()[0].strip()
            yield Request(
                url=print_url,
                callback=self.parse_card,
                meta={'language': lang})

        page_url = response.request.url
        for link in sel.css('div.pagingControls a'):
            if link.xpath('text()').extract()[0].strip().isdigit():
                yield Request(
                    url=up.urljoin(page_url, link.xpath('@href').extract()[0]),
                    callback=self.parse_languages)


def printed_url(url):
    parts = list(up.urlparse(url))
    query = dict(up.parse_qsl(parts[4]))
    query['printed'] = 'true'
    parts[4] = urlencode(query)
    return up.urlunparse(parts)


def is_printed_url(url):
    parts = list(up.urlparse(url))
    query = dict(up.parse_qsl(parts[4]))
    return 'printed' in query and query['printed'].lower() == 'true'


def extract_text(element):
    '''Extract text from element and its descendants. It also normalizes
    spaces and other valuable symbols.
    '''
    is_selector = lambda e: isinstance(e, Selector)
    if is_selector(element) or (isinstance(element, list) and all(is_selector(e) for e in element)):
        text = ' '.join(element.xpath('.//text()').extract())
    elif isinstance(element, basestring):
        text = element
    else:
        raise Exception('Dont know how to normalize text for %s' % element)

    # Backup newlines
    nl = '__new_line__'
    text = re.sub(u'\n', nl, text)
    # Normalize spaces
    text = re.sub(u'\xa0', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    text = re.sub(u'\xe2\x80\x99|\u2019', '\'', text)
    text = re.sub(u'\s*(\xe2\x80\x94|\u2014)\s*', ' - ', text)

    # Remove spaces around bracets
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'(?<!\(|\{|\s|\d)\{', ' {', text)
    text = re.sub(r'\}(?!=\)|\}|\s|\:)', '} ', text)
    text = re.sub(r'}\s+{', '}{', text)

    # Restore line endings and strip final string
    text = re.sub(u'{0}\s*'.format(nl), '\n', text)
    return text.strip()


def encode_mana(el_selector):
    # Unfortunately, Scrapy operates with XPathSelector and dont give
    # access to selected element instances. We have to create html
    # document and use lxml api to access img elements and replace them
    # with mana-encoded text.
    html_el = document_fromstring(el_selector.extract())

    mana_re = re.compile(r'name=(.+?)&')
    for img in html_el.cssselect('img'):
        mana = unicode(mana_re.search(img.get('src')).groups()[0])
        # Add text representation to each mane img
        img.tail = u'{' + mana + u'}' + unicode(img.tail or '')
    # Remove images, only mana-encoded text will remain
    etree.strip_elements(html_el, 'img', with_tail=False)

    # Walk all elements recursively to concatenate all text nodes
    def gettext(elem):
        parts = [elem.text or '']
        for e in elem:
            parts.append(gettext(e))
            if e.tail:
                parts.append(e.tail)
        return ' '.join(parts).strip()
    return gettext(html_el)


def number_suffixes(title):
    names = re.split(r'\s+//\s+', title)

    # No need to add any suffixes for not splited cards
    if len(names) == 1:
        return OrderedDict({title: ''})

    return OrderedDict((n, s) for n, s in it.izip(names, 'abcdefg'))
