from django.contrib import admin
from django.contrib.contenttypes import generic
from oracle import models
from oracle.forms import DataProviderForm


class DataSourceInline(generic.GenericTabularInline):
    model = models.DataSource
    extra = 0


class DataProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'home')
    form = DataProviderForm

admin.site.register(models.DataProvider, DataProviderAdmin)
