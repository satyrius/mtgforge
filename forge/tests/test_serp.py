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

    def get_cards(self, serp, field='name'):
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
        self.assertEqual(set(self.get_cards(data, field='id')), set(expected))

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
        self.assertEqual(self.get_cards(data, field='id'), expected)

        data = self.search(q='artifact flying creatures')
        self.assertEqual(self.get_cards(data, field='id'), expected)

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
        self.assertEqual(self.get_cards(data), expected)

    def test_card_type_ranking(self):
        '''The more terms are matched with type line, the better result is.

        If we are looking for `artifact angel`, first results should countain
        both types, next with one matching, and the rest at the end of SERP.
        '''
        expected = []
        expected.append(self.create_card(
            name='Filigree Angel',
            type_line='Artifact Creature - Angel'
        ).name)
        expected.append(self.create_card(
            name='Angel\'s Tomb',
            type_line='Artifact',
            rules='Whenever a creature enters the battlefield under your '
                  'control, you may have Angel\'s Tomb become a 3/3 white '
                  'Angel artifact creature with flying until end of turn.'
        ).name)
        expected.append(self.create_card(
            name='Indomitable Archangel',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'Metalcraft - Artifacts you control have shroud as long as '
                  'you control three or more artifacts.'
        ).name)
        data = self.search(q='artifact angel')
        self.assertEqual(self.get_cards(data), expected)

    def test_merge_multifaced(self):
        '''All faces of multipart card should be merged.

        If one of the werewolf double-faced cards will be found, only front
        face of this card should appear in SERP.
        '''
        front_face = self.create_card(
            name='Garruk, the Veil-Cursed',
            type_line='Planeswalker - Garruk'
        )
        back_face = any_model(
            CardFace, card=front_face.card, colors=[],
            name='Garruk Relentless',
            type_line='Planeswalker - Garruk',
            place=CardFace.FRONT
        )
        # Assert order of just created card faces. We need it to ensure that
        # default order is not what we want when merge faces for SERP.
        self.assertEqual(
            list(CardFace.objects.values_list('id', flat=True)),
            [front_face.id, back_face.id])

        # Let's go test search
        expected = [front_face.name]
        # If both faces matched, only front face shold be shown
        data = self.search(q='garruk')
        self.assertEqual(self.get_cards(data), expected)
        # The same for back face match
        data = self.search(q='veil cursed')
        self.assertEqual(self.get_cards(data), expected)
