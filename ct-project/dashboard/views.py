from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member, Lead
from .forms import SocialMediaMetricCreateForm, ClientCreateForm, ContractCreateForm, CampaignMetricCreateForm, CompanyCreateForm, ServiceCreateForm, MemberCreateForm, LeadCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from collections import defaultdict
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
  template_name = "dashboard/index.html"

  def get_context_data(self):
    context = super().get_context_data()
    context["clientes"] = Client.objects.all()
    context["empresas"] = Company.objects.all()
    context["contracts"] = Contract.objects.all()
    context["campanhas"] = CampaignMetric.objects.all()
    context["servicos"] = Service.objects.all()
    context["membros"] = Member.objects.all()
    context["rede-social"] = SocialMediaMetric.objects.all()
    
    projects_sold = Service.objects.count()
    context["projects_sold"] = projects_sold
    
    active_members = Member.objects.count()
    context["active_members"] = active_members
       
    context["goal"] = 96000 / 12
    
    revenue = list()
    
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    for month in months:
      sum = 0
      contracts_in_month = Contract.objects.filter(date__month=month)
      if contracts_in_month.count() is 0:
         if revenue:
            revenue.append(revenue[-1])
         else:
            revenue.append(0)
      else:
         for contract in contracts_in_month:
            sum = revenue[-1]
            sum += contract.total_value
            revenue.append(sum)
      
    context["revenue"] = revenue
    
    total_revenue = 0
    for contract in Contract.objects.all():
       total_revenue += contract.total_value
       
    context['sum'] = round(total_revenue)
    
    context['yearly_goal'] = 96000
    
    civil_total = 0
    tec_total = 0
      
    for contract in Contract.objects.filter(sector="CIV"):
      civil_total += contract.total_value
    for contract in Contract.objects.filter(sector="TEC"):
      tec_total += contract.total_value
         
    context["tecTotal"] = tec_total
    context["civilTotal"] = civil_total
    
    return context


