from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Patient
from settings.models import Doctor, Treatment
from appointments.models import Appointment


def patient_list(request):
    patients = Patient.objects.all().order_by('full_name')
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    treatments = Treatment.objects.filter(is_active=True).order_by('name')
    return render(request, 'clients.html', {'patients': patients, 'doctors': doctors, 'treatments': treatments})


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


