import requests
from django.test import TestCase
from django_any import any_model
from mock import patch, Mock

from oracle.management.commands.fetch_scans import fetch_art
from oracle.models import CardRelease
from oracle.tests.helpers import get_jpeg_scan_fixture


class FetchScansCommandTest(TestCase):
    @patch.object(requests, 'get')
    def test_fetch_art(self, get):
        # Get request will return moked response
        r_mock = Mock()
        r_mock.content = get_jpeg_scan_fixture()
        get.return_value = r_mock

        # Prepare CardRelease fixture
        scan_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=366469&type=card'
        mvid = 366469
        cr = any_model(CardRelease, scan=scan_url, mvid=mvid)

        cr = fetch_art(cr, 'scan', 'default_art')
        name = cr.default_art.name

        # Try to save the same content again
        cr = fetch_art(cr, 'scan', 'default_art')
        self.assertEqual(cr.default_art.name, name)
