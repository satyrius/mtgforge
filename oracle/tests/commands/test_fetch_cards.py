# -*- coding: utf-8 -*-
from StringIO import StringIO
from mock import patch

from oracle.management.commands import save_card_face
from oracle.models import CardFace, CardRelease, CardSet
from oracle.providers.gatherer import GathererCard
from oracle.tests.helpers import get_html_fixture
from oracle.tests.providers.base import ProviderTest


@patch('urllib2.urlopen')
class FetchCardsCommandTest(ProviderTest):
    def setUp(self):
        pass

    def test_save_card_oracle_details(self, urlopen):
        cs = CardSet.objects.create(name='Avacyn Restored')
        urlopen.return_value = StringIO(get_html_fixture('gatherer_angel_oracle'))
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertIsInstance(card_face, CardFace)
        self.assertEqual(card_face.name, u'Avacyn, Angel of Hope')
        card = card_face.card
        self.assertEqual(card_face.name, card.name)

        release = card.cardrelease_set.get(card_set=cs)
        self.assertEqual(release.rarity, CardRelease.MYTHIC)
        self.assertEqual(release.card_number, 6)

        provider = page.get_provider()
        self.assertEqual(
            release.sources.filter(data_provider=provider).count(), 1)
        source = release.sources.get(data_provider=provider)
        self.assertEqual(source.url, url)

    def test_save_card_with_no_text(self, urlopen):
        cs = CardSet.objects.create(name='Return to Ravnica')
        urlopen.return_value = StringIO(get_html_fixture('gatherer_vanilla_creature'))
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=265383'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertEqual(card_face.name, u'Axebane Stag')
        self.assertIsNone(card_face.rules)

    def test_save_land_card(self, urlopen):
        cs = CardSet.objects.create(name='Return to Ravnica')
        urlopen.return_value = StringIO(get_html_fixture('gatherer_forest'))
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertEqual(card_face.name, u'Forest')
        self.assertIsNone(card_face.flavor)
        self.assertIsNone(card_face.power)
        self.assertIsNone(card_face.thoughtness)
        self.assertIsNone(card_face.fixed_power)
        self.assertIsNone(card_face.fixed_thoughtness)
        self.assertIsNone(card_face.loyality)

    def test_save_card_with_no_number(self, urlopen):
        cs = CardSet.objects.create(name='Portal Second Age')
        urlopen.return_value = StringIO(get_html_fixture('gatherer_no_number'))
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=6567'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertEqual(card_face.name, u'Abyssal Nightstalker')
        release = card_face.card.cardrelease_set.get(card_set=cs)
        self.assertEqual(release.rarity, CardRelease.UNCOMMON)
        self.assertIsNone(release.card_number)

    def test_save_splited_card(self, urlopen):
        cs = CardSet.objects.create(name='Apocalypse')
        urlopen.return_value = StringIO(get_html_fixture('gatherer_fire_oracle'))
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?part=Fire&multiverseid=27166'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertIsInstance(card_face, CardFace)
        self.assertEqual(card_face.name, u'Fire')
        card = card_face.card
        self.assertEqual(card.name, 'Fire // Ice')
