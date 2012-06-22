from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from contrib.cdn import CDNFileField
from contrib.fields import NullCharField, NullTextField
from contrib.utils import cache_method_calls


# Stub for gettext translation
_ = lambda s: s


class DataProvider(models.Model):
    name = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255, unique=True)
    home = models.URLField()

    @property
    @cache_method_calls
    def provider(self):
        from oracle.providers import Provider
        return Provider.factory(self)

    def absolute_url(self, url):
        return self.provider.absolute_url(url)

    def __unicode__(self):
        return self.name


class DataSource(models.Model):
    url = models.URLField()
    data_provider = models.ForeignKey(DataProvider)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('content_type', 'object_id', 'url'),
                           ('content_type', 'object_id', 'data_provider'))

    def __unicode__(self):
        return self.url


class CardSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    acronym = models.CharField(max_length=10, unique=True)
    cards = models.PositiveIntegerField(null=True, blank=True)
    released_at = models.DateField(null=True, blank=True)
    sources = generic.GenericRelation(DataSource)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    name = NullCharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name or 'Card #{}'.format(self.id)


class CardType(models.Model):
    SUPERTYPE, TYPE, SUBTYPE = 'supertype', 'type', 'subtype'
    CATEGORY_CHOICES = (
        (SUPERTYPE, _('Supertype')),
        (TYPE, _('Type')),
        (SUBTYPE, _('Subtype')),
    )

    name = NullCharField(max_length=255, unique=True)
    category = NullCharField(max_length=9, choices=CATEGORY_CHOICES)

    def __unicode__(self):
        return self.name


class CardFace(models.Model):
    FRONT, BACK, SPLIT, FLIP = 'front', 'back', 'split', 'flip'
    TYPE_CHOICES = (
        (FRONT, _('Front')),
        (BACK, _('Back')),
        (SPLIT, _('Split')),
        (FLIP, _('Flip')),
    )

    card = models.ForeignKey(Card)
    place = NullCharField(max_length=5, choices=TYPE_CHOICES, default=FRONT)

    # Mana cost code and CMC (Converted Mana Cost)
    mana_cost = NullCharField(max_length=255, null=True, blank=True)
    cmc = models.PositiveIntegerField(null=True, blank=True)

    # Oracle's card name, type line, rules text and flavor. Always in English.
    name = NullCharField(max_length=255, unique=True)
    type_line = NullCharField(max_length=255)
    rules = NullTextField(null=True, blank=True)
    flavor = NullTextField(null=True, blank=True)

    types = models.ManyToManyField(CardType)

    # Store power and thoughtness as strings because of */*, *^2/*^2, 2{1/2}/1
    # and other variants of calculated or strange values.
    power = NullCharField(max_length=10, null=True, blank=True)
    thoughtness = NullCharField(max_length=10, null=True, blank=True)
    # Store parsed power and thoughtness if they are integers
    fixed_power = models.PositiveSmallIntegerField(null=True, blank=True)
    fixed_thoughtness = models.PositiveSmallIntegerField(null=True, blank=True)
    # Planeswalker's loyality counters
    loyality = models.PositiveSmallIntegerField(null=True, blank=True)

    sources = generic.GenericRelation(DataSource)

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=CardFace)
def update_card_name(sender, **kwargs):
    card_face = kwargs['instance']
    if card_face.place == card_face.FRONT:
        card = card_face.card
        card.name = card_face.name
        card.save()


class Artist(models.Model):
    name = NullCharField(max_length=255)

    def __unicode__(self):
        return self.name


class CardRelease(models.Model):
    COMMON, UNCOMMON, RARE, MYTHIC = 'c', 'u', 'r', 'm'
    RARITY_CHOICES = (
        (COMMON, _('Common')),
        (UNCOMMON, _('Uncommon')),
        (RARE, _('Rare')),
        (MYTHIC, _('Mythic Rare')),
    )

    card = models.ForeignKey(Card)
    card_set = models.ForeignKey(CardSet)

    rarity = NullCharField(max_length=1, choices=RARITY_CHOICES)
    card_number = models.PositiveIntegerField(null=True, blank=True)
    artist = models.ForeignKey(Artist)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.card.name, self.card_set.name)


STORAGE_PATH = '/mtgforge/media/'
IMAGE_FORMATS = ['orig', 'x220']

class CardL10n(models.Model):
    card_face = models.ForeignKey(CardFace)
    card_release = models.ForeignKey(CardRelease)
    language = NullCharField(max_length=2, choices=settings.LANGUAGES,
                            default=settings.MODELTRANSLATION_DEFAULT_LANGUAGE)

    name = NullCharField(max_length=255)
    type_line = NullCharField(max_length=255)
    rules = NullTextField(null=True, blank=True)
    flavor = NullTextField(null=True, blank=True)

    scan = models.URLField()
    file = CDNFileField(storage_path=STORAGE_PATH, null=True, blank=True)

    class Meta:
        unique_together = (('card_face', 'card_release', 'language'),)
