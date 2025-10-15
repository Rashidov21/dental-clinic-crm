from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Doctor, Treatment


def settings_page(request):
    """Main settings page with doctors and treatments management"""
    doctors = Doctor.objects.all().order_by('name')
    treatments = Treatment.objects.all().order_by('name')
    
    context = {
        'doctors': doctors,
        'treatments': treatments,
    }
    return render(request, 'settings.html', context)


# Doctor Management Views
def doctor_create(request):
    """Create a new doctor"""
    if request.method == 'POST':
        doctor = Doctor.objects.create(
            name=request.POST.get('name', ''),
            specialization=request.POST.get('specialization', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, _('Doctor created successfully!'))
        return redirect('settings_page')
    return redirect('settings_page')


def doctor_update(request, pk):
    """Update an existing doctor"""
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.name = request.POST.get('name', doctor.name)
        doctor.specialization = request.POST.get('specialization', doctor.specialization)
        doctor.phone = request.POST.get('phone', doctor.phone)
        doctor.email = request.POST.get('email', doctor.email)
        doctor.is_active = request.POST.get('is_active') == 'on'
        doctor.save()
        messages.success(request, _('Doctor updated successfully!'))
        return redirect('settings_page')
    return redirect('settings_page')


def doctor_delete(request, pk):
    """Delete a doctor"""
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    messages.success(request, _('Doctor deleted successfully!'))
    return redirect('settings_page')


# Treatment Management Views
def treatment_create(request):
    """Create a new treatment"""
    if request.method == 'POST':
        treatment = Treatment.objects.create(
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            price=request.POST.get('price', 0),
            duration_minutes=request.POST.get('duration_minutes', 30),
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, _('Treatment created successfully!'))
        return redirect('settings_page')
    return redirect('settings_page')


def treatment_update(request, pk):
    """Update an existing treatment"""
    treatment = get_object_or_404(Treatment, pk=pk)
    if request.method == 'POST':
        treatment.name = request.POST.get('name', treatment.name)
        treatment.description = request.POST.get('description', treatment.description)
        treatment.price = request.POST.get('price', treatment.price)
        treatment.duration_minutes = request.POST.get('duration_minutes', treatment.duration_minutes)
        treatment.is_active = request.POST.get('is_active') == 'on'
        treatment.save()
        messages.success(request, _('Treatment updated successfully!'))
        return redirect('settings_page')
    return redirect('settings_page')


def treatment_delete(request, pk):
    """Delete a treatment"""
    treatment = get_object_or_404(Treatment, pk=pk)
    treatment.delete()
    messages.success(request, _('Treatment deleted successfully!'))
    return redirect('settings_page')