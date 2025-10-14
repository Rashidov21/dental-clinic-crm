from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor_name', 'doctor_user', 'service', 'date', 'time',
            'status', 'price', 'notes'
        ]
        read_only_fields = ['id']


