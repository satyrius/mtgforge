# -*- coding: utf-8 -*-
from django.test import TestCase

from oracle.models import Card, CardFace, Color


class CardModelTest(TestCase):
    def setUp(self):
        pass

    def test_card_face_create(self):
        card = Card.objects.create()
        front = CardFace.objects.create(
            card=card, place=CardFace.FRONT,
            name='Mind Spring', type_line='Sorcery',
            rules='Draw X Cards',
        )
        self.assertEqual(card.cardface_set.count(), 1)
        self.assertEqual(card.cardface_set.all()[0].id, front.id)
        # No color identity if no mana_cost specified
        self.assertEqual(front.color_identity, 0)
        self.assertEqual(front.colors, [])

    def test_add_card_face(self):
        card = Card.objects.create()
        card.cardface_set.add(CardFace(
            place=CardFace.FRONT, name='Woolly Thoctar',
            type_line='Creature - Beast',
        ))
        card.save()
        self.assertEqual(card.cardface_set.count(), 1)

    def test_colors(self):
        card = Card.objects.create()
        face = CardFace.objects.create(
            card=card, place=CardFace.FRONT,
            name='Mind Spring', type_line='Sorcery',
            rules='Draw X Cards', mana_cost='{X}{U}{U}',
        )
        self.assertEqual(face.color_identity, Color.BLUE)
        self.assertEqual(face.colors, [Color.BLUE])
