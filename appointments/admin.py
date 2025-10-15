from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'treatment', 'date', 'time', 'status', 'price')
    list_filter = ('status', 'date', 'doctor', 'treatment')
    search_fields = ('patient__full_name', 'doctor__name', 'treatment__name')


