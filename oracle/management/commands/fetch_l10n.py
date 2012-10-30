from .fetch_gatherer import Command as FetchCardsCommand
from django.contrib.contenttypes.models import ContentType
from oracle.providers.gatherer import GathererPage, GathererCard
from oracle.models import DataSource
from django.utils.functional import curry


class Command(FetchCardsCommand):
    args = '<card_set_1 card_set_2 ...>'
    help = ('Fetched card localization pages from Gatherer and save them to '
            'the storage.')

    def handle(self, *args, **options):
        self.handle_args(*args, **options)

        for en_page in self.pages_generator():
            pass

    def fetch_page(self, page):
        en_page = page.printed_card_page()
        en_page.get_content()
        lang_page = page.languages_page()
        lang_page.get_content()
        return en_page, lang_page

    def pages_generator(self):
        for cs in self.sets:
            for en_page, lang_page in self.process_pages(map(
                curry(get_release_page, read_cache=(not self.ignore_cache)),
                cs.cardrelease_set.all().order_by('card_number')
            )):
                yield en_page, lang_page


def get_release_page(card_release, read_cache=True):
    provider = GathererPage().get_provider()
    release_type = ContentType.objects.get_for_model(card_release)
    source = DataSource.objects.get(content_type__pk=release_type.pk,
                                        object_id=card_release.id,
                                        data_provider=provider)
    return GathererCard(source.url, read_cache=read_cache)

def save_l10n(card_data):
    pass
