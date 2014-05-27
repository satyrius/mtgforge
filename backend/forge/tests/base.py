import urllib
import urls  # to be able to reverse resource url
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
        self.resource = CardResource('v1')
        self.uri = self.resource.get_resource_search_uri()

        self.cs_recipe = Recipe(
            CardSet, name=seq('Magic Set '), acronym=seq('set'),
            is_published=True)

        self.img_recipe = Recipe(
            CardImage, mvid=seq(0),
            scan=seq('http://gatherer.wizards.com/image?multiverseid='))

        self.release_recipe = Recipe(
            CardRelease, card_number=seq(0),
            card_set=foreign_key(self.cs_recipe),
            art=foreign_key(self.img_recipe))

        self.face_recipe = Recipe(
            CardFace, name=seq('Card '), card=foreign_key(Recipe(Card)))

    def build_fts(self):
        BuildIndex().handle(verbosity=0)

    def search(self, build_fts=True, **kwargs):
        if build_fts:
            self.build_fts()
        return self.deserialize(self.api_client.get(self.uri, data=kwargs))

    def get_cards(self, serp, field='name'):
        return [cf[field] for cf in serp['objects']]

    def dump_rank(self, data):
        if isinstance(data, dict):
            data = data['objects']
        for d in data:
            print d['name'], d['ranks']
