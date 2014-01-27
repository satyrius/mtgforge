import re
from django.core.files.base import File
from scrapy import log
from scrapy.exceptions import DropItem
from xact import xact

from crawler.items import CardItem
from crawler.models import CardSetAlias
from oracle import models as m
from oracle.forms import CardFaceForm, CardImageForm, \
    validate_collectors_number


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
        img = get_or_create_card_image(item)
        get_or_create_artist(item, img)
        get_or_create_card_release(item, face.card, img)
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
    # Do not update locked cards
    if face.id and face.card.is_locked:
        log.msg(u'"{}" is locked, cannot update "{}"'.format(
            face.card.name, item.get('name', face.name)), level=log.WARNING)
        return face
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
    mvid = int(item['mvid'])
    try:
        img = m.CardImage.objects.get(mvid=mvid)
    except m.CardImage.DoesNotExist:
        cif = CardImageForm(data=dict(mvid=mvid, scan=item['art']))
        img = cif.save()

    if not img.file and 'art_path' in item:
        name = '{0}.image'.format(img.mvid)
        with open(item['art_path'], 'rb') as f:
            img.file.save(name, File(f))

    return img


def get_or_create_artist(item, img):
    artist = m.Artist.objects.get_or_create(name=item['artist'])[0]
    if not img.artist or img.artist.id != artist.id:
        img.artist = artist
        img.save()
    return artist


def get_card_set(item):
    name = item['set']
    try:
        return CardSetAlias.objects.get(name=name).card_set
    except CardSetAlias.DoesNotExist:
        raise InvalidError(u'Cannot find card set with name "{}"'.format(name))


def get_or_create_card_release(item, card, img):
    release = None
    try:
        release = m.CardRelease.objects.get(art__mvid=img.mvid)
    except m.CardRelease.DoesNotExist:
        cs = get_card_set(item)
        number, sub_number = validate_collectors_number(item.get('number'))
        if number:
            try:
                release = m.CardRelease.objects.get(
                    card_set=cs, card=card, card_number=number)
            except m.CardRelease.DoesNotExist:
                pass
            else:
                # Update multiverseid when process card front face
                if not release.art or sub_number == 'a':
                    release.art = img
                    release.save()
    else:
        if release.card_id != card.id:
            raise InvalidError(
                u'Card release for MVID {} card id is {}, expected {}'.format(
                    img.mvid, release.card_id, card.id))
    if not release:
        # TODO user form
        release = m.CardRelease.objects.create(
            card_set=cs, card=card, art=img, card_number=number,
            rarity=item['rarity'].lower()[0])
    return release
