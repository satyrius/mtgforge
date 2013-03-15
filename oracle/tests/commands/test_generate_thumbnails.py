from django.core.files.base import ContentFile
from django.test import TestCase

from oracle.management.commands.generate_thumbnails import \
    thumb_spec, create_thumbnail
from oracle.models import CardImage
from oracle.tests.helpers import get_jpeg_scan_fixture


class GenerateThumbnailsCommandTest(TestCase):
    def test_thumb_spec(self):
        self.assertEqual(thumb_spec('100x200'), (100, 200))

    def test_create_thumb_then_recreate(self):
        img = CardImage()
        img.file.save('jpeg_fixture', ContentFile(get_jpeg_scan_fixture()))
        img.save()

        # Create thumbnail
        fmt = '100x120'
        thumb = create_thumbnail(img, fmt, quality=80)
        self.assertEqual(thumb.original_id, img.id)
        size_q80 = thumb.file.size
        self.assertGreater(size_q80, 0)
        self.assertLess(size_q80, img.file.size)

        # Refresh
        thumb2 = create_thumbnail(img, fmt, quality=60)
        self.assertEqual(thumb.id, thumb2.id)
        self.assertLess(thumb2.file.size, size_q80)
