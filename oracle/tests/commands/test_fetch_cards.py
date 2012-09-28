# -*- coding: utf-8 -*-
from mock import patch

from oracle.management.commands.fetch_gatherer import Command
from oracle.models import CardFace, CardRelease, CardSet, Card
from oracle.providers.gatherer import GathererCard
from oracle.tests.helpers import get_html_fixture
from oracle.tests.providers.base import ProviderTest


class FetchCardsCommandTest(ProviderTest):
    @patch.object(GathererCard, 'get_content')
    def setUp(self, get_content):
        self.cs = CardSet.objects.create(name='Avacyn Restored')
        self.assertEqual(self.cs.cardrelease_set.all().count(), 0)
        self.assertEqual(CardFace.objects.all().count(), 0)
        self.assertEqual(Card.objects.all().count(), 0)

        get_content.return_value = get_html_fixture('gatherer_angel_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961'
        name = u'Avacyn, Angel of Hope'
        page = GathererCard(url, name=name)
        self.details = page.details()

    def test_save_card_oracle_details(self):
        cmd = Command()
        self.assertFalse(cmd.no_update)

        card_face = cmd.save_card_face(self.details, self.cs)
        card = card_face.card
        self.assertIsInstance(card_face, CardFace)

        release = card.cardrelease_set.get(card_set=self.cs)
        self.assertEqual(release.rarity, CardRelease.MYTHIC)
        self.assertEqual(release.card_number, 6)
