from django.test import TestCase
from oracle.forms import CardImageForm


class CardImageFormTest(TestCase):
    def test_required_fields(self):
        form = CardImageForm(dict(mvid=123))
        self.assertTrue(form.is_valid())

        form = CardImageForm(dict(comment='spoiler'))
        self.assertTrue(form.is_valid())

        form = CardImageForm(dict())
        self.assertFalse(form.is_valid())
