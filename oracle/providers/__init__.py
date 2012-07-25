import os
import urllib2
from urlparse import urlparse, urlunparse

from BeautifulSoup import ICantBelieveItsBeautifulSoup, BeautifulStoneSoup
from django.core.cache import get_cache

from oracle.models import DataProvider, CardSet


class BadPageSource(Exception):
    pass


class Page(object):
    def __init__(self, source):
        self.url = self._source_url(source)
        self._content = None
        self._soup = None

    def _source_url(self, source):
        if isinstance(source, basestring):
            return source
        raise BadPageSource(u'Invalid page source: {0}'.format(source))

    def get_content(self):
        """Return page content as a string."""
        if self._content is None:
            cache = get_cache('provider_page')
            self._content = cache.get(self)
            if not self._content:
                self._content = urllib2.urlopen(self.url).read()
                cache.set(self, self._content)
        return self._content

    @property
    def soup(self):
        """Get content and return ICantBelieveItsBeautifulSoup for the document.
        Do not use BeautifulSoup because source HTML is not perfect.
        """
        if not self._soup:
            self._soup = ICantBelieveItsBeautifulSoup(
                self.get_content(),
                convertEntities=BeautifulStoneSoup.HTML_ENTITIES
            )
        return self._soup

    def absolute_url(self, href):
        o = urlparse(href)
        parts = list(urlparse(self.url))
        if o.path:
            if o.path.startswith('..'):
                base_path = os.path.dirname(parts[2])
                parts[2] = os.path.abspath(os.path.join(base_path, o.path))
            else:
                parts[2] = o.path
        parts[4] = o.query or ''
        return urlunparse(parts)


class HomePage(Page):
    def products_list_generator(self):
        """Each product is a tuple. First element is a product name, second is
        a card number, third is a dict with additional info or None.
        """
        raise NotImplementedError

    def products_list(self):
        return [p for p in self.products_list_generator()]


class CardListPage(Page):
    def cards_list_generator(self):
        """Each card in the list is a tuple. First element is a card's name,
        second is GardPage instance.
        """
        raise NotImplementedError


class CardPage(Page):
    def details(self):
        """Parse page and returns dard details dict"""
        raise NotImplementedError


class ProviderPage(Page):
    name = None
    _data_provider = None

    def __init__(self, source=None):
        if source is None:
            source = self.get_provider().home
        super(ProviderPage, self).__init__(source)

    def get_provider(self):
        if not self._data_provider:
            self._data_provider = DataProvider.objects.get(name=self.name)
        return self._data_provider


class ProviderCardListPage(CardListPage, ProviderPage):
    def _source_url(self, source):
        self.card_set = None
        if isinstance(source, CardSet):
            cs = source
            self.card_set = cs
            return cs.sources.get(data_provider=self.get_provider()).url
        return super(CardListPage, self)._source_url(source)


class ProviderCardPage(CardPage, ProviderPage):
    pass
