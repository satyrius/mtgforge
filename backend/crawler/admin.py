from django.contrib import admin
from crawler.models import CardSetAlias


class CardSetAliasInline(admin.TabularInline):
    model = CardSetAlias
    extra = 0
    readonly_fields = ('name', 'domain',)
