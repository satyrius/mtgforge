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

    @measureit(logger=logger)
    def handle(self, *args, **options):
        self.threads_count = int(options['threads'])
        sets = CardSet.objects.all()
        if args:
            sets = sets.filter(acronym__in=args)

        self.process_sets(sets)

    def process_sets(self, sets):
        chunk = self.threads_count
        failed = []
        for sets_chunk in itertools.izip_longest(*([iter(sets)] * chunk)):
            for result in self.process_chunk(sets_chunk):
                if isinstance(result, GathererCardList):
                    self.writeln(u'>>> {0}'.format(result.url))
                else:
                    failed_cs = result.args[0]
                    self.notice(
                        u'Cannot download page "{0}", try again later'.format(
                            failed_cs))
                    failed.append(failed_cs)
        # Try again for failed downloads
        if failed:
            self.process_sets(failed)

    def process_chunk(self, sets):
        jobs = [gevent.spawn(self.fetch_set_page, cs) \
                for cs in filter(None, sets)]
        gevent.joinall(jobs, timeout=10)
        for job in jobs:
            # Return fetched page or job to try again
            yield job.successful() and job.value or job

    def fetch_set_page(self, cs):
        page = GathererCardList(cs)
        # Call this method for http request
        page.get_content()
        return page
