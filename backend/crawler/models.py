from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from contrib.fields import NullCharField, NullTextField


class DataSource(models.Model):
    url = models.URLField()
    provider = NullCharField(max_length=10)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'oracle_datasource'
        unique_together = (('content_type', 'object_id', 'url'),
                           ('content_type', 'object_id', 'provider'))

    def __unicode__(self):
        return self.url


class PageState(object):
    INITIAL = 0
    PARSED = 1


class DataProviderPage(models.Model):
    url = models.URLField()
    url_hash = models.CharField(max_length=40)
    provider = NullCharField(max_length=10, null=True, blank=True)
    content = NullTextField(null=False, blank=False)
    class_name = NullCharField(max_length=255, null=False, blank=False)
    name = NullCharField(max_length=255, null=True, blank=True)
    state = models.PositiveSmallIntegerField(
        default=PageState.INITIAL, blank=True)

    class Meta:
        db_table = 'oracle_dataproviderpage'
        unique_together = ('url_hash', 'class_name')
