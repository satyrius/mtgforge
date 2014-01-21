import re
from xact import xact
from crawler.items import CardItem
from scrapy.exceptions import DropItem


class Duplicate(DropItem):
    pass


class BaseCardItemPipeline(object):
    def _process_item(self, item, spider):
        raise NotImplemented()

    def process_item(self, item, spider):
        if isinstance(item, CardItem):
            self._process_item(item, spider)
        return item


class DupsHandlePipeline(BaseCardItemPipeline):
    def __init__(self):
        self.found = []

    def _process_item(self, item, spider):
        # Check only cards that have siblings (double faced, splited and
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


class CardsPipeline(BaseCardItemPipeline):
    @xact
    def _process_item(self, item, spider):
        # Save the card
        face = get_or_create_card_face(item)
        get_or_create_card_image(item)
        get_or_create_card_release(item, face.card)
        # Increment stat counter
        key = re.sub('[^a-z0-9]', '_', item['set'].lower())
        spider.crawler.stats.inc_value(u'card_item_count/{}'.format(key))


def get_or_create_card_face(item):
    pass


def get_or_create_card_image(item):
    pass


def get_or_create_card_release(item, card):
    pass
