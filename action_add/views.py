from django.shortcuts import render, redirect
from qrcodes.models import Warehouse_stock, Item
from qrcodes.models import QRScan
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='profile')
def add(request):
    return render(request,'action_add/action_add.html')