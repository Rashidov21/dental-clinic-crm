from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Patient
from settings.models import Doctor, Treatment
from appointments.models import Appointment


def patient_list(request):
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    doctor_filter = request.GET.get('doctor', '')
    date_filter = request.GET.get('date', '')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    patients = Patient.objects.all().order_by('-id')
    
    # Apply search filter
    if search_query:
        patients = patients.filter(
            full_name__icontains=search_query
        ) | patients.filter(
            phone__icontains=search_query
        ) | patients.filter(
            email__icontains=search_query
        )
    
    # Apply status filter (based on appointment status)
    if status_filter:
        if status_filter == 'has_appointments':
            patients = patients.filter(appointments__isnull=False).distinct()
        elif status_filter == 'no_appointments':
            patients = patients.filter(appointments__isnull=True)
        elif status_filter == 'upcoming_appointments':
            patients = patients.filter(
                appointments__date__gte=timezone.now().date(),
                appointments__status='scheduled'
            ).distinct()
        elif status_filter == 'completed_appointments':
            patients = patients.filter(
                appointments__status='completed'
            ).distinct()
    
    # Apply doctor filter (based on appointments)
    if doctor_filter:
        patients = patients.filter(
            appointments__doctor_id=doctor_filter
        ).distinct()
    
    # Apply date filter (based on appointment dates)
    if date_filter:
        if date_filter == 'today':
            patients = patients.filter(
                appointments__date=timezone.now().date()
            ).distinct()
        elif date_filter == 'week':
            week_start = timezone.now() - timedelta(days=timezone.now().weekday())
            patients = patients.filter(
                appointments__date__gte=week_start.date()
            ).distinct()
        elif date_filter == 'month':
            month_start = timezone.now().replace(day=1)
            patients = patients.filter(
                appointments__date__gte=month_start.date()
            ).distinct()
        elif date_filter == 'recent':
            recent_date = timezone.now().date() - timedelta(days=30)
            patients = patients.filter(
                appointments__date__gte=recent_date
            ).distinct()
    
    # Get counts for filter buttons
    total_patients = Patient.objects.count()
    has_appointments_count = Patient.objects.filter(appointments__isnull=False).distinct().count()
    no_appointments_count = Patient.objects.filter(appointments__isnull=True).count()
    upcoming_count = Patient.objects.filter(
        appointments__date__gte=timezone.now().date(),
        appointments__status='scheduled'
    ).distinct().count()
    completed_count = Patient.objects.filter(
        appointments__status='completed'
    ).distinct().count()
    
    # Get date counts
    today_count = Patient.objects.filter(
        appointments__date=timezone.now().date()
    ).distinct().count()
    week_start = timezone.now() - timedelta(days=timezone.now().weekday())
    week_count = Patient.objects.filter(
        appointments__date__gte=week_start.date()
    ).distinct().count()
    month_start = timezone.now().replace(day=1)
    month_count = Patient.objects.filter(
        appointments__date__gte=month_start.date()
    ).distinct().count()
    recent_count = Patient.objects.filter(
        appointments__date__gte=timezone.now().date() - timedelta(days=30)
    ).distinct().count()
    
    # Get doctors and treatments for filter dropdowns
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    treatments = Treatment.objects.filter(is_active=True).order_by('name')
    
    context = {
        'patients': patients,
        'doctors': doctors,
        'treatments': treatments,
        'status_filter': status_filter,
        'doctor_filter': doctor_filter,
        'date_filter': date_filter,
        'search_query': search_query,
        'total_patients': total_patients,
        'has_appointments_count': has_appointments_count,
        'no_appointments_count': no_appointments_count,
        'upcoming_count': upcoming_count,
        'completed_count': completed_count,
        'today_count': today_count,
        'week_count': week_count,
        'month_count': month_count,
        'recent_count': recent_count,
    }
    return render(request, 'clients.html', context)


def patient_detail(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    treatments = Treatment.objects.filter(is_active=True).order_by('name')
    return render(request, 'patient.html', {'patient': patient, 'doctors': doctors, 'treatments': treatments})


def patient_update(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.full_name = request.POST.get('full_name', patient.full_name)
        patient.phone = request.POST.get('phone', patient.phone)
        patient.email = request.POST.get('email', patient.email)
        patient.birth_date = request.POST.get('birth_date', patient.birth_date)
        patient.address = request.POST.get('address', patient.address)
        patient.notes = request.POST.get('notes', patient.notes)
        patient.save()
        messages.success(request, 'Patient updated successfully!')
        return redirect('patient_detail', pk=pk)
    return redirect('patient_detail', pk=pk)


def patient_delete(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    messages.success(request, 'Patient deleted successfully!')
    return redirect('clients')


def patient_create_with_booking(request):
    """Create a new patient and book an appointment"""
    if request.method == 'POST':
        try:
            # Create patient
            patient = Patient.objects.create(
                full_name=request.POST.get('full_name', ''),
                phone=request.POST.get('phone', ''),
                email=request.POST.get('email', ''),
                birth_date=request.POST.get('birth_date') or None,
                address=request.POST.get('address', ''),
            )
            
            # Get doctor and treatment
            doctor_id = request.POST.get('doctor')
            treatment_id = request.POST.get('treatment')
            
            doctor = None
            treatment = None
            
            if doctor_id:
                try:
                    doctor = Doctor.objects.get(id=doctor_id)
                except Doctor.DoesNotExist:
                    pass
            
            if treatment_id:
                try:
                    treatment = Treatment.objects.get(id=treatment_id)
                except Treatment.DoesNotExist:
                    pass
            
            # Create appointment
            if doctor and treatment:
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    treatment=treatment,
                    doctor_name=doctor.name,
                    service=treatment.name,
                    date=request.POST.get('date'),
                    time=request.POST.get('time'),
                    status='scheduled',
                    price=treatment.price,
                    notes=request.POST.get('notes', ''),
                )
                messages.success(request, f'Patient "{patient.full_name}" created and appointment booked successfully!')
            else:
                messages.success(request, f'Patient "{patient.full_name}" created successfully!')
            
            return redirect('dashboard_summary')
            
        except Exception as e:
            messages.error(request, f'Error creating patient: {str(e)}')
            return redirect('dashboard_summary')
    
    return redirect('dashboard_summary')


