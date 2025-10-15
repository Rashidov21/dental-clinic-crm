from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    
    # Pagination
    paginator = Paginator(qs, 10)  # Show 10 payments per page
    page = request.GET.get('page')
    
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        payments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        payments = paginator.page(paginator.num_pages)
    
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    treatments = Treatment.objects.filter(is_active=True).order_by('name')
    
    context = {
        'payments': payments,
        'doctors': doctors,
        'treatments': treatments,
        'paginator': paginator,
    }
    return render(request, 'payments.html', context)


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
    return redirect('payments_page')


