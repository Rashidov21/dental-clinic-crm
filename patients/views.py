from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Patient


def patient_list(request):
    patients = Patient.objects.all().order_by('full_name')
    return render(request, 'clients.html', {'patients': patients})


def patient_detail(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patient.html', {'patient': patient})


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
    return redirect('patient_list')


