from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.utils.safestring import mark_safe

from oracle import models
from oracle.admin.card_l10n import CardL10nInline


class CardReleaseInline(admin.TabularInline):
    model = models.CardRelease
    extra = 0
    readonly_fields = ('release_link',)
    ordering = ('card_set__released_at', 'card_set__name', 'card_number')
    raw_id_fields = ('art',)
    related_lookup_fields = {
        'fk': ['art'],
    }

    def queryset(self, request):
        qs = super(CardReleaseInline, self).queryset(request)
        return qs.select_related('card', 'card_set', 'art')

    def release_link(self, instance):
        a, m = instance._meta.app_label, instance._meta.module_name
        url = reverse('admin:{}_{}_change'.format(a, m), args=[instance.pk])
        # TODO use small and croped thumb for the card
        art = instance.art
        return mark_safe(u'<a href="{u}"><img src="{i}" /></a>'.format(
            u=url, i=art.file.url if art.file.name else art.scan))
    release_link.description = 'Edit Release'


def l10n_count(obj):
    return obj.l10n_count
l10n_count.short_description = 'L10n Count'


class CardReleaseAdmin(admin.ModelAdmin):
    model = models.CardRelease

    list_display = ('card_set', 'card', 'card_number', l10n_count)
    list_display_links = ('card',)
    list_filter = ('card_set__name',)
    ordering = ('-card_set__released_at', 'card_set__name', 'card_number')

    readonly_fields = ('card_set', 'card', 'art')
    fieldsets = (
        (None, {
            'fields': (
                ('card', 'card_set'),
                ('rarity', 'card_number'),
                ('art',),
            ),
        }),
    )
    inlines = [CardL10nInline]

    def queryset(self, request):
        qs = super(CardReleaseAdmin, self).queryset(request)
        return qs.select_related(
            'card', 'card_set', 'art'
        ).annotate(
            l10n_count=Count('cardl10n')
        )

admin.site.register(models.CardRelease, CardReleaseAdmin)
