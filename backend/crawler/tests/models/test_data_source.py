# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase
from django_any import any_model

from crawler.providers.base import Gatherer
from crawler.providers.gatherer import GathererPage
from crawler.models import DataSource
from oracle.models import CardSet


class DataSourceTest(TestCase):
    def setUp(self):
        self.data_provider = Gatherer()
        self.new_data = dict(name='new', title='New Gatherer',
                             home='http://example.com')

    def test_add_data_source(self):
        cs = any_model(CardSet)
        page = GathererPage()
        provider = page.get_provider()
        url = page.absolute_url('/link/for/this/card/set')
        self.assertEqual(cs.sources.count(), 0)

        # Create data source generic relation
        ds = DataSource.objects.create(content_object=cs, url=url, provider=provider)

        # Check reverse relation
        self.assertEqual(cs.sources.count(), 1)
        self.assertEqual(cs.sources.all()[0].id, ds.id)
        self.assertEqual(cs.sources.get(provider=provider).id, ds.id)
        with self.assertRaises(DataSource.DoesNotExist):
            cs.sources.get(url='http://example.com/foo/bar')

        # Cannot duplicate links
        with self.assertRaisesRegexp(IntegrityError, 'duplicate key'):
            DataSource.objects.create(content_object=cs, url=url,
                                      provider=provider)
