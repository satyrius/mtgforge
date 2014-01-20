import unittest
import uuid
from django.test import TestCase
from mock import patch, Mock
from model_mommy import mommy
from model_mommy.recipe import Recipe, seq

from crawler.items import CardSetItem, CardItem
from crawler.models import CardSetAlias
from crawler.pipelines import sets
from oracle.models import CardSet


class BaseCardSetPipelineTest(unittest.TestCase):
    def setUp(self):
        self.spider = Mock()
        self.pipeline = sets.BaseCardSetItemPipeline()

    def test_process_item_not_implemented(self):
        item = CardSetItem()
        with self.assertRaises(NotImplementedError):
            self.pipeline.process_item(item, self.spider)

    @patch.object(sets.BaseCardSetItemPipeline, '_process_item')
    def test_item_instance(self, _process_item):
        # Process card set items
        item = CardSetItem()
        self.assertEqual(self.pipeline.process_item(item, self.spider), item)
        _process_item.assert_called_once_with(item, self.spider)

        # And skip all other items
        item = CardItem()
        _process_item.reset_mock()
        self.assertEqual(self.pipeline.process_item(item, self.spider), item)
        self.assertFalse(_process_item.called)


class CardSetPipelineTest(TestCase):
    def setUp(self):
        self.spider = Mock()
        self.pipeline = sets.CardSetsPipeline()
        self.cs_recipe = Recipe(CardSet, name=seq('Magic Set '))

    def test_inheritance(self):
        self.assertTrue(issubclass(
            sets.CardSetsPipeline,
            sets.BaseCardSetItemPipeline))

    def _fetch_item(self):
        # Use model_mommy to generate new card set name (DO NOT SAVE)
        name = self.cs_recipe.prepare().name
        return CardSetItem(name=name)

    @patch.object(sets, 'generate_slug')
    def test_save_card_set(self, slug):
        item = self._fetch_item()
        name = item['name']
        slug.return_value = uuid.uuid4().get_hex()[:10]
        # Assert it is a new item
        count = lambda m: m.objects.filter(name=name).count()
        self.assertEqual(count(CardSet), 0)
        self.assertEqual(count(CardSetAlias), 0)

        # Process item and assert that all saved
        self.pipeline.process_item(item, self.spider)
        alias = CardSetAlias.objects.get(name=name)
        cs = CardSet.objects.get(name=name)
        self.assertEqual(alias.card_set, cs)

        # Ensure the default card set acronym was specified
        slug.assert_called_once_with(name)
        self.assertEqual(cs.acronym, slug())

    def test_existing_alias(self):
        # Create card set and alias with the different names
        cs = self.cs_recipe.make(acronym=seq('set'))
        name_seq = self.cs_recipe.attr_mapping['name']
        alias = mommy.make(CardSetAlias, card_set=cs,
                           name=name_seq.gen(CardSet))
        self.assertNotEqual(cs.name, alias.name)

        # Emulate the case when card set with existing alias name was crawled
        count = lambda m: m.objects.filter().count()
        cs_count = count(CardSet)
        alias_count = count(CardSetAlias)
        self.pipeline.process_item(CardSetItem(name=alias.name), self.spider)
        self.assertEqual(count(CardSet), cs_count)
        self.assertEqual(count(CardSetAlias), alias_count)

    def test_existing_set(self):
        cs = self.cs_recipe.make(acronym=seq('set'))
        mommy.make(CardSetAlias, card_set=cs, name=cs.name)

        # Fetch the same card set again
        count = lambda m: m.objects.filter().count()
        cs_count = count(CardSet)
        alias_count = count(CardSetAlias)
        self.pipeline.process_item(CardSetItem(name=cs.name), self.spider)
        self.assertEqual(count(CardSet), cs_count)
        self.assertEqual(count(CardSetAlias), alias_count)
