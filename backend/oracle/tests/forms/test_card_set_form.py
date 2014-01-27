from django.test import TestCase
from model_mommy.recipe import Recipe, seq

from crawler.pipelines.sets import generate_slug
from oracle.forms import CardSetForm
from oracle.models import CardSet


class CardSetFormTest(TestCase):
    def setUp(self):
        self.cs_recipe = Recipe(
            CardSet, name=seq('Magic Set '), acronym=seq('set'))
        self.cs_recipe.make(_quantity=3)

    def test_new_card_set(self):
        name = self.cs_recipe.prepare().name
        form = CardSetForm({
            'name': name,
            'acronym': generate_slug(name)
        }, instance=None)
        cs = form.save()
        self.assertEqual(cs.name, name)
        self.assertIsNotNone(cs.pk)
