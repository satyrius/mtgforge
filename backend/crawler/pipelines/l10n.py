import re

from xact import xact
from scrapy import log

from contrib import l10n
from crawler.items import L10nItem
from crawler.pipelines import cards
from crawler.pipelines.cards import InvalidError
from oracle.forms import validate_collectors_number, CardL10nForm
from oracle import models as m


class BaseL10nItemPipeline(object):
    def _process_item(self, item, spider):
        raise NotImplemented()

    def process_item(self, item, spider):
        if isinstance(item, L10nItem):
            self._process_item(item, spider)
        return item


class L10nPipeline(BaseL10nItemPipeline):
    @xact
    def _process_item(self, item, spider):
        release, face = get_card_release(item)
        face_l10n = get_l10n_instance(face, release, item['language'])
        save_card_l10n(face_l10n, item)

        # Increment stat counter
        key = re.sub('[^a-z0-9]', '_', item['set'].lower())
        spider.crawler.stats.inc_value(u'cards/{}/l10n'.format(key))


def get_card_release(item):
    number, sub_number = validate_collectors_number(item.get('number'))
    cs = cards.get_card_set(item)
    if number:
        # Try to get release by its number first
        release = m.CardRelease.objects.get(card_set=cs, card_number=number)
    elif item['language'] == l10n.get_name(l10n.EN):
        # Otherwise we can try to get it by mvid for english cards
        release = m.CardRelease.objects.get(
            card_set=cs, art__mvid=item['mvid'])
    else:
        raise InvalidError(u'Cannot setup localization for card without '
                           u'collector\'s number for "{name}"'.format(
                               name=item['name']))
    face = release.card.cardface_set.get(sub_number=sub_number)
    return release, face


def get_l10n_instance(face, release, language):
    language = l10n.get_code(language)
    try:
        face_l10n = m.CardL10n.objects.get(
            card_face=face, card_release=release, language=language)
    except m.CardL10n.DoesNotExist:
        face_l10n = m.CardL10n(
            card_face=face, card_release=release, language=language)
    return face_l10n


def save_card_l10n(face_l10n, item):
    # Do not update locked cards
    face = face_l10n.card_face
    if face.card.is_locked:
        log.msg(u'"{}" is locked, cannot update "{}"'.format(
            face.card.name, item.get('name', face.name)), level=log.WARNING)
        return None

    # Save card face using form to pass through all magic and validation.
    # Face, release and language should be in instance.
    mvid = item['mvid']
    data = {
        'mvid': mvid,
        'name': item['name'],
        'type_line': item['type'],
        'rules': item['text'],
        'flavor': item['flavor'],
        'art': m.CardImage.objects.get(mvid=mvid).id,
    }
    form = CardL10nForm(data, instance=face_l10n)
    if not form.is_valid():
        raise InvalidError(form.errors)
    return form.save()
