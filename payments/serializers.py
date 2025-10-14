from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'patient', 'amount', 'payment_type', 'status', 'date', 'notes']
        read_only_fields = ['id']


