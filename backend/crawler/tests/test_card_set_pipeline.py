import unittest
import uuid
from django.test import TestCase
from mock import patch, Mock
from model_mommy import mommy
from model_mommy.recipe import Recipe, seq, foreign_key

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

    def _fetch_item(self, is_gatherer=False):
        # Use model_mommy to generate new card set name (DO NOT SAVE)
        name = self.cs_recipe.prepare().name
        return CardSetItem(name=name, is_gatherer=is_gatherer)

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


class GathererPipelineTest(TestCase):
    def setUp(self):
        self.spider = Mock()
        self.pipeline = sets.GathererPipeline()
        card_set = Recipe(CardSet, name=seq('Magic Set '), acronym=seq('set'))
        self.recipe = Recipe(CardSetAlias, name=seq('Magic Set Alias '),
                             card_set=foreign_key(card_set))

    def test_inheritance(self):
        self.assertTrue(issubclass(
            sets.GathererPipeline,
            sets.BaseCardSetItemPipeline))

    def test_flag_gatherer_alias(self):
        # Create new alias with alias flagged as `is_gatherer`
        alias = self.recipe.make()
        self.assertFalse(alias.is_gatherer)
        self.pipeline.process_item(
            CardSetItem(name=alias.name, is_gatherer=True),
            self.spider)
        alias = CardSetAlias.objects.get(name=alias.name)
        self.assertTrue(alias.is_gatherer)
        cs = alias.card_set
        aliases = cs.cardsetalias_set.all()
        self.assertEqual(aliases.count(), 1)

        # Add another alias
        alias2 = self.recipe.make(card_set=alias.card_set)
        self.assertFalse(alias2.is_gatherer)
        # And move `is_gatherer` flag to it
        self.pipeline.process_item(
            CardSetItem(name=alias2.name, is_gatherer=True),
            self.spider)
        alias2 = CardSetAlias.objects.get(name=alias2.name)
        self.assertTrue(alias2.is_gatherer)

        # Ensure that only one alias is flaged as `is_gatherer`
        self.assertEqual(aliases.count(), 2)
        self.assertEqual(aliases.filter(is_gatherer=True).count(), 1)
