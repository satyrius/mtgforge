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
