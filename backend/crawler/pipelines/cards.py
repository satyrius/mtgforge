import re
from xact import xact
from scrapy.exceptions import DropItem

from crawler.items import CardItem
from oracle.forms import CardFaceForm
from oracle import models as m


class Duplicate(DropItem):
    pass


class InvalidError(DropItem):
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
        face = get_or_create_card_face(item)
        # Update card before face. Faces count is required to detect face type
        update_card(face.card, item)
        face = save_card_face(face, item)
        get_or_create_card_image(item)
        get_or_create_card_release(item, face.card)
        # Increment stat counter
        key = re.sub('[^a-z0-9]', '_', item['set'].lower())
        spider.crawler.stats.inc_value(u'card_item_count/{}'.format(key))


def get_or_create_card_face(item):
    card = None

    # Get existing card face and card by name
    try:
        return m.CardFace.objects.get(name=item['name'])
    except m.CardFace.DoesNotExist:
        pass

    # If cannot find face by name and card item has sibling name
    # use it to fing existing card. Still have to create new card face.
    if 'sibling' in item:
        try:
            sibling = m.CardFace.objects.get(name=item['sibling'])
            card = sibling.card
        except m.CardFace.DoesNotExist:
            pass

    # If card was not found neither by name nor by sibling name, create new one
    if not card:
        card = m.Card.objects.create(name=item['title'])

    # Create new card face instance if it is not exists
    return m.CardFace(card=card)


def save_card_face(face, item):
    # Save card face using form to pass through all magic and validation
    form = CardFaceForm(dict(item), instance=face)
    if not form.is_valid():
        raise InvalidError(form.errors)
    return form.save()


def update_card(card, item):
    if 'sibling' in item:
        card.faces_count = 2
        card.save()
    return card


def get_or_create_card_image(item):
    pass


def get_or_create_card_release(item, card):
    pass
