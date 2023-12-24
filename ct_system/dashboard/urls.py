from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('leads', views.LeadList.as_view(), name='leads'),
    path('clientes', views.ClientList.as_view(), name='clients'),
    path('redes-sociais', views.SocialMediaMetricList.as_view(), name='social_media'),
    path('campanhas', views.CampaignMetricList.as_view(), name='campaigns'),
    path('contratos', views.ContractList.as_view(), name='contracts'),
    path('membros', views.MemberList.as_view(), name='members'),
    path('servicos', views.ServiceList.as_view(), name='services'),
    path('empresas', views.CompanyList.as_view(), name='companies'),

    path('leads/adicionar-dados', views.LeadCreate.as_view(), name='add_lead'),
    path('clientes/adicionar-dados', views.ClientCreate.as_view(), name='add_client_data'),
    path('redes-sociais/adicionar-metrica', views.SocialMediaMetricCreate.as_view(), name='add_sm_metric'),
    path('campanhas/adicionar-metrica', views.CampaignMetricCreate.as_view(), name='add_campaign_metric'),
    path('contratos/adicionar-dados', views.ContractCreate.as_view(), name='add_contract_data'),
    path('membros/adicionar-dados', views.MemberCreate.as_view(), name='add_member_data'),
    path('servicos/adicionar-dados', views.ServiceCreate.as_view(), name='add_service_data'),
    path('empresas/adicionar-dados', views.CompanyCreate.as_view(), name='add_company_data'),

    path('leads/atualizar-dados/<pk>', views.LeadUpdate.as_view(), name='update_lead'),
    path('clientes/atualizar-dados/<pk>', views.ClientUpdate.as_view(), name='update_client_data'),
    path('redes-sociais/atualizar-metrica/<pk>', views.SocialMediaMetricUpdate.as_view(), name='update_sm_metric'),
    path('campanhas/atualizar-metrica/<pk>', views.CampaignMetricUpdate.as_view(), name='update_campaign_metric'),
    path('contratos/atualizar-dados/<pk>', views.ContractUpdate.as_view(), name='update_contract_data'),
    path('membros/atualizar-dados/<pk>', views.MemberUpdate.as_view(), name='update_member_data'),
    path('servicos/atualizar-dados/<pk>', views.ServiceUpdate.as_view(), name='update_service_data'),
    path('empresas/atualizar-dados/<pk>', views.CompanyUpdate.as_view(), name='update_company_data'),

    path('leads/excluir-dados/<pk>', views.LeadDelete.as_view(), name='delete_lead'),
    path('clientes/excluir-dados/<pk>', views.ClientDelete.as_view(), name='delete_client_data'),
    path('redes-sociais/excluir-metrica/<pk>', views.SocialMediaMetricDelete.as_view(), name='delete_sm_metric'),
    path('campanhas/excluir-metrica/<pk>', views.CampaignMetricDelete.as_view(), name='delete_campaign_metric'),
    path('contratos/excluir-dados/<pk>', views.ContractDelete.as_view(), name='delete_contract_data'),
    path('membros/excluir-dados/<pk>', views.MemberDelete.as_view(), name='delete_member_data'),
    path('servicos/excluir-dados/<pk>', views.ServiceDelete.as_view(), name='delete_service_data'),
    path('empresas/excluir-dados/<pk>', views.CompanyDelete.as_view(), name='delete_company_data'),
    
    path('leads/pesquisar-leads', csrf_exempt(views.search_lead), name='search_lead'),
    path('clientes/pesquisar-clientes', csrf_exempt(views.search_client), name='search_client'),
    
    
    path('leads/exportar-leads-csv', views.export_leads_csv, name='export_leads_csv'),
    path('clientes/exportar-clientes-csv', views.export_clients_csv, name='export_clients_csv'),
    
    
    path('gerar-analise-publico-alvo', views.generate_target_analysis, name='generate_target_analysis'),
]