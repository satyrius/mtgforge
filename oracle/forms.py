# -*- coding: utf-8 -*-
import re

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from oracle import models
from oracle.utils import parse_type_line


class DataProviderForm(forms.ModelForm):
    class Meta:
        model = models.DataProvider


class CardSetForm(forms.ModelForm):
    class Meta:
        model = models.CardSet


class CardPageForm(forms.ModelForm):
    def _fix_data(self, data, field_name, alt_name, default=None, cast=None):
        if not field_name in data:
            data[field_name] = alt_name in data and data[alt_name] or default
        if cast and data[field_name] != default:
            data[field_name] = cast(data[field_name])

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


class CardFaceForm(CardPageForm):
    types = forms.ModelMultipleChoiceField(
        models.CardType.objects.all().order_by('name'),
        widget=FilteredSelectMultiple(
            verbose_name='Card types',
            is_stacked=False
        ),
        required=False,
    )
    rules = forms.CharField(required=False, widget=forms.Textarea)
    flavor = forms.CharField(required=False, widget=forms.Textarea)
    cmc = forms.IntegerField(required=False)
    mana_cost = forms.CharField(max_length=50, required=False)
    type_line = forms.CharField(max_length=255, required=False)

    class Meta:
        model = models.CardFace

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
                pt = re.split(u'\s+/\s+', data['pt'], 2)
                if len(pt) == 2:
                    # Power and Thoughtness for creatures
                    data['power'], data['thoughtness'] = p, t = pt
                else:
                    data['loyality'] = int(pt[0])

        super(CardFaceForm, self).__init__(data=data, **kwargs)

    def clean(self):
        super(CardFaceForm, self).clean()
        cleaned_data = self.cleaned_data
        type_line = cleaned_data['type_line']
        if type_line and not cleaned_data['types']:
            cleaned_data['types'] = parse_type_line(type_line)
        elif not type_line and cleaned_data['types']:
            t0, t1, t2 = [], [], []
            for t in cleaned_data['types']:
                if t.category == models.CardType.TYPE:
                    t1.append(t.name)
                elif t.category == models.CardType.SUPERTYPE:
                    t0.append(t.name)
                elif t.category == models.CardType.SUBTYPE:
                    t2.append(t.name)
            cleaned_data['type_line'] = ' - '.join(
                filter(None, [' '.join(t0 + t1), ' '.join(t2)]))
        return cleaned_data


class CardL10nForm(CardPageForm):
    class Meta:
        model = models.CardL10n

    def __init__(self, data=None, **kwargs):
        if data:
            self._fix_data(data, 'type_line', 'type')
            self._fix_data(data, 'rules', 'text')
            self._fix_data(data, 'scan', 'art')

        super(CardL10nForm, self).__init__(data=data, **kwargs)
