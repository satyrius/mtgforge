import re

from arrayfields import IntegerArrayField
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from contrib.cdn import CDNFileField
from contrib.fields import NullCharField, NullTextField


# Stub for gettext translation
_ = lambda s: s


# {{{ Data providers and sources

class DataProvider(models.Model):
    name = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255, unique=True)
    home = models.URLField()

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


class PageState(object):
    INITIAL = 0
    PARSED = 1


class DataProviderPage(models.Model):
    url = models.URLField()
    url_hash = models.CharField(max_length=40)
    data_provider = models.ForeignKey(DataProvider, null=True, blank=True)
    content = NullTextField(null=False, blank=False)
    class_name = NullCharField(max_length=255, null=False, blank=False)
    name = NullCharField(max_length=255, null=True, blank=True)
    state = models.PositiveSmallIntegerField(
        default=PageState.INITIAL, blank=True)

    class Meta:
        unique_together = ('url_hash', 'class_name')

# }}}


# {{{ Cards and faces

class Card(models.Model):
    name = NullCharField(max_length=255)
    faces_count = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return self.name


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


# Color identity
class Color(object):
    WHITE = 0b1
    BLUE = 0b10
    BLACK = 0b100
    RED = 0b1000
    GREEN = 0b10000
    COLORLESS = 0b100000

    MAP = dict(
        w=WHITE,
        u=BLUE,
        b=BLACK,
        r=RED,
        g=GREEN,
        c=COLORLESS,
    )

    def __init__(self, mana_cost=None):
        self.identity = 0
        self.colors = []

        if mana_cost:
            costs = set(mana_cost.lower())
            has_colorless_mana = len(filter(lambda s: s.isdigit() or s == 'x', costs)) > 0
            allowed_symbols = self.MAP.keys()
            for s in filter(lambda s: s.isalpha() and s in allowed_symbols, costs):
                c = self.MAP[s]
                self.identity |= c
                self.colors.append(c)
            if not self.identity and has_colorless_mana:
                self.identity = self.COLORLESS
                self.colors = [self.COLORLESS]
            self.colors.sort()


class CardFace(models.Model):
    FRONT, BACK, SPLIT, FLIP = 'front', 'back', 'split', 'flip'
    TYPE_CHOICES = (
        (FRONT, _('Front')),
        (BACK, _('Back')),
        (SPLIT, _('Split')),
        (FLIP, _('Flip')),
    )

    card = models.ForeignKey(Card, blank=True)
    place = NullCharField(max_length=5, choices=TYPE_CHOICES, default=FRONT, blank=True)

    # Mana cost code and CMC (Converted Mana Cost)
    mana_cost = NullCharField(max_length=255, null=True)
    cmc = models.PositiveIntegerField(null=True)
    color_identity = models.PositiveSmallIntegerField(default=0, blank=True) # DEPRICATED
    colors = IntegerArrayField(default=[], blank=True)

    # Oracle's card name, type line, rules text and flavor. Always in English.
    name = NullCharField(max_length=255, unique=True)
    type_line = NullCharField(max_length=255)
    rules = NullTextField(null=True)
    flavor = NullTextField(null=True)

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

    def __unicode__(self):
        return self.name


@receiver(pre_save, sender=CardFace)
def update_color_identity(sender, **kwargs):
    card_face = kwargs['instance']
    c = Color(card_face.mana_cost)
    card_face.color_identity = c.identity
    card_face.colors = c.colors


@receiver(pre_save, sender=CardFace)
def update_fixed_power_and_thoughtness(sender, **kwargs):
    card_face = kwargs['instance']
    p, t = card_face.power, card_face.thoughtness
    for field, value in (('fixed_power', p), ('fixed_thoughtness', t)):
        if value is not None:
            m = re.match('^(\d+)[^*]*$', value)
            if m:
                value = int(m.group(1))
            else:
                value = None
        setattr(card_face, field, value)

# }}}


# {{{ Card release and localization models

class CardSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    acronym = models.CharField(max_length=10, unique=True)
    cards = models.PositiveIntegerField(null=True, blank=True)
    released_at = models.DateField(null=True, blank=True)
    sources = generic.GenericRelation(DataSource)

    def __unicode__(self):
        return self.name


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
    mvid = models.PositiveIntegerField(
        help_text='Multiverse ID of english card oracle page', unique=True)

    sources = generic.GenericRelation(DataSource)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.card.name, self.card_set.name)


STORAGE_PATH = '/mtgforge/media/'
IMAGE_FORMATS = ['orig', 'x220']


class CardL10n(models.Model):
    card_face = models.ForeignKey(CardFace, blank=True)
    card_release = models.ForeignKey(CardRelease, blank=True)
    language = NullCharField(
        max_length=2, choices=settings.LANGUAGES, blank=True,
        default=settings.MODELTRANSLATION_DEFAULT_LANGUAGE)

    name = NullCharField(max_length=255)
    type_line = NullCharField(max_length=255)
    rules = NullTextField(null=True, blank=True)
    flavor = NullTextField(null=True, blank=True)

    artist = models.ForeignKey(Artist)
    scan = models.URLField()
    file = CDNFileField(storage_path=STORAGE_PATH, null=True, blank=True)

    class Meta:
        unique_together = (('card_face', 'card_release', 'language'),)

    sources = generic.GenericRelation(DataSource)

# }}}
