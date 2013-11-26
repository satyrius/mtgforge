from planeswalker.spiders.gatherer import GathererSpider


class TestGathererSpider(GathererSpider):
    '''This is a test spider which do absolutele the same as its descendant,
    but has more processing methods to defile more contracts (because Scrapy
    support only one UrlContract per method docstring).
    '''

    def avacyn_angel_of_hope(self, response):
        '''Parse creature details

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961
        @meta card Avacyn, Angel of Hope

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

    def basic_land(self, response):
        '''Parse basic land card

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=289326
        @returns items 1 1
        @returns requests 0 0
        @field name Forest
        @field text G
        @field rarity Common
        @field type Basic Land - Forest
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

    def double_faced_card_front(self, response):
        '''Parse double faced card front face

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244683
        @meta card Hanweir Watchkeep

        @returns items 1 1
        @returns requests 0 0

        @field name Hanweir Watchkeep
        @field sibling Bane of Hanweir
        @field number 145a
        @field color_indicator
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def double_faced_card_back(self, response):
        '''Parse double faced card back

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=244687
        @meta card Bane of Hanweir

        @returns items 1 1
        @returns requests 0 0

        @field name Bane of Hanweir
        @field sibling Hanweir Watchkeep
        @field number 145b
        @field color_indicator Red
        '''
        return super(TestGathererSpider, self).parse_card(response)
