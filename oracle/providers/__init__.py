import hashlib
import os
import re
import urllib2
from urlparse import urlparse, urlunparse

from lxml.html import document_fromstring
from django.conf import settings
from django.core.cache import get_cache
from django.utils.functional import wraps, curry
from django.utils.encoding import smart_str

from oracle.models import DataProvider, CardSet, PageState


class BadPageSource(Exception):
    pass


class NoContent(Exception):
    pass


class Page(object):
    def __init__(self, source, name=None, use_cache=True):
        self.url = self._source_url(source)
        self._content = None
        self._state = None
        self._name = None
        self._doc = None
        self._use_cache = use_cache
        self._cache = get_cache('provider_page')
        self.name = name

    def _source_url(self, source):
        if isinstance(source, basestring):
            return source
        raise BadPageSource(u'Invalid page source: {0}'.format(source))

    def _get_cached_or_modified(self):
        name, content, state = self._cache.get(self)
        return \
            self._name or name, \
            self._content or content, \
            self._state or state

    def get_content(self):
        """Return page content as a string."""
        if self._content is None:
            # Get cached page content
            if self._use_cache:
                self.name, self._content, self.state = \
                    self._get_cached_or_modified()
            # Download content of nothing was cached
            if not self._content:
                self._content = urllib2.urlopen(self.url).read()
                # Save the page content
                if self._use_cache:
                    self._cache.set(self, self._content)
        return self._content is not None and smart_str(self._content) or None

    def delete_cache(self):
        self._cache.delete(self)

    @property
    def name(self):
        if self._name is None and self._use_cache:
            self.name, self._content, self.state = \
                self._get_cached_or_modified()
        return self._name

    @name.setter
    def name(self, value):
        # Do not set empty name
        if value is not None:
            matches = re.match(r'[^(]+\(([^)]+)\)$', value)
            if matches:
                value = matches.group(1)
            self._name = value

    @property
    def state(self):
        if self._state is None:
            if self._use_cache:
                self.name, self._content, self.state = \
                    self._get_cached_or_modified()
        return self._state

    @state.setter
    def state(self, value):
        self._state = value or PageState.INITIAL

    def change_state(self, state):
        # Set new state or use current state as default value. Also load
        # cached name and content while calling 'state' field getter
        if state is not None:
            self.state = state
        if self._use_cache:
            if self._content is None:
                raise NoContent(
                    'You should download page before changing it\'s state')
            self._cache.set(self, self._content)

    def get_url_hash(self):
        return hashlib.sha1(self.url).hexdigest()

    @property
    def doc(self):
        """Get content and return lxml document"""
        if self._doc is None:
            self._doc = document_fromstring(self.get_content())
            self.doc.make_links_absolute(self.url)
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
    def cards_list(self):
        """Each card in the list is a tuple. First element is a card's name,
        second is GardPage instance.
        """
        raise NotImplementedError


class CardPage(Page):
    def details(self):
        """Parse page and return card details dict"""
        raise NotImplementedError


class ProviderPage(Page):
    provider_name = None
    _data_provider = None

    def __init__(self, source=None, *args, **kwargs):
        if source is None:
            source = self.get_provider().home
        super(ProviderPage, self).__init__(source, *args, **kwargs)

    def get_provider(self):
        if not self._data_provider:
            self._data_provider = DataProvider.objects.get(name=self.provider_name)
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


def map_result_as_pages(page_class=None, map_data=None):
    """Wraps result url list and make it list of Page instances of given
    `page_class`. The additional data modifier callback may be passed as
    `map_data` keyword argument"""
    def decorator(func):
        @wraps(func)
        def result_wrapper(self, page_class=None, *args, **kwargs):
            result = func(self, *args, **kwargs)
            page_class = page_class or self.__class__
            cls = lambda r: isinstance(r, tuple) and \
                    page_class(r[1], name=r[0]) or page_class(r)
            pages = map(cls, result)
            if map_data:
                map(curry(map_data, self), pages)
            return pages
        return curry(result_wrapper, page_class=page_class)
    return decorator


def cache_parsed():
    def decorator(func):
        @wraps(func)
        def result_wrapper(self, *args, **kwargs):
            if self._use_cache:
                cache = get_cache(
                    'default',
                    TIMEOUT=settings.DATA_PROVIDER_CACHE_TIMEOUT,
                    KEY_PREFIX=func.__name__)
                key = self.get_url_hash()
                result = cache.get(key, default=[])
            else:
                result = None

            if not result:
                result = func(self, *args, **kwargs)

            if self._use_cache:
                cache.set(key, result)

            return result
        return curry(result_wrapper)
    return decorator
