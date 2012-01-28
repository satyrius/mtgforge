from django.db import models
from contrib.fields import NullCharField, NullURLField


class CardSet(models.Model):
    name = NullCharField(max_length=255, unique=True)
    acronym = NullCharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.name


class DataProvider(models.Model):
    name = NullCharField(max_length=20, unique=True)
    title = NullCharField(max_length=255, unique=True)
    home = NullURLField()

    def __unicode__(self):
        return self.name
