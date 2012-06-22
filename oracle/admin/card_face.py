from django import forms
from django.contrib import admin

from oracle.admin.data_provider import DataSourceInline
from oracle import models


class CardFaceForm(forms.ModelForm):
    power = forms.CharField(max_length=10, required=False)
    thoughtness = forms.CharField(max_length=10, required=False)
    fixed_power = forms.CharField(max_length=10, required=False)
    fixed_thoughtness = forms.CharField(max_length=10, required=False)
    class Meta:
        model = models.CardFace


card_face_fieldsets = (
    (None, {
        'fields': (
            ('name', 'place'),
            ('mana_cost', 'cmc')
        )
    }),
    (None, {
        'fields': (
            'types', 'type_line',
            'rules', 'flavor'
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
    readonly_fields = ('type_line', 'card')
    extra = 0
    fieldsets = card_face_fieldsets


class CardFaceAdmin(admin.ModelAdmin):
    model = models.CardFace
    form = CardFaceForm
    readonly_fields = ('type_line', 'card')
    fieldsets = card_face_fieldsets
    inlines = [DataSourceInline]

admin.site.register(models.CardFace, CardFaceAdmin)
