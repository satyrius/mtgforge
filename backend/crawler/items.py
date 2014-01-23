from scrapy.item import Item, Field


class CardSetItem(Item):
    name = Field()
    slug = Field()
    cards = Field()
    released_at = Field()


class CardItem(Item):
    mvid = Field()  # Multiverse ID
    title = Field()  # card title
    name = Field()  # card name
    sibling = Field()  # name of the sibling card face
    card_set_slug = Field()  # card set slug from list page
    set = Field()  # card set full name
    art = Field()  # url for card scan
    art_path = Field()  # file system path for downloaded card scan

    mana = Field()  # encoded mana cost, e.g. {B}{G}
    color_indicator = Field()  # color for double faced cards back
    cmc = Field()  # converted mana cost
    type = Field()  # type line
    text = Field()  # rules text
    flavor = Field()  # flavor text
    pt = Field()  # power and thoughtness
    rarity = Field()  # card rarity
    number = Field()  # collector's numner
    artist = Field()  # artist name

    mark = Field()  # watermark, TODO alter db schema to store it
