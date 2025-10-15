from django.shortcuts import render, get_object_or_404
from .models import Receipt


def receipt_list(request):
    receipts = Receipt.objects.select_related('appointment').all().order_by('-created_at')
    return render(request, 'receipt.html', {'receipts': receipts})


def receipt_detail(request, pk: int):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt.html', {'receipt': receipt})


