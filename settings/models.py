from django.db import models
from django.utils.translation import gettext_lazy as _


class Doctor(models.Model):
    """Doctor model for managing clinic doctors"""
    name = models.CharField(max_length=100, verbose_name=_("Doctor Name"))
    specialization = models.CharField(max_length=100, verbose_name=_("Specialization"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class Treatment(models.Model):
    """Treatment model for managing available treatments"""
    name = models.CharField(max_length=100, verbose_name=_("Treatment Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    duration_minutes = models.PositiveIntegerField(verbose_name=_("Duration (minutes)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Treatment")
        verbose_name_plural = _("Treatments")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - ${self.price}"