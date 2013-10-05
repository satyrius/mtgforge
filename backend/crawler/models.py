from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from contrib.fields import NullCharField, NullTextField


class DataProvider(models.Model):
    name = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255, unique=True)
    home = models.URLField()

    class Meta:
        db_table = 'oracle_dataprovider'

    def __unicode__(self):
        return self.name


class DataSource(models.Model):
    url = models.URLField()
    data_provider = models.ForeignKey(DataProvider)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'oracle_datasource'
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
        db_table = 'oracle_dataproviderpage'
        unique_together = ('url_hash', 'class_name')
