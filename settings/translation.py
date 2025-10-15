from modeltranslation.translator import register, TranslationOptions
from .models import Doctor, Treatment


@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('name', 'specialization',)


@register(Treatment)
class TreatmentTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)
