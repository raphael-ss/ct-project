from django.contrib import messages
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member, Lead, Diagnostic, PostSales, Proposition, ServiceTag, Installment, Team
from .forms import SocialMediaMetricCreateForm, ClientCreateForm, ContractCreateForm, CampaignMetricCreateForm, CompanyCreateForm, ServiceCreateForm, MemberCreateForm, LeadCreateForm, DiagnosticCreateForm, PostSalesCreateForm, PropositionCreateForm, ServiceTagCreateForm, InstallmentCreateForm, TeamCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
import json
import csv
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
import datetime
from .utils import analysis_utils, pdf_utils
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy


@csrf_exempt
def get_lead_status(request, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id)
        lead_status = lead.status
        return JsonResponse({'lead_status': lead_status})
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'Lead not found'}, status=404)

@csrf_exempt
def update_lead(request):
    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        new_status = request.POST.get('new_status')
        print(new_status)

        try:
            lead = Lead.objects.get(id=lead_id)
            lead.status = new_status
            lead.save()
            return JsonResponse({'message': 'Lead status updated successfully'})
        except Lead.DoesNotExist:
            return JsonResponse({'error': 'Lead not found'}, status=404)

#- SEARCH
@csrf_exempt
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
         Q(arrival_date__icontains=search_string) |
         Q(notes__icontains=search_string))
      
      data = leads.values()
      return JsonResponse(list(data), safe=False)
  
@csrf_exempt
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
  
