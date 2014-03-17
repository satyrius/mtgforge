from django.contrib import admin
from django.utils.safestring import mark_safe

from oracle import models
from oracle.forms import CardL10nForm


class CardL10nInline(admin.StackedInline):
    form = CardL10nForm
    model = models.CardL10n
    readonly_fields = ('scan', 'card_release', 'card_face', 'language',
                       'type_line', 'mvid')
    extra = 0
    raw_id_fields = ('art',)
    related_lookup_fields = {
        'fk': ['art'],
    }
    inline_classes = ('grp-collapse grp-open',)
    fieldsets = (
        (None, {
            'fields': (
                ('scan', 'language', 'type_line', 'mvid'),
                'name',
                'rules',
                'flavor',
            )
        }),
    )

    class Media:
        css = {
            'screen': ('/static/admin/css/card_l10n_inline.css',),
        }

    def scan(self, instance):
        # TODO use small and croped thumb for the card
        art = instance.art
        return mark_safe(u'<img src="{i}" />'.format(
            i=art.file.url if art.file.name else art.scan))
    scan.description = 'Card Scan'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
