# -*- coding: utf-8 -*-
import urllib
from mock import patch

from crawler.models import DataSource, DataProviderPage
from crawler.providers.base import Gatherer
from crawler.providers.common import Page
from crawler.providers.gatherer import (
    GathererPage, GathererHomePage, GathererCardList, GathererCard,
    GathererCardLanguages, normalized_text
)
from crawler.tests.helpers import get_html_fixture
from crawler.tests.providers.base import ProviderTest
from oracle.models import CardSet


class GathererWizardsComParsingTest(ProviderTest):
    fixtures = ['card_set']
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
        DataSource.objects.create(content_object=cs, url=url, provider=gatherer)

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
            provider=Gatherer().name)
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

    @patch.object(Page, '_dowload_content')
    def test_cache(self, _dowload_content):
        page_content = get_html_fixture('gatherer_list')
        _dowload_content.return_value = page_content
        self.assertEqual(_dowload_content.call_count, 0)

        # Create a page, get its content, and assert http request called
        page1 = GathererCardList(self.zen_url)
        # Access doc property to trigger lxml parser
        page1.doc
        self.assertEqual(page1.get_content(), page_content)
        self.assertEqual(_dowload_content.call_count, 1)
        cache_entry = DataProviderPage.objects.get(url=page1.url)
        self.assertEqual(cache_entry.provider, page1.get_provider())

        # Create the page again with the same url and test cache hit. Second
        # instance is to exclude in-memory cache hit.
        page2 = GathererCardList(self.zen_url)
        page2.doc
        self.assertEqual(page2.get_content(), page_content)
        self.assertEqual(_dowload_content.call_count, 1)

        self.assertTrue(page1.url.startswith(self.zen_url))
        _dowload_content.assert_called_once_with(page1.url)

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
            ('Adventuring Gear', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178135'),
            (u'\xc6ther Figment', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170993'),
            ('Akoum Refuge', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189638'),
            ('Archive Trap', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197538'),
            ('Archmage Ascension', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197893'),
            ('Arid Mesa', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177584'),
            ('Armament Master', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190420'),
            ('Arrow Volley Trap', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193404'),
            ('Bala Ged Thief', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197402'),
            ('Baloth Cage Trap', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197531'),
            ('Baloth Woodcrasher', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192231'),
            ('Beast Hunt', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185703'),
            ('Beastmaster Ascension', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197890'),
            ('Blade of the Bloodchief', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193397'),
            ('Bladetusk Boar', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180350'),
            ('Blazing Torch', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191372'),
            ('Blood Seeker', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180362'),
            ('Blood Tribute', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170995'),
            ('Bloodchief Ascension', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197892'),
            ('Bloodghast', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192230'),
            ('Bog Tatters', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177500'),
            ('Bold Defense', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180509'),
            ('Brave the Elements', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185734'),
            ('Burst Lightning', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177558'),
            ('Caller of Gales', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=183417'),
            ('Cancel', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189001'),
            ('Caravan Hurda', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185697'),
            ('Carnage Altar', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193406'),
            ('Celestial Mantle', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=198524'),
            ('Chandra Ablaze', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195402'),
            ('Cliff Threader', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177546'),
            ('Cobra Trap', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197535'),
            ("Conqueror's Pledge", 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195626'),
            ("Cosi's Trickster", 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=186322'),
            ('Crypt of Agadeem', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190394'),
            ('Crypt Ripper', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178121'),
            ('Day of Judgment', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=186309'),
            ('Demolish', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190406'),
            ('Desecrated Earth', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178137'),
            ('Devout Lightcaster', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191374'),
            ('Disfigure', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180115'),
            ('Eldrazi Monument', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193398'),
            ('Electropotence', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191373'),
            ('Elemental Appeal', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192221'),
            ('Emeria Angel', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190399'),
            ('Emeria, the Sky Ruin', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190414'),
            ('Eternity Vessel', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189006'),
            ('Expedition Map', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193405'),
            ("Explorer's Scope", 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190396'),
            ('Feast of Blood', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189629'),
            ('Felidar Sovereign', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185743'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201959'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195158'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201962'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195192'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201960'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195177'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201961'),
            ('Forest', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195183'),
            ('Frontier Guide', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180361'),
            ('Gatekeeper of Malakir', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185698'),
            ('Geyser Glider', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197887'),
            ('Giant Scorpion', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192226'),
            ('Gigantiform', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195627'),
            ('Goblin Bushwhacker', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177501'),
            ('Goblin Guide', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170987'),
            ('Goblin Ruinblaster', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180411'),
            ('Goblin Shortcutter', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180473'),
            ('Goblin War Paint', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185701'),
            ('Gomazoa', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=198523'),
            ('Grappling Hook', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192220'),
            ('Graypelt Refuge', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189631'),
            ('Grazing Gladehart', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189621'),
            ('Greenweaver Druid', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185694'),
            ('Grim Discovery', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180127'),
            ('Guul Draz Specter', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=183418'),
            ('Guul Draz Vampire', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180498'),
            ('Hagra Crocodile', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170998'),
            ('Hagra Diabolist', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197404'),
            ('Halo Hunter', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185752'),
            ('Harrow', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180408'),
            ('Heartstabber Mosquito', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191361'),
            ('Hedron Crab', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180348'),
            ('Hedron Scrabbler', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=193394'),
            ('Hellfire Mongrel', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192215'),
            ('Hellkite Charger', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185727'),
            ('Hideous End', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180435'),
            ('Highland Berserker', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180467'),
            ('Inferno Trap', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=197530'),
            ('Into the Roil', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178151'),
            ('Iona, Shield of Emeria', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190407'),
            ('Ior Ruin Expedition', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185711'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201966'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195187'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201964'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195165'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201963'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195161'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=201965'),
            ('Island', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=195170'),
            ('Joraga Bard', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=192227'),
            ('Journey to Nowhere', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177505'),
            ('Jwar Isle Refuge', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189627'),
            ('Kabira Crossroads', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=169963'),
            ('Kabira Evangel', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180347'),
            ('Kalitas, Bloodchief of Ghet', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=185704'),
            ('Kazandu Blademaster', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=191356'),
            ('Kazandu Refuge', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189635'),
            ('Kazuul Warlord', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=190408'),
            ('Khalni Gem', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=198519'),
            ('Khalni Heart Expedition', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=186320'),
            ('Kor Aeronaut', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177530'),
            ('Kor Cartographer', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=170991'),
            ('Kor Duelist', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=177542'),
        ])

    @patch.object(Page, 'get_content')
    def test_languages_page(self, get_content):
        get_content.return_value = get_html_fixture('gatherer_glimpse_languages')
        url = 'http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=75241'
        page = GathererCardLanguages(url)
        self.assertEqual([(p.language, p.url) for p in page.languages()], [
            ('de', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=85862&printed=true'),
            ('fr', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=85555&printed=true'),
            ('it', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=86169&printed=true'),
            ('jp', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=86476&printed=true'),
            ('cn', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=85248&printed=true'),
            ('pt', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=86783&printed=true'),
            ('es', 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=87090&printed=true'),
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
        self.assertEqual(normalized_text(
            '3{1/2} / 3{1/2}'),
            '3{1/2} / 3{1/2}'
        )
