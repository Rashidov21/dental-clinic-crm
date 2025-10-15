from django.db import models
from django.contrib.auth import get_user_model


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('settings.Doctor', on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    doctor_user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='doctor_appointments')
    treatment = models.ForeignKey('settings.Treatment', on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    # Legacy fields for migration compatibility
    doctor_name = models.CharField(max_length=255, blank=True)
    service = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.patient.full_name} — {self.treatment.name} on {self.date} {self.time}"


