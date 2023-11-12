from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('redes-sociais', views.social_media, name='social_media'),
    path('clientes', views.clients, name='clients'),
    path('campanhas', views.campaigns, name='campaigns'),
    path('contratos', views.contracts, name='contracts'),
    path('membros', views.members, name='members'),
    path('servicos', views.services, name='services'),
    path('empresas', views.companies, name='companies'),

    path('redes-sociais/adicionar-metrica', views.SocialMediaMetricCreate.as_view(), name='add_sm_metric'),
    path('clientes/adicionar-dados', views.ClientCreate.as_view(), name='add_client_data'),
    path('campanhas/adicionar-metrica', views.CampaignMetricCreate.as_view(), name='add_campaign_metric'),
    path('contratos/adicionar-dados', views.ContractCreate.as_view(), name='add_contract_data'),
    path('membros/adicionar-dados', views.MemberCreate.as_view(), name='add_member_data'),
    path('servicos/adicionar-dados', views.ServiceCreate.as_view(), name='add_service_data'),
    path('empresas/adicionar-dados', views.CompanyCreate.as_view(), name='add_company_data'),
]