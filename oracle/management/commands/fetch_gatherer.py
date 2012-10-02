import itertools
import logging
import re
from optparse import make_option

import gevent
import xact
from django.conf import settings
from django.core.cache import get_cache
from django.core.exceptions import ValidationError
from gevent import monkey

from contrib.utils import measureit
from oracle.forms import CardFaceForm
from oracle.management.base import BaseCommand
from oracle.models import CardSet, CardFace, Card, CardRelease
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
        )

    def __init__(self):
        super(Command, self).__init__()
        self.no_update = False

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
            for card_page in self.process_pages(cards, i, print_url=print_url):
                if save:
                    card_face = self.save_card_face(
                        card_page.details(), cs_page.card_set)
                    if total:
                        self.writeln(u'[*] {1:5}/{2} {0}'.format(card_face.name, i, total))
                    else:
                        self.writeln(u'[*] {1:5} {0}'.format(card_face.name, i))
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

    @xact.xact
    def save_card_face(self, card_details, card_set):
        #
        # Get or create the Card instance
        #
        card = None
        face = None
        try:
            face = CardFace.objects.get(name=card_details['name'])
            if self.no_update:
                return face
            card = face.card
        except CardFace.DoesNotExist:
            pass
        finally:
            if 'other_faces' in card_details:
                for f in CardFace.objects.filter(name__in=card_details['other_faces']):
                    if not card:
                        card = f.card
                        break
                    if card.id != f.card_id:
                        # Delete duplicate and link with right card
                        f.card.delete()
                        f.card = card
                        f.save()
            if not card:
                card = Card.objects.create()
            if not face:
                face = CardFace(card=card)

        form = CardFaceForm(card_details, instance=face)
        if not form.is_valid():
            raise ValidationError(form.errors)
        face = form.save()

        #
        # Card release notes
        #
        try:
            release = CardRelease.objects.get(card_set=card_set, card=card)
        except CardRelease.DoesNotExist:
            release = CardRelease(card_set=card_set, card=card)
        release.rarity = card_details['rarity'].lower()[0]
        m = re.match(r'(\d+)\w?', card_details['number'])
        if not m:
            raise Exception('Collector\'s number is undefined')
        release.card_number = m.group(1)
        release.save()

        return face
