from mock import patch
from django.test import TestCase
from oracle.forms import CardFaceForm
from oracle.models import Card, CardFace
from oracle.providers.gatherer import GathererCard
from oracle.tests.helpers import get_html_fixture


class TestCardFaceForm(TestCase):
    @patch.object(GathererCard, 'get_content')
    def test_card_details(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_werewolf_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=2446835'
        name = u'Hanweir Watchkeep'
        page = GathererCard(url, name=name)
        data = page.details()

        card = Card.objects.create()
        face = CardFace(card=card)
        form = CardFaceForm(data, instance=face)
        self.assertTrue(form.is_valid(), '\n' + form.errors.as_text())

        saved_face = form.save()
        card = saved_face.card
        self.assertIsInstance(saved_face, CardFace)
        self.assertEqual(saved_face.name, data['name'])
        self.assertEqual(card.name, data['name'])
        self.assertEqual(saved_face.rules, data['text'])
        self.assertEqual(saved_face.flavor, data['flavor'])
        self.assertEqual(saved_face.type_line, data['type'])
        self.assertEqual(saved_face.cmc, int(data['cmc']))
        self.assertEqual(saved_face.mana_cost, data['mana'])
        self.assertEqual(saved_face.power, '1')
        self.assertEqual(saved_face.thoughtness, '5')
        self.assertEqual(saved_face.fixed_power, 1)
        self.assertEqual(saved_face.fixed_thoughtness, 5)
        self.assertIsNone(saved_face.loyality)

    @patch.object(GathererCard, 'get_content')
    def test_fractional_pt(self, get_content):
        get_content.return_value = get_html_fixture('complex_power_and_thoughtness')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=74251'
        page = GathererCard(url)
        data = page.details()
        self.assertIn('pt', data)
        self.assertEqual(data['pt'], '3{1/2} / 3{1/2}')

        card = Card.objects.create()
        face = CardFace(card=card)
        form = CardFaceForm(data, instance=face)
        self.assertTrue(form.is_valid(), '\n' + form.errors.as_text())

        saved_face = form.save()
        self.assertIsInstance(saved_face, CardFace)
        self.assertEqual(saved_face.power, '3{1/2}')
        self.assertEqual(saved_face.fixed_power, 3)
        self.assertEqual(saved_face.thoughtness, '3{1/2}')
        self.assertEqual(saved_face.fixed_thoughtness, 3)
        self.assertIsNone(saved_face.loyality)
