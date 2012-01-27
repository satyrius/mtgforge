# -*- coding: utf-8 -*-
from django.test import TestCase
from oracle.management.commands.fetch_sets import Command


__all__ = ['FetchCardSetsCommandTest']


class FetchCardSetsCommandTest(TestCase):
    def test_acronym_generation(self):
        generator = Command().generate_acronym
        self.assertEqual(generator('Shards of Alara'), 'soa')
        self.assertEqual(generator('New Phyrexia'), 'nph')
        self.assertEqual(generator('Zendikar'), 'zen')
        self.assertEqual(generator('From the Vault: Exiled'), 'ftve')
        self.assertEqual(generator('Sixth Edition'), '6ed')
