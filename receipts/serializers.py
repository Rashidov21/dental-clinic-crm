from rest_framework import serializers
from .models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'appointment', 'total_amount', 'created_at', 'services_done']
        read_only_fields = ['id', 'created_at']


