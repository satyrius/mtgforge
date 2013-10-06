# -*- coding: utf-8 -*-
from mock import patch

from crawler.management.commands import save_card_face
from crawler.providers.gatherer import GathererCard
from crawler.tests.helpers import get_html_fixture
from crawler.tests.providers.base import ProviderTest
from oracle import models as m


@patch.object(GathererCard, '_dowload_content')
class FetchCardsCommandTest(ProviderTest):
    def setUp(self):
        pass

    def test_save_card_oracle_details(self, _dowload_content):
        cs = m.CardSet.objects.create(name='Avacyn Restored')
        _dowload_content.return_value = get_html_fixture('gatherer_angel_oracle')
        mvid = 239961
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961'
        artist_name = 'Jason Chan'
        page = GathererCard(url)

        # No image yet
        with self.assertRaises(m.CardImage.DoesNotExist):
            m.CardImage.objects.get(mvid=mvid)
        # And no artist
        with self.assertRaises(m.Artist.DoesNotExist):
            m.Artist.objects.get(name=artist_name)

        # Save card face and assert saved data
        card_face = save_card_face(page, cs)
        self.assertIsInstance(card_face, m.CardFace)
        self.assertEqual(card_face.name, u'Avacyn, Angel of Hope')
        card = card_face.card
        self.assertEqual(card_face.name, card.name)
        self.assertEqual(card.faces_count, 1)
        expected_color = m.Color(card_face.mana_cost)
        card_face.color_identity = expected_color.identity
        card_face.colors = expected_color.colors
        self.assertEqual(card_face.types.count(), 3)

        # Release record was created too
        release = card.cardrelease_set.get(card_set=cs)
        self.assertEqual(release.rarity, m.CardRelease.MYTHIC)
        self.assertEqual(release.card_number, 6)

        # And default card image was created for this release
        self.assertIsNotNone(release.art)
        img = release.art
        self.assertEqual(img.mvid, mvid)
        art_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=239961&type=card'
        self.assertEqual(img.scan, art_url)
        self.assertEqual(img.file.name, '')
        self.assertIsNotNone(img.artist)
        self.assertEqual(img.artist.name, artist_name)

        # Source for released card was saved
        provider = page.get_provider()
        self.assertEqual(
            release.sources.filter(provider=provider).count(), 1)
        source = release.sources.get(provider=provider)
        self.assertEqual(source.url, url)

        # And we can get source page for card face released
        restored_page = GathererCard(release)
        self.assertIsInstance(restored_page, GathererCard)
        self.assertEqual(restored_page.url, url)

    def test_save_card_with_no_text(self, _dowload_content):
        cs = m.CardSet.objects.create(name='Return to Ravnica')
        _dowload_content.return_value = get_html_fixture('gatherer_vanilla_creature')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=265383'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertEqual(card_face.name, u'Axebane Stag')
        self.assertIsNone(card_face.rules)

    def test_save_land_card(self, _dowload_content):
        cs = m.CardSet.objects.create(name='Return to Ravnica')
        _dowload_content.return_value = get_html_fixture('gatherer_forest')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertEqual(card_face.name, u'Forest')
        self.assertIsNone(card_face.power)
        self.assertIsNone(card_face.thoughtness)
        self.assertIsNone(card_face.fixed_power)
        self.assertIsNone(card_face.fixed_thoughtness)
        self.assertIsNone(card_face.loyality)

    def test_save_card_with_no_number(self, _dowload_content):
        cs = m.CardSet.objects.create(name='Portal Second Age')
        _dowload_content.return_value = get_html_fixture('gatherer_no_number')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=6567'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertEqual(card_face.name, u'Abyssal Nightstalker')
        release = card_face.card.cardrelease_set.get(card_set=cs)
        self.assertEqual(release.rarity, m.CardRelease.UNCOMMON)
        self.assertIsNone(release.card_number)

    def test_save_splited_card(self, _dowload_content):
        cs = m.CardSet.objects.create(name='Apocalypse')
        _dowload_content.return_value = get_html_fixture('gatherer_fire_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?part=Fire&multiverseid=27166'
        page = GathererCard(url)

        card_face = save_card_face(page, cs)
        self.assertIsInstance(card_face, m.CardFace)
        self.assertEqual(card_face.name, u'Fire')
        self.assertEqual(card_face.place, m.CardFace.SPLIT)
        card = card_face.card
        self.assertEqual(card.name, 'Fire // Ice')
        self.assertEqual(card.faces_count, 2)

    def test_save_fliped_card(self, _dowload_content):
        cs = m.CardSet.objects.create(name='Champions of Kamigawa')
        _dowload_content.return_value = get_html_fixture('gatherer_flip_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694&part=Tok-Tok%2c+Volcano+Born'
        name = u'Akki Lavarunner (Tok-Tok, Volcano Born)'
        page = GathererCard(url, name=name)

        card_face = save_card_face(page, cs)
        card = card_face.card

        self.assertEqual(card.name, 'Akki Lavarunner')
        self.assertEqual(card.faces_count, 2)

        self.assertIsInstance(card_face, m.CardFace)
        self.assertEqual(card_face.name, u'Tok-Tok, Volcano Born')
        self.assertEqual(card_face.sub_number, 'b')
        self.assertEqual(card_face.place, m.CardFace.FLIP)
