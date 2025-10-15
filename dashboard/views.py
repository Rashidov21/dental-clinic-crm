from django.shortcuts import render
from django.utils.timezone import localdate
from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from payments.models import Payment
from leads.models import Lead


def dashboard_summary(request):
    today = localdate()
    total_patients = Patient.objects.count() or 0
    total_appointments_today = Appointment.objects.filter(date=today).count() or 0
    total_income = Payment.objects.filter(status='paid').aggregate(total=models.Sum('amount'))['total'] or 0
    # leads this calendar month
    first_day = today.replace(day=1)
    leads_this_month = Lead.objects.filter(created_at__date__gte=first_day).count() or 0
    
    context = {
        'total_patients': total_patients,
        'total_appointments_today': total_appointments_today,
        'total_income': float(total_income),
        'leads_this_month': leads_this_month,
    }
    return render(request, 'index.html', context)


