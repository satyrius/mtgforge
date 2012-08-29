# -*- coding: utf-8 -*-
import urllib
from StringIO import StringIO

from django.test import TestCase
from django.test.utils import override_settings
from lxml.html import HtmlElement
from mock import Mock, patch

from oracle.models import DataProvider, DataSource, CardSet, DataProviderPage
from oracle.providers import BadPageSource, Page
from oracle.providers.gatherer import GathererPage, GathererHomePage, GathererCardList
from oracle.providers.magiccards import MagiccardsHomePage
from oracle.providers.wizards import WizardsHomePage
from oracle.tests import fixtures
from oracle.tests.helpers import get_html_fixture


@override_settings(CACHES={
    'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'},
    'provider_page': {'BACKEND': 'oracle.providers.cache.PageCache'},
})
class DataProvidersTest(TestCase):
    fixtures = ['data_provider', 'card_set']
    zen_url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Zendikar%22%5D'

    def test_page_init(self):
        url = 'http://example.com/magic/tcg/home.html'
        p = Page(url)
        self.assertEqual(p.url, url)

        with self.assertRaises(BadPageSource):
            p = Page(None)

    def test_normalize_href(self):
        p = Page('http://example.com/magic/tcg/home.html')
        self.assertEqual(p.absolute_url('/foo/bar.html'),
                         'http://example.com/foo/bar.html')
        self.assertEqual(p.absolute_url('/foo.html?x=1'),
                         'http://example.com/foo.html?x=1')
        self.assertEqual(p.absolute_url('?x=1'),
                         'http://example.com/magic/tcg/home.html?x=1')
        self.assertEqual(p.absolute_url('../foo/bar.html'),
                         'http://example.com/magic/foo/bar.html')

    @patch.object(Page, 'get_content')
    def test_get_doc(self, patched_content):
        page_content = '<html><h1>Example</h1></html>'
        patched_content.return_value = page_content

        p = Page('http://example.com/')
        # Call doc property
        doc = p.doc
        self.assertIsInstance(doc, HtmlElement)
        # Call againt and it is still the same instance
        self.assertEqual(p.doc, doc)

    def test_home_page(self):
        gatherer_page = GathererHomePage()
        gatherer = DataProvider.objects.get(name='gatherer')
        self.assertEqual(gatherer_page.url, gatherer.home)

        wizards_page = WizardsHomePage()
        wizards = DataProvider.objects.get(name='wizards')
        self.assertEqual(wizards_page.url, wizards.home)
        self.assertNotEqual(wizards_page.url, gatherer_page.url)

        magiccards_page = MagiccardsHomePage()
        magiccards = DataProvider.objects.get(name='magiccards')
        self.assertEqual(magiccards_page.url, magiccards.home)
        self.assertNotEqual(magiccards_page.url, gatherer_page.url)
        self.assertNotEqual(magiccards_page.url, wizards_page.url)

    def _mock_page_get_content(self, page, fixture):
        page.get_content = Mock(return_value=fixture)

    def test_wizards_list(self):
        p = WizardsHomePage()
        self._mock_page_get_content(p, fixtures.wizards_home_page)
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://wizards.com/magic/tcg/products.aspx?x=mtg/tcg/products/zendikar', {'cards': 249, 'release': 'October 2009'})
        ])

    def test_magiccards_list(self):
        p = MagiccardsHomePage()
        self._mock_page_get_content(p, fixtures.magiccards_home_page)
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://magiccards.info/zen/en.html', {'acronym': 'zen'})
        ])

    def test_gatherer_list(self):
        p = GathererHomePage()
        self._mock_page_get_content(p, fixtures.gatherer_home_page)
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Zendikar%22%5D', None)
        ])

    def test_cards_list_page(self):
        cs = CardSet.objects.all()[0]
        page = GathererPage()
        gatherer = page.get_provider()
        url = page.absolute_url(urllib.quote_plus(cs.name))
        compact_url = url + '?output=compact'
        DataSource.objects.create(content_object=cs, url=url, data_provider=gatherer)

        # Create Gatherer cards list page with simple init interface
        list_page = GathererCardList(cs)
        self.assertEqual(list_page.url, compact_url)
        # Create Gatherer cards list page with page url passed
        list_page = GathererCardList(url)
        self.assertEqual(list_page.url, compact_url)

        # Test adding `output` parameter to existing query
        zen_url = self.zen_url
        compact_zen_url = zen_url + '&output=compact'
        list_page = GathererCardList(zen_url)
        self.assertEqual(list_page.url, compact_zen_url)
        # Test fixing output parameter
        zen_url += '&output=standard'
        list_page = GathererCardList(zen_url)
        self.assertEqual(list_page.url, compact_zen_url)

    @patch.object(Page, 'get_content')
    def test_card_list_pagination(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_list')

        # Get Zendikar card set and create DataSource record for it, because
        # its url will be used as `url` in list page init
        zen = CardSet.objects.get(acronym='zen')
        DataSource.objects.create(
            content_object=zen,
            url=self.zen_url,
            data_provider=GathererPage().get_provider())
        page = GathererCardList(zen)

        urls = []
        for p in page.pages_generator():
            self.assertIsInstance(p, GathererCardList)
            urls.append(p.url)
        self.assertEqual(urls, [
            'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&action=advanced&set=+%5b%22Zendikar%22%5d&output=compact',
            'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=1&action=advanced&set=+%5b%22Zendikar%22%5d&output=compact',
            'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=2&action=advanced&set=+%5b%22Zendikar%22%5d&output=compact'
        ])

    @patch('urllib2.urlopen')
    def test_cache(self, urlopen):
        page_content = get_html_fixture('gatherer_list')
        urlopen.return_value = StringIO(page_content)
        self.assertEqual(urlopen.call_count, 0)

        # Create a page, get its content, and assert http request called
        page1 = GathererCardList(self.zen_url)
        # Access doc property to trigger lxml parser
        page1.doc
        self.assertEqual(page1.get_content(), page_content)
        self.assertEqual(urlopen.call_count, 1)
        cache_entry = DataProviderPage.objects.get(url=page1.url)
        self.assertEqual(cache_entry.data_provider, page1.get_provider())

        # Create the page again with the same url and test cache hit. Second
        # instance is to exclude in-memory cache hit.
        page2 = GathererCardList(self.zen_url)
        page2.doc
        self.assertEqual(page2.get_content(), page_content)
        self.assertEqual(urlopen.call_count, 1)

        self.assertTrue(page1.url.startswith(self.zen_url))
        urlopen.assert_called_once_with(page1.url)

    @patch('urllib2.urlopen')
    def test_common_page_cache(self, urlopen):
        page_content = get_html_fixture('gatherer_list')
        urlopen.return_value = StringIO(page_content)
        dummy_url = 'http://example.com/foo/bar.html'

        # Common page has empty provider FK
        page2 = Page(dummy_url)
        self.assertEqual(page2.get_content(), page_content)
        cache_entry = DataProviderPage.objects.get(url=dummy_url)
        self.assertIsNone(cache_entry.data_provider)
