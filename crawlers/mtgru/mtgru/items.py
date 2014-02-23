from scrapy.item import Item, Field


class PlayerItem(Item):
    name = Field()
    file_urls = Field()
    files = Field()
