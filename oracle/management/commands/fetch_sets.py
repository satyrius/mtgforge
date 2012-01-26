from django.core.management.base import BaseCommand, CommandError
from contrib.commands import translation_aware
from BeautifulSoup import BeautifulSoup
from contrib.soupselect import select
from urllib2 import urlopen

GATHERER_INDEX_PAGE = 'http://gatherer.wizards.com/Pages/Default.aspx'

class Command(BaseCommand):
    def writeln(self, message):
        self.stdout.write(message + u'\n')

    @translation_aware
    def handle(self, *args, **options):
        doc = BeautifulSoup(urlopen(GATHERER_INDEX_PAGE))
        select_id = 'ctl00_ctl00_MainContent_Content_SearchControls_setAddText'
        options = select(doc, 'select#{0} option'.format(select_id))
        if not options:
            raise CommandError(
                u'Cannot find card set select box #{0} on Gatherer\'s index page {1}'.format(
                    select_id, GATHERER_INDEX_PAGE
                )
            )
        for o in options:
            set_name = None
            for attr_name, attr_value in o.attrs:
                if attr_name == 'value':
                    set_name = attr_value
                    break
            if set_name is None:
                raise CommandError(u'Option {0} does not have value attribute'.format(o))
            if not set_name:
                continue
            self.writeln(set_name)
