from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Patient
import json


def patient_list(request):
    if request.method == 'GET':
        patients = list(Patient.objects.all().order_by('full_name').values())
        return JsonResponse({'results': patients})
    return HttpResponseNotAllowed(['GET'])


def patient_detail(request, pk: int):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    patient = get_object_or_404(Patient, pk=pk)
    return JsonResponse(model_to_dict(patient))


@csrf_exempt
def patient_update(request, pk: int):
    if request.method not in ['POST', 'PUT', 'PATCH']:
        return HttpResponseNotAllowed(['POST', 'PUT', 'PATCH'])
    patient = get_object_or_404(Patient, pk=pk)
    data = json.loads(request.body or '{}')
    for field in ['full_name', 'phone', 'email', 'birth_date', 'address', 'notes']:
        if field in data:
            setattr(patient, field, data[field])
    patient.save()
    return JsonResponse(model_to_dict(patient))


@csrf_exempt
def patient_delete(request, pk: int):
    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return JsonResponse({'deleted': True})


