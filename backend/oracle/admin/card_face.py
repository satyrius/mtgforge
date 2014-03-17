from django.contrib import admin

from oracle import models
from oracle.forms import CardFaceForm


class CardFaceInline(admin.StackedInline):
    model = models.CardFace
    form = CardFaceForm
    readonly_fields = ('card', 'color_identity',)
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'place', 'sub_number'),
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
    ordering = ('sub_number',)
