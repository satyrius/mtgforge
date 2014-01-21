from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from crawler.admin import CardSetAliasInline
from crawler.models import CardSetAlias
from crawler.spiders.products import ProductsInfoSpider
from oracle import models
from oracle.forms import CardSetForm


def _merge(queryset, master):
    CardSetAlias.objects.filter(card_set__in=queryset).update(card_set=master)
    queryset.exclude(pk=master.pk).delete()


def merge_card_sets(modeladmin, request, queryset):
    master = None

    links = None
    for cs in queryset:
        if links is None:
            links = [rel.get_accessor_name()
                     for rel in cs._meta.get_all_related_objects()
                     if rel.var_name != 'cardsetalias']
        for link in links:
            if getattr(cs, link).all().count():
                if master is None:
                    master = cs
                else:
                    modeladmin.message_user(
                        request,
                        u'Both "{}" and "{}" has related objects, '
                        u'cannot merge automatically'.format(
                            master.name, cs.name))
                    return
                break

    if not master:
        from_wizards = CardSetAlias.objects.filter(
            card_set__in=queryset, domain=ProductsInfoSpider.domain)
        if from_wizards:
            master = from_wizards[0]

    if not master:
        master = queryset[0]

    _merge(queryset, master)
    modeladmin.message_user(request, u'All selected card sets was '
                            u'merged to {}'.format(master.name))

merge_card_sets.short_description = 'Merge card sets'


class CardSetAdmin(TranslationAdmin):
    form = CardSetForm
    list_display = ('name', 'acronym', 'cards', 'released_at', 'created_at',
                    'updated_at')
    ordering = ['-released_at']
    list_per_page = 200
    inlines = [CardSetAliasInline]
    actions = [merge_card_sets]

    class Media:
        js = (
            '/static/grappelli_modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/grappelli_modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(models.CardSet, CardSetAdmin)
