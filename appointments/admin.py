from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor_name', 'service', 'date', 'time', 'status', 'price')
    list_filter = ('status', 'date', 'doctor_name')
    search_fields = ('patient__full_name', 'doctor_name', 'service')


