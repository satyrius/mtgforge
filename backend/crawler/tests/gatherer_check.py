from crawler.spiders.gatherer import GathererSpider


class TestGathererSpider(GathererSpider):
    '''This is a test spider which do absolutele the same as its descendant,
    but has more processing methods to defile more contracts (because Scrapy
    support only one UrlContract per method docstring).
    '''

    def avacyn_angel_of_hope(self, response):
        '''Parse creature details

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961

        @returns items 1 1
        @returns requests 0 0

        @field title Avacyn, Angel of Hope
        @field name Avacyn, Angel of Hope
        @field set Avacyn Restored
        @field pt 8 / 8
        @field text Flying, vigilance, indestructible\\nOther permanents you control have indestructible.
        @field cmc 8
        @field number 6
        @field mvid 239961
        @field rarity Mythic Rare
        @field mana {5}{W}{W}{W}
        @field flavor A golden helix streaked skyward from the Helvault. A thunderous explosion shattered the silver monolith and Avacyn emerged, free from her prison at last.
        @field type Legendary Creature - Angel

        @field artist Jason Chan
        @field art http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=239961&type=card

        This card has only one face
        @field sibling
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def rules_with_comments(self, response):
        '''Parse card rules with comments

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=178135

        @returns items 1 1
        @returns requests 0 0

        @field name Adventuring Gear
        @field text Landfall - Whenever a land enters the battlefield under your control, equipped creature gets +2/+2 until end of turn.\\nEquip {1} ({1}: Attach to target creature you control. Equip only as a sorcery.)
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def vanilla_creature(self, response):
        '''Parse vanilla creature

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=265383

        @returns items 1 1
        @returns requests 0 0

        @field name Axebane Stag
        @field text
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def basic_land(self, response):
        '''Parse basic land card

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326

        @returns items 1 1
        @returns requests 0 0

        @field name Forest
        @field text G
        @field rarity Common
        @field type Basic Land - Forest
        @field mvid 289326
        @field number 271
        @field artist Yeong-Hao Han
        @field art http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=289326&type=card
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def double_faced_card(self, response):
        '''Parse double faced card

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244683

        @returns items 2 2
        @returns requests 0 0

        @field title Hanweir Watchkeep

        @partial {\
            "name": "Hanweir Watchkeep",\
            "sibling": "Bane of Hanweir",\
            "number": "145a",\
            "mvid": "244683"\
        }

        @partial {\
            "name": "Bane of Hanweir",\
            "sibling": "Hanweir Watchkeep",\
            "number": "145b",\
            "mvid": "244687",\
            "color_indicator": "Red"\
        }
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def double_faced_card_from_second_page(self, response):
        '''Parse double faced card

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244687

        @returns items 2 2
        @returns requests 0 0

        @field title Hanweir Watchkeep

        @partial {\
            "name": "Hanweir Watchkeep",\
            "sibling": "Bane of Hanweir",\
            "number": "145a",\
            "mvid": "244683"\
        }

        @partial {\
            "name": "Bane of Hanweir",\
            "sibling": "Hanweir Watchkeep",\
            "number": "145b",\
            "mvid": "244687",\
            "color_indicator": "Red"\
        }
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def flipped_card(self, response):
        '''Parse flipped card

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=78694

        @returns items 2 2
        @returns requests 0 0

        @field title Akki Lavarunner

        @partial {\
            "name": "Akki Lavarunner",\
            "sibling": "Tok-Tok, Volcano Born",\
            "number": "153a"\
        }

        @partial {\
            "name": "Tok-Tok, Volcano Born",\
            "sibling": "Akki Lavarunner",\
            "number": "153b"\
        }
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def splitted_card(self, response):
        '''Parse splitted card first face

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=27166

        @returns items 2 2
        @returns requests 0 0

        @field title Fire // Ice

        @partial {\
            "name": "Fire",\
            "sibling": "Ice",\
            "text": "Fire deals 2 damage divided as you choose among one or two target creatures and/or players.",\
            "number": "128a"\
        }

        @partial {\
            "name": "Ice",\
            "sibling": "Fire",\
            "text": "Tap target permanent.\\nDraw a card.",\
            "number": "128b"\
        }
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def parse_list(self, response):
        '''Parse compact card list

        @url http://gatherer.wizards.com/Pages/Search/Default.aspx?output=compact&set=%5BTheros%5D
        @returns items 0 0

        100 items per page, but +3 additional land card for Forest and Island
        and +3 pagination requests
        @returns requests 109 109
        '''
        return super(TestGathererSpider, self).parse_list(response)

    def parse_list_without_pagination(self, response):
        '''Parse compact card list without pagination

        @url http://gatherer.wizards.com/Pages/Search/Default.aspx?output=compact&set=%5BUnglued%5D
        @returns items 0 0

        This set has 94 cards released
        @returns requests 94 94
        '''
        return super(TestGathererSpider, self).parse_list(response)

    def planechase_rancor(self, response):
        '''Parse creature details.

        Old crawler went wrong with this page. Issue #9

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=275266

        @returns items 1 1
        @returns requests 0 0

        @field name Rancor
        @field set Planechase 2012 Edition
        @field artist Kev Walker
        @field text Enchant creature\\nEnchanted creature gets +2/+0 and has trample.\\nWhen Rancor is put into a graveyard from the battlefield, return Rancor to its owner's hand.
        @field cmc 1
        @field number 76
        @field mvid 275266
        @field rarity Common
        @field mana {G}
        @field type Enchantment - Aura
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def big_fury_monster(self, response):
        '''Parse Big Fury Monster

        Is is a shity card from a shity un-set, it is only the one of a kind
        but I want my crawler to be perfect. Issue #14

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=false&multiverseid=9780

        @returns items 2 2
        @returns requests 0 0

        @field title B.F.M. (Big Furry Monster)
        @field name B.F.M. (Big Furry Monster)
        @field set Unglued
        @field artist Douglas Shuler
        @field rarity Rare

        @partial {\
            "mvid": "9780",\
            "number": "28b",\
            "text": "You must play both B.F.M. cards to put\\nleaves play, sacrifice the other.\\nB.F.M. can be blocked only by three or"\
        }

        @partial {\
            "mvid": "9844",\
            "number": "29b",\
            "mana": "{B}{B}{B}{B}{B}{B}{B}{B}{B}{B}{B}{B}{B}{B}{B}",\
            "cmc": "15",\
            "text": "B.F.M. into play. If either B.F.M. card\\n\\nmore creatures."\
        }
        '''
        return super(TestGathererSpider, self).parse_card(response)
