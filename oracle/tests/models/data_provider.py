# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase
from oracle.models import DataProvider


class DataProviderModelTest(TestCase):
    def setUp(self):
        self.name = 'wizards'
        self.title = 'Wizzards ot the Coast'
        self.url = 'http://wizards.com/magic/tcg/Article.aspx?x=mtg/tcg/products/allproducts'
        self.kwargs = dict(name=self.name, title=self.title, home=self.url)

    def test_create(self):
        DataProvider.objects.create(**self.kwargs)

    def test_unique_name(self):
        DataProvider.objects.create(**self.kwargs)
        with self.assertRaises(IntegrityError):
            self.kwargs['title'] = 'new' + self.title
            DataProvider.objects.create(**self.kwargs)

    def test_unique_title(self):
        DataProvider.objects.create(**self.kwargs)
        with self.assertRaises(IntegrityError):
            self.kwargs['name'] = 'new' + self.name
            DataProvider.objects.create(**self.kwargs)

    def test_url_required(self):
        with self.assertRaises(IntegrityError):
            DataProvider.objects.create(name=self.name, title=self.title)
