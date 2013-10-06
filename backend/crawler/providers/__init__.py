import os
import re

import hashlib
import requests
from django.conf import settings
from django.core.cache import get_cache
from django.utils.encoding import smart_str
from django.utils.functional import wraps, curry
from lxml.html import document_fromstring
from urlparse import urlparse, urlunparse

from crawler.models import PageState
from oracle.models import CardSet, CardRelease


class BadPageSource(Exception):
    pass


class NoContent(Exception):
    pass


def canonocal_language(language):
    if language == 'English' or language is None:
        return 'en'
    elif language == 'Russian':
        return 'ru'
    elif language == 'Chinese Traditional':
        return 'tw'
    elif language == 'Chinese Simplified':
        return 'cn'
    elif language == 'German':
        return 'de'
    elif language == 'French':
        return 'fr'
    elif language == 'Italian':
        return 'it'
    elif language == 'Japanese':
        return 'jp'
    elif language == 'Korean':
        return 'ko'
    elif language in ('Portuguese', 'Portuguese (Brazil)',):
        return 'pt'
    elif language == 'Spanish':
        return 'es'
    else:
        raise Exception(u'Unknown language "{0}"'.format(language))


class Page(object):
    def __init__(self, source, name=None, read_cache=True, language=None):
        self.url = self._source_url(source)
        self._content = None
        self._state = None
        self._name = None
        self._doc = None
        self._read_cache = read_cache
        self._cache = get_cache('provider_page')
        self.name = name
        self.language = canonocal_language(language)

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

    def _dowload_content(self, url, hooks=None):
        return requests.get(url, hooks=hooks).text

    def force_read_cache(self):
        self._read_cache = True
        return self

    def get_content(self):
        """Return page content as a string."""
        if self._content is None:
            # Get cached page content
            if self._read_cache:
                self.name, self._content, self.state = \
                    self._get_cached_or_modified()
            # Download content of nothing was cached
            if not self._content:
                self._content = self._dowload_content(self.url)
                # Save the page content
                self._cache.set(self, self._content)
        return self._content is not None and smart_str(self._content) or None

    def delete_cache(self):
        self._cache.delete(self)

    def _get_name(self):
        if self._name is None and self._read_cache:
            self.name, self._content, self.state = \
                self._get_cached_or_modified()
        return self._name

    def _set_name(self, value):
        # Do not set empty name
        if value is not None:
            matches = re.match(r'[^(]+\(([^)]+)\)$', value)
            if matches:
                value = matches.group(1)
            self._name = value

    name = property(_get_name, _set_name)

    def _get_state(self):
        if self._state is None and self._read_cache:
            self.name, self._content, self.state = \
                self._get_cached_or_modified()
        return self._state or PageState.INITIAL

    def _set_state(self, value):
        self._state = value or PageState.INITIAL

    state = property(_get_state, _set_state)

    def change_state(self, state):
        # Set new state or use current state as default value. Also load
        # cached name and content while calling 'state' field getter
        if state is not None:
            self.state = state
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
    provider_class = None

    def __init__(self, source=None, *args, **kwargs):
        self._provider = self.provider_class()
        if source is None:
            source = self._provider.home
        super(ProviderPage, self).__init__(source, *args, **kwargs)

    def get_provider(self):
        return self._provider.name


class ProviderCardListPage(CardListPage, ProviderPage):
    def _source_url(self, source):
        self.card_set = None
        if isinstance(source, CardSet):
            cs = source
            self.card_set = cs
            return cs.sources.get(provider=self.get_provider()).url
        return super(CardListPage, self)._source_url(source)


class ProviderCardPage(CardPage, ProviderPage):
    def _source_url(self, source):
        self.card_release = None
        if isinstance(source, CardRelease):
            self.card_release = source
            return self.card_release.sources.get(
                provider=self.get_provider()).url
        return super(CardPage, self)._source_url(source)


def map_result_as_pages(page_class=None, map_data=None):
    """Wraps result url list and make it list of Page instances of given
    `page_class`. The additional data modifier callback may be passed as
    `map_data` keyword argument"""
    def decorator(func):
        @wraps(func)
        def result_wrapper(self, page_class=None, *args, **kwargs):
            result = func(self, *args, **kwargs)
            page_class = page_class or self.__class__

            def cls(r):
                if isinstance(r, dict):
                    page = page_class(
                        r['url'], language=r.get('lang', None),
                        name=r['name'], read_cache=self._read_cache)
                else:
                    page = page_class(r, read_cache=self._read_cache)
                if hasattr(self, 'card_release'):
                    page.card_release = self.card_release
                return page
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
            cache = get_cache(
                'default',
                TIMEOUT=settings.DATA_PROVIDER_CACHE_TIMEOUT,
                KEY_PREFIX=func.__name__)
            key = self.get_url_hash()

            result = self._read_cache and cache.get(key, default=[]) or None
            if not result:
                result = func(self, *args, **kwargs)

            cache.set(key, result)

            return result
        return curry(result_wrapper)
    return decorator
