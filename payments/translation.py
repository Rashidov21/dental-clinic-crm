from modeltranslation.translator import register, TranslationOptions
from .models import Payment


@register(Payment)
class PaymentTranslationOptions(TranslationOptions):
    fields = ('notes',)


