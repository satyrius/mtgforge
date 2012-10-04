from django.contrib import admin
from oracle import models
from oracle.admin.card_face import CardFaceInline


class CardReleaseInline(admin.TabularInline):
    ordering = ('card_set__released_at', 'card_set__name', 'card_number',)
    model = models.CardRelease
    extra = 0


class CardAdmin(admin.ModelAdmin):
    inlines = [CardReleaseInline, CardFaceInline]
    list_filter = ('cardrelease__card_set__name',)
    ordering = ('name',)
    readonly_fields = ('name',)
    search_fields = ('name', 'cardface__cardl10n__name',)

admin.site.register(models.Card, CardAdmin)
