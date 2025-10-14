from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Payment
import json
from datetime import datetime


def payment_list(request):
    if request.method == 'GET':
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
        data = [
            {
                **model_to_dict(p, fields=['id', 'amount', 'payment_type', 'status', 'date', 'notes']),
                'patient': p.patient_id,
            }
            for p in qs
        ]
        return JsonResponse({'results': data})
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def payment_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    data = json.loads(request.body or '{}')
    payment = Payment.objects.create(
        patient_id=data.get('patient'),
        amount=data.get('amount', 0),
        payment_type=data.get('payment_type', 'cash'),
        status=data.get('status', 'paid'),
        date=data.get('date') or datetime.utcnow().isoformat(),
        notes=data.get('notes', ''),
    )
    return JsonResponse(model_to_dict(payment), status=201)


