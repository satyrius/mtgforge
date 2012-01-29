import re
import urllib
import urllib2
from urlparse import urlparse, urlunparse

from BeautifulSoup import ICantBelieveItsBeautifulSoup, BeautifulStoneSoup

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

class Provider(object):
    def __init__(self):
        self.provider = DataProvider.objects.get(name=self.name)

    def get_page(self, url):
        return urllib2.urlopen(url)

    @cache_method_calls
    def soup(self, url):
        """Fetch url and return ICantBelieveItsBeautifulSoup for the document.
        Do not use BeautifulSoup because source HTML is not perfect.
        """
        return ICantBelieveItsBeautifulSoup(
            self.get_page(url),
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
        )

    def absolute_url(self, href):
        o = urlparse(href)
        parts = list(urlparse(self.provider.home))
        if o.path:
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
        soup = self.soup(self.provider.home)
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
        query = u'?' + urllib.quote_plus(u'set=["{0}"]'.format(name), '=[]')
        return self.absolute_url(query)

    def products_list_generator(self):
        soup = self.soup(self.provider.home)
        select_id = 'ctl00_ctl00_MainContent_Content_SearchControls_setAddText'
        options = select(soup, 'select#{0} option'.format(select_id))
        for o in options:
            name = o.get('value')
            if not name or ignore_products_re.match(name):
                continue
            yield name, self.search_url(name), None


class MagiccardsProvider(Provider):
    name = 'magiccards'

    def products_list_generator(self):
        soup = self.soup(self.provider.home)
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
