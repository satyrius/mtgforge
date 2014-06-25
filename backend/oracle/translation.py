from modeltranslation.translator import translator, TranslationOptions
from oracle.models import CardSet


class CardSetTranslationOptions(TranslationOptions):
    fields = ('name',)
    empty_values = None
    required_languages = ('en',)

translator.register(CardSet, CardSetTranslationOptions)
