import re
from optparse import make_option
from urllib2 import urlopen, HTTPError

from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError, smart_str
from django.utils.translation import get_language

from contrib.soupselect import select
from contrib.utils import translation_aware, cache_method_calls
from oracle.models import CardSet


GATHERER_INDEX_PAGE = 'http://gatherer.wizards.com/Pages/Default.aspx'
MAGICARDS_SITEMAP_PAGE = 'http://magiccards.info/sitemap.html'

acronym_pattern = '[a-z0-9]+'

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--no-acronyms',
            action='store_true',
            dest='no_acronyms',
            default=False,
            help='Do not fetch acronyms from magiccards.info, generate then instead'),
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

    def urlopen(self, url):
        try:
            f = urlopen(url)
            return f
        except HTTPError, e:
            raise CommandError(u'{0} {1} {2}'.format(url, e.code, e.msg))

    @cache_method_calls
    def soup(self, url):
        """Fetch url and return BeautifulSoup for the document"""
        return BeautifulSoup(self.urlopen(url))

    def names(self):
        """Card sets names generator which retrieves data from Gatherer's page
        """
        soup = self.soup(GATHERER_INDEX_PAGE)
        select_id = 'ctl00_ctl00_MainContent_Content_SearchControls_setAddText'
        options = select(soup, 'select#{0} option'.format(select_id))
        if not options:
            raise CommandError(
                'Cannot find card set select box #{0} on Gatherer\'s index page {1}'.format(
                    select_id, GATHERER_INDEX_PAGE
                )
            )
        for o in options:
            set_name = o.get('value')
            if set_name is None:
                raise CommandError(u'Option {0} does not have value attribute'.format(o))
            if not set_name:
                continue
            yield set_name

    def is_unique_acronym(self, acronym, print_notice=True):
        if acronym not in self._acronyms:
            return True
        self.notice(u'Acronym "{0}" already for "{1}"'.format(acronym, self._acronyms[acronym]))
        return False

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
        words = filter(None, name.split())
        letters_remain = len(words) < 3 and 3 or len(words)
        acronym = u''
        for w in words:
            w = w.strip('"\'')
            if not letters_remain:
                break
            add = w.isnumeric() and w[-2:] or w[0]
            acronym += add
            letters_remain -= len(add)
        if letters_remain:
            acronym += w[1:letters_remain+1]
        if acronym in self._acronyms:
            acronym = acronym[:-1] + w[-1]
        return acronym


    def acronym(self, name, no_fetch=False):
        """Returns acronym for given name. First it tries to get it from
        magiccards.info sitemap (because they are pretty), but it asks user
        input it not found. If `no_fetch` argiment passed generate acronym
        by name instead of fetching."""
        acronym = None

        if no_fetch:
            acronym = self.generate_acronym(name)
        else:
            soup = self.soup(MAGICARDS_SITEMAP_PAGE)

            acronym_re = re.compile(r'/(?P<acronym>{0})/{1}\.html$'.format(
                acronym_pattern, get_language()
            ))
            match_en_acronym = lambda el: el.parent.name == 'a' and acronym_re.search(el.parent.get('href'))

            links = soup.findAll(text=re.compile(r'^{0}$'.format(name), re.IGNORECASE))
            links = filter(match_en_acronym, links)
            if links:
                acronym = match_en_acronym(links[0]).group('acronym')

        if acronym and not self.is_unique_acronym(acronym):
            acronym = None

        while not acronym:
            acronym = raw_input('Enter acronym for "{0}": '.format(name)).strip()
            match_pattern = re.match(r'{0}$'.format(acronym_pattern), acronym)
            if not match_pattern or not self.is_unique_acronym(acronym):
                acronym = None

        self._acronyms[acronym] = name
        return acronym

    @translation_aware
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        self._acronyms = {}
        for name in self.names():
            try:
                cs = CardSet.objects.get(name=name)
            except CardSet.DoesNotExist:
                cs = CardSet(name=name)
                cs.acronym = self.acronym(name, options['no_acronyms'])
                if not dry_run:
                    cs.save()
            self.writeln(cs)
