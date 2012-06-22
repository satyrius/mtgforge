from django.contrib import admin
from oracle import models
from oracle.admin.card_face import CardFaceInline


class CardReleaseInline(admin.TabularInline):
    model = models.CardRelease
    extra = 0


class CardAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)
    search_fields = ('name', 'cardface__cardl10n__name')
    inlines = [CardReleaseInline, CardFaceInline]

admin.site.register(models.Card, CardAdmin)
