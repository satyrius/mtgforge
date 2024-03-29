from django.db import models

from oracle.models import Card, CardFace


class CardFtsIndex(models.Model):
    card = models.ForeignKey(Card)
    card_face = models.ForeignKey(CardFace)
    cmc = models.IntegerField(null=True)
    color_identity = models.IntegerField(default=0)
    face_order = models.PositiveIntegerField(default=0)


class CardSimilarity(models.Model):
    keyword = models.CharField(max_length=128, unique=True)
    alias = models.ForeignKey('forge.CardSimilarity', null=True)


class FtsSuggest(models.Model):
    term = models.CharField(max_length=20, unique=True)
    weight = models.PositiveIntegerField()
