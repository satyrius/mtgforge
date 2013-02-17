import re
from optparse import make_option

import xact
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from oracle.forms import CardFaceForm
from oracle.management.base import BaseCommand
from oracle.models import CardFace, Card, CardRelease, CardSet, DataSource, \
    CardImage
from oracle.providers.gatherer import GathererCard


class Command(BaseCommand):
    help = ('Fetched card page from Gatherer and save it to the storage.')

    option_list = BaseCommand.option_list + (
        make_option(
            '-s', '--card-set',
            dest='set',
            help='Card set acronym'),
        make_option(
            '-n', '--name',
            dest='name',
            help='Card name'),
        make_option(
            '-u', '--url',
            dest='url',
            help='Card page url'),
        make_option(
            '-c', '--clear-cache',
            dest='clear',
            action='store_true',
            default=False,
            help='Invalidate page cache'),
        make_option(
            '--no-update',
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
def save_card_face(page, card_set, no_update=False):
    card_details = page.details()
    #
    # Get or create the Card instance
    #
    card = None
    face = None

    number = None
    sub_number = None
    cn = card_details['number']
    if cn:
        match = re.match('^(\d+)([a-z])?', cn)
        if not match:
            raise ValidationError(
                'Collector\'s number "{}" does not match format'.format(cn))
        number = int(match.group(1))
        sub_number = match.group(2)

    try:
        face = CardFace.objects.get(name=card_details['name'])
        if no_update:
            return face
        card = face.card
    except CardFace.DoesNotExist:
        pass
    finally:
        multifaced = 'other_faces' in card_details

        # Find existing multipart card to link with this face
        if not card and multifaced:
            for f in CardFace.objects.filter(name__in=card_details['other_faces']):
                card = f.card
                break

        # Create new card or update title if it is front face
        title = card_details['title']
        if not card:
            # Create card with name equal to card page title
            card = Card.objects.create(name=title)
        elif sub_number == 'a':
            # Update title for multipart card, get it from first part
            card.name = title
            card.save()

        # Create new card face instance if it is not exists
        if not face:
            face = CardFace(card=card)

    form = CardFaceForm(card_details, instance=face)
    if not form.is_valid():
        raise ValidationError(form.errors)
    face = form.save()

    if multifaced:
        card.faces_count = len(card_details['other_faces']) + 1
        card.save()

    #
    # Card release notes
    #

    mvid = int(card_details['mvid'])
    rarity = card_details['rarity'].lower()[0]
    try:
        # Try to get existing card by its id
        release = CardRelease.objects.get(mvid=mvid)
        if release.card_id != card.id:
            raise Exception(
                u'Card release for MVID {0} card id is {1}, expected {1}'.format(
                    mvid, release.card_id, card.id))
    except CardRelease.DoesNotExist:
        new_card_release = lambda: CardRelease(
            card_set=card_set, card=card, mvid=mvid,
            card_number=number, rarity=rarity)
        if number:
            try:
                release = CardRelease.objects.get(
                    card_set=card_set, card=card, card_number=number)
                # Update multiverseid when process card front face
                if sub_number == 'a':
                    release.mvid = mvid
            except CardRelease.DoesNotExist:
                release = new_card_release()
        else:
            release = new_card_release()
    release.save()

    # Remember card release source
    provider = page.get_provider()
    release_type = ContentType.objects.get_for_model(release)
    try:
        source = DataSource.objects.get(content_type__pk=release_type.pk,
                                        object_id=release.id,
                                        data_provider=provider)
    except DataSource.DoesNotExist:
        source = DataSource(content_object=release, data_provider=provider)
    finally:
        if not source.url or sub_number == 'a':
            source.url = card_details['url']
        source.save()

    # Save card face scan
    img, created = CardImage.objects.get_or_create(
        mvid=mvid, defaults=dict(scan=card_details['art']))

    page.set_parsed()
    return face
