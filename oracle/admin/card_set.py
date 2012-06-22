from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from oracle import models
from oracle.admin.data_provider import DataSourceInline
from oracle.forms import CardSetForm


class CardSetAdmin(TranslationAdmin):
    form = CardSetForm
    list_display = ('name', 'acronym', 'cards', 'released_at')
    ordering = ['-released_at']
    list_per_page = 150
    inlines = [DataSourceInline]

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            '/static/modeltranslation/js/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(models.CardSet, CardSetAdmin)

