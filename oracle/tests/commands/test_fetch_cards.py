# -*- coding: utf-8 -*-
from mock import patch

from oracle.management.commands import save_card_face
from oracle.models import CardFace, CardRelease, CardSet
from oracle.providers.gatherer import GathererCard
from oracle.tests.helpers import get_html_fixture
from oracle.tests.providers.base import ProviderTest


class FetchCardsCommandTest(ProviderTest):
    def setUp(self):
        pass

    @patch.object(GathererCard, 'get_content')
    def test_save_card_oracle_details(self, get_content):
        cs = CardSet.objects.create(name='Avacyn Restored')
        get_content.return_value = get_html_fixture('gatherer_angel_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961'
        page = GathererCard(url)

        card_face = save_card_face(page.details(), cs)
        self.assertIsInstance(card_face, CardFace)
        self.assertEqual(card_face.name, u'Avacyn, Angel of Hope')
        card = card_face.card
        self.assertEqual(card_face.name, card.name)

        release = card.cardrelease_set.get(card_set=cs)
        self.assertEqual(release.rarity, CardRelease.MYTHIC)
        self.assertEqual(release.card_number, '6')

    @patch.object(GathererCard, 'get_content')
    def test_save_card_with_no_text(self, get_content):
        cs = CardSet.objects.create(name='Return to Ravnica')
        get_content.return_value = get_html_fixture('gatherer_vanilla_creature')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=265383'
        page = GathererCard(url)

        card_face = save_card_face(page.details(), cs)
        self.assertEqual(card_face.name, u'Axebane Stag')
        self.assertIsNone(card_face.rules)

    @patch.object(GathererCard, 'get_content')
    def test_save_land_card(self, get_content):
        cs = CardSet.objects.create(name='Return to Ravnica')
        get_content.return_value = get_html_fixture('gatherer_forest')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326'
        page = GathererCard(url)

        card_face = save_card_face(page.details(), cs)
        self.assertEqual(card_face.name, u'Forest')
        self.assertIsNone(card_face.flavor)
        self.assertIsNone(card_face.power)
        self.assertIsNone(card_face.thoughtness)
        self.assertIsNone(card_face.fixed_power)
        self.assertIsNone(card_face.fixed_thoughtness)
        self.assertIsNone(card_face.loyality)

    @patch.object(GathererCard, 'get_content')
    def test_save_card_with_no_number(self, get_content):
        cs = CardSet.objects.create(name='Portal Second Age')
        get_content.return_value = get_html_fixture('gatherer_no_number')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=6567'
        page = GathererCard(url)

        card_face = save_card_face(page.details(), cs)
        self.assertEqual(card_face.name, u'Abyssal Nightstalker')
        release = card_face.card.cardrelease_set.get(card_set=cs)
        self.assertEqual(release.rarity, CardRelease.UNCOMMON)
        self.assertIsNone(release.card_number)

    @patch.object(GathererCard, 'get_content')
    def test_save_splited_card(self, get_content):
        cs = CardSet.objects.create(name='Apocalypse')
        get_content.return_value = get_html_fixture('gatherer_fire_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?part=Fire&multiverseid=27166'
        page = GathererCard(url)

        card_face = save_card_face(page.details(), cs)
        self.assertIsInstance(card_face, CardFace)
        self.assertEqual(card_face.name, u'Fire')
        card = card_face.card
        self.assertEqual(card.name, 'Fire // Ice')
