from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='profile')
def remove(request):
    return render(request,'action_remove/action_remove.html')