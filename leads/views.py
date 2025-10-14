from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Lead
import json


def lead_list(request):
    if request.method == 'GET':
        leads = list(Lead.objects.all().order_by('-created_at').values())
        return JsonResponse({'results': leads})
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def lead_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    lead = Lead.objects.create(
        full_name=data.get('full_name', ''),
        phone=data.get('phone', ''),
        source=data.get('source', ''),
        status=data.get('status', 'new'),
        notes=data.get('notes', ''),
    )
    return JsonResponse(model_to_dict(lead), status=201)


@csrf_exempt
def lead_update(request, pk: int):
    if request.method not in ['POST', 'PUT', 'PATCH']:
        return HttpResponseNotAllowed(['POST', 'PUT', 'PATCH'])
    lead = get_object_or_404(Lead, pk=pk)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    for field in ['full_name', 'phone', 'source', 'status', 'notes']:
        if field in data:
            setattr(lead, field, data[field])
    lead.save()
    return JsonResponse(model_to_dict(lead))


@csrf_exempt
def lead_delete(request, pk: int):
    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    return JsonResponse({'deleted': True})


