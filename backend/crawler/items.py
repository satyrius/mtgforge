from scrapy.item import Item, Field


class CardSetItem(Item):
    name = Field()
    slug = Field()
    cards = Field()
    released_at = Field()


class CardImageItem(Item):
    mvid = Field()  # Multiverse ID
    art = Field()  # url for card scan


class BaseCarditem(Item):
    art = Field()  # url for card scan
    mvid = Field()  # Multiverse ID
    number = Field()  # collector's numner

    title = Field()  # card title
    name = Field()  # card name
    type = Field()  # type line
    text = Field()  # rules text
    flavor = Field()  # flavor text
    sibling = Field()  # name of the sibling card face


class CardItem(BaseCarditem):
    set = Field()  # card set full name
    mana = Field()  # encoded mana cost, e.g. {B}{G}
    color_indicator = Field()  # color for double faced cards back
    cmc = Field()  # converted mana cost
    pt = Field()  # power and thoughtness
    rarity = Field()  # card rarity
    artist = Field()  # artist name
    mark = Field()  # watermark, TODO alter db schema to store it


class L10nItem(BaseCarditem):
    language = Field()
