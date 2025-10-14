from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'full_name', 'phone', 'source', 'status', 'created_at', 'notes']
        read_only_fields = ['id', 'created_at']


