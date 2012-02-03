from django.contrib import admin
from oracle import models


class CardFaceInline(admin.StackedInline):
    model = models.CardFace
    extra = 0


class CardAdmin(admin.ModelAdmin):
    inlines = [CardFaceInline]

admin.site.register(models.Card, CardAdmin)
