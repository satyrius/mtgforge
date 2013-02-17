from mock import patch
from django_any import any_model
from django.test import TestCase
from oracle.forms import CardFaceForm
from oracle.models import Card, CardFace, CardType
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

        card = Card.objects.create(name=name)
        face = CardFace(card=card)
        form = CardFaceForm(data, instance=face)
        self.assertTrue(form.is_valid(), '\n' + form.errors.as_text())

        saved_face = form.save()
        card = saved_face.card
        self.assertIsInstance(saved_face, CardFace)
        self.assertEqual(saved_face.name, data['name'])
        self.assertEqual(card.name, data['name'])
        self.assertEqual(saved_face.rules, data['text'])
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
        get_content.return_value = get_html_fixture('gatherer_fractional_pt')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=74251'
        page = GathererCard(url)
        data = page.details()
        self.assertIn('pt', data)
        self.assertEqual(data['pt'], '3{1/2} / 3{1/2}')

        card = Card.objects.create(name='Assquatch')
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

    @patch.object(GathererCard, 'get_content')
    def test_pt_with_stats(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_tarmogoyf')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=136142'
        page = GathererCard(url)
        data = page.details()
        self.assertIn('pt', data)
        self.assertEqual(data['pt'], '* / 1+*')

        card = Card.objects.create(name='Tarmogoyf')
        face = CardFace(card=card)
        form = CardFaceForm(data, instance=face)
        self.assertTrue(form.is_valid(), '\n' + form.errors.as_text())

        saved_face = form.save()
        self.assertIsInstance(saved_face, CardFace)
        self.assertEqual(saved_face.power, '*')
        self.assertIsNone(saved_face.fixed_power)
        self.assertEqual(saved_face.thoughtness, '1+*')
        self.assertIsNone(saved_face.fixed_thoughtness)
        self.assertIsNone(saved_face.loyality)

    def test_save_as_in_admin(self):
        types = (
            any_model(CardType, name='a', category=CardType.SUBTYPE).id,
            any_model(CardType, name='b', category=CardType.TYPE).id,
            any_model(CardType, name='c', category=CardType.SUBTYPE).id,
            any_model(CardType, name='d', category=CardType.SUPERTYPE).id,
        )
        form = CardFaceForm(dict(
            name='New Test Angel',
            types=types,
            card=any_model(Card).id,
        ))
        face = form.save()
        self.assertEqual(face.type_line, 'd b - a c')

        # But if type_line is already seted, do not update it
        form = CardFaceForm(dict(
            name='New Test Angel',
            types=(
                any_model(CardType, name='e', category=CardType.TYPE).id,
                any_model(CardType, name='f', category=CardType.SUPERTYPE).id,
            )
        ), instance=face)
        face = form.save()
        self.assertEqual(face.type_line, 'd b - a c')
