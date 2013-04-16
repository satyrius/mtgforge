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

    def search(self, build_fts=True, **kwargs):
        if build_fts:
            self.build_fts()
        return self.deserialize(self.api_client.get(self.uri, data=kwargs))

    def create_card(self, **kwargs):
        card = any_model(Card)
        face = any_model(CardFace, card=card, colors=[], **kwargs)
        any_model(CardRelease, card=card, card_set=any_model(CardSet),
                  art=any_model(CardImage))
        return face

    def get_cards(self, serp, field='id'):
        return [cf[field] for cf in serp['objects']]

    def test_filter_white(self):
        '''We can filter by one color.

        Both monocolored and multicolored should be in SERP. If we are looking
        for `white` cards, for example, both `white` and `red-white` will be
        found but not `red`.
        '''
        expected = []
        expected.append(self.create_card(mana_cost='w').id)
        expected.append(self.create_card(mana_cost='rw').id)
        self.create_card(mana_cost='r')

        data = self.search(color=['w'])
        self.assertEqual(data['meta']['total_count'], 2)
        self.assertEqual(set(self.get_cards(data)), set(expected))

    def test_plural(self):
        '''There is no difference between single and plural form of term word.

        So `creature` and `creatures` will be normalized and will be the same
        for search engine
        '''
        expected = []
        expected.append(self.create_card(
            type_line='Artifact Creature - Angel',
            rules='Flying'
        ).id)

        data = self.search(q='artifact flying creature')
        self.assertEqual(self.get_cards(data), expected)

        data = self.search(q='artifact flying creatures')
        self.assertEqual(self.get_cards(data), expected)

    def test_angel(self):
        '''Matching creature type is much important than with name or text.

        For example, if we are looking for `angel`, we expect than creatures
        with subtype `Angel` will be at the top of SERP. Then cards with
        `Angel` in their names, and in the rules text at last.
        '''
        expected = []
        expected.append(self.create_card(
            name='Baneslayer Angel',
            type_line='Creature - Angel'
        ).name)
        expected.append(self.create_card(
            name='Guardian Seraph',
            type_line='Creature - Angel'
        ).name)
        expected.append(self.create_card(
            name='Angel\' Mercy',
            type_line='Instant'
        ).name)
        data = self.search(q='angel')
        self.assertEqual(self.get_cards(data, field='name'), expected)
