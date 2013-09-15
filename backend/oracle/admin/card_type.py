from django.contrib import admin
from oracle import models


class CardTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    ordering = ['name']

admin.site.register(models.CardType, CardTypeAdmin)
