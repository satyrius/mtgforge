import re
from optparse import make_option

import xact
from django.core.exceptions import ValidationError

from oracle.forms import CardFaceForm
from oracle.management.base import BaseCommand
from oracle.models import CardFace, Card, CardRelease, CardSet
from oracle.providers.gatherer import GathererCard


class Command(BaseCommand):
    help = ('Fetched card page from Gatherer and save it to the storage.')

    option_list = BaseCommand.option_list + (
        make_option('-s', '--card-set',
            dest='set',
            help='Card set acronym'),
        make_option('-n', '--name',
            dest='name',
            help='Card name'),
        make_option('-u', '--url',
            dest='url',
            help='Card page url'),
        make_option('-c', '--clear-cache',
            dest='clear',
            action='store_true',
            default=False,
            help='Invalidate page cache'),
        make_option('--no-update',
            action='store_true',
            dest='no_update',
            default=False,
            help='Do not update existing card faces'),
        )

    def handle(self, *args, **options):
        card_set = CardSet.objects.get(acronym=options['set'].lower())
        page = GathererCard(options['url'], name=options['name'] or None)
        if options['clear']:
            page.delete_cache()
        details = page.details()
        card_face = save_card_face(details, card_set, options['no_update'])
        page.set_parsed()
        for field in card_face._meta.fields:
            self.writeln(u'{0}: {1}'.format(
                field.name, getattr(card_face, field.name)))


@xact.xact
def save_card_face(card_details, card_set, no_update=False):
    #
    # Get or create the Card instance
    #
    card = None
    face = None
    try:
        face = CardFace.objects.get(name=card_details['name'])
        if no_update:
            return face
        card = face.card
    except CardFace.DoesNotExist:
        pass
    finally:
        if 'other_faces' in card_details:
            for f in CardFace.objects.filter(name__in=card_details['other_faces']):
                if not card:
                    card = f.card
                    break
                if card.id != f.card_id:
                    # Delete duplicate and link with right card
                    f.card.delete()
                    f.card = card
                    f.save()
        if not card:
            card = Card.objects.create()
        if not face:
            face = CardFace(card=card)

    form = CardFaceForm(card_details, instance=face)
    if not form.is_valid():
        raise ValidationError(form.errors)
    face = form.save()

    #
    # Card release notes
    #
    try:
        release = CardRelease.objects.get(card_set=card_set, card=card)
    except CardRelease.DoesNotExist:
        release = CardRelease(card_set=card_set, card=card)
    release.rarity = card_details['rarity'].lower()[0]
    match = re.match(r'(\d+)\w?', card_details.get('number', ''))
    if match :
        release.card_number = match.group(1)
    release.save()

    return face

