# -*- coding: utf-8 -*-
from django.test import TestCase
from oracle.models import Card, CardFace


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

    def test_add_card_face(self):
        card = Card.objects.create()
        card.cardface_set.add(CardFace(
            place=CardFace.FRONT, name='Woolly Thoctar',
            type_line='Creature - Beast',
        ))
        card.save()
        self.assertEqual(card.cardface_set.count(), 1)
