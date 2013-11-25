from planeswalker.spiders.gatherer import GathererSpider


class TestGathererSpider(GathererSpider):
    '''This is a test spider which do absolutele the same as its descendant,
    but has more processing methods to defile more contracts (because Scrapy
    support only one UrlContract per method docstring).
    '''

    def avacyn_angel_of_hope(self, response):
        '''Parse compact card list and follow card details for each printing.

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961
        @returns items 1 1
        @returns requests 0 0
        @item_json {\
            "set": "Avacyn Restored",\
            "name": "Avacyn, Angel of Hope",\
            "pt": "8 / 8",\
            "artist": "Jason Chan",\
            "text": "Flying, vigilance, indestructible\\nOther permanents you control have indestructible.",\
            "cmc": "8",\
            "number": "6",\
            "mvid": "239961",\
            "rarity": "Mythic Rare",\
            "mana": "{5}{W}{W}{W}",\
            "flavor": "A golden helix streaked skyward from the Helvault. A thunderous explosion shattered the silver monolith and Avacyn emerged, free from her prison at last.",\
            "type": "Legendary Creature - Angel"\
        }
        '''
        # TODO check that the following data parsed or computed
        # "art": "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=239961&type=card",\
        # "title": "Avacyn, Angel of Hope",\
        return super(TestGathererSpider, self).parse_card(response)
