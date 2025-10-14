from modeltranslation.translator import register, TranslationOptions
from .models import Patient


@register(Patient)
class PatientTranslationOptions(TranslationOptions):
    fields = ('full_name', 'address', 'notes',)


