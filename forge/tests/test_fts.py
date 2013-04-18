from django_any import any_model

from forge.tests.base import SerpTest
from oracle.models import CardFace, CardSet, CardImage, CardRelease


class SearchTest(SerpTest):
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

    def test_merge_releases(self):
        '''Only one card release should be shown.

        If a card was released several times, we still should show only one
        it's release.
        '''
        expected = []
        gideon = self.create_card(
            name='Gideon Jura',
            type_line='Planeswalker - Gideon'
        )
        expected.append(gideon.name)
        any_model(CardRelease, card=gideon.card,
                  card_set=any_model(CardSet, name='Zendikar'),
                  art=any_model(CardImage))
        data = self.search(types='planeswalker')
        self.assertEqual(self.get_cards(data), expected)