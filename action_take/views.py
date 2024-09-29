from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='profile')
def take(request):
    return render(request,'action_take/action_take.html')