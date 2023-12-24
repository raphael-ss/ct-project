from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member, Lead
from .forms import SocialMediaMetricCreateForm, ClientCreateForm, ContractCreateForm, CampaignMetricCreateForm, CompanyCreateForm, ServiceCreateForm, MemberCreateForm, LeadCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
import json
import csv
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
import datetime
from .utils import analysis_utils, pdf_utils
from io import BytesIO
# Create your views here.

def search_lead(request):
   if request.method == "POST":
      search_string = json.loads(request.body).get("searchText")
      
      leads = Lead.objects.filter(
         Q(first_name__icontains=search_string) |
         Q(last_name__icontains=search_string) |
         Q(gender__icontains=search_string) |
         Q(status__icontains=search_string) |
         Q(email__icontains=search_string) |
         Q(phone__icontains=search_string) |
         Q(field_of_action__icontains=search_string) |
         Q(source__icontains=search_string) |
         Q(date__icontains=search_string) |
         Q(notes__icontains=search_string))
      
      data = leads.values()
      return JsonResponse(list(data), safe=False)
  
def search_client(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        clients = Client.objects.filter(
            Q(lead_id__first_name__icontains=search_string) |
            Q(lead_id__last_name__icontains=search_string) |
            Q(lead_id__gender__icontains=search_string) |
            Q(lead_id__email__icontains=search_string) |
            Q(lead_id__phone__icontains=search_string) |
            Q(lead_id__field_of_action__icontains=search_string) |
            Q(lead_id__source__icontains=search_string) |
            Q(cpf__icontains=search_string) |
            Q(notes__icontains=search_string)
        )

        data = []
        for client in clients:
            client_info = {
                'id': client.id,
                'lead_id': client.lead_id.id,
                'first_name': client.lead_id.first_name,
                'last_name': client.lead_id.last_name,
                'gender': client.lead_id.gender,
                'email': client.lead_id.email,
                'phone': client.lead_id.phone,
                'field_of_action': client.lead_id.field_of_action,
                'source': client.lead_id.source,
                'cpf': client.cpf,
                'score': client.lead_id.score,
                'funnel_time': client.funnel_time,
                'notes': client.notes,
            }
            data.append(client_info)

        return JsonResponse(data, safe=False)
  
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
    context["projects_sold"] = Service.objects.count()
    context["active_members"] = Member.objects.count()
    context["goal"] = 96000 / 12
    context["revenue"] = analysis_utils.revenue_per_month()  
    context['sum'] = analysis_utils.total_revenue()
    context['yearly_goal'] = 96000
    context["revenue_per_sector"] = analysis_utils.revenue_per_sector()
    context['total_leads'] = analysis_utils.total_leads()
    context['current_year'] = datetime.datetime.now().date().year
    
    
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
        context['leads_per_source'] = analysis_utils.leads_per_source()
        context['leads_over_time'] = analysis_utils.leads_per_time()
        context['leads'] = analysis_utils.total_leads()
        context['cpl'] = analysis_utils.cpl()
        context['leads_goal'] = analysis_utils.leads_goal(60)
        context['leads_per_gender'] = analysis_utils.leads_per_gender()
        context["sales_funnel"] = analysis_utils.sales_funnel()
        context["leads_per_sector"] = analysis_utils.leads_per_sector()
        context["leads_per_score"] = analysis_utils.leads_per_score()
        context['most_frequent_score'] = analysis_utils.most_frequent_lead_score()
        context['most_frequent_source'] = analysis_utils.most_frequent_lead_source()
        context['conversion_rate_diag_prop'] = analysis_utils.conversion_rate_diagnostic_to_proposition()
        context['conversion_rate_prop_closed'] = analysis_utils.conversion_rate_proposition_to_closed()
        
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
        
        context['cac'] = analysis_utils.cac()
        context['client_education_distribution'] = analysis_utils.client_education_distribution()
        context['client_income_distribution'] = analysis_utils.client_income_distribution()
        context['client_civil_state_distribution'] = analysis_utils.client_civil_state_distribution()
        context['client_age_distribution'] = analysis_utils.client_age_distribution()
        context['current_year'] = datetime.datetime.now().date().year
        context['mean_funnel_time'] = analysis_utils.client_mean_funnel_time()
        context['client_count'] = analysis_utils.client_count()
        context['conversion_rate'] = analysis_utils.conversion_rate_general()

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
        context['average_company_revenue'] = analysis_utils.average_company_revenue()
        context['average_company_size'] = analysis_utils.average_company_size()
        context['most_frequent_sector_for_companies'] = analysis_utils.most_frequent_sector_for_companies()
        context['most_frequent_company_field'] = analysis_utils.most_frequent_company_field()
        
        
        
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
        context['avg_ticket'] = analysis_utils.average_ticket()
        context['tec_avg_ticket'] = analysis_utils.average_ticket(sector="TEC")
        context['civ_avg_ticket'] = analysis_utils.average_ticket(sector="CIV")
        context['con_avg_ticket'] = analysis_utils.average_ticket(sector="CON")
        
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
    queryset = Member.objects.all().order_by('role')
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
     
def export_leads_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Leads-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Nome', 'Sobrenome', 'Sexo', 'Etapa', 'Origem', 'Email', 'Telefone', 'Área de Atuação', 'Data', 'Notas'])
   
   leads = Lead.objects.all()
   
   for lead in leads:
      writer.writerow([
         lead.first_name,
         lead.last_name,
         lead.gender,
         lead.status,
         lead.source,
         lead.email,
         lead.phone,
         lead.field_of_action,
         lead.date,
         lead.notes,
      ])
      
   return response

def export_clients_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Clientes-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Nome', 'Sobrenome', 'Sexo', 'Etapa', 
                    'Origem', 'Email', 'Telefone', 'Área de Atuação', 
                    'Data', 'CPF', 'Data de Nascimento', 'Nível Educacional',
                    'Estado Civil', 'Renda Mensal', 'Tempo de Funil',
                    'Notas'])
   
   clients = Client.objects.all()
   
   for client in clients:
      writer.writerow([
         client.lead_id.first_name,
         client.lead_id.last_name,
         client.lead_id.gender,
         client.lead_id.status,
         client.lead_id.source,
         client.lead_id.email,
         client.lead_id.phone,
         client.lead_id.field_of_action,
         client.lead_id.date,
         client.cpf,
         client.birth_date,
         client.education,
         client.marital_status,
         client.income,
         client.funnel_time,
         client.notes,
      ])
      
   return response

