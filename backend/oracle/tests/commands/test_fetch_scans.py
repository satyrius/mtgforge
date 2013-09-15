import requests
from django.test import TestCase
from django_any import any_model
from mock import patch, Mock

from oracle.management.commands.fetch_scans import fetch_art
from oracle.models import CardImage
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
        img = any_model(CardImage, scan=scan_url, mvid=mvid)

        img = fetch_art(img)
        name = img.file.name

        # Try to save the same content again
        img = fetch_art(img)
        self.assertEqual(img.file.name, name)
