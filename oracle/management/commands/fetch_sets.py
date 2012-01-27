from django.core.management.base import BaseCommand, CommandError, smart_str
from contrib.utils import translation_aware, cache
from BeautifulSoup import BeautifulSoup
from contrib.soupselect import select
from urllib2 import urlopen, HTTPError
from django.utils.translation import get_language
from oracle.models import CardSet
import re

GATHERER_INDEX_PAGE = 'http://gatherer.wizards.com/Pages/Default.aspx'
MAGICARDS_SITEMAP_PAGE = 'http://magiccards.info/sitemap.html'

acronym_pattern = '[a-z0-9]+'

class Command(BaseCommand):
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

    @cache
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
                u'Cannot find card set select box #{0} on Gatherer\'s index page {1}'.format(
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
        self.notice('Acronym {0} already for "{1}"'.format(acronym, self._acronyms[acronym]))
        return False

    def acronym(self, name):
        """Returns acronym for given name. First it tries to get it from
        magiccards.info sitemap (because they are pretty), but it asks user
        input it not found"""
        soup = self.soup(MAGICARDS_SITEMAP_PAGE)

        acronym_re = re.compile(r'/(?P<acronym>{0})/{1}\.html$'.format(
            acronym_pattern, get_language()
        ))
        match_en_acronym = lambda el: el.parent.name == 'a' and acronym_re.search(el.parent.get('href'))

        links = soup.findAll(text=re.compile(r'^{0}$'.format(name), re.IGNORECASE))
        links = filter(match_en_acronym, links)
        acronym = None
        if links:
            acronym = match_en_acronym(links[0]).group('acronym')
            if not self.is_unique_acronym(acronym):
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
        self._acronyms = {}
        sets = []
        for name in self.names():
            cs = CardSet(name=name)
            cs.acronym = self.acronym(name)
            sets.append(cs)
            self.writeln(cs)
