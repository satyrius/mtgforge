# -*- coding: utf-8 -*-
import StringIO

from django.test import TestCase
from mock import Mock

from oracle.models import DataProvider
from oracle.providers import WizardsProvider, GathererProvider, MagiccardsProvider
from oracle.tests import fixtures


class DataProvidersTest(TestCase):
    fixtures = ['data_provider']

    def test_normalize_href(self):
        p = WizardsProvider()
        self.assertEqual(p.absolute_url('/foo/bar.aspx'),
                         'http://wizards.com/foo/bar.aspx')
        self.assertEqual(p.absolute_url('/foo.aspx?x=1'),
                         'http://wizards.com/foo.aspx?x=1')
        self.assertEqual(p.absolute_url('?x=1'),
                         'http://wizards.com/magic/tcg/Article.aspx?x=1')
        self.assertEqual(p.absolute_url('../foo/Bar.aspx'),
                         'http://wizards.com/magic/foo/Bar.aspx')
        self.assertEqual(p.absolute_url('../foo/Bar.aspx',
                                        'http://wizards.com/magic/tcg/mtg/Article.aspx'),
                         'http://wizards.com/magic/tcg/foo/Bar.aspx')

    def test_provider_factory(self):
        wizards = DataProvider.objects.get(name='wizards')
        provider = wizards.provider
        self.assertIsInstance(provider, WizardsProvider)
        # Assert that property always return the same instance
        self.assertEqual(provider, wizards.provider)

        gatherer = DataProvider.objects.get(name='gatherer')
        self.assertNotEqual(gatherer.provider, wizards.provider)

    def _mock_provider_get_page(self, provider, fixture):
        provider.get_page = Mock(return_value=StringIO.StringIO(fixture))

    def test_wizards_list(self):
        p = WizardsProvider()
        self._mock_provider_get_page(p, fixtures.wizards_home_page)
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://wizards.com/magic/tcg/products.aspx?x=mtg/tcg/products/zendikar', {'cards': 249, 'release': 'October 2009'})
        ])

    def test_magiccards_list(self):
        p = MagiccardsProvider()
        self._mock_provider_get_page(p, fixtures.magiccards_home_page)
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://magiccards.info/zen/en.html', {'acronym': 'zen'})
        ])

    def test_gatherer_list(self):
        p = GathererProvider()
        self._mock_provider_get_page(p, fixtures.gatherer_home_page)
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Zendikar%22%5D', None)
        ])
