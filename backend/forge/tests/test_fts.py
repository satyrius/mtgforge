from django_any import any_model

from forge.tests.base import SerpTest
from oracle.models import CardFace


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
        face of this card should appear in SERP. But exact match with back
        face will return fliped card.
        '''
        back = self.create_card(
            name='Garruk, the Veil-Cursed',
            type_line='Planeswalker - Garruk',
            place=CardFace.BACK
        )
        front = any_model(
            CardFace, card=back.card, colors=[],
            name='Garruk Relentless',
            type_line='Planeswalker - Garruk',
            place=CardFace.FRONT
        )
        self.assertEqual(front.card_id, back.card_id)
        # Assert order of just created card faces. We need it to ensure that
        # default order is not what we want when merge faces for SERP.
        self.assertEqual(
            list(CardFace.objects.values_list('id', flat=True)),
            [back.id, front.id])

        # Let's go test search
        # If both faces matched, only front face should be shown
        data = self.search(q='garruk')
        self.assertEqual(self.get_cards(data), [front.name])
        # If exact face is matched it will be shown
        data = self.search(q='veil cursed')
        self.assertEqual(self.get_cards(data), [back.name])

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
        self.release_recipe.make(card=gideon.card)
        data = self.search(types='planeswalker')
        self.assertEqual(self.get_cards(data), expected)

    def test_no_comments(self):
        '''Do not add abilities comments to FTS index.

        For example, cut `intimmidate` comment, otherwise we get these
        creatures when we search for `artifact`, because rules contains
        "can't be blocked except by artifact creatures..." comment.
        '''
        expected = []
        expected.append(self.create_card(
            name='Platinum Angel',
            type_line='Artifact Creature - Angel',
        ).name)
        self.create_card(
            name='Halo Hunter',
            rules='Intimidate (This creature can\'t be blocked except by '
                  'artifact creatures and/or creatures that share a color '
                  'with it.)\n'
                  'When Halo Hunter enters the battlefield, destroy target '
                  'Angel.'
        )
        data = self.search(q='artifact')
        self.assertEqual(self.get_cards(data), expected)

    def test_filter_by_type(self):
        expected = []
        expected.append(self.create_card(
            name='Abrupt Decay',
            type_line='Instant',
        ).name)
        self.create_card(
            name='Dreadbore',
            type_line='Sorcery',
        )
        data = self.search(type='instant')
        self.assertEqual(self.get_cards(data), expected)

    def test_not_published_sets(self):
        set1 = self.cs_recipe.make(is_published=True)
        set2 = self.cs_recipe.make(is_published=False)

        face1 = self.face_recipe.make()
        self.release_recipe.make(card_set=set1, card=face1.card)
        face2 = self.face_recipe.make()
        self.release_recipe.make(card_set=set1, card=face2.card)
        self.release_recipe.make(card_set=set2, card=face2.card)
        # This card should not appears on the serp, because it was released for
        # unpublished card set only
        face3 = self.face_recipe.make()
        self.release_recipe.make(card_set=set2, card=face3.card)

        expected = {face1.name, face2.name}
        data = self.search()
        self.assertEqual(set(self.get_cards(data)), expected)
