# -*- coding: utf-8 -*-

from django.test import TestCase
from crawler.management.commands.fetch_sets import Command


class FetchCardSetsCommandTest(TestCase):
    def test_acronym_generation(self):
        generator = Command().generate_acronym
        self.assertEqual(generator('Shards of Alara'), 'soa')
        self.assertEqual(generator('New Phyrexia'), 'nph')
        self.assertEqual(generator('Zendikar'), 'zen')
        self.assertEqual(generator('From the Vault: Exiled'), 'ftve')
        self.assertEqual(generator('Sixth Edition'), '6ed')
        self.assertEqual(generator('Magic 2010'), 'm10')
        self.assertEqual(generator('Premium Deck Series: Fire & Lightning'), 'pdsfl')
        self.assertEqual(generator('Chronicles / Renaissance'), 'cre')
