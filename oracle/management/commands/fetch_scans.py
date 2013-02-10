import itertools
import sys
from optparse import make_option

import gevent
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from gevent import monkey

from oracle.management.base import BaseCommand
from oracle.models import CardRelease


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
        cards = CardRelease.objects.filter(default_art=None)
        self.download(cards, n)

    def download(self, cards, threads, tries=[]):
        tries.append(len(tries) + 1)
        if len(tries) > threads:
            self.error(u'This is a {0} try and there is {1} failed pages. '
                       u'Give up!'.format(len(tries), len(cards)))
            sys.exit(1)
        failed = []
        for chunk in itertools.izip_longest(*([iter(cards)] * threads)):
            chunk = filter(None, chunk)
            jobs = [gevent.spawn(fetch_art, cr, 'scan', 'default_art') for cr in chunk]
            gevent.joinall(jobs, timeout=settings.DATA_PROVIDER_TIMEOUT)
            for job, cr in zip(jobs, chunk):
                if job.successful():
                    self.writeln(u'{0:30} {1}'.format(
                        unicode(cr.card.name), cr.scan))
                else:
                    failed.append(cr)
                    self.error(
                        u'Cannot complete job for page {0}, '
                        u'try again later'.format(cr.scan))
        if failed:
            self.download(failed, threads)


def fetch_art(card, orig_url_attr='scan', image_attr='art'):
    r = requests.get(getattr(card, orig_url_attr))
    name = '{0}.image'.format(card.mvid)
    content = ContentFile(r.content)
    image_field = getattr(card, image_attr)
    image_field.save(name, content)
    return card
