from django.db import models

from oracle.models import Card, CardFace

class CardFtsIndex(models.Model):
    card = models.ForeignKey(Card)
    card_face = models.ForeignKey(CardFace, null=True)
    cmc = models.IntegerField(null=True)
    color_identity = models.IntegerField(default=0)
