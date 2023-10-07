from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='auth/login')
def index(request):
    return render(request, 'dashboard/index.html')
    