from django.shortcuts import render, get_object_or_404
from .models import Receipt
from payments.models import Payment


def receipt_list(request):
    payment_id = request.GET.get('payment_id')
    
    if payment_id:
        # Show receipt for specific payment
        try:
            payment = get_object_or_404(Payment, id=payment_id)
            # Create a receipt context for the payment
            receipt_data = {
                'payment': payment,
                'patient': payment.patient,
                'amount': payment.amount,
                'payment_type': payment.get_payment_type_display(),
                'date': payment.date,
                'status': payment.get_status_display(),
                'notes': payment.notes,
            }
            return render(request, 'receipt.html', {'receipt_data': receipt_data, 'is_payment_receipt': True})
        except Payment.DoesNotExist:
            pass
    
    # Default: show all receipts
    receipts = Receipt.objects.select_related('appointment').all().order_by('-created_at')
    return render(request, 'receipt.html', {'receipts': receipts})


def receipt_detail(request, pk: int):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt.html', {'receipt': receipt})


