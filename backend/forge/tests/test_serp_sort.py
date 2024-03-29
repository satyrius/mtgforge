from forge.tests.base import SerpTest


class SerpSortTest(SerpTest):
    def test_angel(self):
        '''Matching creature type is much important than with name or text.

        For example, if we are looking for `angel`, we expect than creatures
        with subtype `Angel` will be at the top of SERP. Then cards with
        `Angel` in their names, and in the rules text at last.
        '''
        expected = []

        angel1 = self.face_recipe.make(
            name='Baneslayer Angel',
            type_line='Creature - Angel'
        )
        self.release_recipe.make(card=angel1.card)
        expected.append(angel1.name)

        angel2 = self.face_recipe.make(
            name='Guardian Seraph',
            type_line='Creature - Angel'
        )
        self.release_recipe.make(card=angel2.card)
        expected.append(angel2.name)

        angel3 = self.face_recipe.make(
            name='Angel\' Mercy',
            type_line='Instant'
        )
        self.release_recipe.make(card=angel3.card)
        expected.append(angel3.name)

        data = self.search(q='angel')
        self.assertEqual(self.get_cards(data), expected)

    def test_card_type_ranking(self):
        '''The more terms are matched with type line, the better result is.

        If we are looking for `artifact angel`, first results should countain
        both types, next with one matching, and the rest at the end of SERP.
        '''
        expected = []

        card1 = self.face_recipe.make(
            name='Filigree Angel',
            type_line='Artifact Creature - Angel'
        )
        self.release_recipe.make(card=card1.card)
        expected.append(card1.name)

        card2 = self.face_recipe.make(
            name='Angel\'s Tomb',
            type_line='Artifact',
            rules='Whenever a creature enters the battlefield under your '
                  'control, you may have Angel\'s Tomb become a 3/3 white '
                  'Angel artifact creature with flying until end of turn.'
        )
        self.release_recipe.make(card=card2.card)
        expected.append(card2.name)

        card3 = self.face_recipe.make(
            name='Indomitable Archangel',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'Metalcraft - Artifacts you control have shroud as long as '
                  'you control three or more artifacts.'
        )
        self.release_recipe.make(card=card3.card)
        expected.append(card3.name)

        data = self.search(q='artifact angel')
        self.assertEqual(self.get_cards(data), expected)

    def test_color_ranking(self):
        '''Filtering by color should rank monocolored spells higher

        If we filter by `w` we will get monocolored white spells and
        multicolored spells with white color. The less different colors are in
        card's color identity the higher rank it should gain.
        '''
        expected = []

        card1 = self.face_recipe.make(
            mana_cost='wubrg',
            name='Scion of the Ur-Dragon'
        )
        self.release_recipe.make(card=card1.card)
        expected.append(card1.name)

        card2 = self.face_recipe.make(
            mana_cost='2wb',
            name='Alms Beast'
        )
        self.release_recipe.make(card=card2.card)
        expected.append(card2.name)

        card3 = self.face_recipe.make(
            mana_cost='1w',
            name='Stoneforge Mystic'
        )
        self.release_recipe.make(card=card3.card)
        expected.append(card3.name)

        # Models was created in reversed order because postgresql default
        # sorting is usually by id. So we need bad default sorting to
        # ensure that card search resource will sort them in a right way.
        expected.reverse()

        data = self.search(color=['w'])
        self.assertEqual(self.get_cards(data), expected)

    def test_color_with_different_card_types(self):
        '''Matching type is stronger that matching exact color.

        If we are looking for a `creature` and filtering by `white` color, we
        should get white creatures first, then other white spells with
        a `creature` term somewhere in their rules.
        '''
        expected = []

        card1 = self.face_recipe.make(
            mana_cost='w',
            name='Smite',
            type_line='Instant',
            rules='Destroy target blocked creature.',
        )
        self.release_recipe.make(card=card1.card)
        expected.append(card1.name)

        card2 = self.face_recipe.make(
            mana_cost='wb',
            name='Alms Beast',
            type_line='Creature - Beast'
        )
        self.release_recipe.make(card=card2.card)
        expected.append(card2.name)

        # Models was created in reversed order because postgresql default
        # sorting is usually by id. So we need bad default sorting to
        # ensure that card search resource will sort them in a right way.
        expected.reverse()

        data = self.search(q='creature', color=['w'])
        self.assertEqual(self.get_cards(data), expected)
        data = self.search(q='white creature')
        self.assertEqual(self.get_cards(data), expected)

    def test_monocolored_is_better_if_types_equal(self):
        '''Monocolored cards are better if card types are the same.

        If we are looking for `angel` and then filter by `white` color, the
        white angel will be higer ranked than white-black angel.
        '''
        expected = []

        card1 = self.face_recipe.make(
            mana_cost='3wbb',
            name='Deathpact Angel',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'When Deathpact Angel dies, put a 1/1 white and black '
                  'Cleric creature token onto the battlefield. It has '
                  '"{3}{W}{B}{B}, {T}, Sacrifice this creature: Return a card '
                  'named Deathpact Angel from your graveyard to the '
                  'battlefield."'
        )
        self.release_recipe.make(card=card1.card)
        expected.append(card1.name)

        card2 = self.face_recipe.make(
            mana_cost='3wwbb',
            name='Angel of Despair',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'When Angel of Despair enters the battlefield, destroy '
                  'target permanent.'
        )
        self.release_recipe.make(card=card2.card)
        expected.append(card2.name)

        card3 = self.face_recipe.make(
            mana_cost='ww',
            name='Serra Avenger',
            type_line='Creature - Angel',
            rules='You can\'t cast Serra Avenger during your first, second, '
                  'or third turns of the game.\n'
                  'Flying\n'
                  'Vigilance (Attacking doesn\'t cause this creature to tap.)'
        )
        self.release_recipe.make(card=card3.card)
        expected.append(card3.name)

        card4 = self.face_recipe.make(
            mana_cost='3w',
            name='Restoration Angel',
            type_line='Creature - Angel',
            rules='Flash\n'
                  'Flying\n'
                  'When Restoration Angel enters the battlefield, you may '
                  'exile target non-Angel creature you control, then return '
                  'that card to the battlefield under your control.'
        )
        self.release_recipe.make(card=card4.card)
        expected.append(card4.name)

        card5 = self.face_recipe.make(
            mana_cost='3www',
            name='Admonition Angel',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'Landfall - Whenever a land enters the battlefield under '
                  'your control, you may exile target nonland permanent other '
                  'than Admonition Angel.\n'
                  'When Admonition Angel leaves the battlefield, return all '
                  'cards exiled with it to the battlefield under their '
                  'owners\' control.'
        )
        self.release_recipe.make(card=card5.card)
        expected.append(card5.name)

        # Models was created in reversed order because postgresql default
        # sorting is usually by id. So we need bad default sorting to
        # ensure that card search resource will sort them in a right way.
        expected.reverse()

        data = self.search(q='angel', color=['w'])
        self.assertEqual(self.get_cards(data), expected)

    def test_color_and_type_averywhere(self):
        '''Monocolored should be first even if more matches in rules.

        If we are looking for a `black angel` we expect black angel creatures
        first, then multicolored angels.
        '''
        expected = []

        card1 = self.face_recipe.make(
            mana_cost='3wbb',
            name='Deathpact Angel',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'When Deathpact Angel dies, put a 1/1 white and black '
                  'Cleric creature token onto the battlefield. It has '
                  '"{3}{W}{B}{B}, {T}, Sacrifice this creature: Return a card '
                  'named Deathpact Angel from your graveyard to the '
                  'battlefield."'
        )
        self.release_recipe.make(card=card1.card)
        expected.append(card1.name)

        card2 = self.face_recipe.make(
            mana_cost='4b',
            name='Crypt Angel',
            type_line='Creature - Angel',
            rules='Flying, protection from white\n'
                  'When Crypt Angel enters the battlefield, return target '
                  'blue or red creature card from your graveyard to your hand.'
        )
        self.release_recipe.make(card=card2.card)
        expected.append(card2.name)

        # Models was created in reversed order because postgresql default
        # sorting is usually by id. So we need bad default sorting to
        # ensure that card search resource will sort them in a right way.
        expected.reverse()

        data = self.search(q='black angel')
        self.assertEqual(self.get_cards(data), expected)

    def test_order_by_card_number(self):
        '''Order by collector's number if rank is equal.

        For example, we look at the card set spoiler (cards filtered by card
        set acronym), all cards will have the same rank and should be sorted
        by collector's number. And it does not matter thar it had released in
        a few sets with different collector's number.
        '''
        m14 = self.cs_recipe.make(name='Magic 2014', acronym='m14')
        reissue = self.cs_recipe.make(acronym='rei')

        act_of_treason = self.face_recipe.make(name='Act of Treason')
        self.release_recipe.make(
            card=act_of_treason.card, card_set=m14, card_number=125)
        self.release_recipe.make(
            card=act_of_treason.card, card_set=reissue, card_number=1)

        cancel = self.face_recipe.make(name='Cancel')
        self.release_recipe.make(
            card=cancel.card, card_set=m14, card_number=45)

        data = self.search(set='m14')
        self.assertEqual(self.get_cards(data),
                         [cancel.name, act_of_treason.name])
