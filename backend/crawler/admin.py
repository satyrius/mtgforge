from django.contrib import admin
from django.contrib.contenttypes import generic

from crawler.forms import DataProviderForm
from crawler.models import DataSource, DataProvider


class DataSourceInline(generic.GenericTabularInline):
    model = DataSource
    extra = 0


class DataProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'home')
    form = DataProviderForm

admin.site.register(DataProvider, DataProviderAdmin)
