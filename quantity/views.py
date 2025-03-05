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
    response['Content-Disposition'] = 'attachment; filename="qr-scans.csv"'

    writer = csv.writer(response)
    writer.writerow(["Scanned By", "Action", "Quantity", "Item Name", "Scanned At", 'Invoice photo', 'Invoice id'])

    for scan in QRScan.objects.all():
        writer.writerow([
            scan.scanned_by,
            scan.action,
            scan.quantity,
            scan.item.name,
            scan.scanned_at,
            scan.invoice_photo.url if scan.invoice_photo else scan.invoice_photo,
            scan.invoice_id
        ])

    return response


@login_required(login_url='profile')
def quantity(request):
    current_url = request.path
    last_scan = QRScan.objects.last()
    stock = Warehouse_stock.objects.get(item=last_scan.item)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))

        # Получаем файл
        invoice_image = request.FILES.get('invoice_image')

        # Пытаемся получить ID
        try:
            invoice_id = int(request.POST.get('invoice_id'))
        except (TypeError, ValueError):
            invoice_id = None

        # Проверяем, что хотя бы одно из полей заполнено
        if not invoice_id and not invoice_image:
            notification('You have to add an id or a photo of an invoice', 'InvoiceError')
            return redirect(request.path)  # Перезагружаем страницу с ошибкой

        if quantity >= 1:
            last_scan.quantity = quantity
            last_scan.invoice_id = invoice_id

            # Сохраняем фото, если загружено
            if invoice_image:
                last_scan.invoice_photo = invoice_image

            last_scan.save()

            # Обновление количества на складе
            if 'action_add' in current_url:
                stock.quantity += quantity
                stock.save()
                return redirect('home')

            if 'action_take' in current_url:
                if stock.quantity - quantity < 0:
                    messages.error(request, 'Not enough items in the warehouse.')
                else:
                    stock.quantity = max(stock.quantity - quantity, 0)
                    stock.save()
                    return redirect('home')

            if 'action_remove' in current_url:
                if stock.quantity - quantity < 0:
                    messages.error(request, 'Not enough items in the warehouse.')
                else:
                    stock.quantity = max(stock.quantity - quantity, 0)
                    stock.save()
                    return redirect('home')

            if 'action_return' in current_url:
                stock.quantity += quantity
                stock.save()
                return redirect('home')

    return render(request, 'quantity/quantity.html', {'last_scan': last_scan})
