from django.contrib.contenttypes import generic
from crawler.models import DataSource


class DataSourceInline(generic.GenericTabularInline):
    model = DataSource
    extra = 0
