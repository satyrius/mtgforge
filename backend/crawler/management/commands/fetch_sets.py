import datetime
import re
from optparse import make_option

from django.core.management.base import CommandError

from contrib.utils import translation_aware
from crawler.management.base import BaseCommand
from crawler.pages.gatherer import GathererHomePage
from crawler.pages.wizards import WizardsHomePage
from oracle.forms import CardSetForm
from oracle.models import CardSet, DataSource


acronym_re = re.compile('[a-z0-9]+$')

# Ignore products which was printed without new expansion sybmol
ignore_products = [
    'World Champ Decks',
    'Premium Foil Booster',
    'Momir Vig Basic',
    'Legacy',
    'Deck Builder\'s Toolkit',
    'Vanguard',
    'Promo set for Gatherer',  # This name is from Gatherer's list
]
ignore_products_re = re.compile('|'.join(ignore_products))


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-c', '--clear-cache',
            dest='clear',
            action='store_true',
            default=False,
            help='Invalidate pages cache'),
    )

    _acronyms = {}

    def is_unique_acronym(self, acronym, print_notice=True):
        if acronym not in self._acronyms:
            return True
        self.error(u'Acronym "{0}" already for "{1}"'.format(acronym, self._acronyms[acronym]))
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
            acronym += w[1:letters_remain + 1]
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

        self._acronyms = {}
        ignored_filter = lambda p: p and not ignore_products_re.match(isinstance(p, basestring) and p or p[0])

        wizards = WizardsHomePage()
        gatherer = GathererHomePage()
        if options['clear']:
            for page in (wizards, gatherer):
                page.delete_cache()
        gatherer_products = filter(ignored_filter, gatherer.products_list())

        # Wizards
        for name, url, extra in wizards.products_list_generator():
            if not ignored_filter(name):
                continue
            # Gatherer
            g_product = self.find_in_list(name, gatherer_products)
            if not g_product:
                self.error(u'Skip "{0}", because it is not present in Gatherer\'s list'.format(name))
                continue
            gatherer_products.remove(g_product)

            # Magiccards product and acronym
            acronym = self.generate_acronym(name)
            acronym = self.check_acronym(acronym, name, skip_on_fail=dry_run)

            # Get or create CardSet
            try:
                cs = CardSet.objects.get(name=name)
            except CardSet.DoesNotExist:
                try:
                    cs = CardSet.objects.get(acronym=acronym)
                except CardSet.DoesNotExist:
                    cs = None

            # Save new object or update existing
            if not dry_run:
                data = dict(name=name, acronym=acronym)

                if not cs or not cs.cards:
                    data['cards'] = extra['cards'] or None
                elif cs and cs.cards:
                    data['cards'] = cs.cards

                if not cs or not cs.released_at:
                    # Use first of given month, because particular day of
                    # month is not provided
                    data['released_at'] = datetime.datetime.strptime('1 ' + extra['release'], '%d %B %Y')
                elif cs or cs.released_at:
                    data['released_at'] = cs.released_at

                form = CardSetForm(data, instance=cs)
                if not form.is_valid():
                    raise Exception(form.errors.as_text())
                cs = form.save()
                for page, ds_url in (
                        (wizards, url),
                        (gatherer, g_product[1])):
                    if not ds_url:
                        continue
                    p = page.get_provider()
                    try:
                        cs.sources.get(provider=p)
                    except DataSource.DoesNotExist:
                        cs.sources.create(content_object=cs, provider=p, url=ds_url)

            info = dict(name=name, url=url, acronym=acronym or '-',
                        cards=extra['cards'] or '?', release=extra['release'])
            self.writeln(u'{name:<40} {acronym:<6} {cards:<4} {release:<14} {url}'.format(**info))

        if gatherer_products:
            self.error(
                u'Following Gatherer\'s names was not found in products list: {0}'.format(
                    u', '.join([p[0] for p in gatherer_products])))
