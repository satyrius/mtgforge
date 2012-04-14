from django.contrib import admin
from oracle import models
from oracle.forms import DataProviderForm


class DataProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'home')
    form = DataProviderForm

admin.site.register(models.DataProvider, DataProviderAdmin)
