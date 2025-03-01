from django.shortcuts import render, redirect
from rest_framework.exceptions import PermissionDenied

from qrcodes.models import QRScan, Warehouse_stock
from django.contrib.auth.decorators import login_required
from notifypy import Notify


def notification(message, title):
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.send()

import csv
from django.http import HttpResponse

def download_qrscans_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qrscans.csv"'

    writer = csv.writer(response)
    writer.writerow(["Scanned By", "Action", "Quantity", "Item Name", "Scanned At", 'Invoice photo', 'Invoice id'])

    for scan in QRScan.objects.all():
        writer.writerow([
            scan.scanned_by,
            scan.action,
            scan.quantity,
            scan.item.name,
            scan.scanned_at,
            scan.invoice_photo,
            scan.invoice_id
        ])

    return response


@login_required(login_url='profile')
def quantity(request):
    current_url = request.path
    last_scan = QRScan.objects.last()
    stock = Warehouse_stock.objects.get(item=last_scan.item)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        try:
            invoice_id = int(request.POST.get('invoice_id'))
            invoice_image = request.POST.get('invoice_image')
        except (TypeError, ValueError):
            invoice_id = None
            invoice_image = None

        if 1 <= quantity:
            last_scan.quantity = quantity
            last_scan.invoice_id = invoice_id
            last_scan.invoice_photo = invoice_image
            last_scan.save()

            if 'action_add' in current_url:
                stock.quantity += quantity
                stock.save()

                return redirect('home')
            if 'action_take' in current_url:
                if (stock.quantity - quantity) < 0:
                    notification('Not enough items in a warehouse, please insert the right quantity', 'AmountError')
                else:
                    stock.quantity = max(stock.quantity - quantity, 0)
                    stock.save()
                    return redirect('home')
            if 'action_remove' in current_url:
                if (stock.quantity - quantity) < 0:
                    notification('Not enough items in a warehouse, please insert the right quantity', 'AmountError')
                else:
                    stock.quantity = max(stock.quantity - quantity, 0)
                    stock.save()
                    return redirect('home')
            if 'action_return' in current_url:
                stock.quantity += quantity
                stock.save()
                return redirect('home')

    return render(request, 'quantity/quantity.html', {'last_scan': last_scan})