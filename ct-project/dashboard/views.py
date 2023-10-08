from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='auth/login')
def index(request):
    return render(request, 'dashboard/index.html')
    

@login_required(login_url='auth/login')
def social_media(request):
    return render(request, 'dashboard/sm_metric.html')

@login_required(login_url='auth/login')
def clients(request):
    return render(request, 'dashboard/clients.html')

@login_required(login_url='auth/login')
def campaigns(request):
    return render(request, 'dashboard/campaigns.html')

@login_required(login_url='auth/login')
def services(request):
    return render(request, 'dashboard/services.html')

@login_required(login_url='auth/login')
def members(request):
    return render(request, 'dashboard/members.html')

@login_required(login_url='auth/login')
def contracts(request):
    return render(request, 'dashboard/contracts.html')

@login_required(login_url='auth/login')
def companies(request):
    return render(request, 'dashboard/companies.html')

@login_required(login_url='auth/login')
def add_sm_metric(request):
    return render(request, 'dashboard/add_sm_metric.html')