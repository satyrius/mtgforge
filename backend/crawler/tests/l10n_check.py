from crawler.spiders.gatherer import GathererSpider


class TestGathererSpider(GathererSpider):
    '''This is a test spider which do absolutele the same as its descendant,
    but has more processing methods to defile more contracts (because Scrapy
    support only one UrlContract per method docstring).
    '''
    name = 'prints'

    def print_page_and_languages_requests(self, response):
        '''Parsing oracle rules should return request for parsing card print
        data and list of languages

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961

        @returns items 1 1
        @items CardItem 1

        @returns requests 2 2
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961&printed=true @printed English
        @request http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=239961
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def do_not_cycle(self, response):
        '''Do not return any request if we are already parsing card print page

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961&printed=true
        @meta printed English

        @returns items 1 1
        @items L10nItem 1

        @returns requests 0 0
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def print_for_each_language(self, response):
        '''Return links to the card print for each langiage

        @url http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=239961

        @returns items 0 0
        @returns requests 10 10
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295034&printed=true @printed Chinese Traditional
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=340526&printed=true @printed German
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295522&printed=true @printed French
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=296254&printed=true @printed Italian
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=294245&printed=true @printed Japanese
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=294790&printed=true @printed Korean
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295278&printed=true @printed Portuguese (Brazil)
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295766&printed=true @printed Russian
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=294546&printed=true @printed Chinese Simplified
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=296010&printed=true @printed Spanish
        '''
        return super(TestGathererSpider, self).parse_languages(response)
