import re
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError, smart_str

from contrib.utils import translation_aware, cache_method_calls
from oracle.models import CardSet
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
        products_dict = dict()
        for product in products:
            pname, url, extra = product
            if pname == name:
                return product
            if pname in products_dict:
                raise CommandError(u'Product name "{0}" is not unique in the list'.format(pname))
            products_dict[pname] = product

        # Simplyfy name and try to found its occurancies
        name = re.sub(r'&', 'and', name)
        name = re.sub(r'Magic: The Gathering', '', name).strip()
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

    @cache_method_calls
    def magiccards_products(self):
        return MagiccardsProvider().products_list()

    def acronym(self, name, fetch=False, skip_on_fail=False):
        """Returns acronym for given name. If `fetch` argument passed acronyms
        will be fetched from magiccards.info sitemap (because they are pretty),
        but it asks user input it not found."""
        acronym = None

        if not fetch:
            acronym = self.generate_acronym(name)
        else:
            product = self.find_in_list(name, self.magiccards_products())
            if not product:
                self.notice('Cannot find acronym for "{0}"'.format(name))
            else:
                acronym = product[2]['acronym']

        if acronym and not self.is_unique_acronym(acronym):
            acronym = None

        while not acronym and not skip_on_fail:
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
        gatherer_products = GathererProvider().products_list()
        products = WizardsProvider().products_list_generator()
        for name, url, extra in products:
            # Process only sets fount in Gatherer's list
            g_product = self.find_in_list(name, gatherer_products)
            if not g_product:
                self.notice(u'Skip "{0}", because it is not present in Gatherer\'s list'.format(name))
                continue
            gatherer_products.remove(g_product)

            try:
                cs = CardSet.objects.get(name=name)
            except CardSet.DoesNotExist:
                cs = CardSet(name=name)
                cs.acronym = self.acronym(
                    name, fetch_acronyms,
                    # Do not prompt acronyms on dry run
                    skip_on_fail=fetch_acronyms and dry_run)
                if not dry_run:
                    cs.save()
                    self.writeln('Saved')

            info = extra
            extra.update(dict(name=name, url=url,
                              cards=extra['cards'] or '?',
                              acronym=cs.acronym or '-'))
            self.writeln(u'{name:<40} {acronym:<6} {cards:<4} {release:<14} {url}'.format(**info))

        if gatherer_products:
            self.notice(
                u'Following Gatherer\'s names was not found in products list: {0}'.format(
                    u', '.join([p[0] for p in gatherer_products])))
