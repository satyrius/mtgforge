import datetime
import re
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError, smart_str

from contrib.utils import translation_aware
from oracle.models import CardSet, DataSource
from oracle.providers import WizardsProvider, GathererProvider, MagiccardsProvider


acronym_re = re.compile('[a-z0-9]+$')

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', '--fetch-acronyms',
            action='store_true',
            dest='fetch_acronyms',
            default=False,
            help='Fetch acronyms from magiccards.info'),
        make_option('-d', '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Do not save fetched data'),
        )

    _acronyms = {}

    def writeln(self, message):
        self.stdout.write(u'{0}\n'.format(message))

    def notice(self, message):
        colorized_message = self.style.NOTICE(u'Notice: {0}\n'.format(message))
        self.stderr.write(smart_str(colorized_message))

    def is_unique_acronym(self, acronym, print_notice=True):
        if acronym not in self._acronyms:
            return True
        self.notice(u'Acronym "{0}" already for "{1}"'.format(acronym, self._acronyms[acronym]))
        return False

    def find_in_list(self, name, products):
        # Convert list of tuples into dict with product names as keys. Return
        # product name immediately if it will exactly match next needle.
        name = name.lower()
        products_dict = dict()
        for product in products:
            pname, url, extra = product
            pname = pname.lower()
            if pname == name:
                return product
            if pname in products_dict:
                raise CommandError(u'Product name "{0}" is not unique in the list'.format(pname))
            products_dict[pname] = product

        # Simplyfy name and try to found its occurancies
        name = re.sub(r'&', 'and', name)
        name = re.sub(r'magic: the gathering', '', name).strip()
        endswith_re = re.compile(name + '$')
        endswith = filter(lambda n: endswith_re.search(n), products_dict.keys())
        if len(endswith) == 1:
            return products_dict[endswith[0]]
        similar = filter(lambda n: n.find(name) >= 0 or name.find(n) >= 0, products_dict.keys())
        return len(similar) == 1 and products_dict[similar[0]] or None

    def generate_acronym(self, name):
        name = name.lower()
        word2num = [
            (('one', 'first', 'i'), 1),
            (('two', 'second', 'ii'), 2),
            (('three', 'third', 'iii'), 3),
            (('four', 'fourth', 'iv'), 4),
            (('five', 'fifth', 'v'), 5),
            (('six', 'sixth', 'vi'), 6),
            (('seven', 'seventh', 'vii'), 7),
            (('eight', 'eightth', 'viii'), 8),
            (('nine', 'nineth', 'ix'), 9),
            (('ten', 'tenth', 'x'), 10),
        ]
        for strs, num in word2num:
            name = re.sub(r'(?<=\b)({0})(?<=\b)'.format('|'.join(strs)), str(num), name)
        name = re.sub(r'[:&-/]', ' ', name)
        words = filter(None, name.split())
        letters_remain = len(words) < 3 and 3 or len(words)
        acronym = u''
        for w in words:
            w = w.strip('"\'')
            if not letters_remain:
                break
            add = w.isdigit() and w[-2:] or w[0]
            acronym += add
            letters_remain -= len(add)
        if letters_remain:
            acronym += w[1:letters_remain+1]
        if acronym in self._acronyms:
            acronym = acronym[:-1] + w[-1]

        if acronym_re.match(acronym):
            return acronym
        return None

    def check_acronym(self, acronym, name, skip_on_fail=False):
        if acronym and not self.is_unique_acronym(acronym):
            acronym = None

        if not acronym and skip_on_fail:
            return None

        while not acronym:
            acronym = raw_input('Enter acronym for "{0}": '.format(name)).strip()
            match_pattern = acronym_re.match(acronym)
            if not match_pattern or not self.is_unique_acronym(acronym):
                acronym = None

        self._acronyms[acronym] = name
        return acronym

    @translation_aware
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fetch_acronyms = options['fetch_acronyms']

        self._acronyms = {}

        wizards = WizardsProvider()
        gatherer = GathererProvider()
        gatherer_products = gatherer.products_list()
        magiccards = MagiccardsProvider()
        magiccards_products = magiccards.products_list()

        # Wizards
        for name, url, extra in wizards.products_list_generator():
            # Gatherer
            g_product = self.find_in_list(name, gatherer_products)
            if not g_product:
                self.notice(u'Skip "{0}", because it is not present in Gatherer\'s list'.format(name))
                continue
            gatherer_products.remove(g_product)

            # Magiccards product and acronym
            mc_product = None
            acronym = None
            if not fetch_acronyms:
                acronym = self.generate_acronym(name)
            else:
                mc_product = self.find_in_list(name, magiccards_products)
                if not mc_product:
                    self.notice(u'Cannot find acronym for "{0}"'.format(name))
                else:
                    acronym = mc_product[2]['acronym']
            acronym = self.check_acronym(acronym, name, skip_on_fail=dry_run)

            # Get or create CardSet
            try:
                cs = CardSet.objects.get(name=name)
            except CardSet.DoesNotExist:
                try:
                    cs = CardSet.objects.get(acronym=acronym)
                except CardSet.DoesNotExist:
                    cs = CardSet(name=name, acronym=acronym)

            # Save new object or update existing
            if not dry_run:
                if not cs.cards:
                    cs.cards = extra['cards'] or None
                if not cs.released_at:
                    # Use first of given month, because particular day of
                    # month is not provided
                    cs.released_at = datetime.datetime.strptime('1 ' + extra['release'], '%d %B %Y')
                cs.save()
                for ds_provider, ds_url in ((wizards, url),
                                            (gatherer, g_product[1]),
                                            (magiccards, mc_product[1])):
                    if not ds_url:
                        continue
                    try:
                        source_data = dict(
                            data_provider=ds_provider.data_provider, url=ds_url)
                        cs.sources.get(**source_data)
                    except DataSource.DoesNotExist:
                        cs.sources.create(content_object=cs, **source_data)

            info = dict(name=name, url=url, acronym=acronym or '-',
                        cards=extra['cards'] or '?', release=extra['release'])
            self.writeln(u'{name:<40} {acronym:<6} {cards:<4} {release:<14} {url}'.format(**info))

        if gatherer_products:
            self.notice(
                u'Following Gatherer\'s names was not found in products list: {0}'.format(
                    u', '.join([p[0] for p in gatherer_products])))
