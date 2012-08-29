import itertools
import logging
from optparse import make_option

import gevent
from django.conf import settings
from django.core.cache import get_cache
from gevent import monkey

from contrib.utils import measureit
from oracle.management.base import BaseCommand
from oracle.models import CardSet
from oracle.providers.gatherer import GathererCardList, GathererPage


logger = logging.getLogger(__name__)

monkey.patch_all(thread=False, select=False)


class Command(BaseCommand):
    args = '<card_set_1 card_set_2 ...>'
    help = ('Fetched pages from Gatherer and save then to the storage. This '
            'data will bu used to fill cards database.self')

    option_list = BaseCommand.option_list + (
        make_option('-t', '--threads',
            dest='threads',
            default=30,
            help='Number of threads will be spawn to download content'),
        make_option('-c', '--clear-cache',
            dest='clear',
            action='store_true',
            default=False,
            help='Invalidate pages cache'),
        )

    @measureit(logger=logger)
    def handle(self, *args, **options):
        if options['clear']:
            get_cache('provider_page').clear()
            get_cache('default', KEY_PREFIX='pagination').clear()

        self.threads_count = int(options['threads'])
        sets = CardSet.objects.all()
        if args:
            sets = sets.filter(acronym__in=args)

        pagination = []
        self.notice('Fetch home page for each card set')
        message_shown = False
        for cs_page in self.process_pages(map(GathererCardList, sets)):
            if not message_shown:
                self.notice('Parse card sets pages to get pagination')
                message_shown = True
            for page in cs_page.pages_generator():
                pagination.append(page)

        self.notice('Fetch card list pages for each set')
        for cs_page in self.process_pages(pagination):
            self.notice('Fetch card page for list {}'.format(cs_page.url))
            self.process_pages(cs_page.cards_list_generator())

    def process_pages(self, pages, i=0):
        chunk = self.threads_count
        failed = []
        for pages_chunk in itertools.izip_longest(*([iter(pages)] * chunk)):
            for result in self.process_chunk(pages_chunk):
                if isinstance(result, GathererPage):
                    i += 1
                    self.writeln(u'>>> {1:3} {0}'.format(result.url, i))
                else:
                    page = result.args[0]
                    self.error(
                        u'Cannot download page {0}, try again later'.format(
                            page.url))
                    failed.append(page)
        # Try again for failed downloads
        if failed:
            self.process_pages(failed, i)
        return pages

    def process_chunk(self, pages):
        def fetch_page(page):
            page.get_content()
            return page
        jobs = [gevent.spawn(fetch_page, page) for page in filter(None, pages)]
        gevent.joinall(jobs, timeout=settings.DATA_PROVIDER_TIMEOUT)
        for job in jobs:
            # Return fetched page or job to try again
            yield job.successful() and job.value or job
