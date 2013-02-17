from django.contrib import admin

from oracle import models
from oracle.forms import CardFaceForm


class CardL10nInline(admin.TabularInline):
    model = models.CardL10n
    readonly_fields = ('card_release', 'language',)
    fields = ('card_release', 'language', 'name', 'scan')
    extra = 0


card_face_fieldsets = (
    (None, {
        'fields': (
            ('name', 'place'),
            ('mana_cost', 'cmc', 'color_identity')
        )
    }),
    (None, {
        'fields': (
            'types', 'type_line', 'rules',
        )
    }),
    (None, {
        'fields': (
            ('power', 'thoughtness'),
            ('fixed_power', 'fixed_thoughtness'),
            'loyality'
        )
    })
)


class CardFaceInline(admin.StackedInline):
    model = models.CardFace
    form = CardFaceForm
    readonly_fields = ('card', 'color_identity',)
    extra = 0
    fieldsets = card_face_fieldsets


class CardFaceAdmin(admin.ModelAdmin):
    model = models.CardFace
    form = CardFaceForm
    readonly_fields = ('card',)
    fieldsets = card_face_fieldsets
    inlines = [CardL10nInline]

admin.site.register(models.CardFace, CardFaceAdmin)
