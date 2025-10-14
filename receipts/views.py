from django.http import JsonResponse, HttpResponseNotAllowed
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Receipt


def receipt_list(request):
    if request.method == 'GET':
        qs = Receipt.objects.select_related('appointment').all().order_by('-created_at')
        data = [
            {
                **model_to_dict(r, fields=['id', 'total_amount', 'created_at', 'services_done']),
                'appointment': r.appointment_id,
            }
            for r in qs
        ]
        return JsonResponse({'results': data})
    return HttpResponseNotAllowed(['GET'])


def receipt_detail(request, pk: int):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    r = get_object_or_404(Receipt, pk=pk)
    data = model_to_dict(r, fields=['id', 'total_amount', 'created_at', 'services_done'])
    data['appointment'] = r.appointment_id
    return JsonResponse(data)


