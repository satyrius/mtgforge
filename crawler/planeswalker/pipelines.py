from planeswalker.items import CardItem


class CardsPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CardItem):
            # Save the card
            pass
        return item
