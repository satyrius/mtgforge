from django_any import any_model
from django.test import TestCase

from oracle.forms import CardFaceForm
from oracle.models import Card, CardType


class TestCardFaceForm(TestCase):
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
