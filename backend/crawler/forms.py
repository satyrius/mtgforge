from django import forms
from crawler.models import DataProvider


class DataProviderForm(forms.ModelForm):
    class Meta:
        model = DataProvider
