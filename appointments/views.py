from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Appointment
from settings.models import Doctor, Treatment


def appointment_list(request):
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    doctor_filter = request.GET.get('doctor', '')
    date_filter = request.GET.get('date', '')
    time_filter = request.GET.get('time', '')
    
    # Base queryset
    appointments = Appointment.objects.select_related('patient', 'doctor', 'treatment').all().order_by('-date', '-time')
    
    # Apply status filter
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Apply doctor filter
    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)
    
    # Apply date filter
    if date_filter:
        if date_filter == 'today':
            appointments = appointments.filter(date=timezone.now().date())
        elif date_filter == 'week':
            week_start = timezone.now() - timedelta(days=timezone.now().weekday())
            appointments = appointments.filter(date__gte=week_start.date())
        elif date_filter == 'month':
            month_start = timezone.now().replace(day=1)
            appointments = appointments.filter(date__gte=month_start.date())
        elif date_filter == 'upcoming':
            appointments = appointments.filter(date__gte=timezone.now().date())
    
    # Apply time filter
    if time_filter:
        if time_filter == 'morning':
            appointments = appointments.filter(time__lt='12:00')
        elif time_filter == 'afternoon':
            appointments = appointments.filter(time__gte='12:00', time__lt='17:00')
        elif time_filter == 'evening':
            appointments = appointments.filter(time__gte='17:00')
    
    # Get counts for filter buttons
    total_appointments = Appointment.objects.count()
    today_count = Appointment.objects.filter(date=timezone.now().date()).count()
    week_start = timezone.now() - timedelta(days=timezone.now().weekday())
    week_count = Appointment.objects.filter(date__gte=week_start.date()).count()
    month_start = timezone.now().replace(day=1)
    month_count = Appointment.objects.filter(date__gte=month_start.date()).count()
    upcoming_count = Appointment.objects.filter(date__gte=timezone.now().date()).count()
    
    # Get status counts
    status_counts = {
        'scheduled': Appointment.objects.filter(status='scheduled').count(),
        'completed': Appointment.objects.filter(status='completed').count(),
        'cancelled': Appointment.objects.filter(status='cancelled').count(),
        'no_show': Appointment.objects.filter(status='no_show').count(),
    }
    
    # Get doctors for filter dropdown
    from settings.models import Doctor
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
        'doctor_filter': doctor_filter,
        'date_filter': date_filter,
        'time_filter': time_filter,
        'total_appointments': total_appointments,
        'today_count': today_count,
        'week_count': week_count,
        'month_count': month_count,
        'upcoming_count': upcoming_count,
        'status_counts': status_counts,
        'doctors': doctors,
    }
    return render(request, 'calendar.html', context)


def appointment_create(request):
    if request.method == 'POST':
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
        
        appt = Appointment.objects.create(
            patient_id=request.POST.get('patient'),
            doctor=doctor,
            treatment=treatment,
            doctor_name=doctor.name if doctor else '',
            service=treatment.name if treatment else '',
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            status=request.POST.get('status', 'scheduled'),
            price=request.POST.get('price', 0),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Appointment created successfully!')
        return redirect('book_page')
    return redirect('book_page')


def appointment_update(request, pk: int):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appt.patient_id = request.POST.get('patient', appt.patient_id)
        appt.doctor_name = request.POST.get('doctor_name', appt.doctor_name)
        appt.service = request.POST.get('service', appt.service)
        appt.date = request.POST.get('date', appt.date)
        appt.time = request.POST.get('time', appt.time)
        appt.status = request.POST.get('status', appt.status)
        appt.price = request.POST.get('price', appt.price)
        appt.notes = request.POST.get('notes', appt.notes)
        appt.save()
        
        # Auto-create receipt when completed
        if appt.status == 'completed' and not hasattr(appt, 'receipt'):
            from receipts.models import Receipt
            Receipt.objects.create(
                appointment=appt,
                total_amount=appt.price,
                services_done=appt.notes or appt.service,
            )
        messages.success(request, 'Appointment updated successfully!')
        return redirect('book_page')
    return redirect('book_page')


def appointment_delete(request, pk: int):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.delete()
    messages.success(request, 'Appointment deleted successfully!')
    return redirect('book_page')


def book_page(request):
    """Book appointment page with doctors and treatments"""
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    treatments = Treatment.objects.filter(is_active=True).order_by('name')
    appointments = Appointment.objects.all().order_by('-date', '-time')[:10]  # Recent appointments
    
    context = {
        'doctors': doctors,
        'treatments': treatments,
        'appointments': appointments,
    }
    return render(request, 'book.html', context)