@csrf_exempt
def search_company(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        companies = Company.objects.filter(
            Q(client_id__lead_id__first_name__icontains=search_string) |
            Q(client_id__lead_id__last_name__icontains=search_string) |
            Q(client_id__lead_id__email__icontains=search_string) |
            Q(client_id__lead_id__phone__icontains=search_string) |
            Q(client_id__cpf__icontains=search_string) |
            Q(company_name__icontains=search_string) |
            Q(cnpj__icontains=search_string) |
            Q(field_of_action__icontains=search_string) |
            Q(notes__icontains=search_string)
        )

        data = []
        for company in companies:
            company_info = {
                'id': company.id,
                'company_name': company.company_name,
                'first_name': company.client_id.lead_id.first_name,
                'last_name': company.client_id.lead_id.last_name,
                'cnpj': company.cnpj,
                'field_of_action': company.field_of_action,
                'annual_revenue': company.annual_revenue,
                'n_of_employees': company.n_of_employees,
                'notes': company.notes
            }
            data.append(company_info)

        return JsonResponse(data, safe=False)
 
@csrf_exempt   
def search_contract(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        contracts = Contract.objects.filter(
            Q(client_id__lead_id__first_name__icontains=search_string) |
            Q(client_id__lead_id__last_name__icontains=search_string) |
            Q(client_id__lead_id__email__icontains=search_string) |
            Q(client_id__lead_id__phone__icontains=search_string) |
            Q(client_id__cpf__icontains=search_string) |
            Q(date__icontains=search_string) |
            Q(sector__icontains=search_string)
        )

        data = []
        for contract in contracts:
            contract_info = {
                'id': contract.id,
                'first_name': contract.client_id.lead_id.first_name,
                'last_name': contract.client_id.lead_id.last_name,
                'sector': contract.sector,
                'total_value': contract.total_value,
                'n_of_services': contract.n_of_services,
                'date': contract.date,
                'link_of_contract': contract.link_of_contract,
                'notes': contract.notes
            }
            data.append(contract_info)

        return JsonResponse(data, safe=False)
   
@csrf_exempt 
def search_campaign(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        campaigns = CampaignMetric.objects.filter(
            Q(date__icontains=search_string) |
            Q(platform__icontains=search_string) |
            Q(funnel_position__icontains=search_string) |
            Q(campaign_sector__icontains=search_string)
        )

        data = []
        for campaign in campaigns:
            campaign_info = {
                'id': campaign.id,
                'date': campaign.date,
                'platform': campaign.platform,
                'campaign_sector': campaign.campaign_sector,
                'objective': campaign.objetive,
                'clicks': campaign.clicks,
                'cost': campaign.weekly_cost,
                'notes': campaign.notes
            }
            data.append(campaign_info)

        return JsonResponse(data, safe=False)

@csrf_exempt
def search_social_media(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        metrics = SocialMediaMetric.objects.filter(
            Q(date__icontains=search_string) |
            Q(network__icontains=search_string) |
            Q(followers__icontains=search_string) |
            Q(notes__icontains=search_string)
        )

        data = []
        for metric in metrics:
            metric_info = {
                'id': metric.id,
                'date': metric.date,
                'network': metric.network,
                'followers': metric.followers,
                'impressions': metric.impressions,
                'reach': metric.reach,
                'engagement': metric.engagement,
                'notes': metric.notes
            }
            data.append(metric_info)

        return JsonResponse(data, safe=False)

@csrf_exempt   
def search_project(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        projects = Service.objects.filter(
            Q(member_id__first_name__icontains=search_string) |
            Q(contract_id__client_id__lead_id__first_name__icontains=search_string) |
            Q(contract_id__client_id__cpf__icontains=search_string) |
            Q(project__icontains=search_string) |
            Q(price__icontains=search_string)
        )

        data = []
        for project in projects:
            project_info = {
                'id': project.id,
                'first_name': project.contract_id.client_id.lead_id.first_name,
                'last_name': project.contract_id.client_id.lead_id.last_name,
                'member_first_name': project.member_id.first_name,
                'member_last_name': project.member_id.last_name,
                'project': project.project,
                'estimated_time': project.estimated_time,
                'actual_time': project.actual_time,
                'n_of_consultants': project.n_of_consultants,
                'price': project.price,
                'notes': project.notes,
            }
            data.append(project_info)

        return JsonResponse(data, safe=False)
    
@csrf_exempt   
def search_member(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        members = Member.objects.filter(
            Q(first_name__icontains=search_string) |
            Q(last_name__icontains=search_string) |
            Q(sector__icontains=search_string) |
            Q(role__icontains=search_string) |
            Q(professional_email__icontains=search_string) |
            Q(academic_email__icontains=search_string) |
            Q(phone__icontains=search_string) |
            Q(cpf__icontains=search_string) |
            Q(rg__icontains=search_string) |
            Q(degree__icontains=search_string)
        )

        data = []
        for member in members:
            member_info = {
                'id': member.id,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'sector': member.sector,
                'role': member.role,
                'professional_email': member.professional_email,
                'phone': member.phone,
                'degree': member.degree,
                'date_of_entry': member.date_of_entry,
                'notes': member.notes
            }
            data.append(member_info)

        return JsonResponse(data, safe=False)

class IndexView(LoginRequiredMixin, TemplateView):
  template_name = "dashboard/index.html"

  def get_context_data(self):
    context = super().get_context_data()
    authenticated_username = self.request.user.full_name.split()[0]
    context["name"] = authenticated_username
    context["clientes"] = Client.objects.all()
    context["empresas"] = Company.objects.all()
    context["contracts"] = Contract.objects.all()
    context["campanhas"] = CampaignMetric.objects.all()
    context["servicos"] = Service.objects.all()
    context["membros"] = Member.objects.all()
    context["rede-social"] = SocialMediaMetric.objects.all()
    context["projects_sold"] = analysis_utils.projects_sold()
    context["active_members"] = Member.objects.count()
    context["goal"] = [8900, 17800, 26700, 38700, 50700, 64200, 76200, 88200, 101000, 112000, 120000, 127000]
    context["revenue"] = analysis_utils.revenue_per_month()  
    context['sum'] = analysis_utils.total_revenue()
    context['yearly_goal'] = 127000
    context["revenue_per_sector"] = analysis_utils.revenue_per_sector()
    context['total_leads'] = analysis_utils.total_leads()
    context['current_year'] = datetime.datetime.now().date().year
    
    return context

class Funnel(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "dashboard/funnel.html"
    queryset = Lead.objects.filter(arrival_date__year=datetime.datetime.now().year).order_by('-arrival_date')
    context_object_name = 'items'

    def get_queryset(self):
        return Lead.objects.order_by('-arrival_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['queryset'] = queryset
        context['current_year'] = datetime.datetime.now().year
        
        return context

class LeadList(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "dashboard/leads.html"
    queryset = Lead.objects.all().order_by('-arrival_date')
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Lead.objects.all().order_by('-arrival_date')

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
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
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
        context['queryset'] = queryset
        
        return context

class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = "dashboard/clients.html"
    queryset = Client.objects.all().order_by('id')
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Client.objects.order_by('-lead_id__arrival_date')

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
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['cac'] = analysis_utils.cac()
        context['client_education_distribution'] = analysis_utils.client_education_distribution()
        context['client_income_distribution'] = analysis_utils.client_income_distribution()
        context['client_civil_state_distribution'] = analysis_utils.client_civil_state_distribution()
        context['client_age_distribution'] = analysis_utils.client_age_distribution()
        context['current_year'] = datetime.datetime.now().date().year
        context['mean_funnel_time'] = analysis_utils.client_mean_funnel_time()
        context['client_count'] = analysis_utils.client_count()
        context['conversion_rate'] = analysis_utils.conversion_rate_general(string=True)

        return context

class CompanyList(LoginRequiredMixin, ListView):
    model = Company
    template_name = "dashboard/companies.html"
    queryset = Company.objects.all()
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Company.objects.order_by('-client_id__lead_id__arrival_date')

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
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['average_company_revenue'] = analysis_utils.average_company_revenue()
        context['average_company_size'] = analysis_utils.average_company_size()
        context['most_frequent_sector_for_companies'] = analysis_utils.most_frequent_sector_for_companies()
        context['most_frequent_company_field'] = analysis_utils.most_frequent_company_field()
        context['company_size_distribution'] = analysis_utils.company_size_distribution()
        
        return context

class ContractList(LoginRequiredMixin, ListView):
    model = Contract
    template_name = "dashboard/contracts.html"
    queryset = Contract.objects.all()
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return Contract.objects.order_by('-client_id__lead_id__arrival_date')

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
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['avg_ticket'] = analysis_utils.average_ticket()
        context['tec_avg_ticket'] = analysis_utils.average_ticket(sector="Tecnologia")
        context['civ_avg_ticket'] = analysis_utils.average_ticket(sector="Civil")
        context['con_avg_ticket'] = analysis_utils.average_ticket(sector="Consultoria")
        context['contract_ticket_over_time'] = analysis_utils.contract_ticket_over_time()
        context['tec_contract_ticket_over_time'] = analysis_utils.tec_contract_ticket_over_time()
        context['civ_contract_ticket_over_time'] = analysis_utils.civ_contract_ticket_over_time()
        context['con_contract_ticket_over_time'] = analysis_utils.con_contract_ticket_over_time()
        
        return context

class CampaignMetricList(LoginRequiredMixin, ListView):
    queryset = CampaignMetric.objects.all()
    model = CampaignMetric
    template_name = "dashboard/campaigns.html"
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return CampaignMetric.objects.order_by('date')

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
        context['cpc'] = analysis_utils.cpc()
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['conversion'] = analysis_utils.conversion_rate_campaign()
        context['most_efficient_platform'] = analysis_utils.most_efficient_platform()
        context['avg_weekly_cost'] = analysis_utils.avg_weekly_cost()
        context['google_clicks_over_time'] = analysis_utils.google_clicks_over_time()
        context['fb_clicks_over_time'] = analysis_utils.fb_clicks_over_time()
        context['google_conversion_rate_over_time'] = analysis_utils.google_conversion_rate_over_time()
        context['fb_conversion_rate_over_time'] = analysis_utils.fb_conversion_rate_over_time()
        context['google_cpc_over_time'] = analysis_utils.google_cpc_over_time()
        context['fb_cpc_over_time'] = analysis_utils.fb_cpc_over_time()
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
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['mean_delay'] = analysis_utils.mean_delay()
        context['real_mean_deadline'] = analysis_utils.real_mean_deadline()
        context['projects_on_time'] = analysis_utils.projects_on_time()
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
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        return context

class SocialMediaMetricList(LoginRequiredMixin, ListView):
    model = SocialMediaMetric
    template_name = "dashboard/sm_metric.html"
    queryset = SocialMediaMetric.objects.all()
    context_object_name = 'items'
    paginate_by = 8 

    def get_queryset(self):
        return SocialMediaMetric.objects.order_by('date')

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
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['total_followers'] = analysis_utils.total_followers()
        context['social_media_growth'] = analysis_utils.social_media_growth()
        context['mean_engagement'] = analysis_utils.mean_engagement()
        context['most_impact_network'] = analysis_utils.most_impact_network()
        context['ig_followers_over_time'] = analysis_utils.ig_followers_over_time()
        context['face_followers_over_time'] = analysis_utils.face_followers_over_time()
        context['linkedin_followers_over_time'] = analysis_utils.linkedin_followers_over_time()
        context['tiktok_followers_over_time'] = analysis_utils.tiktok_followers_over_time()
        context['ig_reach_over_time'] = analysis_utils.ig_reach_over_time()
        context['face_reach_over_time'] = analysis_utils.face_reach_over_time()
        context['linkedin_reach_over_time'] = analysis_utils.linkedin_reach_over_time()
        context['tiktok_reach_over_time'] = analysis_utils.tiktok_reach_over_time()
        context['ig_engagement_over_time'] = analysis_utils.ig_engagement_over_time()
        context['face_engagement_over_time'] = analysis_utils.face_engagament_over_time()
        context['linkedin_engagement_over_time'] = analysis_utils.linkedin_engagement_over_time()
        context['tiktok_engagement_over_time'] = analysis_utils.tiktok_engagement_over_time()
        return context


#-ADD DATA
class LeadCreate(LoginRequiredMixin, CreateView):
    model = Lead
    template_name = 'dashboard/add_lead.html'
    form_class = LeadCreateForm
    success_url = reverse_lazy('leads')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Lead adicionado com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar o lead. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['members'] = Member.objects.filter(sector="Comercial")          
        context['current_year'] = datetime.datetime.now().date().year
        return context

class DiagnosticCreate(LoginRequiredMixin, CreateView):
    model = Diagnostic
    template_name = "dashboard/add_diagnostic.html"
    form_class = DiagnosticCreateForm
    success_url = reverse_lazy('leads')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Diagnóstico adicionado com sucesso.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar o diagnóstico. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['leads'] = Lead.objects.all()
        return context
    
class PropositionCreate(LoginRequiredMixin, CreateView):
    model = Proposition
    template_name = "dashboard/add_proposition.html"
    form_class = PropositionCreateForm
    success_url = reverse_lazy('leads')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Proposta adicionada com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar a proposta. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['leads'] = Lead.objects.all()
        return context
    
class ClientCreate(LoginRequiredMixin, CreateView):
   model = Client
   template_name = 'dashboard/add_client_data.html'
   form_class = ClientCreateForm
   success_url = reverse_lazy('clients')

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente adicionado com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar o cliente. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['closed_leads'] = Lead.objects.filter(status="CONTRATO FECHADO")
        return context
    
class CompanyCreate(LoginRequiredMixin, CreateView):
   model = Company
   template_name = 'dashboard/add_company_data.html'
   form_class = CompanyCreateForm
   success_url = reverse_lazy('companies')

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empresa adicionada com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar a empresa. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['clients'] = Client.objects.all()
        return context
    
class ContractCreate(LoginRequiredMixin, CreateView):
   model = Contract
   template_name = 'dashboard/add_contract_data.html'
   form_class = ContractCreateForm
   success_url = reverse_lazy('contracts')

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contrato adicionado com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar o contrato. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['clients'] = Client.objects.all()
        return context

class InstallmentCreate(LoginRequiredMixin, CreateView):
    model = Installment
    template_name = "dashboard/add_installment.html"
    form_class = InstallmentCreateForm
    success_url = reverse_lazy('contracts')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Parcelas adicionadas com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar as parcelas. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class CampaignMetricCreate(LoginRequiredMixin, CreateView):
   model = CampaignMetric
   template_name = 'dashboard/add_campaign_metric.html'
   form_class = CampaignMetricCreateForm
   success_url = reverse_lazy('campaigns')

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica adicionada com sucesso.')
        return response

   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar a campanha. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class ServiceTagCreate(LoginRequiredMixin, CreateView):
    model = ServiceTag
    template_name = "dashboard/add_servicetag.html"
    form_class = ServiceTagCreateForm
    success_url = reverse_lazy('services')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Tag adicionada com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar a tag. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class ServiceCreate(LoginRequiredMixin, CreateView):
   model = Service
   template_name = 'dashboard/add_service_data.html'
   form_class = ServiceCreateForm
   success_url = reverse_lazy('services')

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Serviço adicionado com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar o projeto. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    template_name = "dashboard/add_team.html"
    form_class = TeamCreateForm
    success_url = reverse_lazy('services')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Equipe adicionada com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar a equipe. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class PostSalesCreate(LoginRequiredMixin, CreateView):
    model = PostSales
    template_name = "dashboard/add_postsales.html"
    form_class = PostSalesCreateForm
    success_url = reverse_lazy('contracts')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Pós-venda adicionado com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar o pós-venda. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class MemberCreate(LoginRequiredMixin, CreateView):
   model = Member
   template_name = 'dashboard/add_member_data.html'
   form_class = MemberCreateForm
   success_url = reverse_lazy('members')

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Membro adicionado com sucesso.')
        return response

   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar o membro. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class SocialMediaMetricCreate(LoginRequiredMixin, CreateView):
   model = SocialMediaMetric
   template_name = 'dashboard/add_sm_metric.html'
   form_class = SocialMediaMetricCreateForm
   success_url = reverse_lazy('social_media')

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica adicionada com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao adicionar a métrica. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
    
#-UPDATE DATA
class LeadUpdate(LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = 'dashboard/update_lead.html'
    form_class = LeadCreateForm
    success_url = reverse_lazy('leads')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Lead atualizado com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar o lead. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['members'] = Member.objects.filter(sector="Comercial")          
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class DiagnosticUpdate(LoginRequiredMixin, UpdateView):
    model = Diagnostic
    template_name = "dashboard/update_diagnostic.html"
    form_class = DiagnosticCreateForm
    success_url = reverse_lazy('leads')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Diagnóstico atualizado com sucesso.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar o diagnóstico. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['leads'] = Lead.objects.all()
        return context
    
class PropositionUpdate(LoginRequiredMixin, UpdateView):
    model = Proposition
    template_name = "dashboard/update_proposition.html"
    form_class = PropositionCreateForm
    success_url = reverse_lazy('leads')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Proposta atualizada com sucesso.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar a proposta. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['leads'] = Lead.objects.all()
        return context
    
class ClientUpdate(LoginRequiredMixin, UpdateView):
   model = Client
   template_name = 'dashboard/update_client_data.html'
   form_class = ClientCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente atualizado com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar o cliente. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class CompanyUpdate(LoginRequiredMixin, UpdateView):
   model = Company
   template_name = 'dashboard/update_company_data.html'
   form_class = CompanyCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empresa atualizada com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar a empresa. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['clients'] = Client.objects.all()
        return context
    
class ContractUpdate(LoginRequiredMixin, UpdateView):
   model = Contract
   template_name = 'dashboard/update_contract_data.html'
   form_class = ContractCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contrato atualizado com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar o contrato. Verifique os campos e tente novamente:')
        errors = form.errors
        for error in errors:
            for e in errors[error]:
                messages.warning(self.request, f'{error}: {e}')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        context['selected_client'] = Contract.objects.get(pk=self.kwargs['pk']).client_id
        context['clients'] = Client.objects.all()
        return context
    
class InstallmentUpdate(LoginRequiredMixin, UpdateView):
   model = Installment
   template_name = 'dashboard/update_installment.html'
   form_class = InstallmentCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Parcelas atualizadas com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar a parcela. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class CampaignMetricUpdate(LoginRequiredMixin, UpdateView):
   model = CampaignMetric
   template_name = 'dashboard/update_campaign_metric.html'
   form_class = CampaignMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica atualizada com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar a campanha. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context

class ServiceTagUpdate(LoginRequiredMixin, UpdateView):
   model = ServiceTag
   template_name = 'dashboard/update_servicetag.html'
   form_class = ServiceTagCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Tag atualizada com sucesso.')
        return response
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context

class ServiceUpdate(LoginRequiredMixin, UpdateView):
   model = Service
   template_name = 'dashboard/update_service_data.html'
   form_class = ServiceCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Serviço atualizado com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar o serviço. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
    
class TeamUpdate(LoginRequiredMixin, UpdateView):
   model = Team
   template_name = 'dashboard/update_team.html'
   form_class = TeamCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Equipe atualizada com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar a equipe. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class PostSalesUpdate(LoginRequiredMixin, UpdateView):
   model = PostSales
   template_name = 'dashboard/update_postsales.html'
   form_class = PostSalesCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Pós-venda atualizado com sucesso.')
        return response
    
   def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao atualizar o pós-venda. Verifique os campos e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class MemberUpdate(LoginRequiredMixin, UpdateView):
   model = Member
   template_name = 'dashboard/update_member_data.html'
   form_class = MemberCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Membro atualizado com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class SocialMediaMetricUpdate(LoginRequiredMixin, UpdateView):
   model = SocialMediaMetric
   template_name = 'dashboard/update_sm_metric.html'
   form_class = SocialMediaMetricCreateForm

   def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Métrica atualizada com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
    
#-DELETE DATA
class LeadDelete(LoginRequiredMixin, DeleteView):
   model = Lead
   template_name = 'dashboard/delete_lead.html'
   success_url = "/leads"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Lead deletado com sucesso.')
        return response
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class DiagnosticDelete(LoginRequiredMixin, DeleteView):
   model = Diagnostic
   template_name = 'dashboard/delete_diagnostic.html'
   success_url = "/leads"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Diagnóstico deletado com sucesso.')
        return response
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class PropositionDelete(LoginRequiredMixin, DeleteView):
   model = Proposition
   template_name = 'dashboard/delete_proposition.html'
   success_url = "/leads"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Proposta deletado com sucesso.')
        return response
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class ClientDelete(LoginRequiredMixin, DeleteView):
   model = Client
   template_name = 'dashboard/delete_client_data.html'
   success_url = "/clientes"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Cliente deletado com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class CompanyDelete(LoginRequiredMixin, DeleteView):
   model = Company
   template_name = 'dashboard/delete_company_data.html'
   success_url = "/empresas"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Empresa deletada com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class ContractDelete(LoginRequiredMixin, DeleteView):
   model = Contract
   template_name = 'dashboard/delete_contract_data.html'
   success_url = "/contratos"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Contrato deletado com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class CampaignMetricDelete(LoginRequiredMixin, DeleteView):
   model = CampaignMetric
   template_name = 'dashboard/delete_campaign_metric.html'
   success_url = "/campanhas"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Métrica deletada com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class ServiceDelete(LoginRequiredMixin, DeleteView):
   model = Service
   template_name = 'dashboard/delete_service_data.html'
   success_url = "/servicos"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Serviço deletado com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class MemberDelete(LoginRequiredMixin, DeleteView):
   model = Member
   template_name = 'dashboard/delete_member_data.html'
   success_url = "/membros"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Membro deletado com sucesso.')
        return response
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
class SocialMediaMetricDelete(LoginRequiredMixin, DeleteView):
   model = SocialMediaMetric
   template_name = 'dashboard/delete_sm_metric.html'
   success_url = "/redes-sociais"

   def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Métrica deletada com sucesso.')
        return response
    
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        return context
    
    
#- DETAIL VIEWS
class LeadDetail(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'dashboard/lead_detail.html'
    context_object_name = 'lead'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        diagnostic = self.object.diagnostic_set.all()
        context['diagnostic'] = diagnostic[0] if diagnostic else None
        proposition = self.object.proposition_set.all()
        context['proposition'] = proposition[0] if proposition else None
        return context  
    
class ClientDetail(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'dashboard/client_detail.html'
    context_object_name = 'client'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username
        context['current_year'] = datetime.datetime.now().date().year
        diagnostic = self.object.lead_id.diagnostic_set.all()
        context['diagnostic'] = diagnostic[0] if diagnostic else None
        print(diagnostic)
        return context  

     
#- CSV
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
         lead.arrival_date,
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
         client.lead_id.arrival_date,
         client.cpf,
         client.birth_date,
         client.education,
         client.marital_status,
         client.income,
         client.funnel_time,
         client.notes,
      ])
      
   return response

def export_companies_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Empresas-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Nome', 'Sobrenome', 'Sexo', 'Etapa', 
                    'Origem', 'Email', 'Telefone', 'Área de Atuação', 
                    'Data', 'CPF', 'Data de Nascimento', 'Nível Educacional',
                    'Estado Civil', 'Renda Mensal', 'Tempo de Funil', 'Nome da Empresa',
                    'CNPJ', 'Setor', 'Faturamento Anual', 'Número de Locais',
                    'Número de Funcionários', 'Link da Prova de Registro', 'Notas'])
   
   companies = Company.objects.all()
   
   for company in companies:
      writer.writerow([
         company.client_id.lead_id.first_name,
         company.client_id.lead_id.last_name,
         company.client_id.lead_id.gender,
         company.client_id.lead_id.status,
         company.client_id.lead_id.source,
         company.client_id.lead_id.email,
         company.client_id.lead_id.phone,
         company.client_id.lead_id.field_of_action,
         company.client_id.lead_id.date,
         company.client_id.cpf,
         company.client_id.birth_date,
         company.client_id.education,
         company.client_id.marital_status,
         company.client_id.income,
         company.client_id.funnel_time,
         company.company_name,
         company.cnpj,
         company.field_of_action,
         company.annual_revenue,
         company.n_of_locations,
         company.n_of_employees,
         company.proof_of_registration_link,
         company.notes,
      ])
      
   return response

def export_contracts_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Contratos-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Nome', 'Sobrenome', 'Sexo', 'Etapa', 
                    'Origem', 'Email', 'Telefone', 'Área de Atuação', 
                    'Data', 'CPF', 'Data de Nascimento', 'Nível Educacional',
                    'Estado Civil', 'Renda Mensal', 'Tempo de Funil', 'Vendedor',
                    'Diretoria', 'Valor Total', 'Número de Serviços', 'Data',
                    'Link do Contrato', 'Notas'])
   
   contracts = Contract.objects.all()
   
   for contract in contracts:
      writer.writerow([
         contract.client_id.lead_id.first_name,
         contract.client_id.lead_id.last_name,
         contract.client_id.lead_id.gender,
         contract.client_id.lead_id.status,
         contract.client_id.lead_id.source,
         contract.client_id.lead_id.email,
         contract.client_id.lead_id.phone,
         contract.client_id.lead_id.field_of_action,
         contract.client_id.lead_id.arrival_date,
         contract.client_id.cpf,
         contract.client_id.birth_date,
         contract.client_id.education,
         contract.client_id.marital_status,
         contract.client_id.income,
         contract.client_id.funnel_time,
         f"{contract.client_id.lead_id.member_id.first_name} {contract.client_id.lead_id.member_id.last_name}",
         contract.sector,
         contract.total_value,
         contract.n_of_services,
         contract.date,
         contract.deadline,
         contract.contract_link,
         contract.notes
      ])
      
   return response

def export_campaigns_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Campanhas-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Data', 'Plataforma', 'Setor', 'Posição', 'Cliques',
                    'Conversões', 'Custo Semanal', 'Notas'])
   
   campaigns = CampaignMetric.objects.all()
   
   for campaign in campaigns:
      writer.writerow([
         campaign.date,
         campaign.platform,
         campaign.campaign_sector,
         campaign.funnel_position,
         campaign.clicks,
         campaign.conversions,
         campaign.weekly_cost,
         campaign.notes
      ])
      
   return response

def export_sm_metrics_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Redes-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Data', 'Rede Social', 'Seguidores', 'Impressões', 'Alcance',
                    'Engajamento', 'Notas'])
   
   sm_metrics = SocialMediaMetric.objects.all()
   
   for metric in sm_metrics:
      writer.writerow([
         metric.date,
         metric.network,
         metric.followers,
         metric.impressions,
         metric.reach,
         metric.engagement,
         metric.notes
      ])
      
   return response

def export_members_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Membros-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Nome', 'Sobrenome', 'Diretoria', 'Cargo', 
                    'Entrada', 'Saída', 'Email Profissional', 'Email Institucional', 
                    'Telefone', 'CPF', 'RG', 'Curso',
                    'Data de Nascimento', 'Endereço'])
   
   members = Member.objects.all()
   
   for member in members:
      writer.writerow([
         member.first_name,
         member.last_name,
         member.sector,
         member.role,
         member.date_of_entry,
         member.date_of_leave,
         member.professional_email,
         member.academic_email,
         member.phone,
         member.cpf,
         member.rg,
         member.degree,
         member.date_of_birth,
         member.address,
         member.notes
      ])
      
   return response

def export_services_csv(request):
   response = HttpResponse(content_type="text/csv")
   response['Content-Disposition'] = 'attachment; filename=Projetos-'+ str(datetime.datetime.now())+ '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Cliente', 'Link do Contrato', 'Gerente', 'Serviço', 
                    'Tempo Estimado', 'Tempo Real', 'Número de Consultores', 'Preço', 
                    'Notas'])
   
   services = Service.objects.all()
   
   for service in services:
      writer.writerow([
         f"{service.contract_id.client_id.lead_id.first_name} {service.contract_id.client_id.lead_id.last_name}",
         service.contract_id.link_of_contract,
         f"{service.member_id.first_name} {service.member_id.last_name}",
         service.project,
         service.estimated_time,
         service.actual_time,
         service.n_of_consultants,
         service.price,
         service.notes
      ])
      
   return response


#- REPORTS
class SalesReports(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/reports_sales.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username.split(".")[0].title()
        
        
        return context
    

#- HELP
class LearnMore(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/learn_more.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        authenticated_username = self.request.user.full_name.split()[0]
        context["name"] = authenticated_username.split(".")[0].title()
        
        
        return context


#- ANALYSIS
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