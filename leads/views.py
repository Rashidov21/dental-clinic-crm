from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Lead
from settings.models import Doctor


def lead_list(request):
    leads = Lead.objects.all().order_by('-created_at')
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    return render(request, 'leads.html', {'leads': leads, 'doctors': doctors})


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


