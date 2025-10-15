from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Lead
from settings.models import Doctor


def lead_list(request):
    leads = Lead.objects.all().order_by('-created_at')
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    time_filter = request.GET.get('time', '')
    
    # Apply status filter
    if status_filter:
        leads = leads.filter(status=status_filter)
    
    # Apply time filters
    now = timezone.now()
    today = now.date()
    
    if time_filter == 'today':
        leads = leads.filter(created_at__date=today)
    elif time_filter == 'week':
        week_ago = today - timedelta(days=7)
        leads = leads.filter(created_at__date__gte=week_ago)
    elif time_filter == 'month':
        month_ago = today - timedelta(days=30)
        leads = leads.filter(created_at__date__gte=month_ago)
    
    # Get filter counts for display
    total_leads = Lead.objects.count()
    today_count = Lead.objects.filter(created_at__date=today).count()
    week_count = Lead.objects.filter(created_at__date__gte=today - timedelta(days=7)).count()
    month_count = Lead.objects.filter(created_at__date__gte=today - timedelta(days=30)).count()
    
    # Status counts
    status_counts = {}
    for status_choice in Lead.STATUS_CHOICES:
        status_counts[status_choice[0]] = Lead.objects.filter(status=status_choice[0]).count()
    
    context = {
        'leads': leads,
        'doctors': doctors,
        'status_filter': status_filter,
        'time_filter': time_filter,
        'total_leads': total_leads,
        'today_count': today_count,
        'week_count': week_count,
        'month_count': month_count,
        'status_counts': status_counts,
    }
    return render(request, 'leads.html', context)


def lead_create(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('assigned_doctor')
        doctor = None
        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
            except Doctor.DoesNotExist:
                pass
        
        lead = Lead.objects.create(
            full_name=request.POST.get('full_name', ''),
            phone=request.POST.get('phone', ''),
            source=request.POST.get('source', ''),
            assigned_doctor=doctor,
            status=request.POST.get('status', 'new'),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Lead created successfully!')
        return redirect('leads_page')
    return redirect('leads_page')


def lead_update(request, pk: int):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        doctor_id = request.POST.get('assigned_doctor')
        doctor = None
        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
            except Doctor.DoesNotExist:
                pass
        
        lead.full_name = request.POST.get('full_name', lead.full_name)
        lead.phone = request.POST.get('phone', lead.phone)
        lead.source = request.POST.get('source', lead.source)
        lead.assigned_doctor = doctor
        lead.status = request.POST.get('status', lead.status)
        lead.notes = request.POST.get('notes', lead.notes)
        lead.save()
        messages.success(request, 'Lead updated successfully!')
        return redirect('leads_page')
    return redirect('leads_page')


def lead_delete(request, pk: int):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.success(request, 'Lead deleted successfully!')
    return redirect('leads_page')


