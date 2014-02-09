from unittest import TestCase
from crawler.spiders.gatherer import printed_url


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
