import urllib
import urls  # to be able to reverse resource url
from django_any import any_model
from model_mommy.recipe import Recipe, seq, foreign_key
from tastypie.test import ResourceTestCase

from forge.management.commands.build_fts_index import Command as BuildIndex
from forge.resources.card import CardResource
from oracle.models import Card, CardFace, CardSet, CardRelease, CardImage


def get_uri(resource, **kwargs):
    uri = resource.get_resource_uri()
    if kwargs:
        uri += '?' + urllib.urlencode(kwargs)
    return uri


class SerpTest(ResourceTestCase):
    def setUp(self):
        super(SerpTest, self).setUp()
        self.uri = CardResource('v1').get_resource_search_uri()
        self.cs_recipe = Recipe(
            CardSet, name=seq('Magic Set '), acronym=seq('set'),
            is_published=True)
        self.release_recipe = Recipe(
            CardRelease, card_number=seq(0),
            card_set=foreign_key(self.cs_recipe),
            art=foreign_key(Recipe(CardImage)))
        self.face_recipe = Recipe(
            CardFace, name=seq('Card '), card=foreign_key(Recipe(Card)))

    def build_fts(self):
        BuildIndex().handle(verbosity=0)

    def search(self, build_fts=True, **kwargs):
        if build_fts:
            self.build_fts()
        return self.deserialize(self.api_client.get(self.uri, data=kwargs))

    def create_card(self, card_set=None, card_number=None, **kwargs):
        # TODO replace `any_model` with `model_mommy` recipes
        card = any_model(Card)
        face = any_model(CardFace, card=card, colors=[], **kwargs)
        self.create_card_release(card, card_set, card_number)
        return face

    def create_card_release(self, card, card_set=None, card_number=None):
        extra = {}
        extra['card_set'] = self.cs_recipe.make() if not card_set else card_set
        if card_number:
            extra['card_number'] = card_number
        return self.release_recipe.make(card=card, **extra)

    def get_cards(self, serp, field='name'):
        return [cf[field] for cf in serp['objects']]

    def dump_rank(self, data):
        if isinstance(data, dict):
            data = data['objects']
        for d in data:
            print d['name'], d['ranks']
