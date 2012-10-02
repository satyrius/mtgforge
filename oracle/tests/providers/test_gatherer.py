# -*- coding: utf-8 -*-

import urllib
from StringIO import StringIO

from mock import patch, call

from oracle.models import DataSource, CardSet, DataProviderPage
from oracle.providers import Page
from oracle.providers.gatherer import (
    GathererPage, GathererHomePage, GathererCardList, GathererCard,
    GathererCardPrint, GathererCardLanguages, normalized_text
)
from oracle.tests.helpers import get_html_fixture
from oracle.tests.providers.base import ProviderTest


class GathererWizardsComParsingTest(ProviderTest):
    fixtures = ProviderTest.fixtures + ['card_set']
    zen_url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Zendikar%22%5D'

    @patch.object(GathererHomePage, 'get_content')
    def test_gatherer_list(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_products')
        p = GathererHomePage()
        products = p.products_list()
        self.assertEqual(products, [
            ('Alara Reborn', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Alara+Reborn%22%5D', None),
            ('Alliances', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Alliances%22%5D', None),
            ('Antiquities', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Antiquities%22%5D', None),
            ('Apocalypse', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Apocalypse%22%5D', None),
            ('Arabian Nights', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Arabian+Nights%22%5D', None),
            ('Archenemy', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Archenemy%22%5D', None),
            ('Avacyn Restored', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Avacyn+Restored%22%5D', None),
            ('Battle Royale Box Set', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Battle+Royale+Box+Set%22%5D', None),
            ('Beatdown Box Set', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Beatdown+Box+Set%22%5D', None),
            ('Betrayers of Kamigawa', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Betrayers+of+Kamigawa%22%5D', None),
            ('Champions of Kamigawa', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Champions+of+Kamigawa%22%5D', None),
            ('Chronicles', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Chronicles%22%5D', None),
            ('Classic Sixth Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Classic+Sixth+Edition%22%5D', None),
            ('Coldsnap', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Coldsnap%22%5D', None),
            ('Conflux', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Conflux%22%5D', None),
            ('Dark Ascension', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Dark+Ascension%22%5D', None),
            ('Darksteel', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Darksteel%22%5D', None),
            ('Dissension', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Dissension%22%5D', None),
            ('Duel Decks: Ajani vs. Nicol Bolas', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Ajani+vs.+Nicol+Bolas%22%5D', None),
            ('Duel Decks: Divine vs. Demonic', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Divine+vs.+Demonic%22%5D', None),
            ('Duel Decks: Elspeth vs. Tezzeret', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Elspeth+vs.+Tezzeret%22%5D', None),
            ('Duel Decks: Elves vs. Goblins', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Elves+vs.+Goblins%22%5D', None),
            ('Duel Decks: Garruk vs. Liliana', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Garruk+vs.+Liliana%22%5D', None),
            ('Duel Decks: Jace vs. Chandra', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Jace+vs.+Chandra%22%5D', None),
            ('Duel Decks: Knights vs. Dragons', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Knights+vs.+Dragons%22%5D', None),
            ('Duel Decks: Phyrexia vs. the Coalition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Phyrexia+vs.+the+Coalition%22%5D', None),
            ('Duel Decks: Venser vs. Koth', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Duel+Decks%3A+Venser+vs.+Koth%22%5D', None),
            ('Eighth Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Eighth+Edition%22%5D', None),
            ('Eventide', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Eventide%22%5D', None),
            ('Exodus', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Exodus%22%5D', None),
            ('Fallen Empires', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Fallen+Empires%22%5D', None),
            ('Fifth Dawn', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Fifth+Dawn%22%5D', None),
            ('Fifth Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Fifth+Edition%22%5D', None),
            ('Fourth Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Fourth+Edition%22%5D', None),
            ('From the Vault: Dragons', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22From+the+Vault%3A+Dragons%22%5D', None),
            ('From the Vault: Exiled', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22From+the+Vault%3A+Exiled%22%5D', None),
            ('From the Vault: Legends', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22From+the+Vault%3A+Legends%22%5D', None),
            ('From the Vault: Relics', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22From+the+Vault%3A+Relics%22%5D', None),
            ('Future Sight', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Future+Sight%22%5D', None),
            ('Guildpact', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Guildpact%22%5D', None),
            ('Homelands', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Homelands%22%5D', None),
            ('Ice Age', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Ice+Age%22%5D', None),
            ('Innistrad', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Innistrad%22%5D', None),
            ('Invasion', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Invasion%22%5D', None),
            ('Judgment', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Judgment%22%5D', None),
            ('Legends', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Legends%22%5D', None),
            ('Legions', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Legions%22%5D', None),
            ('Limited Edition Alpha', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Limited+Edition+Alpha%22%5D', None),
            ('Limited Edition Beta', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Limited+Edition+Beta%22%5D', None),
            ('Lorwyn', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Lorwyn%22%5D', None),
            ('Magic 2010', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Magic+2010%22%5D', None),
            ('Magic 2011', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Magic+2011%22%5D', None),
            ('Magic 2012', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Magic+2012%22%5D', None),
            ('Magic 2013', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Magic+2013%22%5D', None),
            ('Magic: The Gathering-Commander', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Magic%3A+The+Gathering-Commander%22%5D', None),
            ('Masters Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Masters+Edition%22%5D', None),
            ('Masters Edition II', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Masters+Edition+II%22%5D', None),
            ('Masters Edition III', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Masters+Edition+III%22%5D', None),
            ('Masters Edition IV', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Masters+Edition+IV%22%5D', None),
            ('Mercadian Masques', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Mercadian+Masques%22%5D', None),
            ('Mirage', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Mirage%22%5D', None),
            ('Mirrodin', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Mirrodin%22%5D', None),
            ('Mirrodin Besieged', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Mirrodin+Besieged%22%5D', None),
            ('Morningtide', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Morningtide%22%5D', None),
            ('Nemesis', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Nemesis%22%5D', None),
            ('New Phyrexia', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22New+Phyrexia%22%5D', None),
            ('Ninth Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Ninth+Edition%22%5D', None),
            ('Odyssey', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Odyssey%22%5D', None),
            ('Onslaught', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Onslaught%22%5D', None),
            ('Planar Chaos', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Planar+Chaos%22%5D', None),
            ('Planechase', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Planechase%22%5D', None),
            ('Planechase 2012 Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Planechase+2012+Edition%22%5D', None),
            ('Planeshift', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Planeshift%22%5D', None),
            ('Portal', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Portal%22%5D', None),
            ('Portal Second Age', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Portal+Second+Age%22%5D', None),
            ('Portal Three Kingdoms', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Portal+Three+Kingdoms%22%5D', None),
            ('Premium Deck Series: Fire and Lightning', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Premium+Deck+Series%3A+Fire+and+Lightning%22%5D', None),
            ('Premium Deck Series: Graveborn', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Premium+Deck+Series%3A+Graveborn%22%5D', None),
            ('Premium Deck Series: Slivers', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Premium+Deck+Series%3A+Slivers%22%5D', None),
            ('Promo set for Gatherer', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Promo+set+for+Gatherer%22%5D', None),
            ('Prophecy', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Prophecy%22%5D', None),
            ('Ravnica: City of Guilds', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Ravnica%3A+City+of+Guilds%22%5D', None),
            ('Revised Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Revised+Edition%22%5D', None),
            ('Rise of the Eldrazi', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Rise+of+the+Eldrazi%22%5D', None),
            ('Saviors of Kamigawa', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Saviors+of+Kamigawa%22%5D', None),
            ('Scars of Mirrodin', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Scars+of+Mirrodin%22%5D', None),
            ('Scourge', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Scourge%22%5D', None),
            ('Seventh Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Seventh+Edition%22%5D', None),
            ('Shadowmoor', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Shadowmoor%22%5D', None),
            ('Shards of Alara', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Shards+of+Alara%22%5D', None),
            ('Starter 1999', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Starter+1999%22%5D', None),
            ('Starter 2000', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Starter+2000%22%5D', None),
            ('Stronghold', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Stronghold%22%5D', None),
            ('Tempest', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Tempest%22%5D', None),
            ('Tenth Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Tenth+Edition%22%5D', None),
            ('The Dark', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22The+Dark%22%5D', None),
            ('Time Spiral', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Time+Spiral%22%5D', None),
            ('Time Spiral "Timeshifted"', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Time+Spiral+%22Timeshifted%22%22%5D', None),
            ('Torment', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Torment%22%5D', None),
            ('Unglued', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Unglued%22%5D', None),
            ('Unhinged', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Unhinged%22%5D', None),
            ('Unlimited Edition', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Unlimited+Edition%22%5D', None),
            ("Urza's Destiny", u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Urza%27s+Destiny%22%5D', None),
            ("Urza's Legacy", u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Urza%27s+Legacy%22%5D', None),
            ("Urza's Saga", u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Urza%27s+Saga%22%5D', None),
            ('Vanguard', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Vanguard%22%5D', None),
            ('Visions', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Visions%22%5D', None),
            ('Weatherlight', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Weatherlight%22%5D', None),
            ('Worldwake', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Worldwake%22%5D', None),
            ('Zendikar', u'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Zendikar%22%5D', None),
        ])

    def test_cards_list_page(self):
        cs = CardSet.objects.all()[0]
        page = GathererPage()
        gatherer = page.get_provider()
        url = page.absolute_url(urllib.quote_plus(cs.name))
        compact_url = url + '?output=compact'
        DataSource.objects.create(content_object=cs, url=url, data_provider=gatherer)

        # Create Gatherer cards list page with simple init interface
        list_page = GathererCardList(cs)
        self.assertEqual(list_page.url, compact_url)
        # Create Gatherer cards list page with page url passed
        list_page = GathererCardList(url)
        self.assertEqual(list_page.url, compact_url)

        # Test adding `output` parameter to existing query
        zen_url = self.zen_url
        compact_zen_url = zen_url + '&output=compact'
        list_page = GathererCardList(zen_url)
        self.assertEqual(list_page.url, compact_zen_url)
        # Test fixing output parameter
        zen_url += '&output=standard'
        list_page = GathererCardList(zen_url)
        self.assertEqual(list_page.url, compact_zen_url)

    def card_set_and_page(self, acronym, url):
        cs = CardSet.objects.get(acronym=acronym)
        DataSource.objects.create(
            content_object=cs,
            url=url,
            data_provider=GathererPage().get_provider())
        return cs, GathererCardList(cs)

    @patch.object(Page, 'get_content')
    def test_card_list_pagination(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_list')

        # Get Zendikar card set and create DataSource record for it, because
        # its url will be used as `url` in list page init
        zen, page = self.card_set_and_page('zen', self.zen_url)

        urls = []
        for p in page.pages():
            self.assertIsInstance(p, GathererCardList)
            self.assertEqual(p.card_set, page.card_set)
            urls.append(p.url)
        self.assertEqual(urls, [
            'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&action=advanced&set=+%5b%22Zendikar%22%5d&output=compact',
            'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=1&action=advanced&set=+%5b%22Zendikar%22%5d&output=compact',
            'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=2&action=advanced&set=+%5b%22Zendikar%22%5d&output=compact'
        ])

    @patch('urllib2.urlopen')
    def test_cache(self, urlopen):
        page_content = get_html_fixture('gatherer_list')
        urlopen.return_value = StringIO(page_content)
        self.assertEqual(urlopen.call_count, 0)

        # Create a page, get its content, and assert http request called
        page1 = GathererCardList(self.zen_url)
        # Access doc property to trigger lxml parser
        page1.doc
        self.assertEqual(page1.get_content(), page_content)
        self.assertEqual(urlopen.call_count, 1)
        cache_entry = DataProviderPage.objects.get(url=page1.url)
        self.assertEqual(cache_entry.data_provider, page1.get_provider())

        # Create the page again with the same url and test cache hit. Second
        # instance is to exclude in-memory cache hit.
        page2 = GathererCardList(self.zen_url)
        page2.doc
        self.assertEqual(page2.get_content(), page_content)
        self.assertEqual(urlopen.call_count, 1)

        self.assertTrue(page1.url.startswith(self.zen_url))
        urlopen.assert_called_once_with(page1.url)

    @patch.object(Page, 'get_content')
    def test_get_cards_urls(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_list')
        url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&action=advanced&set=+%5b%22Zendikar%22%5d&output=compact'
        zen, page = self.card_set_and_page('zen', url)
        self.assertEqual(page.url, url)
        pages = []
        for p in page.cards_list():
            self.assertIsInstance(p, GathererCard)
            pages.append((p.name, p.url))
        self.assertEqual(pages, [
            ('Adventuring Gear', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178135'),
            (u'\xc6ther Figment', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170993'),
            ('Akoum Refuge', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189638'),
            ('Archive Trap', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197538'),
            ('Archmage Ascension', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197893'),
            ('Arid Mesa', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177584'),
            ('Armament Master', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190420'),
            ('Arrow Volley Trap', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193404'),
            ('Bala Ged Thief', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197402'),
            ('Baloth Cage Trap', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197531'),
            ('Baloth Woodcrasher', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192231'),
            ('Beast Hunt', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185703'),
            ('Beastmaster Ascension', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197890'),
            ('Blade of the Bloodchief', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193397'),
            ('Bladetusk Boar', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180350'),
            ('Blazing Torch', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191372'),
            ('Blood Seeker', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180362'),
            ('Blood Tribute', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170995'),
            ('Bloodchief Ascension', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197892'),
            ('Bloodghast', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192230'),
            ('Bog Tatters', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177500'),
            ('Bold Defense', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180509'),
            ('Brave the Elements', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185734'),
            ('Burst Lightning', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177558'),
            ('Caller of Gales', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=183417'),
            ('Cancel', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189001'),
            ('Caravan Hurda', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185697'),
            ('Carnage Altar', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193406'),
            ('Celestial Mantle', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=198524'),
            ('Chandra Ablaze', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195402'),
            ('Cliff Threader', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177546'),
            ('Cobra Trap', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197535'),
            ("Conqueror's Pledge", u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195626'),
            ("Cosi's Trickster", u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=186322'),
            ('Crypt of Agadeem', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190394'),
            ('Crypt Ripper', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178121'),
            ('Day of Judgment', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=186309'),
            ('Demolish', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190406'),
            ('Desecrated Earth', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178137'),
            ('Devout Lightcaster', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191374'),
            ('Disfigure', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180115'),
            ('Eldrazi Monument', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193398'),
            ('Electropotence', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191373'),
            ('Elemental Appeal', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192221'),
            ('Emeria Angel', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190399'),
            ('Emeria, the Sky Ruin', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190414'),
            ('Eternity Vessel', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189006'),
            ('Expedition Map', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193405'),
            ("Explorer's Scope", u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190396'),
            ('Feast of Blood', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189629'),
            ('Felidar Sovereign', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185743'),
            ('Forest', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201962'),
            ('Frontier Guide', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180361'),
            ('Gatekeeper of Malakir', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185698'),
            ('Geyser Glider', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197887'),
            ('Giant Scorpion', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192226'),
            ('Gigantiform', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195627'),
            ('Goblin Bushwhacker', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177501'),
            ('Goblin Guide', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170987'),
            ('Goblin Ruinblaster', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180411'),
            ('Goblin Shortcutter', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180473'),
            ('Goblin War Paint', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185701'),
            ('Gomazoa', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=198523'),
            ('Grappling Hook', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192220'),
            ('Graypelt Refuge', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189631'),
            ('Grazing Gladehart', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189621'),
            ('Greenweaver Druid', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185694'),
            ('Grim Discovery', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180127'),
            ('Guul Draz Specter', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=183418'),
            ('Guul Draz Vampire', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180498'),
            ('Hagra Crocodile', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170998'),
            ('Hagra Diabolist', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197404'),
            ('Halo Hunter', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185752'),
            ('Harrow', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180408'),
            ('Heartstabber Mosquito', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191361'),
            ('Hedron Crab', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180348'),
            ('Hedron Scrabbler', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193394'),
            ('Hellfire Mongrel', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192215'),
            ('Hellkite Charger', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185727'),
            ('Hideous End', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180435'),
            ('Highland Berserker', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180467'),
            ('Inferno Trap', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197530'),
            ('Into the Roil', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178151'),
            ('Iona, Shield of Emeria', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190407'),
            ('Ior Ruin Expedition', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185711'),
            ('Island', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201964'),
            ('Joraga Bard', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192227'),
            ('Journey to Nowhere', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177505'),
            ('Jwar Isle Refuge', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189627'),
            ('Kabira Crossroads', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=169963'),
            ('Kabira Evangel', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180347'),
            ('Kalitas, Bloodchief of Ghet', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185704'),
            ('Kazandu Blademaster', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191356'),
            ('Kazandu Refuge', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189635'),
            ('Kazuul Warlord', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190408'),
            ('Khalni Gem', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=198519'),
            ('Khalni Heart Expedition', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=186320'),
            ('Kor Aeronaut', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177530'),
            ('Kor Cartographer', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170991'),
            ('Kor Duelist', u'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177542'),
        ])

    def assert_dict_items(self, subject, standard):
        for k, v in standard.items():
            self.assertIn(k, subject)
            self.assertEqual(subject[k], standard[k])
        for k, v in subject.items():
            self.assertIn(k, standard)

    @patch.object(Page, 'get_content')
    def test_card_oracle_details(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_angel_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961'
        name = u'Avacyn, Angel of Hope'
        page = GathererCard(url, name=name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Avacyn Restored',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=239961&type=card',
            name='Avacyn, Angel of Hope',
            pt='8 / 8',
            artist='Jason Chan',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961',
            text='Flying, vigilance\nAvacyn, Angel of Hope and other permanents you control are indestructible.',
            cmc='8',
            number='6',
            mvid='239961',
            rarity='Mythic Rare',
            mana='{5}{W}{W}{W}',
            playerRating='Rating: 4.202 / 5 (146 votes)',
            flavor='A golden helix streaked skyward from the Helvault. A thunderous explosion shattered the silver monolith and Avacyn emerged, free from her prison at last.',
            type='Legendary Creature - Angel',
        ))

        printed_page = page.printed_card_page()
        self.assertIsInstance(printed_page, GathererCardPrint)
        self.assertEqual(
            printed_page.url,
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=239961'
        )

        lang_page = page.languages_page()
        self.assertIsInstance(lang_page, GathererCardLanguages)
        self.assertEqual(
            lang_page.url,
            'http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=239961'
        )

    @patch.object(Page, 'get_content')
    def test_card_rules_with_comments(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_gear_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178135'
        name = u'Adventuring Gear'
        page = GathererCard(url, name=name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Zendikar',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=178135&type=card',
            name='Adventuring Gear',
            artist='Howard Lyon',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178135',
            text='Landfall - Whenever a land enters the battlefield under your control, equipped creature gets +2/+2 until end of turn.\nEquip {1} ({1}: Attach to target creature you control. Equip only as a sorcery.)',
            cmc='1',
            number='195',
            mvid='178135',
            rarity='Common',
            mana='{1}',
            playerRating='Rating: 3.389 / 5 (90 votes)',
            flavor='An explorer\'s essentials in a wild world.',
            type='Artifact - Equipment',
        ))

        printed_page = page.printed_card_page()
        self.assertIsInstance(printed_page, GathererCardPrint)
        self.assertEqual(
            printed_page.url,
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=178135'
        )

    @patch.object(Page, 'get_content')
    def test_double_faced_card_front(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_werewolf_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=2446835'

        front_name = u'Hanweir Watchkeep'
        page = GathererCard(url, name=front_name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Innistrad',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=244683&type=card',
            name='Hanweir Watchkeep',
            pt='1 / 5',
            artist='Wayne Reynolds',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=2446835',
            text='Defender\nAt the beginning of each upkeep, if no spells were cast last turn, transform Hanweir Watchkeep.',
            cmc='3',
            number='145a',
            mvid='2446835',
            rarity='Uncommon',
            mana='{2}{R}',
            playerRating='Rating: 3.520 / 5 (51 votes)',
            other_faces=['Bane of Hanweir'],
            flavor='He scans for wolves, knowing there\'s one he can never anticipate.',
            type='Creature - Human Warrior Werewolf',
        ))

        printed_page = page.printed_card_page()
        self.assertIsInstance(printed_page, GathererCardPrint)
        self.assertEqual(
            printed_page.url,
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=244683'
        )

    @patch.object(Page, 'get_content')
    def test_double_faced_card_back(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_werewolf_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244687'

        back_name = u'Bane of Hanweir'
        page = GathererCard(url, name=back_name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Innistrad',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=244687&type=card',
            name='Bane of Hanweir',
            pt='5 / 5',
            artist='Wayne Reynolds',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244687',
            text='Bane of Hanweir attacks each turn if able.\nAt the beginning of each upkeep, if a player cast two or more spells last turn, transform Bane of Hanweir.',
            playerRating='Rating: 3.806 / 5 (54 votes)',
            number='145b',
            mvid='244687',
            rarity='Uncommon',
            colorIndicator='Red',
            other_faces=['Hanweir Watchkeep'],
            flavor='Technically he never left his post. He looks after the wolf wherever it goes.',
            type='Creature - Werewolf',
        ))

    @patch.object(Page, 'get_content')
    def test_fliped_card_normal(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_flip_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694'

        front_name = u'Akki Lavarunner'
        page = GathererCard(url, name=front_name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Champions of Kamigawa',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=78694&type=card',
            name='Akki Lavarunner',
            pt='1 / 1',
            artist='Matt Cavotta',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694',
            text='Haste\nWhenever Akki Lavarunner deals damage to an opponent, flip it.',
            cmc='4',
            number='153a',
            mvid='78694',
            rarity='Rare',
            mana='{3}{R}',
            playerRating='Rating: 2.716 / 5 (44 votes)',
            other_faces=['Tok-Tok, Volcano Born'],
            type='Creature - Goblin Warrior',
        ))

        printed_page = page.printed_card_page()
        self.assertIsInstance(printed_page, GathererCardPrint)
        self.assertEqual(
            printed_page.url,
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=78694'
        )

    @patch.object(Page, 'get_content')
    def test_fliped_card_flip(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_flip_oracle')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694&part=Tok-Tok%2c+Volcano+Born'

        fliped_name = u'Akki Lavarunner (Tok-Tok, Volcano Born)'
        page = GathererCard(url, name=fliped_name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Champions of Kamigawa',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=78694&type=card&options=rotate180',
            name='Tok-Tok, Volcano Born',
            pt='2 / 2',
            artist='Matt Cavotta',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694&part=Tok-Tok%2c+Volcano+Born',
            text='Protection from red\nIf a red source would deal damage to a player, it deals that much damage plus 1 to that player instead.',
            cmc='4',
            number='153b',
            mvid='78694',
            rarity='Rare',
            mana='{3}{R}',
            playerRating='Rating: 2.716 / 5 (44 votes)',
            other_faces=['Akki Lavarunner'],
            type='Legendary Creature - Goblin Shaman',
        ))

    @patch('urllib2.urlopen')
    def test_splited_card(self, urlopen):
        page_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=27166'
        fire_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?part=Fire&multiverseid=27166'

        card_page = StringIO(get_html_fixture('gatherer_split_oracle'))
        fire_page = StringIO(get_html_fixture('gatherer_fire_oracle'))
        urlopen.side_effect = [card_page, fire_page]

        name = u'Fire'
        page = GathererCard(page_url, name=name)
        details = page.details()
        self.assertEqual(urlopen.call_args_list, [call(page_url), call(fire_url)])
        self.assert_dict_items(details, dict(
            set='Apocalypse',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=27166&type=card',
            name='Fire',
            artist='Franz Vohwinkel',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?part=Fire&multiverseid=27166',
            text='Fire deals 2 damage divided as you choose among one or two target creatures and/or players.',
            cmc='2',
            number='128',
            mvid='27166',
            rarity='Uncommon',
            mana='{1}{R}',
            playerRating='Rating: 4.533 / 5 (45 votes)',
            other_faces=['Ice'],
            otherSets='',
            type='Instant',
        ))

        printed_page = page.printed_card_page()
        self.assertIsInstance(printed_page, GathererCardPrint)
        self.assertEqual(
            printed_page.url,
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=27166'
        )

    @patch.object(Page, 'get_content')
    def test_land_card_details(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_forest')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326'
        name = u'Forest'
        page = GathererCard(url, name=name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Return to Ravnica',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=289326&type=card',
            name='Forest',
            artist='Yeong-Hao Han',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326',
            text='G',
            number='271',
            mvid='289326',
            rarity='Common',
            playerRating='Rating: 5.000 / 5 (3 votes)',
            otherSets='',
            type='Basic Land - Forest',
        ))

        printed_page = page.printed_card_page()
        self.assertIsInstance(printed_page, GathererCardPrint)
        self.assertEqual(
            printed_page.url,
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=289326'
        )

    @patch.object(Page, 'get_content')
    def test_vanilla_creature(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_vanilla_creature')
        url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=265383'
        name = u'Axebane Stag'
        page = GathererCard(url, name=name)
        details = page.details()
        self.assert_dict_items(details, dict(
            set='Return to Ravnica',
            art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=265383&type=card',
            name='Axebane Stag',
            pt='6 / 7',
            artist='Martina Pilcerova',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=265383',
            number='116',
            mvid='265383',
            rarity='Common',
            playerRating='Rating: 2.735 / 5 (17 votes)',
            type='Creature - Elk',
            cmc='7',
            mana='{6}{G}',
            flavor='"When the spires have burned and the cobblestones are dust, he will take his rightful place as king of the wilds."\n- Kirce, Axebane guardian',
        ))

        printed_page = page.printed_card_page()
        self.assertIsInstance(printed_page, GathererCardPrint)
        self.assertEqual(
            printed_page.url,
            'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=265383'
        )

    @patch.object(Page, 'get_content')
    def test_languages_page(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_glimpse_languages')
        url = 'http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=75241'
        page = GathererCardLanguages(url)
        self.assertEqual([(p.name, p.url) for p in page.languages()], [
            ('German', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=85862'),
            ('French', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=85555'),
            ('Italian', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=86169'),
            ('Japanese', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=86476'),
            ('Chinese Simplified', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=85248'),
            ('Portuguese', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=86783'),
            ('Spanish', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=87090'),
        ])

    def test_normalize_text(self):
        self.assertEqual(normalized_text(
            '( abc )'),
            '(abc)'
        )
        self.assertEqual(normalized_text(
            '{G} {W}'),
            '{G}{W}'
        )
        self.assertEqual(normalized_text(
            u'abc—dfg'),
            'abc - dfg'
        )
        self.assertEqual(normalized_text(
            u'abc\n—dfg'),
            'abc\n- dfg'
        )
