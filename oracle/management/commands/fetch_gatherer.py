import itertools
import logging
from optparse import make_option

import gevent
from django.conf import settings
from django.core.cache import get_cache
from gevent import monkey

from contrib.utils import measureit
from oracle.management.base import BaseCommand
from oracle.management.commands import save_card_face
from oracle.models import CardSet
from oracle.providers.gatherer import GathererCardList


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
        make_option('--ignore-cache',
            dest='ignore_cache',
            action='store_true',
            default=False,
            help='Ignore cached paged and download content again'),
        make_option('--sim', '--simultaneously-parse',
            dest='simultaneously',
            action='store_true',
            default=False,
            help='Parse page right after it has been dowloaded'),
        make_option('--no-update',
            action='store_true',
            dest='no_update',
            default=False,
            help='Do not update existing card faces'),
        make_option('--skip-parsed',
            action='store_true',
            dest='skip_parsed',
            default=False,
            help='Skip parsing pages already parsed'),
        )

    def __init__(self):
        super(Command, self).__init__()
        self.no_update = False
        self.skip_parsed = False

    def handle_args(self, *args, **options):
        if options['clear']:
            get_cache('provider_page').clear()
            get_cache('default', KEY_PREFIX='pagination').clear()

        self.threads_count = int(options['threads'])
        self.sets = CardSet.objects.all()
        if args:
            self.sets = self.sets.filter(acronym__in=args)

        self.no_update = options['no_update']
        self.skip_parsed = options['skip_parsed']
        self.ignore_cache = options['ignore_cache']

    @measureit(logger=logger)
    def handle(self, *args, **options):
        self.handle_args(*args, **options)

        pagination = []
        self.notice(u'(1) Fetch home page for each card set')
        message_shown = False
        create_cs_page = lambda cs: GathererCardList(
            cs, read_cache=(not self.ignore_cache))
        for cs_page in self.process_pages(map(create_cs_page, self.sets)):
            if not message_shown:
                self.notice(u'(2) Parse card sets pages to get pagination')
                message_shown = True
            for page in cs_page.pages():
                pagination.append(page)

        simultaneously = options['simultaneously']
        self.notice(u'(3{0}) Fetch card list pages for each set'.format(
            not simultaneously and 'a' or ''))
        total = self.fetch_card_pages(pagination, save=simultaneously)
        if not simultaneously:
            self.notice(u'(3b) Go through all card pages and save card data')
            self.fetch_card_pages(
                map(lambda p: p.force_read_cache(), pagination), total=total)

    def fetch_card_pages(self, pagination, save=True, total=None):
        cards_counter = 0
        pages_counter, total_pages = 0, len(pagination)
        failed_pages = []
        for cs_page in self.process_pages(pagination):
            pages_counter += 1
            self.notice(u'{1:3}/{2} Process cards for list {0}'.format(
                cs_page.url, pages_counter, total_pages))
            cards = cs_page.cards_list()
            for page in self.process_pages(cards):
                if save:
                    self.writeln(u'[*] {1:5}/{2} {0} from {3}'.format(
                        page.name, cards_counter + 1, total or '?', page.url))
                    if not self.skip_parsed or not page.is_parsed():
                        try:
                            save_card_face(page, cs_page.card_set, self.no_update)
                        except Exception, e:
                            self.error(e)
                            failed_pages.append((page.name, page.url))
                cards_counter += 1
        if failed_pages:
            self.error('The following card pages parsing failed:')
            for name, url in failed_pages:
                self.error(u'{0} from {1}'.format(name, url))
        return cards_counter

    def process_pages(self, pages, run=None):
        '''Process list of pages chunk by chunk. Use ``run`` for job'''
        chunk = self.threads_count
        result = []
        failed = []
        for pages_chunk in itertools.izip_longest(*([iter(pages)] * chunk)):
            for job, page in self.process_chunk(pages_chunk, run):
                # Report successful job or try again
                if job.successful():
                    result.append(job.value)
                else:
                    failed.append(page)
                    self.error(
                        u'Cannot complete job for page {0}, try again later'.format(
                            page.url))

        # Try again for failed downloads
        if failed:
            result.extend(self.process_pages(failed))
        return result

    def log_request(self, response):
        self.writeln(u'>>> {0}'.format(response.url))

    def fetch_page(self, page):
        page.get_content(hooks=dict(response=self.log_request))
        return page

    def process_chunk(self, pages, run=None):
        pages = filter(None, pages)
        jobs = [gevent.spawn(run or self.fetch_page, page) for page in pages]
        gevent.joinall(jobs, timeout=settings.DATA_PROVIDER_TIMEOUT)
        for job, page in zip(jobs, pages):
            yield job, page
