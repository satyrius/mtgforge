import re
from optparse import make_option

from django.conf import settings
import xact

from contrib.utils import translation_aware
from oracle.management.base import BaseCommand
from oracle.models import (
    CardSet, CardFace, Card, DataSource, CardRelease, Artist, CardL10n
)
from oracle.providers import GathererProvider


pt_separator_re = re.compile(u'\s*/\s*')


class Command(BaseCommand):
    args = '<card_set_acronym_1 card_set_acronym_2 ...>'
    option_list = BaseCommand.option_list + (
        make_option('-s', '--no-update',
            action='store_true',
            dest='no_update',
            default=False,
            help='Do not update existing card faces'),
        )
    verbose = False
    no_update = False

    def __init__(self):
        super(Command, self).__init__()
        self.provider = GathererProvider()

    @translation_aware
    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.verbosity = int(options['verbosity'])
        self.verbose = self.verbosity > 1
        self.no_update = options['no_update']

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
                self.writeln(u'{0:>20}: {1}'.format(level, unicode(item)))

    def fetch_cards(self, cs):
        cards_found = 0
        gatherer = self.provider
        cs_page = gatherer.cards_list_url(cs)
        self.writeln(u'=== {0} === {1}'.format(cs.name, cs_page))
        for name, url, extra in gatherer.cards_list_generator(cs, full_info=True):
            cards_found += 1
            if not self.verbose:
                self.writeln(u'{2:10} {0:30} {1}'.format(unicode(name), url, extra['mvid']))
            else:
                self.writeln(u'#{0} {1}'.format(extra['mvid'], unicode(name)))
                self.writeln_dict(extra)

            if not self.dry_run:
                self.save(extra)

        if cs.cards and cards_found is not cs.cards:
            self.notice(u'"{0}" should contain {1} cards, {2} found'.format(
                cs.name, cs.cards, cards_found))

    @xact.xact
    def save(self, card_details):
        '''Save or update card details'''
        oracle = card_details['oracle']

        #
        # Get or create the Card instance
        #
        card = None
        try:
            face = CardFace.objects.get(name=oracle['name'])
            if self.no_update:
                return
            card = face.card
        except CardFace.DoesNotExist:
            if 'other_faces' in oracle:
                faces = CardFace.objects.filter(name__in=oracle['other_faces'])
                if faces:
                    card = faces[0].card
            if not card:
                card = Card.objects.create()
            face = CardFace(card=card)

        #
        # Oracle rules data
        #
        face.mana_cost = 'mana' in oracle and oracle['mana'] or None
        face.cmc = 'cmc' in oracle and int(oracle['cmc']) or None
        face.name = oracle['name']
        face.type_line = oracle['type']
        # TODO Parse types and join them
        face.rules = 'text' in oracle and oracle['text'] or None
        face.flavor = 'flavor' in oracle and oracle['flavor'] or None
        # TODO Add color identyty
        face.power, face.thoughtness, face.loyality = None, None, None
        if 'pt' in oracle:
            pt = pt_separator_re.split(oracle['pt'], 2)
            if len(pt) == 2:
                # Power and Thoughtness for creatures
                face.power, face.thoughtness = p, t = pt
                face.fixed_power = (p is not None and p.isdigit() and [int(p)] or [None])[0]
                face.fixed_thoughtness = (t is not None and t.isdigit() and [int(t)] or [None])[0]
            else:
                face.loyality = int(pt[0])

        face.save()

        #
        # Card release notes
        #
        cs = CardSet.objects.get(name=oracle['set'])
        artist = Artist.objects.get_or_create(name=oracle['artist'])[0]
        try:
            release = CardRelease.objects.get(card_set=cs, card=card)
        except CardRelease.DoesNotExist:
            release = CardRelease(card_set=cs, card=card)
        release.artist = artist
        release.rarity = oracle['rarity'].lower()[0]
        release.card_number = oracle['number']
        release.save()

        #
        # Localization details
        #
        lang = settings.MODELTRANSLATION_DEFAULT_LANGUAGE
        data = dict(card_face=face, card_release=release, language=lang)
        try:
            l10n = CardL10n.objects.get(**data)
        except CardL10n.DoesNotExist:
            l10n = CardL10n(**data)
        l10n.name = card_details['name']
        l10n.type_line = card_details['type']
        l10n.rules = 'text' in card_details and card_details['text'] or None
        l10n.flavor = 'flavor' in card_details and card_details['flavor'] or None
        l10n.scan = card_details['art']
        l10n.save()

        #
        # Remember the source
        #
        ds_provider = self.provider
        try:
            source_data = dict(
                data_provider=ds_provider.data_provider, url=oracle['url'])
            l10n.sources.get(**source_data)
        except DataSource.DoesNotExist:
            l10n.sources.create(content_object=l10n, **source_data)
