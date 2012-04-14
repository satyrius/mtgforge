# -*- coding: utf-8 -*-
from django.test import TestCase

from oracle.forms import CardSetForm
from oracle.models import CardSet


class CardSetModelTest(TestCase):
    def setUp(self):
        self.name, self.acronym = 'Zendikar', 'zen'

    def test_card_set_empty_name(self):
        form = CardSetForm(dict(acronym=self.acronym))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(len(form.errors['name']), 1)
        self.assertRegexpMatches(form.errors['name'][0], 'field is required')

    def test_card_set_empty_acronym(self):
        form = CardSetForm(dict(name=self.name))
        self.assertFalse(form.is_valid())
        self.assertIn('acronym', form.errors)
        self.assertEqual(len(form.errors['acronym']), 1)
        self.assertRegexpMatches(form.errors['acronym'][0], 'field is required')

    def test_card_set_unique_name(self):
        form = CardSetForm(dict(name=self.name, acronym=self.acronym))
        self.assertTrue(form.is_valid())
        form.save()

        # Post the same name thing twice
        new_set_acronym = 'new' + self.acronym
        form = CardSetForm(dict(name=self.name, acronym=new_set_acronym))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(len(form.errors['name']), 1)
        self.assertRegexpMatches(form.errors['name'][0], 'already exists')

    def test_card_set_unique_acronym(self):
        form = CardSetForm(dict(name=self.name, acronym=self.acronym))
        self.assertTrue(form.is_valid())
        form.save()

        # Post the same acronym thing twice
        new_set_name = 'new' + self.name
        form = CardSetForm(dict(name=new_set_name, acronym=self.acronym))
        self.assertFalse(form.is_valid())
        self.assertIn('acronym', form.errors)
        self.assertEqual(len(form.errors['acronym']), 1)
        self.assertRegexpMatches(form.errors['acronym'][0], 'already exists')

    def test_card_set_long_acronym(self):
        long_acronym = '1234567890a'
        form = CardSetForm(dict(name=self.name, acronym=long_acronym))
        self.assertFalse(form.is_valid())
        self.assertIn('acronym', form.errors)
        self.assertEqual(len(form.errors['acronym']), 1)
        self.assertRegexpMatches(
            form.errors['acronym'][0],
            'Ensure this value has at most 10 characters')

    def test_name_translation(self):
        # Create object without translations and assert that only default was
        # specified after creation
        cs = CardSet.objects.create(name=self.name, acronym=self.acronym)
        self.assertEqual(cs.name, self.name)
        self.assertEqual(cs.name_en, self.name)
        self.assertIsNone(cs.name_ru)

        get_cs = lambda: CardSet.objects.get(acronym=self.acronym)

        # Check uptate original
        name_en = 'Zendikar Set'
        cs.name = name_en
        cs.save()
        cs = get_cs()
        self.assertEqual(cs.name, name_en)
        self.assertEqual(cs.name_en, name_en)
        self.assertIsNone(cs.name_ru)

        # Check update default translation
        cs.name_en = self.name
        cs.save()
        cs = get_cs()
        self.assertEqual(cs.name, self.name)
        self.assertEqual(cs.name_en, self.name)
        self.assertIsNone(cs.name_ru)

        # Check update non-default translation
        name_ru = u'Зендикар'
        cs.name_ru = name_ru
        cs.save()
        cs = get_cs()
        self.assertEqual(cs.name, cs.name_en)
        self.assertNotEqual(cs.name, cs.name_ru)
        self.assertEqual(cs.name_ru, name_ru)

        # Check create with translations
        cs.delete()
        CardSet.objects.create(name=self.name, acronym=self.acronym, name_ru=name_ru)
        cs = get_cs()
        self.assertEqual(cs.name, self.name)
        self.assertEqual(cs.name_en, self.name)
        self.assertEqual(cs.name_ru, name_ru)
