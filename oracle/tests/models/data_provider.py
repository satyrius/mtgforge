# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase
from oracle.models import DataProvider


class DataProviderModelTest(TestCase):
    def setUp(self):
        self.name = 'wizards'
        self.title = 'Wizzards ot the Coast'

    def test_create(self):
        DataProvider.objects.create(name=self.name, title=self.title)

    def test_unique_name(self):
        DataProvider.objects.create(name=self.name, title=self.title)
        with self.assertRaises(IntegrityError):
            new_title = 'new' + self.title
            DataProvider.objects.create(name=self.name, title=new_title)

    def test_unique_title(self):
        DataProvider.objects.create(name=self.name, title=self.title)
        with self.assertRaises(IntegrityError):
            new_name = 'new' + self.name
            DataProvider.objects.create(name=new_name, title=self.title)
