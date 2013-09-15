from django.contrib import admin
from oracle import models
from oracle.forms import CardImageForm
from django.utils.html import mark_safe, escape


class CardImageAdmin(admin.ModelAdmin):
    form = CardImageForm
    list_display = ('mvid', 'artist', 'art_thumbnail',)
    ordering = ('mvid',)
    search_fields = ('mvid',)

    # I dont know, but list_select_related option does not work
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_select_related
    def queryset(self, request):
        return super(CardImageAdmin, self).queryset(request).select_related(
            'artist')

    def art_thumbnail(self, obj):
        url = obj.file and obj.file.url or obj.scan
        return mark_safe(u'<img src="{0}"/>'.format(escape(url)))
    art_thumbnail.allow_tags = True

admin.site.register(models.CardImage, CardImageAdmin)
