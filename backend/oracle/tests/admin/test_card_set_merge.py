# -*- coding: utf-8 -*-
import datetime as dt

from django.db import models
from django.test import TestCase
from mock import patch, Mock
from model_mommy import mommy
from model_mommy.recipe import Recipe, seq

from crawler.models import CardSetAlias
from crawler.spiders.products import ProductsInfoSpider, ProductsSpider
from oracle.admin import card_set as admin
from oracle.models import CardSet, CardRelease


class CardSetMergeActionTest(TestCase):
    def setUp(self):
        self.cs_recipe = Recipe(CardSet, name=seq('Card Set '),
                                acronym=seq('set'))
        self.alias_recipe = Recipe(CardSetAlias, name=seq('Alias '))

    def test_merge(self):
        cs1 = self.cs_recipe.make()
        alias1 = self.alias_recipe.make(card_set=cs1)
        cs2 = self.cs_recipe.make()
        alias2 = self.alias_recipe.make(card_set=cs2)

        admin._merge(CardSet.objects.filter(pk__in=(cs1.pk, cs2.pk)), cs1)

        # All aliases should be moved to master card set
        self.assertEqual(CardSetAlias.objects.get(pk=alias2.pk).card_set, cs1)
        self.assertEqual(
            set(cs1.cardsetalias_set.all().values_list('pk', flat=True)),
            {alias1.pk, alias2.pk})
        # And all non-master card sets will be droped
        with self.assertRaises(CardSet.DoesNotExist):
            CardSet.objects.get(pk=cs2.pk)

    def test_cannot_merge_if_has_related_objects(self):
        cs1 = self.cs_recipe.make()
        cs2 = self.cs_recipe.make()
        mommy.make(CardRelease, card_set=cs2)
        with self.assertRaises(models.ProtectedError):
            admin._merge(CardSet.objects.filter(pk__in=(cs1.pk, cs2.pk)), cs1)

    @patch.object(admin, '_merge')
    def test_choose_master_record_by_related_objects(self, merge):
        cs1 = self.cs_recipe.make()
        self.alias_recipe.make(card_set=cs1, domain=ProductsInfoSpider.domain)
        cs2 = self.cs_recipe.make()
        mommy.make(CardRelease, card_set=cs2)
        queryset = CardSet.objects.filter(pk__in=(cs1.pk, cs2.pk))
        admin.merge_card_sets(Mock(), Mock(), queryset)
        # Master record is a record that has related objects (except aliases)
        merge.assert_called_once_with(queryset, cs2)

    @patch.object(admin, '_merge')
    def test_choose_master_record_by_alias(self, merge):
        cs1 = self.cs_recipe.make()
        self.alias_recipe.make(card_set=cs1, domain=ProductsSpider.domain)
        cs2 = self.cs_recipe.make()
        self.alias_recipe.make(card_set=cs2, domain=ProductsInfoSpider.domain)
        queryset = CardSet.objects.filter(pk__in=(cs1.pk, cs2.pk))
        admin.merge_card_sets(Mock(), Mock(), queryset)
        # Master record is a record that has alias from wizards.com
        merge.assert_called_once_with(queryset, cs2)

    @patch.object(admin, '_merge')
    def test_choose_master_record_by_default(self, merge):
        cs1 = self.cs_recipe.make()
        cs2 = self.cs_recipe.make()
        queryset = CardSet.objects.filter(pk__in=(cs1.pk, cs2.pk))
        admin.merge_card_sets(Mock(), Mock(), queryset)
        # Choose any record if there is no related objects
        merge.assert_called_once_with(queryset, cs1)

    def test_mege_fields(self):
        cs1 = self.cs_recipe.make(
            cards=123, released_at=None, name_ru='')
        cs2 = self.cs_recipe.make(
            cards=None, released_at=dt.date(2013, 1, 1), name_ru=u'Картон')

        # Merge and refresh card set
        admin._merge(CardSet.objects.filter(pk__in=(cs1.pk, cs2.pk)), cs1)
        cs1 = CardSet.objects.get(pk=cs1.pk)

        self.assertEqual(cs1.cards, 123)
        self.assertEqual(cs1.released_at, cs2.released_at)
        self.assertEqual(cs1.name_ru, cs2.name_ru)
