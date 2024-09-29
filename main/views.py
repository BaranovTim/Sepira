from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from qrcodes.models import QRScan, Warehouse_stock
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import News
from .forms import NewsForm
from win10toast import ToastNotifier
# Create your views here.

def notification(title, message):
    toast = ToastNotifier()
    toast.show_toast(title, message, duration=3)

def home(request):
    return render(request,'main/home.html')

@login_required(login_url='profile')
def info(request):
    return render(request, 'main/info.html')

@login_required(login_url='profile')
def news(request):
    news = News.objects.order_by('-date')
    return render(request,'main/news.html', {"news":news})

@login_required(login_url='profile')
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Include files for image upload
        if form.is_valid():
            news = form.save(commit=False)
            news.user = request.user  # Set the logged-in user
            news.save()
            notification('Success!', "News has been added")
            return redirect('home')
    else:
        form = NewsForm()

    return render(request, 'main/add_news.html', {"form": form})


def profile(request):
    return render(request, 'main/profile.html')

@login_required(login_url='profile')
def statistics(request):
    actions = QRScan.objects.filter(scanned_by=request.user).order_by('-scanned_at')
    actions_all = QRScan.objects.order_by('-scanned_at')
    context = {
        'actions': actions,
        'actions_all': actions_all
    }
    return render(request, 'main/statistics.html', context)

@login_required(login_url='profile')
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/add_user.html', {'form': form})


@login_required(login_url='profile')
def stock(request):
    query = request.GET.get('item')  # Получаем поисковый запрос

    if query:
        # Фильтруем элементы по имени (case-insensitive поиск)
        items = Warehouse_stock.objects.filter(item__name__icontains=query)
    else:
        # Если запрос не передан, отображаем все элементы
        items = Warehouse_stock.objects.order_by('quantity')

    return render(request, 'main/stock.html', {'items': items})

