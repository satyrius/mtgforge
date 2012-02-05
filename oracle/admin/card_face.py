from django.contrib import admin
from oracle import models


class CardFaceAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.CardFace, CardFaceAdmin)
