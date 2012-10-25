from .fetch_gatherer import Command as FetchCardsCommand
from django.contrib.contenttypes.models import ContentType
from oracle.providers.gatherer import GathererPage, GathererCard
from oracle.models import DataSource


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
        page.languages_page().get_content()
        return en_page

    def pages_generator(self):
        i = 0
        for cs in self.sets:
            for en_page in self.process_pages(map(
                get_release_page,
                cs.cardrelease_set.all().order_by('card_number')
            ), i, run=self.fetch_page):
                yield en_page


def get_release_page(card_release):
    provider = GathererPage().get_provider()
    release_type = ContentType.objects.get_for_model(card_release)
    source = DataSource.objects.get(content_type__pk=release_type.pk,
                                        object_id=card_release.id,
                                        data_provider=provider)
    return GathererCard(source.url)

def save_l10n(card_data):
    pass
