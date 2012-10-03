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

    @measureit(logger=logger)
    def handle(self, *args, **options):
        if options['clear']:
            get_cache('provider_page').clear()
            get_cache('default', KEY_PREFIX='pagination').clear()

        self.threads_count = int(options['threads'])
        sets = CardSet.objects.all()
        if args:
            sets = sets.filter(acronym__in=args)

        self.no_update = options['no_update']
        self.skip_parsed = options['skip_parsed']

        pagination = []
        self.notice('Fetch home page for each card set')
        message_shown = False
        for cs_page in self.process_pages(map(GathererCardList, sets)):
            if not message_shown:
                self.notice('Parse card sets pages to get pagination')
                message_shown = True
            for page in cs_page.pages():
                pagination.append(page)

        self.notice('Fetch card list pages for each set')
        simultaneously = options['simultaneously']
        total = self.fetch_card_pages(pagination, save=simultaneously)
        if not simultaneously:
            self.notice('Go through all card pages and save card data')
            self.fetch_card_pages(pagination, print_url=False, total=total)

    def fetch_card_pages(self, pagination, save=True, print_url=True, total=None):
        i = 0
        for cs_page in self.process_pages(pagination, print_url=print_url):
            if print_url:
                self.notice(u'Fetch card pages for list {}'.format(cs_page.url))
            cards = cs_page.cards_list()
            for page in self.process_pages(cards, i, print_url=print_url):
                if save:
                    self.writeln(u'[*] {1:5}/{2} {0} from {3}'.format(
                        page.name, i, total or '?', page.url))
                    if not self.skip_parsed or not page.is_parsed():
                        save_card_face(
                            page.details(), cs_page.card_set, self.no_update)
                        page.set_parsed()
                i += 1
        return i

    def process_pages(self, pages, i=0, print_url=True):
        chunk = self.threads_count
        failed = []
        for pages_chunk in itertools.izip_longest(*([iter(pages)] * chunk)):
            for result in self.process_chunk(pages_chunk):
                if isinstance(result, GathererPage):
                    i += 1
                    if print_url:
                        self.writeln(u'>>> {1:5} {0}'.format(result.url, i))
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
