import hashlib
import os
import urllib2
from urlparse import urlparse, urlunparse

from lxml.html import document_fromstring
from django.core.cache import get_cache
from django.utils.functional import wraps, curry
from django.utils.encoding import smart_str

from oracle.models import DataProvider, CardSet


class BadPageSource(Exception):
    pass


class Page(object):
    def __init__(self, source, use_cache=True):
        self.url = self._source_url(source)
        self._content = None
        self._doc = None
        self._use_cache = use_cache

    def _source_url(self, source):
        if isinstance(source, basestring):
            return source
        raise BadPageSource(u'Invalid page source: {0}'.format(source))

    def get_content(self):
        """Return page content as a string."""
        if self._content is None:
            if self._use_cache:
                cache = get_cache('provider_page')
                self._content = cache.get(self)
            if not self._content:
                self._content = urllib2.urlopen(self.url).read()
                if self._use_cache:
                    cache.set(self, self._content)
        return smart_str(self._content)

    def get_url_hash(self):
        return hashlib.sha1(self.url).hexdigest()

    @property
    def doc(self):
        """Get content and return lxml document"""
        if self._doc is None:
            self._doc = document_fromstring(self.get_content())
        return self._doc

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

    def __init__(self, source=None, *args, **kwargs):
        if source is None:
            source = self.get_provider().home
        super(ProviderPage, self).__init__(source, *args, **kwargs)

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


def map_result_as_pages(page_class=None):
    def decorator(func):
        @wraps(func)
        def result_wrapper(self, page_class=None, *args, **kwargs):
            result = func(self, *args, **kwargs)
            page_class = page_class or self.__class__
            return map(page_class, result)
        return curry(result_wrapper, page_class=page_class)
    return decorator
