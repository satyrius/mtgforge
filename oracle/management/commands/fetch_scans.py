from contrib.cdn import save_to_cdn, cdn_thumbnail
from oracle.management.base import BaseCommand
from oracle.models import CardL10n, STORAGE_PATH, IMAGE_FORMATS


class Command(BaseCommand):
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        for card in CardL10n.objects.filter(file=None):
            self.writeln(u'{0:30} {1}'.format(unicode(card.name), card.scan))
            if dry_run:
                continue
            card.file = save_to_cdn(card.scan, STORAGE_PATH, IMAGE_FORMATS)
            url = cdn_thumbnail(card.file.name, format='orig', secure=False)
            self.writeln(u'>>> {0}'.format(url))
            card.save()
