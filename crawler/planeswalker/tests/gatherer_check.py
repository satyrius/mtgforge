from planeswalker.spiders.gatherer import GathererSpider


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

        @field name Avacyn, Angel of Hope
        @field set Avacyn Restored
        @field pt 8 / 8
        @field artist Jason Chan
        @field text Flying, vigilance, indestructible\\nOther permanents you control have indestructible.
        @field cmc 8
        @field number 6
        @field mvid 239961
        @field rarity Mythic Rare
        @field mana {5}{W}{W}{W}
        @field flavor A golden helix streaked skyward from the Helvault. A thunderous explosion shattered the silver monolith and Avacyn emerged, free from her prison at last.
        @field type Legendary Creature - Angel

        This card has only one face
        @field sibling
        '''
        # TODO check that the following data parsed or computed
        # @field art http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=239961&type=card
        # @field title Avacyn, Angel of Hope
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
        @field artist Yeong-Hao Han
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def double_faced_card(self, response):
        '''Parse double faced card

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244683

        @returns items 2 2
        @returns requests 0 0

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
        @returns requests 106 106
        '''
        return super(TestGathererSpider, self).parse_list(response)
