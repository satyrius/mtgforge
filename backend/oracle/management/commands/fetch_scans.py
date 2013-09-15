import itertools
import sys
from optparse import make_option

import gevent
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from gevent import monkey

from oracle.management.base import BaseCommand
from oracle.models import CardImage


monkey.patch_all(thread=False, select=False)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-t', '--threads',
            dest='threads',
            default=30,
            help='Number of threads will be spawn to download images'),
    )

    def handle(self, *args, **options):
        n = int(options['threads'])
        card_images = CardImage.objects.filter(file='').exclude(scan='')
        self.download(card_images, n)

    def download(self, card_images, threads, tries=[]):
        tries.append(len(tries) + 1)
        if len(tries) > threads:
            self.error(u'This is a {0} try and there is {1} failed pages. '
                       u'Give up!'.format(len(tries), len(card_images)))
            sys.exit(1)
        failed = []
        for chunk in itertools.izip_longest(*([iter(card_images)] * threads)):
            chunk = filter(None, chunk)
            jobs = [gevent.spawn(fetch_art, img) for img in chunk]
            gevent.joinall(jobs, timeout=settings.DATA_PROVIDER_TIMEOUT)
            for job, img in zip(jobs, chunk):
                if job.successful():
                    self.writeln(u'{0:15} {1}'.format(
                        img.mvid, img.scan))
                else:
                    failed.append(img)
                    self.error(
                        u'Cannot complete job for page {0}, '
                        u'try again later'.format(img.scan))
        if failed:
            self.download(failed, threads)


def fetch_art(img):
    r = requests.get(img.scan)
    name = '{0}.image'.format(img.mvid)
    img.file.save(name, ContentFile(r.content))
    return img
