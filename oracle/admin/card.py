from django import forms
from django.contrib import admin
from oracle import models


class CardFaceForm(forms.ModelForm):
    power = forms.CharField(max_length=10, required=False)
    thoughtness = forms.CharField(max_length=10, required=False)
    fixed_power = forms.CharField(max_length=10, required=False)
    fixed_thoughtness = forms.CharField(max_length=10, required=False)
    class Meta:
        model = models.CardFace


class CardFaceInline(admin.StackedInline):
    model = models.CardFace
    form = CardFaceForm
    readonly_fields = ('type_line',)
    extra = 0
    fieldsets = (
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


class CardReleaseInline(admin.TabularInline):
    model = models.CardRelease
    extra = 0


class CardAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)
    inlines = [CardReleaseInline, CardFaceInline]

admin.site.register(models.Card, CardAdmin)
