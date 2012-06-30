import itertools
import logging
import gevent
from optparse import make_option
from contrib.utils import measureit
from oracle.models import CardSet
from oracle.management.base import BaseCommand
from oracle.providers.gatherer import GathererCardList


logger = logging.getLogger(__name__)

from gevent import monkey
monkey.patch_all(thread=False, select=False)


class Command(BaseCommand):
    args = '<card_set_1 card_set_2 ...>'
    help = ('Fetched pages from Gatherer and save then to the store. This '
            'data will bu used to fill cards database.self')

    option_list = BaseCommand.option_list + (
        make_option('-t', '--threads',
            dest='threads',
            default=30,
            help='Number of threads will be spawn to download content'),
        )

    def handle(self, *args, **options):
        self.threads_count = int(options['threads'])
        sets = CardSet.objects.all()
        if args:
            sets = sets.filter(acronym__in=args)

        self.process_sets(sets)

    @measureit(logger=logger)
    def process_sets(self, sets):
        chunk = self.threads_count
        for sets_chunk in itertools.izip_longest(*([iter(sets)] * chunk)):
            self.process_chunk(sets_chunk)

    @measureit(logger=logger)
    def process_chunk(self, sets):
        jobs = [gevent.spawn(self.fetch_set_page, cs) \
                for cs in filter(None, sets)]
        gevent.joinall(jobs, timeout=60)
        for job in jobs:
            if not job.value:
                raise Exception(u'Cannot download content for "{0}"'.format(
                    job.args[0]))

    def fetch_set_page(self, cs):
        page = GathererCardList(cs)
        # Call this method for http request
        content = page.get_content()
        if not content:
            raise Exception('Cannot get content for "{0}" from {1}'.format(
                cs.name, page.url))
        self.writeln(u'{0} >>> {1}'.format(cs.name, page.url))
        return page
