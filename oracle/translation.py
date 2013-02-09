from modeltranslation.translator import translator, TranslationOptions
from oracle.models import CardSet
from django.db.models.signals import pre_save
from modeltranslation.utils import get_language, build_localized_fieldname


class CardSetTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(CardSet, CardSetTranslationOptions)


# Workaround with missing default translation problem
# http://code.google.com/p/django-modeltranslation/wiki/InstallationAndUsage03#Caveats
def set_default_translation(sender, instance, **kwargs):
    field_name = 'name'
    lang = get_language()
    loc_field_name = build_localized_fieldname(field_name, lang)
    val = getattr(instance, loc_field_name, None)
    if not val:
        setattr(instance, loc_field_name, getattr(instance, field_name))

pre_save.connect(set_default_translation, CardSet)
