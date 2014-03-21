from modeltranslation.translator import translator, TranslationOptions
from oracle.models import CardSet


class CardSetTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en',)

translator.register(CardSet, CardSetTranslationOptions)
