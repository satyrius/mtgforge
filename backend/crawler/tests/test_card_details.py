import unittest
from crawler.spiders.gatherer import number_suffixes


class NumberSiffixTest(unittest.TestCase):
    def test_no_split(self):
        title = 'Forest'
        self.assertEqual(number_suffixes(title), {title: ''})

    def test_double_faced(self):
        title = 'Hanweir Watchkeep'
        self.assertEqual(number_suffixes(title), {title: ''})

    def test_splited(self):
        title = 'Fire // Ice'
        self.assertEqual(number_suffixes(title), {
            'Fire': 'a',
            'Ice': 'b',
        })
