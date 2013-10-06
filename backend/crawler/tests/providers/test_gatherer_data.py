import requests
from mock import patch, call

from crawler.providers.common import Page
from crawler.providers.gatherer import GathererCard, GathererCardPrint, \
    GathererCardLanguages
from crawler.tests.helpers import get_html_fixture
from crawler.tests.providers.base import ProviderTest
from oracle.forms import CardFaceForm
from oracle.models import Card, CardFace


class GathererDataParsingTest(ProviderTest):
    def assert_dict_items(self, subject, standard):
        for k, v in standard.items():
            self.assertIn(k, subject)
            self.assertEqual(subject[k], standard[k])
        for k, v in subject.items():
            self.assertIn(k, standard)

    def assert_card_parse(self, name, url, expected_data, html_fixture=None,
                          print_url=None, lang_url=None, save=False):
        page = GathererCard(url, name=name)
        if html_fixture:
            with patch.object(Page, 'get_content') as get_content:
                get_content.return_value = get_html_fixture(html_fixture)
                details = page.details()
        else:
            # All http requests is already mocked and should return right
            # content. Mock low level calls, just to enshure that there was
            # no real http calls.
            with patch.object(requests, 'get') as get:
                get.side_effect = Exception('You should mock getting data')
                details = page.details()
        self.assert_dict_items(details, expected_data)

        if print_url:
            printed_page = page.printed_card_page()
            self.assertIsInstance(printed_page, GathererCardPrint)
            self.assertEqual(printed_page.url, print_url)

        if lang_url:
            lang_page = page.languages_page()
            self.assertIsInstance(lang_page, GathererCardLanguages)
            self.assertEqual(lang_page.url, lang_url)

        if save:
            card_name = 'title' in details or name
            faces_count = 'other_faces' in details and \
                len(details['other_faces']) + 1 or 1
            card = Card.objects.create(name=card_name, faces_count=faces_count)
            face = CardFace(card=card)
            form = CardFaceForm(details, instance=face)
            self.assertTrue(form.is_valid(), '\n' + form.errors.as_text())

            saved_face = form.save()
            self.assertIsInstance(saved_face, CardFace)
            return saved_face
        else:
            return None

    def test_card_oracle_details(self):
        self.assert_card_parse(
            name=u'Avacyn, Angel of Hope',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961',
            print_url='http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=239961',
            lang_url='http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=239961',
            html_fixture='gatherer_angel_oracle',
            expected_data=dict(
                set='Avacyn Restored',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=239961&type=card',
                name='Avacyn, Angel of Hope',
                title='Avacyn, Angel of Hope',
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

    def test_card_rules_with_comments(self):
        self.assert_card_parse(
            name=u'Adventuring Gear',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178135',
            print_url='http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=178135',
            html_fixture='gatherer_gear_oracle',
            expected_data=dict(
                set='Zendikar',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=178135&type=card',
                name='Adventuring Gear',
                title='Adventuring Gear',
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

    def test_double_faced_card_front(self):
        face = self.assert_card_parse(
            name=u'Hanweir Watchkeep',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=2446835',
            print_url='http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=244683',
            html_fixture='gatherer_werewolf_oracle',
            expected_data=dict(
                set='Innistrad',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=244683&type=card',
                name='Hanweir Watchkeep',
                title='Hanweir Watchkeep',
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
            ),
            save=True)
        # It should be 'front' face type
        self.assertEqual(face.card.faces_count, 2)
        self.assertEqual(face.place, CardFace.FRONT)

    def test_double_faced_card_back(self):
        face = self.assert_card_parse(
            name=u'Bane of Hanweir',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244687',
            html_fixture='gatherer_werewolf_oracle',
            expected_data=dict(
                set='Innistrad',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=244687&type=card',
                name='Bane of Hanweir',
                title='Hanweir Watchkeep',
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
            ),
            save=True)
        # It should be 'back' face type
        self.assertEqual(face.card.faces_count, 2)
        self.assertEqual(face.place, CardFace.BACK)

    def test_fliped_card_normal(self):
        face = self.assert_card_parse(
            name=u'Akki Lavarunner',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694',
            print_url='http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=78694',
            html_fixture='gatherer_flip_oracle',
            expected_data=dict(
                set='Champions of Kamigawa',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=78694&type=card',
                name='Akki Lavarunner',
                title='Akki Lavarunner',
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
            ),
            save=True)
        # It should be 'front' face type
        self.assertEqual(face.card.faces_count, 2)
        self.assertEqual(face.place, CardFace.FRONT)

    def test_fliped_card_flip(self):
        face = self.assert_card_parse(
            name=u'Akki Lavarunner (Tok-Tok, Volcano Born)',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694&part=Tok-Tok%2c+Volcano+Born',
            html_fixture='gatherer_flip_oracle',
            expected_data=dict(
                set='Champions of Kamigawa',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=78694&type=card&options=rotate180',
                name='Tok-Tok, Volcano Born',
                title='Akki Lavarunner',
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
            ),
            save=True)
        # It should be 'flip' face type
        self.assertEqual(face.card.faces_count, 2)
        self.assertEqual(face.place, CardFace.FLIP)

    @patch.object(Page, '_dowload_content')
    def test_splited_card(self, urlopen):
        page_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=27166'
        fire_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?part=Fire&multiverseid=27166'

        card_page = get_html_fixture('gatherer_split_oracle')
        fire_page = get_html_fixture('gatherer_fire_oracle')
        urlopen.side_effect = [card_page, fire_page]

        card_name = 'Fire // Ice'
        face = self.assert_card_parse(
            name=u'Fire',
            url=page_url,
            print_url='http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=27166',
            expected_data=dict(
                set='Apocalypse',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=27166&type=card',
                name='Fire',
                title=card_name,
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
            ),
            save=True)

        # Check that both mocked pages was requested
        self.assertEqual(urlopen.call_args_list, [call(page_url), call(fire_url)])

        # It should be 'split' face type
        self.assertEqual(face.card.faces_count, 2)
        self.assertEqual(face.place, CardFace.SPLIT)

    def test_land_card_details(self):
        self.assert_card_parse(
            name=u'Forest',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326',
            print_url='http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=289326',
            html_fixture='gatherer_forest',
            expected_data=dict(
                set='Return to Ravnica',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=289326&type=card',
                name='Forest',
                title='Forest',
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

    def test_vanilla_creature(self):
        self.assert_card_parse(
            name=u'Axebane Stag',
            url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=265383',
            print_url='http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=265383',
            html_fixture='gatherer_vanilla_creature',
            expected_data=dict(
                set='Return to Ravnica',
                art='http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=265383&type=card',
                name='Axebane Stag',
                title='Axebane Stag',
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
