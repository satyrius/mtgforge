from forge.tests.base import SerpTest
from oracle.models import CardFace


class SearchTest(SerpTest):
    def test_filter_white(self):
        '''We can filter by one color.

        Both monocolored and multicolored should be in SERP. If we are looking
        for `white` cards, for example, both `white` and `red-white` will be
        found but not `red`.
        '''
        c1 = self.face_recipe.make(mana_cost='w')
        self.release_recipe.make(card=c1.card)
        c2 = self.face_recipe.make(mana_cost='rw')
        self.release_recipe.make(card=c2.card)
        c3 = self.face_recipe.make(mana_cost='r')
        self.release_recipe.make(card=c3.card)

        data = self.search(color=['w'])
        self.assertEqual(data['meta']['total_count'], 2)
        self.assertEqual(set(self.get_cards(data, field='id')), {c1.id, c2.id})

    def test_plural(self):
        '''There is no difference between single and plural form of term word.

        So `creature` and `creatures` will be normalized and will be the same
        for search engine
        '''
        angel = self.face_recipe.make(
            type_line='Artifact Creature - Angel',
            rules='Flying'
        )
        self.release_recipe.make(card=angel.card)

        data = self.search(q='artifact flying creature')
        self.assertEqual(self.get_cards(data, field='id'), [angel.id])

        # Note plural form: creature[s]
        data = self.search(q='artifact flying creatures')
        self.assertEqual(self.get_cards(data, field='id'), [angel.id])

    def test_merge_multifaced(self):
        '''All faces of multipart card should be merged.

        If one of the werewolf double-faced cards will be found, only front
        face of this card should appear in SERP. But exact match with back
        face will return fliped card.
        '''
        back = self.face_recipe.make(
            name='Garruk, the Veil-Cursed',
            type_line='Planeswalker - Garruk',
            place=CardFace.BACK
        )
        front = self.face_recipe.make(
            card=back.card, colors=[],
            name='Garruk Relentless',
            type_line='Planeswalker - Garruk',
            place=CardFace.FRONT
        )
        self.release_recipe.make(card=back.card)

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
        gideon = self.face_recipe.make(
            name='Gideon Jura',
            type_line='Planeswalker - Gideon'
        )
        self.release_recipe.make(card=gideon.card, _quantity=2)

        data = self.search(types='planeswalker')
        self.assertEqual(self.get_cards(data), [gideon.name])

    def test_no_comments(self):
        '''Do not add abilities comments to FTS index.

        For example, cut `intimmidate` comment, otherwise we get these
        creatures when we search for `artifact`, because rules contains
        "can't be blocked except by artifact creatures..." comment.
        '''
        angel = self.face_recipe.make(
            name='Platinum Angel',
            type_line='Artifact Creature - Angel',
        )
        self.release_recipe.make(card=angel.card)

        hunder = self.face_recipe.make(
            name='Halo Hunter',
            rules='Intimidate (This creature can\'t be blocked except by '
                  'artifact creatures and/or creatures that share a color '
                  'with it.)\n'
                  'When Halo Hunter enters the battlefield, destroy target '
                  'Angel.'
        )
        self.release_recipe.make(card=hunder.card)

        data = self.search(q='artifact')
        self.assertEqual(self.get_cards(data), [angel.name])

    def test_filter_by_type(self):
        decay = self.face_recipe.make(
            name='Abrupt Decay',
            type_line='Instant',
        )
        self.release_recipe.make(card=decay.card)

        dreaadbore = self.face_recipe.make(
            name='Dreadbore',
            type_line='Sorcery',
        )
        self.release_recipe.make(card=dreaadbore.card)

        data = self.search(type='instant')
        self.assertEqual(self.get_cards(data), [decay.name])

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

    def test_search_by_set_name(self):
        set1, set2 = self.cs_recipe.make(_quantity=2)
        face1 = self.face_recipe.make()
        self.release_recipe.make(card_set=set1, card=face1.card)
        face2 = self.face_recipe.make()
        self.release_recipe.make(card_set=set2, card=face2.card)

        data = self.search(q=set1.name)
        self.assertEqual(self.get_cards(data), [face1.name])
