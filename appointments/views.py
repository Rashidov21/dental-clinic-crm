from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Appointment
import json


def appointment_list(request):
    if request.method == 'GET':
        qs = Appointment.objects.select_related('patient').all().order_by('-date', '-time')
        patient_id = request.GET.get('patient')
        status = request.GET.get('status')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        if status:
            qs = qs.filter(status=status)
        data = [
            {
                **model_to_dict(a, fields=['id', 'doctor_name', 'service', 'date', 'time', 'status', 'price', 'notes']),
                'patient': a.patient_id,
            }
            for a in qs
        ]
        return JsonResponse({'results': data})
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def appointment_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    data = json.loads(request.body or '{}')
    appt = Appointment.objects.create(
        patient_id=data.get('patient'),
        doctor_name=data.get('doctor_name', ''),
        service=data.get('service', ''),
        date=data.get('date'),
        time=data.get('time'),
        status=data.get('status', 'scheduled'),
        price=data.get('price', 0),
        notes=data.get('notes', ''),
    )
    return JsonResponse(model_to_dict(appt), status=201)


@csrf_exempt
def appointment_update(request, pk: int):
    if request.method not in ['POST', 'PUT', 'PATCH']:
        return HttpResponseNotAllowed(['POST', 'PUT', 'PATCH'])
    appt = get_object_or_404(Appointment, pk=pk)
    data = json.loads(request.body or '{}')
    for field in ['patient', 'doctor_name', 'service', 'date', 'time', 'status', 'price', 'notes']:
        if field in data:
            if field == 'patient':
                appt.patient_id = data['patient']
            else:
                setattr(appt, field, data[field])
    appt.save()
    # Auto-create receipt when completed
    if appt.status == 'completed' and not hasattr(appt, 'receipt'):
        from receipts.models import Receipt
        Receipt.objects.create(
            appointment=appt,
            total_amount=appt.price,
            services_done=appt.notes or appt.service,
        )
    return JsonResponse(model_to_dict(appt))


@csrf_exempt
def appointment_delete(request, pk: int):
    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])
    appt = get_object_or_404(Appointment, pk=pk)
    appt.delete()
    return JsonResponse({'deleted': True})


