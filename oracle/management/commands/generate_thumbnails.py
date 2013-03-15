from PIL import Image
from django.core.files.base import ContentFile
from oracle.management.base import BaseCommand
from oracle.models import CardImage, CardImageThumb
from django.conf import settings
from tempfile import NamedTemporaryFile


class Command(BaseCommand):
    help = 'Generate thumbnails for given formats'

    def handle(self, *args, **options):
        for fmt in settings.CARD_IMAGE_THUMBS:
            images = CardImage.objects.exclude(cardimagethumb__format=fmt).exclude(file=None)

            if not images.count():
                self.notice(u'All "{0}" thumbnails are already '
                            u'generated'.format(fmt))
                continue

            self.notice(u'Generate "{0}" thumbnails'.format(fmt))
            for img in images:
                thumb = create_thumbnail(img, fmt)
                self.writeln(u'{0}, compression {1:.2f}%'.format(
                    thumb.file.url,
                    float(img.file.size) * 100 / float(thumb.file.size)
                ))
                map(lambda m: m.file.close(), [img, thumb])


def thumb_spec(fmt):
    width, height = map(
        lambda s: s.isdigit() and int(s) or None,
        fmt.split('x', 1)
    )
    return width, height


def create_thumbnail(card_image, thumb_format):
    thumb = CardImageThumb(original=card_image, format=thumb_format)
    img = Image.open(card_image.file)
    img.thumbnail((thumb_spec(thumb_format)), Image.ANTIALIAS)
    with NamedTemporaryFile() as tmp:
        img.save(tmp, 'JPEG', optimize=True, progressive=True)
        tmp.seek(0)
        name = '{0}_{1}.thumb'.format(card_image.mvid, thumb_format)
        thumb.file.save(name, ContentFile(tmp.read()))
        thumb.save()
    return thumb
