# -*- coding: utf-8 -*-
import StringIO
import urllib

from BeautifulSoup import ICantBelieveItsBeautifulSoup
from django.test import TestCase
from mock import Mock, patch

from oracle.models import DataProvider, DataSource, CardSet
from oracle.providers import BadPageSource, Page
from oracle.providers.gatherer import GathererPage, GathererHomePage, GathererCardList
from oracle.providers.magiccards import MagiccardsHomePage
from oracle.providers.wizards import WizardsHomePage
from oracle.tests import fixtures


class DataProvidersTest(TestCase):
    fixtures = ['data_provider', 'card_set']

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

    @patch('urllib2.urlopen')
    def test_get_content(self, patched_urlopen):
        url = 'http://example.com/'
        page_content = '<html><h1>Example</h1></html>'
        patched_urlopen.return_value = page_content

        p = Page(url)
        # Call get_content
        self.assertEqual(p.get_content(), page_content)
        # Call again and assert result is cached
        self.assertEqual(p.get_content(), page_content)

        patched_urlopen.assert_called_once_with(url)

    @patch.object(Page, 'get_content')
    def test_get_soup(self, patched_content):
        page_content = '<html><h1>Example</h1></html>'
        patched_content.return_value = page_content

        p = Page('http://example.com/')
        # Call soup property
        soup = p.soup
        self.assertIsInstance(soup, ICantBelieveItsBeautifulSoup)
        # Call againt and it is still the same instance
        self.assertEqual(p.soup, soup)

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
        page.get_content = Mock(return_value=StringIO.StringIO(fixture))

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
        zen_url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Zendikar%22%5D'
        compact_zen_url = zen_url + '&output=compact'
        list_page = GathererCardList(zen_url)
        self.assertEqual(list_page.url, compact_zen_url)
        # Test fixing output parameter
        zen_url += '&output=standard'
        list_page = GathererCardList(zen_url)
        self.assertEqual(list_page.url, compact_zen_url)
