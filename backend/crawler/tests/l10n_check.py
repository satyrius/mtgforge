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
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961&printed=true @language English
        @request http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=239961
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def do_not_cycle(self, response):
        '''Do not return any request if we are already parsing card print page

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=239961&printed=true
        @meta language English

        @returns items 1 1
        @items L10nItem 1
        @field language English

        @returns requests 0 0
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def splitted_card_print(self, response):
        '''Parse splitted card

        @url http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=27166

        @returns items 2 2
        @returns requests 0 0

        @field title Fire // Ice

        @partial {\
            "name": "Fire",\
            "sibling": "Ice",\
            "number": "128a"\
        }

        @partial {\
            "name": "Ice",\
            "sibling": "Fire",\
            "number": "128b"\
        }
        '''
        return super(TestGathererSpider, self).parse_card(response)

    def print_for_each_language(self, response):
        '''Return links to the card print for each language

        @url http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=239961

        @returns items 0 0
        @returns requests 10 10
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295034&printed=true @language Chinese Traditional
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=340526&printed=true @language German
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295522&printed=true @language French
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=296254&printed=true @language Italian
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=294245&printed=true @language Japanese
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=294790&printed=true @language Korean
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295278&printed=true @language Portuguese (Brazil)
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=295766&printed=true @language Russian
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=294546&printed=true @language Chinese Simplified
        @request http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=296010&printed=true @language Spanish
        '''
        return super(TestGathererSpider, self).parse_languages(response)

    def languages_pagination(self, response):
        '''Return links for languages pagination

        @url http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=245247

        @returns items 0 0
        @request http://gatherer.wizards.com/Pages/Card/Languages.aspx?page=0&multiverseid=245247
        @request http://gatherer.wizards.com/Pages/Card/Languages.aspx?page=1&multiverseid=245247
        '''
        return super(TestGathererSpider, self).parse_languages(response)
