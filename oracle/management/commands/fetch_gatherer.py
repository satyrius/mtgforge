import itertools
import logging
import gevent
from contrib.utils import measureit
from oracle.models import CardSet
from oracle.management.base import BaseCommand
from oracle.providers.gatherer import GathererCardList


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<card_set_1 card_set_2 ...>'
    help = ('Fetched pages from Gatherer and save then to the store. This '
            'data will bu used to fill cards database.self')

    def handle(self, *args, **options):
        sets = CardSet.objects.all()
        if args:
            sets = sets.filter(acronym__in=args)

        self.card_set_pages(sets)

    @measureit(logger=logger)
    def card_set_pages(self, sets):
        chunk = 3
        for sets_chunk in itertools.izip_longest(*([iter(sets)] * chunk)):
            jobs = [gevent.spawn(self.fetch_set_page, cs) for cs in filter(None, sets_chunk)]
            gevent.joinall(jobs, timeout=5)
            self.writeln(u'Downloaded pages: {0}'.format(
                [job.value.url for job in jobs]))

    @measureit(logger=logger)
    def fetch_set_page(self, cs):
        page = GathererCardList(cs)
        # Call this method for http request
        page.get_content()
        self.writeln(u'{0} >>> {1}'.format(cs.name, page.url))
        return page
