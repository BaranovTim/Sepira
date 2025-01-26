from django.shortcuts import redirect
from .models import Warehouse_stock
import qrcode
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from .models import QRScan, Item

@login_required(login_url='profile')
def qr_scanner(request):
    if request.method == "POST":
        data = request.POST.get("barcode_data", "").strip()
        current_url = request.path
        try:
            item = Item.objects.get(name=data)

            action = None
            if 'action_add' in current_url:
                action = 'added'
            elif 'action_take' in current_url:
                action = 'took'
            elif 'action_remove' in current_url:
                action = 'removed'
            elif 'action_return' in current_url:
                action = 'returned'

            if action:
                QRScan.objects.create(
                    scanned_by=request.user,
                    item=item,
                    scanned_at=datetime.now(),
                    action=action
                )
                return JsonResponse({'success': True, 'redirect_url': 'quantity/'})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'redirect_url': '/home/'})

    return render(request, 'qrcodes/qr_scanner.html')

import io
import base64

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validate input
        if not name:
            return JsonResponse({'status': 'error', 'message': 'Name is required'})

        # Generate QR code
        qr_code = qrcode.make(name)

        # Сохранение QR-кода в формате Base64
        buffer = io.BytesIO()
        qr_code.save(buffer, format="PNG")
        buffer.seek(0)
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Create and save the new item in the database
        item = Item.objects.create(
            name=name,
            description=description,
            qr_code_base64=qr_code_base64
        )
        Warehouse_stock.objects.create(item=item, quantity=0)
        item.save()

        # Set location_name
        if 1 <= item.id <= 100:
            item.location_name = 'A1'
        elif 101 <= item.id <= 200:
            item.location_name = 'A2'
        elif 201 <= item.id <= 300:
            item.location_name = 'A3'
        elif 301 <= item.id <= 400:
            item.location_name = 'A4'
        elif 401 <= item.id <= 500:
            item.location_name = 'A5'
        item.save()

        return redirect('home')

    return render(request, 'qrcodes/add_item.html')