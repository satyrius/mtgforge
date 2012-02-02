from django.contrib import admin
from oracle import models


class DataProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'home')

admin.site.register(models.DataProvider, DataProviderAdmin)
