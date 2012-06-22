import os
import re
import urllib
import urllib2
from hashlib import sha1
from StringIO import StringIO
from urlparse import urlparse, urlunparse

from BeautifulSoup import ICantBelieveItsBeautifulSoup, BeautifulStoneSoup
from django.conf import settings
from django.core.cache import cache

from contrib.soupselect import select
from contrib.utils import cache_method_calls
from oracle.models import DataProvider


# Ignore products which was printed without new expansion sybmol
ignore_products = [
    'World Champ Decks',
    'Premium Foil Booster',
    'Momir Vig Basic',
    'Legacy',
    'Deck Builder\'s Toolkit',
    'Vanguard',
    'Promo set for Gatherer', # This name is from Gatherer's list
]
ignore_products_re = re.compile('|'.join(ignore_products))


class ProviderMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(ProviderMeta, cls).__new__(cls, name, bases, attrs)
        if name is not 'Provider':
            new_class._providers[attrs['name']] = new_class
        return new_class


class Provider(object):
    __metaclass__ = ProviderMeta
    _providers = {}

    def __init__(self, data_provider=None):
        if data_provider and self.name != data_provider.name:
            raise Exception(
                u'DataProvider data_provider name "{0}" does not match provider name "{1}"'.format(
                    data_provider.name, self.name))
        self.data_provider = data_provider or \
            DataProvider.objects.get(name=self.name)

    @classmethod
    def factory(cls, model):
        return cls._providers[model.name](model)

    def get_page(self, url):
        k = sha1(url).hexdigest()
        content = cache.get(k)
        if not content:
            content = urllib2.urlopen(url).read()
            cache.set(k, content, settings.DATA_PROVIDER_TIMEOUT)
        return StringIO(content)

    @cache_method_calls
    def soup(self, url):
        """Fetch url and return ICantBelieveItsBeautifulSoup for the document.
        Do not use BeautifulSoup because source HTML is not perfect.
        """
        return ICantBelieveItsBeautifulSoup(
            self.get_page(url),
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
        )

    def absolute_url(self, href, base=None):
        o = urlparse(href)
        parts = list(urlparse(base or self.data_provider.home))
        if o.path:
            if o.path.startswith('..'):
                base_path = os.path.dirname(parts[2])
                parts[2] = os.path.abspath(os.path.join(base_path, o.path))
            else:
                parts[2] = o.path
        parts[4] = o.query or ''
        return urlunparse(parts)

    def products_list_generator(self):
        """Eack product is a tuple. First element is a product name, second is
        a card number, third is a dict with additional info or None"""
        raise NotImplementedError

    def products_list(self):
        return [p for p in self.products_list_generator()]


class WizardsProvider(Provider):
    name = 'wizards'

    def products_list_generator(self):
        soup = self.soup(self.data_provider.home)
        product_link_re = re.compile(r'x=mtg[/_]tcg[/_](?:products[/_]([^/_]+)|([^/_]+)[/_]productinfo)$')
        cards_count_re = re.compile(r'(\d+)\s+cards', re.IGNORECASE)
        separator_re = re.compile(r'\s*(?:,|and)\s*')
        for link in select(soup, 'div.article-content a'):
            href = link.get('href')
            if not href:
                continue
            match = product_link_re.search(href)
            if match:
                name = re.sub(r'\s+', ' ', link.getText(u' ')).strip()
                if ignore_products_re.match(name):
                    continue

                cards = link.findParent('td').findNextSibling('td')
                match_cards = cards_count_re.match(cards.text.strip())
                cards_count = match_cards and int(match_cards.group(1)) or None

                release = cards.findNextSibling('td').find('br').nextSibling.strip()
                release_date = release or None

                url = self.absolute_url(href)
                result = lambda name: (name, url, dict(cards=cards_count, release=release_date))
                if ',' in name:
                    # Comma separated editions
                    for separated_name in filter(None, separator_re.split(name)):
                        yield result(separated_name)
                else:
                    yield result(name)


