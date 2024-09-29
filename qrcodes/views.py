from django.http import JsonResponse
import cv2
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import QRScan, Warehouse_stock
from .models import Item
from django.contrib.auth.models import User
from pyzbar.pyzbar import decode
from datetime import datetime
import qrcode
import pygame
import os
from win10toast import ToastNotifier
from django.contrib.auth.decorators import login_required


scanning_active = True
pygame.mixer.init()


# Путь к звуковому файлу для сканирования
sounds_directory = r'C:\Users\Admin\Desktop\Dima_Proj\warehouse\qrcodes\sounds'
sound_file_path = os.path.join(sounds_directory, 'qr-code-scan-beep.mp3')

def notification(title, message):
    toast = ToastNotifier()
    toast.show_toast(title, message, duration=3)

def play_sound():
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()

@login_required(login_url='profile')
def qr_scanner(request):
    global scanning_active
    current_url = request.path

    # Camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
        notification('Error','Your camera is not connected' )
        return redirect('home')
    cv2.namedWindow("Scanner")

    fps = 30
    cap.set(cv2.CAP_PROP_FPS, fps)

    while True:
        success, frame = cap.read()

        if not success:
            cap.release()
            cv2.destroyAllWindows()
            notification('Error', 'Your camera is not working' )
            return redirect('home')

        cv2.line(frame, (620, 5), (635, 20), (0, 0, 0), 2)  # Crosshair line 1
        cv2.line(frame, (635, 5), (620, 20), (0, 0, 0), 2)  # Crosshair line 2

        detected_barcodes = decode(frame)
        if detected_barcodes:
            for barcode in detected_barcodes:
                barcode_data = barcode.data.decode('utf-8')
                try:
                    item = Item.objects.get(name=barcode_data)

                    if 'action_add' in current_url:
                        QRScan.objects.create(scanned_by=request.user, item=item, scanned_at=datetime.now(), action='added')
                    if 'action_take' in current_url:
                        QRScan.objects.create(scanned_by=request.user, item=item, scanned_at=datetime.now(), action='took')
                    if 'action_remove' in current_url:
                        QRScan.objects.create(scanned_by=request.user, item=item, scanned_at=datetime.now(), action='removed')
                    if 'action_return' in current_url:
                        QRScan.objects.create(scanned_by=request.user, item=item, scanned_at=datetime.now(), action='returned')

                    play_sound()
                    cap.release()
                    cv2.destroyAllWindows()
                    return redirect('quantity/')
                except Item.DoesNotExist:
                    cap.release()
                    cv2.destroyAllWindows()
                    return redirect('home')  # or another error page

        cv2.imshow('Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            scanning_active = False
            break

        #if event == cv2.EVENT_LBUTTONDOWN and x >= 635 and y <= 20:
        #    scanning_active = False
        #    cap.release()
        #    cv2.destroyAllWindows()
         #   return redirect('home')

    cap.release()
    cv2.destroyAllWindows()


def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validate input
        if not name:
            return JsonResponse({'status': 'error', 'message': 'Name is required'})

        # Generate QR code
        qr_code = qrcode.make(name)
        qr_directory = r'media\qrcodes'
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


        notification('Item has been added!',f'Item {item.name} has been successfully added!')
        return redirect('home')

    return render(request, 'qrcodes/add_item.html')