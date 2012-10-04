from django.contrib import admin
from oracle import models
from oracle.admin.card_face import CardFaceInline
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count


class CardReleaseInline(admin.TabularInline):
    ordering = ('card_set__released_at', 'card_set__name', 'card_number',)
    model = models.CardRelease
    extra = 0


class PartsCountFilter(SimpleListFilter):
    title = _('parts count')

    parameter_name = 'parts'

    def lookups(self, request, model_admin):
        return (
            ('multipart', 'Multipart'),
            ('normal', 'Normal'),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(num_faces=Count('cardface'))
        if self.value() == 'multipart':
            return queryset.filter(num_faces__gt=1)
        if self.value() == 'normal':
            return queryset.filter(num_faces=1)


class CardAdmin(admin.ModelAdmin):
    inlines = [CardReleaseInline, CardFaceInline]
    list_filter = (PartsCountFilter, 'cardrelease__card_set__name',)
    ordering = ('name',)
    readonly_fields = ('name',)
    search_fields = ('name', 'cardface__cardl10n__name',)

admin.site.register(models.Card, CardAdmin)
