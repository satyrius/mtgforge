# -*- coding: utf-8 -*-
import urllib

from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.test import TestCase

from oracle.models import DataProvider, CardSet, DataSource


class DataProviderModelTest(TestCase):
    fixtures = ['data_provider', 'card_set']

    def setUp(self):
        self.data_provider = DataProvider.objects.all()[0]
        self.kwargs = model_to_dict(self.data_provider)
        del self.kwargs['id']

    def test_create(self):
        DataProvider.objects.create(name='new', title='New Gatherer',
                                    home='http:/example.com')

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            self.kwargs['title'] = 'new' + self.kwargs['title']
            DataProvider.objects.create(**self.kwargs)

    def test_unique_title(self):
        with self.assertRaises(IntegrityError):
            self.kwargs['name'] = 'new' + self.kwargs['name']
            DataProvider.objects.create(**self.kwargs)

    def test_url_required(self):
        with self.assertRaises(IntegrityError):
            DataProvider.objects.create(name=self.kwargs['name'],
                                        title=self.kwargs['title'])

    def test_add_data_source(self):
        cs = CardSet.objects.all()[0]
        url = self.data_provider.absolute_url(urllib.quote_plus(cs.name))
        ds = DataSource.objects.create(content_object=cs, url=url,
                                  data_provider=self.data_provider)

        # Check reverse relation
        self.assertEqual(cs.sources.count(), 1)
        self.assertEqual(cs.sources.all()[0].id, ds.id)
        self.assertEqual(
            cs.sources.get(data_provider=self.data_provider).id, ds.id)
        with self.assertRaises(DataSource.DoesNotExist):
            cs.sources.get(url='http://example.com/foo/bar')

        # Cannot duplicate links
        with self.assertRaisesRegexp(IntegrityError, 'duplicate key'):
            DataSource.objects.create(content_object=cs, url=url,
                                    data_provider=self.data_provider)
