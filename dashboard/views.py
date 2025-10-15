from django.shortcuts import render
from django.utils.timezone import localdate
from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from payments.models import Payment
from leads.models import Lead
from settings.models import Doctor, Treatment


def dashboard_summary(request):
    today = localdate()
    total_patients = Patient.objects.count() or 0
    total_appointments_today = Appointment.objects.filter(date=today).count() 
    appointments = Appointment.objects.filter(status='scheduled').order_by('time')[:7]
    completed_appointments = Appointment.objects.filter(status='completed', date=today).count()
    total_income = Payment.objects.filter(status='paid').aggregate(total=models.Sum('amount'))['total'] 
    today_income = Payment.objects.filter(status='paid', date=today).aggregate(total=models.Sum('amount'))['total']
    # leads this calendar month
    first_day = today.replace(day=1)
    leads_this_month = Lead.objects.filter(created_at__date__gte=first_day).count()
    new_leads = Lead.objects.filter(status='new').count()
    contacted_leads = Lead.objects.filter(status='contacted').count()
    converted_leads = Lead.objects.filter(status='converted').count()
    lost_leads = Lead.objects.filter(status='lost').count()
    # Settings data
    total_doctors = Doctor.objects.filter(is_active=True).count()
    total_treatments = Treatment.objects.filter(is_active=True).count()
    
    # Get doctors and treatments for the modal
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    treatments = Treatment.objects.filter(is_active=True).order_by('name')
    
    context = {
        'total_patients': total_patients,
        'total_appointments_today': total_appointments_today,
        'total_income': float(total_income),
        'today_income': today_income,
        'leads_this_month': leads_this_month,
        'total_doctors': total_doctors,
        'total_treatments': total_treatments,
        'doctors': doctors,
        'treatments': treatments,
        'appointments': appointments,
        'completed_appointments': completed_appointments,
        'new_leads': new_leads,
        'contacted_leads': contacted_leads,
        'converted_leads': converted_leads,
        'lost_leads': lost_leads,
    }
    return render(request, 'index.html', context)


def doctor_dashboard(request):
    """Doctor dashboard with doctor-specific information"""
    try:
        today = localdate()
        
        # Get all active doctors
        doctors = Doctor.objects.filter(is_active=True).order_by('name')
        print(doctors)
        # Get today's appointments
        today_appointments = Appointment.objects.filter(date=today).order_by('time')
        print(today_appointments)
        # Get upcoming appointments (next 7 days)
        from datetime import timedelta
        next_week = today + timedelta(days=7)
        upcoming_appointments = Appointment.objects.filter(
            date__range=[today, next_week]
        ).order_by('date', 'time')
        
        # Get recent patients (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        recent_patients = Patient.objects.filter(
            created_at__date__gte=thirty_days_ago
        ).order_by('-created_at')[:10]
        
        # Get doctor statistics
        total_appointments = Appointment.objects.count()
        total_patients = Patient.objects.count()
        
        context = {
            'doctors': doctors,
            'today_appointments': today_appointments,
            'upcoming_appointments': upcoming_appointments,
            'recent_patients': recent_patients,
            'total_appointments': total_appointments,
            'total_patients': total_patients,
            'today': today,
        }
        return render(request, 'doctor-dashboard.html', context)
    except Exception as e:
        # Fallback context in case of errors
        context = {
            'doctors': [],
            'today_appointments': [],
            'upcoming_appointments': [],
            'recent_patients': [],
            'total_appointments': 0,
            'total_patients': 0,
            'today': localdate(),
        }
        return render(request, 'doctor-dashboard.html', context)


