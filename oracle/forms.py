# -*- coding: utf-8 -*-
from django import forms

from oracle import models


class DataProviderForm(forms.ModelForm):
    class Meta:
        model = models.DataProvider
