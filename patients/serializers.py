from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'phone', 'email', 'birth_date', 'address', 'notes']
        read_only_fields = ['id']


