# -*- coding: utf-8 -*-
import urllib

from django.db import IntegrityError
from django.test import TestCase

from oracle.forms import DataProviderForm
from oracle.models import DataProvider, CardSet, DataSource


class DataProviderModelTest(TestCase):
    fixtures = ['data_provider', 'card_set']

    def setUp(self):
        self.data_provider = DataProvider.objects.all()[0]
        self.new_data = dict(name='new', title='New Gatherer',
                           home='http://example.com')

    def test_create(self):
        form = DataProviderForm(self.new_data)
        self.assertTrue(form.is_valid())
        form.save()

    def test_unique_name(self):
        self.new_data['name'] = self.data_provider.name
        form = DataProviderForm(self.new_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(len(form.errors['name']), 1)
        self.assertRegexpMatches(form.errors['name'][0], 'already exists')

    def test_unique_title(self):
        self.new_data['title'] = self.data_provider.title
        form = DataProviderForm(self.new_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(len(form.errors['title']), 1)
        self.assertRegexpMatches(form.errors['title'][0], 'already exists')

    def test_url_required(self):
        del self.new_data['home']
        form = DataProviderForm(self.new_data)
        self.assertFalse(form.is_valid())
        self.assertIn('home', form.errors)
        self.assertEqual(len(form.errors['home']), 1)
        self.assertRegexpMatches(form.errors['home'][0], 'field is required')

    def test_add_data_source(self):
        cs = CardSet.objects.all()[0]
        url = self.data_provider.absolute_url(urllib.quote_plus(cs.name))
        self.assertEqual(cs.sources.count(), 0)

        # Create data source generic relation
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
