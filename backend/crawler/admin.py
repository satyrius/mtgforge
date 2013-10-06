from django.contrib.contenttypes import generic
from crawler.models import DataSource


class DataSourceInline(generic.GenericTabularInline):
    model = DataSource
    extra = 0
    readonly_fields = ('provider', 'url',)
    can_delete = False
    can_add = False

    def has_add_permission(self, *args, **kwargs):
        return False
