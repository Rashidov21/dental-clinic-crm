from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Appointment


def appointment_list(request):
    qs = Appointment.objects.select_related('patient').all().order_by('-date', '-time')
    patient_id = request.GET.get('patient')
    status = request.GET.get('status')
    if patient_id:
        qs = qs.filter(patient_id=patient_id)
    if status:
        qs = qs.filter(status=status)
    return render(request, 'appointments/appointment_list.html', {'appointments': qs})


def appointment_create(request):
    if request.method == 'POST':
        appt = Appointment.objects.create(
            patient_id=request.POST.get('patient'),
            doctor_name=request.POST.get('doctor_name', ''),
            service=request.POST.get('service', ''),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            status=request.POST.get('status', 'scheduled'),
            price=request.POST.get('price', 0),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Appointment created successfully!')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_form.html')


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
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_form.html', {'appointment': appt})


def appointment_delete(request, pk: int):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.delete()
    messages.success(request, 'Appointment deleted successfully!')
    return redirect('appointment_list')


