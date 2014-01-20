from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from oracle import models
from oracle.forms import CardSetForm


class CardSetAdmin(TranslationAdmin):
    form = CardSetForm
    list_display = ('name', 'acronym', 'cards', 'released_at', 'created_at',
                    'updated_at')
    ordering = ['-released_at']
    list_per_page = 150

    class Media:
        js = (
            '/static/grappelli_modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/grappelli_modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(models.CardSet, CardSetAdmin)
