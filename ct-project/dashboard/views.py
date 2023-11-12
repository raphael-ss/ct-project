from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member
from .forms import SocialMediaMetricCreateForm, ClientCreateForm, ContractCreateForm, CampaignMetricCreateForm, CompanyCreateForm, ServiceCreateForm, MemberCreateForm
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

#-ADD DATA
class SocialMediaMetricCreate(CreateView):
   model = SocialMediaMetric
   template_name = 'dashboard/add_sm_metric.html'
   form_class = SocialMediaMetricCreateForm

class ClientCreate(CreateView):
   model = Client
   template_name = 'dashboard/add_client_data.html'
   form_class = ClientCreateForm

class CompanyCreate(CreateView):
   model = Company
   template_name = 'dashboard/add_company_data.html'
   form_class = CompanyCreateForm

class ContractCreate(CreateView):
   model = Contract
   template_name = 'dashboard/add_contract_data.html'
   form_class = ContractCreateForm

class CampaignMetricCreate(CreateView):
   model = CampaignMetric
   template_name = 'dashboard/add_campaign_metric.html'
   form_class = CampaignMetricCreateForm

class ServiceCreate(CreateView):
   model = Service
   template_name = 'dashboard/add_service_data.html'
   form_class = ServiceCreateForm

class MemberCreate(CreateView):
   model = Member
   template_name = 'dashboard/add_member_data.html'
   form_class = MemberCreateForm