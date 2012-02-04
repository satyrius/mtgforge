from django.contrib import admin
from oracle import models


class ArtistAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Artist, ArtistAdmin)
