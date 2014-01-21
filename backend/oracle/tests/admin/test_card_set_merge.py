from django.db import models
from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe, seq
from oracle.models import CardSet, CardRelease
from crawler.models import CardSetAlias
from oracle.admin import card_set as admin


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
