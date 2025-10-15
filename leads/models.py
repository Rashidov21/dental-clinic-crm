from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    source = models.CharField(max_length=100, blank=True)
    assigned_doctor = models.ForeignKey('settings.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.full_name} — {self.status}"