def generate_target_analysis(request):
    
    chart_configs:list = [
    {
        'type': 'pie',
        'kwargs': {
            'data': analysis_utils.revenue_per_sector(),
            'labels': ['Tecnologia', 'Construção Civil', 'Consultoria'],
            'title': 'Faturamento por Diretoria',
        },
    },
    {
        'type': 'pie',
        'kwargs': {
            'data': analysis_utils.leads_per_sector(),
            'labels': ['Construção Civil', 'Consultoria', 'Tecnologia'],
            'title': 'Leads por Diretoria',
        },
    },
    {
        'type': 'pie',
        'kwargs': {
            'data': analysis_utils.leads_per_source(),
            'labels': ['Prospec. Ativa', 'Facebook Ads', 'Google Ads', 'Indicação', 'Prospec. Passiva'],
            'title': 'Leads por Canal',
        },
    },
    {
        'type': 'bar',
        'kwargs': {
            'data': analysis_utils.client_age_distribution(),
            'labels': ['Até 25', '25-40', '40-60', '+60'],
            'title': 'Distribuição da Idade dos Clientes',
        },
    },
    {
        'type': 'bar',
        'kwargs': {
            'data': analysis_utils.client_civil_state_distribution(),
            'labels': ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'União Estável', 'Outro'],
            'title': 'Distribuição do Estado Civil dos Clientes',
        },
    },
    {
        'type': 'bar',
        'kwargs': {
            'data': analysis_utils.client_education_distribution(),
            'labels': ['EF-Completo', 'EM-Completo', 'ES-Completo'],
            'title': 'Distribuição do Nível Educacional dos Clientes',
        },
    },
    {
        'type': 'bar',
        'kwargs': {
            'data': analysis_utils.client_income_distribution(),
            'labels': ['Até 3 S.M', 'Até 6 S.M.', 'Até 9 S.M.', '+9 S.M.'],
            'title': 'Distribuição da Renda Mensal dos Clientes',
        },
    },
    {
        'type': 'bar',
        'kwargs': {
            'data': analysis_utils.most_frequent_area_in_closing_leads_count(),
            'labels': analysis_utils.most_frequent_area_in_closing_leads(),
            'title': 'Áreas de Trabalho Mais Frequentes em Clientes',
        },
    },
    {
        'type': 'radar',
        'kwargs': {
            'data': analysis_utils.lead_scoring_radar_data(),
            'labels':  ['Orçamento', 'Autoridade', 'Necessidade', 'Timing', 'Tempo de Resposta', 'Comportamento'],
            'title': 'Radar da Média dos Atributos do Lead Scoring',
        },
    },
    {
        'type': 'parallel',
        'kwargs': {
            'data': analysis_utils.get_lead_scoring_data(),
            #'labels':  ['Orçamento', 'Autoridade', 'Necessidade', 'Timing', 'Tempo de Resposta', 'Comportamento'],
            'title': 'Coordenadas Paralelas: Parametros do Lead Scoring',
        },
    },
    ]

    buffer = pdf_utils.gen_target_analysis(chart_configs)

    # Set the buffer's file pointer to the beginning of the buffer
    buffer.seek(0)

    # Create an HTTP response with the PDF as the content
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Público-Alvo-'+ str(datetime.datetime.today().date())+ '.pdf'

    # Return the HTTP response
    return response