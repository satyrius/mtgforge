from tastypie.test import ResourceTestCase
from forge.resources.card import CardResource
from django_any import any_model
from oracle.models import Card, CardFace, CardSet, CardImage, CardRelease
from forge.management.commands.build_fts_index import Command as BuildIndex


class SerpTest(ResourceTestCase):
    def setUp(self):
        super(SerpTest, self).setUp()
        self.uri = CardResource('v1').get_resource_search_uri()

    def build_fts(self):
        BuildIndex().handle(verbosity=0)

    def search(self, colors=None):
        self.build_fts()
        data = {}
        if colors:
            data['color'] = colors
        return self.deserialize(self.api_client.get(self.uri, data=data))

    def create_card(self, mana_cost=None):
        card = any_model(Card)
        face = any_model(CardFace, card=card, mana_cost=mana_cost, colors=[])
        any_model(CardRelease, card=card, card_set=any_model(CardSet),
                  art=any_model(CardImage))
        return face

    def get_card_ids(self, serp):
        return [cf['id'] for cf in serp['objects']]

    def test_filter_white(self):
        expected = []
        expected.append(self.create_card(mana_cost='w').id)
        expected.append(self.create_card(mana_cost='rw').id)
        self.create_card(mana_cost='r')

        data = self.search(colors=['w'])
        self.assertEqual(data['meta']['total_count'], 2)
        self.assertEqual(set(self.get_card_ids(data)), set(expected))
