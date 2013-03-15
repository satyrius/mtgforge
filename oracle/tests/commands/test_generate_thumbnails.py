from django.core.files.base import ContentFile
from django.test import TestCase

from oracle.management.commands.generate_thumbnails import \
    thumb_spec, create_thumbnail
from oracle.models import CardImage
from oracle.tests.helpers import get_jpeg_scan_fixture


class GenerateThumbnailsCommandTest(TestCase):
    def test_thumb_spec(self):
        self.assertEqual(thumb_spec('100x200'), (100, 200))

    def test_create_thumb(self):
        img = CardImage()
        img.file.save('jpeg_fixture', ContentFile(get_jpeg_scan_fixture()))
        img.save()
        thumb = create_thumbnail(img, '100x120')
        self.assertEqual(thumb.original_id, img.id)
        self.assertGreater(thumb.file.size, 0)
        self.assertLess(thumb.file.size, img.file.size)
