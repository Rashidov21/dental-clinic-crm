from modeltranslation.translator import register, TranslationOptions
from .models import Receipt


@register(Receipt)
class ReceiptTranslationOptions(TranslationOptions):
    fields = ('services_done',)


