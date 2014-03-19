from unittest import TestCase
from nose_parameterized import parameterized
from crawler.spiders.gatherer import printed_url, is_printed_url, get_mvid


class GathererUtilsTest(TestCase):
    def test_print_url(self):
        self.assertEqual(
            printed_url(
                'http://gatherer.wizards.com/Pages/Card/Details.aspx?'
                'multiverseid=378376'
            ),
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?'
            'multiverseid=378376&printed=true'
        )

    def test_print_url_from_false_to_true(self):
        self.assertEqual(
            printed_url(
                'http://gatherer.wizards.com/Pages/Card/Details.aspx?'
                'multiverseid=378376&printed=false'
            ),
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?'
            'multiverseid=378376&printed=true'
        )

    @parameterized.expand([
        ('multiverseid=378376', False),
        ('printed=false&multiverseid=378376', False),
        ('printed=true&multiverseid=378376', True),
    ])
    def test_is_print_url(self, query, is_printed):
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?' + query
        self.assertEqual(is_printed_url(url), is_printed)

    @parameterized.expand([
        ('multiverseid=378376', 378376),
        ('printed=false&multiverseid=378376', 378376),
        ('printed=true', None),
    ])
    def test_get_mvid(self, query, mvid):
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?' + query
        self.assertEqual(get_mvid(url), mvid)
