from django.db import models
from appointments.models import Appointment


class Receipt(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='receipt')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    services_done = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Receipt for {self.appointment} — ${self.total_amount}"


