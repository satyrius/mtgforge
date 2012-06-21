from contrib.utils import translation_aware
from oracle.management.base import BaseCommand
from oracle.models import CardSet
from oracle.providers import GathererProvider


class Command(BaseCommand):
    args = '<card_set_acronym_1 card_set_acronym_2 ...>'
    verbose = False

    @translation_aware
    def handle(self, *args, **options):
        self.verbosity = int(options['verbosity'])
        self.verbose = self.verbosity > 1
        sets = not args and CardSet.objects.all() or \
            CardSet.objects.filter(acronym__in=args)
        for cs in sets:
            self.fetch_cards(cs)

    def writeln_dict(self, d, prev_level=None):
        for k in sorted(d.keys()):
            level = prev_level and '{}.{}'.format(prev_level, k) or k
            item = d[k]
            if isinstance(item, dict):
                if self.verbosity <= 2:
                    continue
                self.writeln_dict(item, level)
            else:
                self.writeln(u'{0:>22}: {1}'.format(level, unicode(item)))

    def fetch_cards(self, cs):
        cards_found = 0
        gatherer = GathererProvider()
        cs_page = gatherer.cards_list_url(cs)
        self.writeln(u'=== {0} === {1}'.format(cs.name, cs_page))
        for name, url, extra in gatherer.cards_list_generator(cs, full_info=True):
            cards_found += 1
            if not self.verbose:
                self.writeln(u'{2:10} {0:30} {1}'.format(unicode(name), url, extra['mvid']))
            else:
                self.writeln(u'#{0} {1}'.format(extra['mvid'], unicode(name)))
                self.writeln_dict(extra)

        if cs.cards and cards_found is not cs.cards:
            self.notice(u'"{0}" should contain {1} cards, {2} found'.format(
                cs.name, cs.cards, cards_found))

