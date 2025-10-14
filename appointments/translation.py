from modeltranslation.translator import register, TranslationOptions
from .models import Appointment


@register(Appointment)
class AppointmentTranslationOptions(TranslationOptions):
    fields = ('doctor_name', 'service', 'notes',)


