import re

from arrayfields import IntegerArrayField
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from contrib.fields import NullCharField, NullTextField
from oracle.utils import Color


# Stub for gettext translation
_ = lambda s: s


# {{{ Cards and faces

class Card(models.Model):
    name = NullCharField(max_length=255)
    faces_count = models.PositiveSmallIntegerField(default=1)

    is_locked = models.BooleanField(
        default=False, help_text='Locked for update with crawler. It is '
                                 'important to do not override cards fixed '
                                 'munually.')

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
    sub_number = NullCharField(max_length=1, null=True, blank=True,
                               choices=(('a', 'a'), ('b', 'b')))

    # Mana cost code and CMC (Converted Mana Cost)
    mana_cost = NullCharField(max_length=255, null=True)
    cmc = models.PositiveIntegerField(null=True)
    color_identity = models.PositiveSmallIntegerField(default=0, blank=True)  # DEPRICATED
    colors = IntegerArrayField(default=[], blank=True)

    # Oracle's card name, type line, rules text and flavor. Always in English.
    name = NullCharField(max_length=255, unique=True)
    type_line = NullCharField(max_length=255)
    rules = NullTextField(null=True)

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

    @property
    def color_short_names(self):
        return Color(self.colors).short_names

    @property
    def color_names(self):
        return Color(self.colors).names


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
            elif re.match('^\{[^}]+\}$', value):
                value = 0
            else:
                value = None
        setattr(card_face, field, value)


@receiver(post_save, sender=CardFace)
def update_faces_count(sender, **kwargs):
    card_face = kwargs['instance']
    card = card_face.card
    count = max(1, card.faces_count, card.cardface_set.count())
    if count != card.faces_count:
        card.faces_count = count
        card.save()

# }}}


# {{{ Card release and localization models

class CardSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    acronym = models.CharField(max_length=10, unique=True)
    cards = models.PositiveIntegerField(null=True, blank=True)
    released_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Artist(models.Model):
    name = NullCharField(max_length=255)

    def __unicode__(self):
        return self.name


class CardImage(models.Model):
    mvid = models.PositiveIntegerField(null=True, blank=True, unique=True)
    scan = models.URLField(help_text='Url of the original art on the Gatherer',
                           null=True, blank=True)
    file = models.ImageField(upload_to='art', null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    artist = models.ForeignKey(Artist, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.mvid)


class CardImageThumb(models.Model):
    original = models.ForeignKey(CardImage)
    format = models.CharField(max_length=10)
    file = models.ImageField(upload_to='thumbs')

    class Meta:
        unique_together = ('original', 'format')


class CardRelease(models.Model):
    COMMON, UNCOMMON, RARE, MYTHIC = 'c', 'u', 'r', 'm'
    RARITY_CHOICES = (
        (COMMON, _('Common')),
        (UNCOMMON, _('Uncommon')),
        (RARE, _('Rare')),
        (MYTHIC, _('Mythic Rare')),
    )

    card = models.ForeignKey(Card)
    card_set = models.ForeignKey(CardSet, on_delete=models.PROTECT)

    rarity = NullCharField(max_length=1, choices=RARITY_CHOICES)
    card_number = models.PositiveIntegerField(null=True, blank=True)

    art = models.ForeignKey(CardImage, null=True, blank=True)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.card.name, self.card_set.name)


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

    art = models.ForeignKey(CardImage, null=True, blank=True)

    class Meta:
        unique_together = (('card_face', 'card_release', 'language'),)

# }}}
