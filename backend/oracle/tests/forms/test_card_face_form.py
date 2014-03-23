from django.test import TestCase
from model_mommy.recipe import Recipe, seq

from oracle.forms import CardFaceForm
from oracle.models import Card, CardType, CardFace
from oracle.utils import Color


class TestCardFaceForm(TestCase):
    def setUp(self):
        self.card_recipe = Recipe(Card)
        self.face_recipe = Recipe(CardFace, name=seq('Card '))
        self.card_type = Recipe(CardType)

    def test_save_as_in_admin(self):
        types = (
            self.card_type.make(name='a', category=CardType.SUBTYPE).id,
            self.card_type.make(name='b', category=CardType.TYPE).id,
            self.card_type.make(name='c', category=CardType.SUBTYPE).id,
            self.card_type.make(name='d', category=CardType.SUPERTYPE).id,
        )
        form = CardFaceForm(dict(
            name='New Test Angel',
            types=types,
            card=self.card_recipe.make().id,
        ))
        face = form.save()
        self.assertEqual(face.type_line, 'd b - a c')

        # But if type_line is already seted, do not update it
        form = CardFaceForm(dict(
            name='New Test Angel',
            types=(
                self.card_type.make(name='e', category=CardType.TYPE).id,
                self.card_type.make(name='f', category=CardType.SUPERTYPE).id,
            )
        ), instance=face)
        face = form.save()
        self.assertEqual(face.type_line, 'd b - a c')

    def test_little_girl_save(self):
        data = {
            'artist': 'Rebecca Guay',
            'cmc': '0.5',
            'flavor': 'In the future, she may be a distinguished leader, a '
                      'great scholar, or a decorated hero. These days all '
                      'she does is pee the bed.',
            'mana': '{500}',
            'mvid': '74257',
            'name': 'Little Girl',
            'number': '16',
            'pt': '{1/2} / {1/2}',
            'rarity': 'Common',
            'set': 'Unhinged',
            'title': 'Little Girl',
            'type': 'Creature - Human Child'}

        card = self.card_recipe.make()
        form = CardFaceForm(data, instance=CardFace(card=card))
        self.assertTrue(form.is_valid(), form.errors)
        face = form.save()
        self.assertEqual(face.card, card)
        self.assertEqual(face.name, data['name'])
        self.assertEqual(face.cmc, None)
        self.assertEqual(face.mana_cost, '{500}')
        self.assertEqual(face.colors, [Color.WHITE])
        self.assertEqual(face.power, '{1/2}')
        self.assertEqual(face.thoughtness, '{1/2}')
        self.assertEqual(face.fixed_power, 0)
        self.assertEqual(face.fixed_thoughtness, 0)
