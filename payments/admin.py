from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'payment_type', 'status', 'date')
    list_filter = ('payment_type', 'status', 'date')
    search_fields = ('patient__full_name',)


