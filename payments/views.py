from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Payment
from datetime import datetime
from settings.models import Doctor, Treatment


def payment_list(request):
    qs = Payment.objects.select_related('patient').all().order_by('-date')
    patient_id = request.GET.get('patient')
    start = request.GET.get('start')
    end = request.GET.get('end')
    if patient_id:
        qs = qs.filter(patient_id=patient_id)
    if start:
        try:
            start_dt = datetime.fromisoformat(start)
            qs = qs.filter(date__gte=start_dt)
        except ValueError:
            pass
    if end:
        try:
            end_dt = datetime.fromisoformat(end)
            qs = qs.filter(date__lte=end_dt)
        except ValueError:
            pass
    
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    treatments = Treatment.objects.filter(is_active=True).order_by('name')
    return render(request, 'payments.html', {'payments': qs, 'doctors': doctors, 'treatments': treatments})


def payment_create(request):
    if request.method == 'POST':
        payment = Payment.objects.create(
            patient_id=request.POST.get('patient'),
            amount=request.POST.get('amount', 0),
            payment_type=request.POST.get('payment_type', 'cash'),
            status=request.POST.get('status', 'paid'),
            date=request.POST.get('date') or datetime.utcnow().isoformat(),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Payment created successfully!')
        return redirect('payment_list')
    return render(request, 'payments/payment_form.html')


