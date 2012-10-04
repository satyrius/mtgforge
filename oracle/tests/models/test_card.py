# -*- coding: utf-8 -*-
from django.test import TestCase

from oracle.models import Card, CardFace, Color


class CardModelTest(TestCase):
    def setUp(self):
        pass

    def test_card_face_create(self):
        name = 'Mind Spring'
        card = Card.objects.create(name=name)
        front = CardFace.objects.create(
            card=card, place=CardFace.FRONT,
            name=name, type_line='Sorcery',
            rules='Draw X Cards',
        )
        self.assertEqual(card.cardface_set.count(), 1)
        self.assertEqual(card.cardface_set.all()[0].id, front.id)
        # No color identity if no mana_cost specified
        self.assertEqual(front.color_identity, 0)
        self.assertEqual(front.colors, [])

    def test_add_card_face(self):
        name = 'Woolly Thoctar'
        card = Card.objects.create(name=name)
        card.cardface_set.add(CardFace(
            place=CardFace.FRONT, name=name,
            type_line='Creature - Beast',
        ))
        card.save()
        self.assertEqual(card.cardface_set.count(), 1)

    def test_colors(self):
        name = 'Draw X Cards'
        card = Card.objects.create(name=name)
        face = CardFace.objects.create(
            card=card, place=CardFace.FRONT,
            name='Mind Spring', type_line='Sorcery',
            rules=name, mana_cost='{X}{U}{U}',
        )
        self.assertEqual(face.color_identity, Color.BLUE)
        self.assertEqual(face.colors, [Color.BLUE])
