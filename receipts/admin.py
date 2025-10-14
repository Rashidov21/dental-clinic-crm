from django.contrib import admin
from .models import Receipt


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('appointment__patient__full_name',)


