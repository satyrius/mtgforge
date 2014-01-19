import re
from crawler.items import CardItem
from scrapy.exceptions import DropItem


class Duplicate(DropItem):
    pass


class DupsHandlePipeline(object):
    def __init__(self):
        self.found = []

    def process_item(self, item, spider):
        if isinstance(item, CardItem):
            # Check only cars that have siblings (double faced, splited and
            # fliped cards). Only these cards may have duped because there
            # more than one link follows to the card page and a card page has
            # all card faces on on it.
            sibling = item.get('sibling')
            number = item.get('number')
            if sibling and number:
                key = (item['set'], number)
                if key in self.found:
                    raise Duplicate(
                        '"{}" has already scraped for "{}"'.format(
                            item['name'], item['set']))
                else:
                    self.found.append(key)

        return item


class CardsPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CardItem):
            key = re.sub('[^a-z0-9]', '_', item['set'].lower())
            spider.crawler.stats.inc_value(u'card_item_count/{}'.format(key))
            # Save the card
            pass
        return item
