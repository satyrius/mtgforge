from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from oracle import models


class CardL10nInline(admin.TabularInline):
    model = models.CardL10n
    readonly_fields = ('card_release', 'language',)
    fields = ('card_release', 'language', 'name', 'scan')
    extra = 0


class CardFaceForm(forms.ModelForm):
    power = forms.CharField(max_length=10, required=False)
    thoughtness = forms.CharField(max_length=10, required=False)
    fixed_power = forms.IntegerField(required=False)
    fixed_thoughtness = forms.IntegerField(required=False)
    types = forms.ModelMultipleChoiceField(
        models.CardType.objects.all().order_by('name'),
        widget=FilteredSelectMultiple(
            verbose_name='Card face types',
            is_stacked=False
        ),
        required=False,
    )
    class Meta:
        model = models.CardFace


card_face_fieldsets = (
    (None, {
        'fields': (
            ('name', 'place'),
            ('mana_cost', 'cmc', 'color_identity')
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
    readonly_fields = ('type_line', 'card', 'color_identity')
    extra = 0
    fieldsets = card_face_fieldsets


class CardFaceAdmin(admin.ModelAdmin):
    model = models.CardFace
    form = CardFaceForm
    readonly_fields = ('type_line', 'card')
    fieldsets = card_face_fieldsets
    inlines = [CardL10nInline]

admin.site.register(models.CardFace, CardFaceAdmin)
