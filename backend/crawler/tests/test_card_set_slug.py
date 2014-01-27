import unittest
from crawler.pipelines.sets import generate_slug


class CardSetSlugTest(unittest.TestCase):
    def test_generate_slug(self):
        generator = generate_slug
        self.assertEqual(generator('Shards of Alara'), 'soa')
        self.assertEqual(generator('New Phyrexia'), 'nph')
        self.assertEqual(generator('Zendikar'), 'zen')
        self.assertEqual(generator('From the Vault: Exiled'), 'ftve')
        self.assertEqual(generator('Sixth Edition'), '6ed')
        self.assertEqual(generator('Magic 2010'), 'm10')
        self.assertEqual(generator('Premium Deck Series: Fire & Lightning'), 'pdsfl')
        self.assertEqual(generator('Chronicles / Renaissance'), 'cre')