class GathererProvider(Provider):
    name = 'gatherer'

    def search_url(self, name):
        query = u'/Pages/Search/Default.aspx?' + urllib.quote_plus(u'set=["{0}"]'.format(name), '=')
        return self.absolute_url(query)

    def products_list_generator(self):
        soup = self.soup(self.data_provider.home)
        select_id = 'ctl00_ctl00_MainContent_Content_SearchControls_setAddText'
        options = select(soup, 'select#{0} option'.format(select_id))
        for o in options:
            name = o.get('value')
            if not name or ignore_products_re.match(name):
                continue
            yield name, self.search_url(name), None

    def card_set_source(self, card_set):
        return card_set.sources.get(data_provider__name=self.name)

    def cards_list_url(self, card_set):
        source = self.card_set_source(card_set)
        return '{0}&output=compact'.format(source.url)

    def cards_pages_generator(self, card_set):
        url = self.cards_list_url(card_set)
        start_page_soup = self.soup(url)
        pagination = select(start_page_soup, 'div.pagingControls a')
        if pagination:
            for page_link in pagination:
                page_url = page_link.get('href')
                if not page_url or not page_link.text.strip().isdigit():
                    continue
                page_url = self.absolute_url(page_url)
                yield self.soup(page_url), page_url
        else:
            yield start_page_soup, url

    def _replace_mana_img(self, img):
        mana_re = re.compile(r'name=(.+?)&')
        mana = unicode(mana_re.search(img.get('src')).groups()[0])
        img.replaceWith(u'{' + mana + u'}')

    def _encode_mana(self, html_el):
        map(self._replace_mana_img, select(html_el, 'img'))

    def _normalize_spaces(self, text):
        text = re.sub(r'(?<!\(|\{|\s)\{', ' {', text)
        text = re.sub(r'\}(?!=\)|\}|\s|\:)', '} ', text)
        text = re.sub(r'}\s+{', '}{', text)
        return text

    def _normalize_puct(self, text):
        text = re.sub(u'\xe2\x80\x99|\u2019', '\'', text)
        text = re.sub(u'\s*(\xe2\x80\x94|\u2014)\s*', ' - ', text)
        return text

    def parse_mana(self, html_el):
        self._encode_mana(html_el)
        return html_el.getText()

    def parse_text(self, html_el):
        blocks = []
        for block in select(html_el, 'div.cardtextbox'):
            self._encode_mana(block)
            blocks.append(block.getText())
        text = self._normalize_spaces('\n'.join(blocks))
        return self._normalize_puct(text)

    def card_details(self, url, name, oracle_text=True):
        '''Fetch cards details from page by given `url`. Use `name` to choose
        cards face or flip to choose'''
        card_page_soup = self.soup(url)

        found = False
        subcontent_re = re.compile('MainContent_SubContent_SubContent')
        name_row_key = 'name'
        to_normalize = ['name', 'text', 'type']
        for face in select(card_page_soup, 'table.cardDetails'):
            details = {}
            for subcontent in select(face, 'td.rightCol div.row'):
                id = subcontent.get('id')
                if subcontent_re.search(id):
                    k = id.split('_')[-1][:-3]
                    el = select(subcontent, 'div.value')[0]
                    parse_method_name = 'parse_' + k
                    if hasattr(self, parse_method_name):
                        v = getattr(self, parse_method_name)(el)
                    else:
                        v = el.getText()
                    if k in to_normalize:
                        v = self._normalize_puct(v)
                    if k == name_row_key and v != name:
                        break
                    details[k] = v.strip()
            if name_row_key in details:
                found = True
                art_src = select(face, 'td.leftCol img')[0].get('src')
                details['art'] = self.absolute_url(art_src, url)
                break

        if not found:
            raise Exception(u'Card \'{0}\' not found on page \'{1}\''.format(
                name, url))

        details['url'] = url

        if oracle_text:
            printed_rulings_url = select(card_page_soup, '#cardTextSwitchLink2')[0].get('href')
            printed_details = self.card_details(
                url=self.absolute_url(printed_rulings_url, url),
                name=name, oracle_text=False)
            printed_details['oracle'] = details
            details = printed_details

        other_names = []
        for name_block in select(card_page_soup, 'td.rightCol div[id$="nameRow"] div.value'):
            value = self._normalize_spaces(name_block.getText())
            if value != name:
                other_names.append(value)
        if other_names:
            details['other_faces'] = other_names

        return details

    def cards_list_generator(self, card_set, full_info=False, names=None):
        '''Generates list of cards info for given card set. If `full_info`
        argument is True fetch card details page for complete details. If
        names argument passed, fetch infor only for those cards.'''
        mvid_re = re.compile('multiverseid\=(?P<id>\d+)')
        for page_soup, page_url in self.cards_pages_generator(card_set):
            for row in select(page_soup, 'tr.cardItem td.name'):
                card_link = row.find('a')
                name = self._normalize_puct(card_link.text.strip())
                if names and name not in names:
                    continue
                url = self.absolute_url(card_link.get('href'), page_url)
                m = mvid_re.search(url)
                if not m:
                    raise Exception('Cannot get multiverseid for {0}'.format(name))
                extra = dict(mvid=m.group('id'))
                if full_info:
                    extra.update(self.card_details(url, name))
                yield name, url, extra


class MagiccardsProvider(Provider):
    name = 'magiccards'

    def products_list_generator(self):
        soup = self.soup(self.data_provider.home)
        english_header = filter(lambda el: el.text.strip().startswith('English'), soup.findAll('h2'))[0]
        for link in english_header.findNextSibling('table').findAll('a'):
            href = link.get('href')
            if not href:
                continue
            name = link.text.strip()
            if ignore_products_re.match(name):
                continue
            acronym = link.findNextSibling('small').text.strip() or None
            yield name, self.absolute_url(href), dict(acronym=acronym)
