from django.http import JsonResponse
import cv2
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import QRScan, Warehouse_stock
from .models import Item
from django.contrib.auth.models import User
from datetime import datetime
import qrcode
import os
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


@login_required(login_url='profile')
def qr_scanner(request):
    return render(request, 'qr_scanner.html')

@csrf_exempt
@login_required(login_url='profile')
def process_qr_scan(request):
    if request.method == "POST":
        data = json.loads(request.body).get("data", "").strip()
        try:
            item = Item.objects.get(name=data)
            # Дальнейшая обработка, как в вашем коде
            QRScan.objects.create(
                scanned_by=request.user,
                item=item,
                scanned_at=datetime.now(),
                action='added'  # Здесь задайте нужное действие
            )
            return JsonResponse({"redirect": "/quantity/"})
        except Item.DoesNotExist:
            return JsonResponse({"redirect": "/home/"})

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validate input
        if not name:
            return JsonResponse({'status': 'error', 'message': 'Name is required'})

        # Generate QR code
        qr_code = qrcode.make(name)
        qr_directory = os.path.join('media', 'qrcodes')
        os.makedirs(qr_directory, exist_ok=True)  # Ensure directory exists
        file_path = os.path.join(qr_directory, f'{name}.png')

        # Save the QR code image
        qr_code.save(file_path)

        # Create and save the new item in the database
        item = Item.objects.create(name=name, description=description, qr_code=f'qrcodes/{name}.png')  # Save relative path
        Warehouse_stock.objects.create(item=item, quantity=0)
        item.save()

        if item.id >=1 and item.id <= 100 :
            item.location_name = 'A1'
        if item.id >=101 and item.id <= 200 :
            item.location_name = 'A2'
        if item.id >=201 and item.id <= 300 :
            item.location_name = 'A3'
        if item.id >=301 and item.id <= 400 :
            item.location_name = 'A4'
        if item.id >=401 and item.id <= 500 :
            item.location_name = 'A5'

        item.save()


        #notification('Item has been added!',f'Item {item.name} has been successfully added!')
        return redirect('home')

    return render(request, 'qrcodes/add_item.html')