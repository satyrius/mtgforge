from scrapy.item import Item, Field


class CardSetItem(Item):
    name = Field()
    slug = Field()


class CardItem(Item):
    name = Field()
    card_set_slug = Field()
