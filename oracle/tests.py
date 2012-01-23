# -*- coding: utf-8 -*-
from django.test import TestCase
from oracle.models import CardSet
from django.db import IntegrityError, DatabaseError
from django.utils.functional import curry


class CardSetModelTest(TestCase):
    def setUp(self):
        self.not_null_integrity_error = 'null value in column "{0}" violates not-null constraint'
        self.value_too_long_error = 'value too long for type character varying({0})'
        self.name, self.acronym = 'Zendikar', 'zen'

    def test_card_set_empty_name(self):
        with self.assertRaises(IntegrityError) as context:
            CardSet.objects.create(acronym=self.acronym)
        msg = self.not_null_integrity_error.format('name')
        self.assertTrue(context.exception.message.startswith(msg))

    def test_card_set_empty_acronym(self):
        with self.assertRaises(IntegrityError) as context:
            CardSet.objects.create(name=self.name)
        msg = self.not_null_integrity_error.format('acronym')
        self.assertTrue(context.exception.message.startswith(msg))

    def test_card_set_unique_name(self):
        CardSet.objects.create(name=self.name, acronym=self.acronym)
        with self.assertRaises(IntegrityError) as context:
            new_set_acronym = 'new' + self.acronym
            CardSet.objects.create(name=self.name, acronym=new_set_acronym)
        self.assertRegexpMatches(
            context.exception.message,
            r'Key \(name\)=\({0}\) already exists'.format(self.name)
        )

    def test_card_set_unique_acronym(self):
        CardSet.objects.create(name=self.name, acronym=self.acronym)
        with self.assertRaises(IntegrityError) as context:
            new_set_name = 'new' + self.name
            CardSet.objects.create(name=new_set_name, acronym=self.acronym)
        self.assertRegexpMatches(
            context.exception.message,
            r'Key \(acronym\)=\({0}\) already exists'.format(self.acronym)
        )

    def test_card_set_long_acronym(self):
        with self.assertRaises(DatabaseError) as context:
            long_acronym = '1234567890a'
            CardSet.objects.create(name=self.name, acronym=long_acronym)
        max_acronym_length = 10
        msg = self.value_too_long_error.format(max_acronym_length)
        self.assertTrue(context.exception.message.startswith(msg))

    def test_name_translation(self):
        # Create object without translations and assert that only default was
        # specified after creation
        CardSet.objects.create(name=self.name, acronym=self.acronym)
        get_cs = curry(CardSet.objects.get, acronym=self.acronym)
        cs = get_cs()
        self.assertEqual(cs.name, self.name)
        self.assertEqual(cs.name_en, self.name)
        self.assertIsNone(cs.name_ru)

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
