from django.db import models
from contrib.fields import NullCharField


class CardSet(models.Model):
    name = NullCharField(max_length=255, unique=True)
    acronym = NullCharField(max_length=10, unique=True)

    def __unicode__(self):
        if not self.acronym:
            return self.name
        return u'{0} ({1})'.format(self.name, self.acronym)
