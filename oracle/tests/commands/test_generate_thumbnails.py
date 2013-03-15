from django.test import TestCase
from django_any import any_model
from mock import patch, Mock

from oracle.management.commands.generate_thumbnails import \
    thumb_spec, create_thumbnail
from oracle.models import CardImage
from oracle.tests.helpers import get_jpeg_scan_fixture
from django.core.files.base import ContentFile


class GenerateThumbnailsCommandTest(TestCase):
    def test_thumb_spec(self):
        self.assertEqual(thumb_spec('100x200'), (100, 200))

    def test_create_thumb(self):
        img = any_model(CardImage)
        img.file.save('jpeg_fixture', ContentFile(get_jpeg_scan_fixture()))
        img.save()
        thumb = create_thumbnail(img, '100x120')
        self.assertEqual(thumb.original_id, img.id)
        self.assertGreater(thumb.file.size, 0)
        self.assertLess(thumb.file.size, img.file.size)

    #@patch.object(requests, 'get')
    #def test_fetch_art(self, get):
        ## Get request will return moked response
        #r_mock = Mock()
        #r_mock.content = get_jpeg_scan_fixture()
        #get.return_value = r_mock

        ## Prepare CardRelease fixture
        #scan_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=366469&type=card'
        #mvid = 366469
        #img = any_model(CardImage, scan=scan_url, mvid=mvid)

        #img = fetch_art(img)
        #name = img.file.name

        ## Try to save the same content again
        #img = fetch_art(img)
        #self.assertEqual(img.file.name, name)
