from django.contrib import admin
from oracle import models


class CardFaceInline(admin.StackedInline):
    model = models.CardFace
    extra = 0


class CardAdmin(admin.ModelAdmin):
    inlines = [CardFaceInline]
    readonly_fields = ('name',)

admin.site.register(models.Card, CardAdmin)
