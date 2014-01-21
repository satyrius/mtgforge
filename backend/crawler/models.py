from django.db import models
from oracle import models as om


class CardSetAlias(models.Model):
    '''Card set found on Gather or other MTG resources. It is used as oracle
    app CardSet model name alias.
    '''
    name = models.CharField(max_length=255, unique=True)
    card_set = models.ForeignKey(om.CardSet)
    domain = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