class LeadList(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "dashboard/leads.html"
    queryset = Lead.objects.all().order_by('date')
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Lead.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context
class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = "dashboard/clients.html"
    queryset = Client.objects.all().order_by('id')
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Client.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context

class CompanyList(LoginRequiredMixin, ListView):
    model = Company
    template_name = "dashboard/companies.html"
    queryset = Company.objects.all()
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Company.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context

class ContractList(LoginRequiredMixin, ListView):
    model = Contract
    template_name = "dashboard/contracts.html"
    queryset = Contract.objects.all()
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Contract.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context

class CampaignMetricList(LoginRequiredMixin, ListView):
    queryset = CampaignMetric.objects.all()
    model = CampaignMetric
    template_name = "dashboard/campaigns.html"
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return CampaignMetric.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context

class ServiceList(LoginRequiredMixin, ListView):
    model = Service
    template_name = "dashboard/services.html"
    queryset = Service.objects.all()
    context_object_name = 'items'
    paginate_by = 8

    def get_queryset(self):
        return Service.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context

class MemberList(LoginRequiredMixin, ListView):
    model = Member
    template_name = "dashboard/members.html"
    queryset = Member.objects.all()
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Member.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context

class SocialMediaMetricList(LoginRequiredMixin, ListView):
    model = SocialMediaMetric
    template_name = "dashboard/sm_metric.html"
    queryset = SocialMediaMetric.objects.all()
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return SocialMediaMetric.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')

        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        return context


#-ADD DATA
class LeadCreate(LoginRequiredMixin, CreateView):
   model = Lead
   template_name = 'dashboard/add_lead.html'
   form_class = LeadCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Lead adicionado com sucesso.')
        return response

class ClientCreate(LoginRequiredMixin, CreateView):
   model = Client
   template_name = 'dashboard/add_client_data.html'
   form_class = ClientCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente adicionado com sucesso.')
        return response

class CompanyCreate(LoginRequiredMixin, CreateView):
   model = Company
   template_name = 'dashboard/add_company_data.html'
   form_class = CompanyCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empresa adicionada com sucesso.')
        return response

class ContractCreate(LoginRequiredMixin, CreateView):
   model = Contract
   template_name = 'dashboard/add_contract_data.html'
   form_class = ContractCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contrato adicionado com sucesso.')
        return response

class CampaignMetricCreate(LoginRequiredMixin, CreateView):
   model = CampaignMetric
   template_name = 'dashboard/add_campaign_metric.html'
   form_class = CampaignMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica adicionada com sucesso.')
        return response

class ServiceCreate(LoginRequiredMixin, CreateView):
   model = Service
   template_name = 'dashboard/add_service_data.html'
   form_class = ServiceCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Serviço adicionado com sucesso.')
        return response

class MemberCreate(LoginRequiredMixin, CreateView):
   model = Member
   template_name = 'dashboard/add_member_data.html'
   form_class = MemberCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Membro adicionado com sucesso.')
        return response

class SocialMediaMetricCreate(LoginRequiredMixin, CreateView):
   model = SocialMediaMetric
   template_name = 'dashboard/add_sm_metric.html'
   form_class = SocialMediaMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica adicionada com sucesso.')
        return response

#-UPDATE DATA
class LeadUpdate(LoginRequiredMixin, UpdateView):
   model = Lead
   template_name = 'dashboard/update_lead.html'
   form_class = LeadCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Lead atualizado com sucesso.')
        return response

class ClientUpdate(LoginRequiredMixin, UpdateView):
   model = Client
   template_name = 'dashboard/update_client_data.html'
   form_class = ClientCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente atualizado com sucesso.')
        return response

class CompanyUpdate(LoginRequiredMixin, UpdateView):
   model = Company
   template_name = 'dashboard/update_company_data.html'
   form_class = CompanyCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empresa atualizada com sucesso.')
        return response

class ContractUpdate(LoginRequiredMixin, UpdateView):
   model = Contract
   template_name = 'dashboard/update_contract_data.html'
   form_class = ContractCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contrato atualizado com sucesso.')
        return response

class CampaignMetricUpdate(LoginRequiredMixin, UpdateView):
   model = CampaignMetric
   template_name = 'dashboard/update_campaign_metric.html'
   form_class = CampaignMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica atualizada com sucesso.')
        return response

class ServiceUpdate(LoginRequiredMixin, UpdateView):
   model = Service
   template_name = 'dashboard/update_service_data.html'
   form_class = ServiceCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Serviço atualizado com sucesso.')
        return response

class MemberUpdate(LoginRequiredMixin, UpdateView):
   model = Member
   template_name = 'dashboard/update_member_data.html'
   form_class = MemberCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Membro atualizado com sucesso.')
        return response

class SocialMediaMetricUpdate(LoginRequiredMixin, UpdateView):
   model = SocialMediaMetric
   template_name = 'dashboard/update_sm_metric.html'
   form_class = SocialMediaMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica atualizada com sucesso.')
        return response

#-DELETE DATA
class LeadDelete(LoginRequiredMixin, DeleteView):
   model = Lead
   template_name = 'dashboard/delete_lead.html'
   success_url = "/leads"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Lead deletado com sucesso.')
        return response

class ClientDelete(LoginRequiredMixin, DeleteView):
   model = Client
   template_name = 'dashboard/delete_client_data.html'
   success_url = "/clientes"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Cliente deletado com sucesso.')
        return response

class CompanyDelete(LoginRequiredMixin, DeleteView):
   model = Company
   template_name = 'dashboard/delete_company_data.html'
   success_url = "/empresas"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Empresa deletada com sucesso.')
        return response

class ContractDelete(LoginRequiredMixin, DeleteView):
   model = Contract
   template_name = 'dashboard/delete_contract_data.html'
   success_url = "/contratos"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Contrato deletado com sucesso.')
        return response

class CampaignMetricDelete(LoginRequiredMixin, DeleteView):
   model = CampaignMetric
   template_name = 'dashboard/delete_campaign_metric.html'
   success_url = "/campanhas"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Métrica deletada com sucesso.')
        return response

class ServiceDelete(LoginRequiredMixin, DeleteView):
   model = Service
   template_name = 'dashboard/delete_service_data.html'
   success_url = "/servicos"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Serviço deletado com sucesso.')
        return response

class MemberDelete(LoginRequiredMixin, DeleteView):
   model = Member
   template_name = 'dashboard/delete_member_data.html'
   success_url = "/membros"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Membro deletado com sucesso.')
        return response

class SocialMediaMetricDelete(LoginRequiredMixin, DeleteView):
   model = SocialMediaMetric
   template_name = 'dashboard/delete_sm_metric.html'
   success_url = "/redes-sociais"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Métrica deletada com sucesso.')
        return response