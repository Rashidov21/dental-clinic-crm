from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'birth_date')
    search_fields = ('full_name', 'phone', 'email')


