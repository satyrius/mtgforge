from itertools import chain
from optparse import make_option

from django.core.exceptions import ValidationError
from django.utils.functional import curry

from crawler.management.commands.fetch_gatherer import Command as FetchCardsCommand
from crawler.providers.gatherer import GathererCard, GathererCardPrint
from oracle.forms import CardL10nForm
from oracle.models import CardL10n, Artist


class Command(FetchCardsCommand):
    args = '<card_set_1 card_set_2 ...>'
    help = ('Fetched card localization pages from Gatherer and save them to '
            'the storage.')

    option_list = FetchCardsCommand.option_list + (
        make_option(
            '--english-only',
            action='store_true',
            dest='english_only',
            default=False,
            help='Get only English cards localization'),
    )

    def __init__(self):
        super(FetchCardsCommand, self).__init__()
        self.english_only = False

    def handle(self, *args, **options):
        raise NotImplemented()

        self.handle_args(*args, **options)
        self.english_only = options['english_only']

        self.notice(u'(1) Walk though card release print and languages pages')
        message_shown = False
        self.cards_total = i = 0
        failed_pages = []
        for page in self.process_pages(chain(*self.l10n_pages_generator())):
            if not message_shown:
                message_shown = True
                self.notice(u'(2) Save localization')
            i += 1
            try:
                for saved_face_l10n in save_l10n(page):
                    self.writeln(u'[*] {2}/{3} {4} {0} from {1}'.format(
                        saved_face_l10n.name, page.url, i,
                        self.cards_total, page.language))
            except Exception, e:
                self.error(e)
                failed_pages.append(page)

        if failed_pages:
            self.error('The following card pages parsing failed:')
            for page in failed_pages:
                self.error(u'{0} from {1}'.format(page.name, page.url))

    def pages_generator(self):
        for cs in self.sets:
            for oracle_page in self.process_pages(map(
                curry(GathererCard, read_cache=(not self.ignore_cache)),
                cs.cardrelease_set.all().order_by('card_number')
            )):
                yield [oracle_page.printed_card_page(),
                       oracle_page.languages_page()]

    def l10n_pages_generator(self):
        for page in self.process_pages(chain(*self.pages_generator())):
            if isinstance(page, GathererCardPrint):
                pages = [page]
            else:
                pages = not self.english_only and page.languages() or []
            self.cards_total += len(pages)
            yield pages


def save_l10n(card_page):
    release = card_page.card_release
    for card_face in release.card.cardface_set.all():
        card_details = card_page.details(name=card_face.name)
        data = dict(
            card_face=card_face,
            card_release=release,
            language=card_page.language,
        )
        try:
            l10n = CardL10n.objects.get(**data)
        except CardL10n.DoesNotExist:
            l10n = CardL10n(**data)

        artist, _ = Artist.objects.get_or_create(name=card_details['artist'])
        card_details['artist'] = artist.id

        form = CardL10nForm(card_details, instance=l10n)
        if not form.is_valid():
            raise ValidationError(form.errors)
        yield form.save()
