from django.conf import settings
from django.utils import translation


def translation_aware(func):
    def wrapper(self, *args, **options):
        translation.activate(settings.MODELTRANSLATION_DEFAULT_LANGUAGE)
        func(self, *args, **options)
        translation.deactivate()
    return wrapper
