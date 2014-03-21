from django.contrib import admin
from django.db.models import Count
from django.db.transaction import atomic
from modeltranslation.admin import TranslationAdmin

from crawler.admin import CardSetAliasInline
from crawler.models import CardSetAlias
from crawler.spiders.products import ProductsInfoSpider
from oracle import models
from oracle.forms import CardSetForm


@atomic
def _merge(queryset, master):
    CardSetAlias.objects.filter(card_set__in=queryset).update(card_set=master)
    objects = queryset.exclude(pk=master.pk)
    for f in master._meta.fields:
        if not f.primary_key and not getattr(master, f.name):
            for obj in objects:
                val = getattr(obj, f.name)
                if val:
                    setattr(master, f.name, val)
                    break
    queryset.exclude(pk=master.pk).delete()
    master.save()


def merge_card_sets(modeladmin, request, queryset):
    master = None

    published = queryset.filter(is_published=True)
    if len(published) == 1:
        master = published[0]

    if not master:
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
            master = from_wizards[0].card_set

    if not master:
        master = queryset[0]

    _merge(queryset, master)
    modeladmin.message_user(request, u'All selected card sets was '
                            u'merged to {}'.format(master.name))

merge_card_sets.short_description = 'Merge card sets'


def cards_count(obj):
    return obj.cards_count
cards_count.short_description = 'Scraped Cards'


def cards_count_ok(obj):
    if not obj.cards_count:
        return False
    return obj.cards is None or obj.cards_count == obj.cards
cards_count_ok.boolean = True
cards_count_ok.short_description = 'Status'


class CardSetAdmin(TranslationAdmin):
    form = CardSetForm
    list_display = ('name', 'acronym', 'cards', cards_count, cards_count_ok, 'released_at', 'created_at',
                    'updated_at', 'is_published')
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

    def queryset(self, request):
        qs = super(CardSetAdmin, self).queryset(request)
        return qs.annotate(cards_count=Count('cardrelease__card'))

admin.site.register(models.CardSet, CardSetAdmin)
