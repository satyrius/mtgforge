from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from optparse import make_option
from tempfile import NamedTemporaryFile

from contrib.commands import BaseCommand
from oracle.models import CardImage, CardImageThumb


class Command(BaseCommand):
    help = 'Generate thumbnails for given formats'

    option_list = BaseCommand.option_list + (
        make_option(
            '--refresh',
            dest='refresh',
            action='store_true',
            default=False,
            help='Recreate thumbnail if already exists'),
        make_option(
            '--quality',
            dest='quality',
            type='int',
            default=90,
            help='JPEG quality'),
    )

    def handle(self, *args, **options):
        refresh = options['refresh']
        quality = options['quality']
        for fmt in settings.CARD_IMAGE_THUMBS:
            images = CardImage.objects.exclude(file='')
            if not refresh:
                images = images.exclude(cardimagethumb__format=fmt)

            if not images.count():
                self.notice(u'All "{0}" thumbnails are already '
                            u'generated'.format(fmt))
                continue

            self.notice(u'Generate "{0}" thumbnails'.format(fmt))
            for img in images:
                thumb = create_thumbnail(img, fmt, quality=quality)
                self.writeln(u'{0}, {1} compression {2:.2f}%'.format(
                    thumb.file.url, fmt,
                    float(img.file.size) * 100 / float(thumb.file.size)
                ))
                img.file.close()
                thumb.file.close()


def thumb_spec(fmt):
    width, height = map(
        lambda s: s.isdigit() and int(s) or None,
        fmt.split('x', 1)
    )
    return width, height


def create_thumbnail(card_image, thumb_format, quality=90):
    thumb, _ = CardImageThumb.objects.get_or_create(
        original=card_image, format=thumb_format)
    card_image.file.seek(0)
    img = Image.open(card_image.file)
    img.thumbnail(thumb_spec(thumb_format), Image.ANTIALIAS)
    with NamedTemporaryFile() as tmp:
        img.save(tmp, 'JPEG', quality=quality, optimize=True, progressive=True)
        tmp.seek(0)
        name = '{0}_{1}.thumb'.format(card_image.mvid, thumb_format)
        thumb.file.save(name, ContentFile(tmp.read()))
        thumb.save()
    return thumb
