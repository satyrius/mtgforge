from scrapy.item import Item, Field


class CardSetItem(Item):
    name = Field()
    slug = Field()


class CardItem(Item):
    mvid = Field()  # Multiverse ID
    name = Field()  # card name
    card_set_slug = Field()  # card set slug from list page
    set = Field()  # card set full name

    mana = Field()  # encoded mana cost, e.g. {B}{G}
    cmc = Field()  # converted mana cost
    type = Field()  # type line
    text = Field()  # rules text
    flavor = Field()  # flavor text
    pt = Field()  # power and thoughtness
    rarity = Field()  # card rarity
    number = Field()  # collector's numner
    artist = Field()  # artist name

    mark = Field()  # watermark, TODO alter db schema to store it
