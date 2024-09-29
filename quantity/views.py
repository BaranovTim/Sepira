from django.shortcuts import render, redirect
from qrcodes.models import QRScan, Warehouse_stock
from django.contrib.auth.decorators import login_required
from win10toast import ToastNotifier


def notification(title, message):
    toast = ToastNotifier()
    toast.show_toast(title, message, duration=2)
@login_required(login_url='profile')
def quantity(request):
    current_url = request.path
    last_scan = QRScan.objects.last()
    stock = Warehouse_stock.objects.get(item=last_scan.item)


    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if 1 <= quantity <= 1000:
            last_scan.quantity = quantity
            last_scan.save()

            if 'action_add' in current_url:
                stock.quantity += quantity
            if 'action_take' in current_url:
                stock.quantity = max(stock.quantity - quantity, 0)
            if 'action_remove' in current_url:
                stock.quantity = max(stock.quantity - quantity, 0)
            if 'action_return' in current_url:
                stock.quantity += quantity

            stock.save()
            notification('Done', 'Good job!')
            return redirect('home')

    return render(request, 'quantity/quantity.html', {'last_scan': last_scan})