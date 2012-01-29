from django.db import models
from contrib.fields import NullCharField, NullURLField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from contrib.utils import cache_method_calls


class DataProvider(models.Model):
    name = NullCharField(max_length=20, unique=True)
    title = NullCharField(max_length=255, unique=True)
    home = NullURLField()

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
    url = NullURLField()
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
    name = NullCharField(max_length=255, unique=True)
    acronym = NullCharField(max_length=10, unique=True)
    cards = models.PositiveIntegerField(null=True, blank=True)
    released_at = models.DateField(null=True, blank=True)
    sources = generic.GenericRelation(DataSource)

    def __unicode__(self):
        return self.name
