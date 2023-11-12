from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member
from .forms import SocialMediaMetricCreateForm, ClientCreateForm, ContractCreateForm, CampaignMetricCreateForm, CompanyCreateForm, ServiceCreateForm, MemberCreateForm
# Create your views here.
'''
@login_required(login_url='auth/login')
def index(request):
    return render(request, 'dashboard/index.html')
'''
class IndexView(TemplateView):
  template_name = "dashboard/index.html"

  def get_context_data(self):
    context = super().get_context_data()
    context["clientes"] = Client.objects.all()
    context["empresas"] = Company.objects.all()
    context["contratos"] = Contract.objects.all()
    context["campanhas"] = CampaignMetric.objects.all()
    context["servicos"] = Service.objects.all()
    context["membros"] = Member.objects.all()
    context["rede-social"] = SocialMediaMetric.objects.all()
    return context

class ClientList(ListView):
    model = Client
    template_name = "dashboard/clients.html"
    queryset = Client.objects.all().order_by('id')

class CompanyList(ListView):
    model = Company
    template_name = "dashboard/companies.html"
    queryset = Company.objects.all()

class ContractList(ListView):
    model = Contract
    template_name = "dashboard/contracts.html"
    queryset = Contract.objects.all()

class CampaignMetricList(ListView):
    queryset = CampaignMetric.objects.all()
    model = CampaignMetric
    template_name = "dashboard/campaigns.html"

class ServiceList(ListView):
    model = Service
    template_name = "dashboard/services.html"
    queryset = Service.objects.all()

class MemberList(ListView):
    model = Member
    template_name = "dashboard/members.html"
    queryset = Member.objects.all()

class SocialMediaMetricList(ListView):
    model = SocialMediaMetric
    template_name = "dashboard/sm_metric.html"
    queryset = SocialMediaMetric.objects.all()


#-ADD DATA
class ClientCreate(CreateView):
   model = Client
   template_name = 'dashboard/add_client_data.html'
   form_class = ClientCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente adicionado com sucesso.')
        return response

class CompanyCreate(CreateView):
   model = Company
   template_name = 'dashboard/add_company_data.html'
   form_class = CompanyCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empresa adicionada com sucesso.')
        return response

class ContractCreate(CreateView):
   model = Contract
   template_name = 'dashboard/add_contract_data.html'
   form_class = ContractCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contrato adicionado com sucesso.')
        return response

class CampaignMetricCreate(CreateView):
   model = CampaignMetric
   template_name = 'dashboard/add_campaign_metric.html'
   form_class = CampaignMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica adicionada com sucesso.')
        return response

class ServiceCreate(CreateView):
   model = Service
   template_name = 'dashboard/add_service_data.html'
   form_class = ServiceCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Serviço adicionado com sucesso.')
        return response

class MemberCreate(CreateView):
   model = Member
   template_name = 'dashboard/add_member_data.html'
   form_class = MemberCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Membro adicionado com sucesso.')
        return response

class SocialMediaMetricCreate(CreateView):
   model = SocialMediaMetric
   template_name = 'dashboard/add_sm_metric.html'
   form_class = SocialMediaMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica adicionada com sucesso.')
        return response

#-UPDATE DATA
class ClientUpdate(UpdateView):
   model = Client
   template_name = 'dashboard/update_client_data.html'
   form_class = ClientCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente atualizado com sucesso.')
        return response

class CompanyUpdate(UpdateView):
   model = Company
   template_name = 'dashboard/update_company_data.html'
   form_class = CompanyCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empresa atualizada com sucesso.')
        return response

class ContractUpdate(UpdateView):
   model = Contract
   template_name = 'dashboard/update_contract_data.html'
   form_class = ContractCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contrato atualizado com sucesso.')
        return response

class CampaignMetricUpdate(UpdateView):
   model = CampaignMetric
   template_name = 'dashboard/update_campaign_metric.html'
   form_class = CampaignMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica atualizada com sucesso.')
        return response

class ServiceUpdate(UpdateView):
   model = Service
   template_name = 'dashboard/update_service_data.html'
   form_class = ServiceCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Serviço atualizado com sucesso.')
        return response

class MemberUpdate(UpdateView):
   model = Member
   template_name = 'dashboard/update_member_data.html'
   form_class = MemberCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Membro atualizado com sucesso.')
        return response

class SocialMediaMetricUpdate(UpdateView):
   model = SocialMediaMetric
   template_name = 'dashboard/update_sm_metric.html'
   form_class = SocialMediaMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica atualizada com sucesso.')
        return response

#-DELETE DATA
class ClientDelete(DeleteView):
   model = Client
   template_name = 'dashboard/delete_client_data.html'
   success_url = "/clientes"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Cliente deletado com sucesso.')
        return response

class CompanyDelete(DeleteView):
   model = Company
   template_name = 'dashboard/delete_company_data.html'
   success_url = "/empresas"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Empresa deletada com sucesso.')
        return response

class ContractDelete(DeleteView):
   model = Contract
   template_name = 'dashboard/delete_contract_data.html'
   success_url = "/contratos"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Contrato deletado com sucesso.')
        return response

class CampaignMetricDelete(DeleteView):
   model = CampaignMetric
   template_name = 'dashboard/delete_campaign_metric.html'
   success_url = "/campanhas"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Métrica deletada com sucesso.')
        return response

class ServiceDelete(DeleteView):
   model = Service
   template_name = 'dashboard/delete_service_data.html'
   success_url = "/servicos"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Serviço deletado com sucesso.')
        return response

class MemberDelete(DeleteView):
   model = Member
   template_name = 'dashboard/delete_member_data.html'
   success_url = "/membros"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Membro deletado com sucesso.')
        return response

class SocialMediaMetricDelete(DeleteView):
   model = SocialMediaMetric
   template_name = 'dashboard/delete_sm_metric.html'
   success_url = "/redes-sociais"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Métrica deletada com sucesso.')
        return response