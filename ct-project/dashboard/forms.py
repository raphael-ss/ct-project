from django import forms
from .models import Client, SocialMediaMetric, Contract, Company, CampaignMetric, Member, Service


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'gender': 'Sexo',
            'source': 'Origem',
            'email': 'E-mail',
            'phone': 'Telefone',
            'cpf': 'CPF',
            'birth_date': 'Data de Nascimento',
            'profession': 'Profissão',
            'education': 'Nível Educacional',
            'marital_status': 'Estado Civil',
            'monthly_income': 'Renda Mensal',
            'funnel_time': 'Tempo de Funil (Dias)',
            'notes': 'Notas',
        }
        

class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        labels = {
            'company_name': 'Nome da Empresa',
            'cnpj': 'CNPJ',
            'field_of_action': 'Área de Atuação',
            'annual_revenue': 'Faturamento Anual',
            'n_of_locations': 'N° de Locais',
            'n_of_employees': 'N° de Funcionários',
            'proof_of_registration_link': 'Link da Prova de Registro',
            'notes': 'Notas',
        }
        
class ContractCreateForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        labels = {
            'sector': 'Setor',
            'total_value': 'Valor Total',
            'n_of_services': 'N° de Serviços',
            'date': 'Data',
            'link_of_contract': 'Link do Contrato',
            'notes': 'Notas',
        }
        
class MemberCreateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'sector': 'Setor',
            'email': 'E-mail',
            'phone': 'Telefone',
            'cpf': 'CPF',
            'degree': 'Curso de Graduação',
            'date_of_birth': 'Data de Nascimento',
            'role': 'Cargo',
            'date_of_entry': 'Data de Início',
            'date_of_leave': 'Data de Saída',
            'notes': 'Notas',
        }


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        labels = {
            'project': 'Projeto',
            'estimated_time': 'Tempo Estimado',
            'actual_time': 'Tempo Real',
            'n_of_consultants': 'N° de Consultores',
            'price': 'Preço',
            'notes': 'Notas',
        }


class CampaignMetricCreateForm(forms.ModelForm):
    class Meta:
        model = CampaignMetric
        fields = '__all__'
        labels = {
            'date': 'Data',
            'platform': 'Plataforma',
            'campaign_sector': 'Setor da Campanha',
            'funnel_position': 'Posição do Funil',
            'weekly_cost': 'Custo Semanal',
            'notes': 'Notas',
        }


class SocialMediaMetricCreateForm(forms.ModelForm):
    class Meta:
        model = SocialMediaMetric
        fields = '__all__'
        labels = {
            'date': 'Data',
            'network': 'Rede Social',
            'followers': 'Seguidores',
            'impressions': 'Impressões',
            'reach': 'Alcance',
            'engagement': 'Engajamento',
            'visits': 'Visitas',
            'notes': 'Notas',
        }
