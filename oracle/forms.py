# -*- coding: utf-8 -*-
import re

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from oracle import models


class DataProviderForm(forms.ModelForm):
    class Meta:
        model = models.DataProvider


class CardSetForm(forms.ModelForm):
    class Meta:
        model = models.CardSet


class CardFaceForm(forms.ModelForm):
    power = forms.CharField(max_length=10, required=False)
    thoughtness = forms.CharField(max_length=10, required=False)
    fixed_power = forms.IntegerField(required=False)
    fixed_thoughtness = forms.IntegerField(required=False)
    types = forms.ModelMultipleChoiceField(
        models.CardType.objects.all().order_by('name'),
        widget=FilteredSelectMultiple(
            verbose_name='Card types',
            is_stacked=False
        ),
        required=False,
    )

    class Meta:
        model = models.CardFace

    def _fix_data(self, data, field_name, alt_name, default=None, cast=None):
        if not field_name in data:
            data[field_name] = alt_name in data and data[alt_name] or default
        if cast and data[field_name] != default:
            data[field_name] = cast(data[field_name])

    def __init__(self, data=None, **kwargs):
        if data:
            self._fix_data(data, 'mana_cost', 'mana')
            self._fix_data(data, 'cmc', 'cmc', cast=int)
            self._fix_data(data, 'type_line', 'type')
            self._fix_data(data, 'rules', 'text')
            self._fix_data(data, 'power', 'power')
            self._fix_data(data, 'thoughtness', 'thoughtness')
            self._fix_data(data, 'loyality', 'loyality')
            if 'pt' in data:
                pt = re.split(u'\s*/\s*', data['pt'], 2)
                if len(pt) == 2:
                    # Power and Thoughtness for creatures
                    data['power'], data['thoughtness'] = p, t = pt
                    data['fixed_power'] = (p is not None and p.isdigit() and [int(p)] or [None])[0]
                    data['fixed_thoughtness'] = (t is not None and t.isdigit() and [int(t)] or [None])[0]
                else:
                    data['loyality'] = int(pt[0])

        super(CardFaceForm, self).__init__(data=data, **kwargs)

    def clean(self):
        '''Copy default data from instance or get its default values'''
        instance = self.instance
        cleaned_data = self.cleaned_data

        if not instance:
            return cleaned_data

        opts = instance._meta
        for f in opts.fields:
            if f.name in cleaned_data and (
                cleaned_data[f.name] is None or cleaned_data[f.name] == ''
            ):
                value = getattr(instance, f.name)
                cleaned_data[f.name] = (
                    value is not None and [value] or [f.get_default()])[0]
        return self.cleaned_data
