from contrib.utils import translation_aware
from oracle.management.base import BaseCommand
from oracle.models import CardSet
from oracle.providers import GathererProvider


class Command(BaseCommand):
    args = '<card_set_acronym_1 card_set_acronym_2 ...>'

    @translation_aware
    def handle(self, *args, **options):
        sets = not args and CardSet.objects.all() or \
            CardSet.objects.filter(acronym__in=args)
        for cs in sets:
            self.fetch_cards(cs)

    def fetch_cards(self, cs):
        cards_found = 0
        gatherer = GathererProvider()
        cs_page = gatherer.cards_list_url(cs)
        self.writeln(u'=== {0} === {1}'.format(cs.name, cs_page))
        for name, url, extra in gatherer.cards_list_generator(cs):
            cards_found += 1
            self.writeln(u'{0:30} {1}'.format(unicode(name), url))
        if cs.cards and cards_found is not cs.cards and \
                cs.cards - cards_found != 15: # Every set has 4 different basic land card
            self.notice(u'"{0}" should contain {1} cards, {2} found'.format(
                cs.name, cs.cards, cards_found))

