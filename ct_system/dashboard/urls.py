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
    path('projetos', views.ServiceList.as_view(), name='services'),
    path('empresas', views.CompanyList.as_view(), name='companies'),

    path('leads/adicionar-lead', views.LeadCreate.as_view(), name='add_lead'),
    path('clientes/adicionar-cliente', views.ClientCreate.as_view(), name='add_client_data'),
    path('redes-sociais/adicionar-metrica', views.SocialMediaMetricCreate.as_view(), name='add_sm_metric'),
    path('campanhas/adicionar-metrica', views.CampaignMetricCreate.as_view(), name='add_campaign_metric'),
    path('contratos/adicionar-contrato', views.ContractCreate.as_view(), name='add_contract_data'),
    path('membros/adicionar-membro', views.MemberCreate.as_view(), name='add_member_data'),
    path('projetos/adicionar-projeto', views.ServiceCreate.as_view(), name='add_service_data'),
    path('empresas/adicionar-empresa', views.CompanyCreate.as_view(), name='add_company_data'),
    path('leads/adicionar-diagnostico', views.DiagnosticCreate.as_view(), name='add_diagnostic'),
    path('leads/adicionar-proposta', views.PropositionCreate.as_view(), name='add_proposition'),
    path('leads/adicionar-diagnostico', views.DiagnosticCreate.as_view(), name='add_diagnostic'),
    path('contratos/adicionar-parcelas', views.InstallmentCreate.as_view(), name='add_installment'),
    path('projetos/adicionar-tag', views.ServiceTagCreate.as_view(), name='add_servicetag'),
    path('projetos/adicionar-equipe', views.TeamCreate.as_view(), name='add_team'),
    path('contratos/adicionar-pos-venda', views.PostSalesCreate.as_view(), name='add_postsales'),

    path('leads/atualizar-dados/<pk>', views.LeadUpdate.as_view(), name='update_lead'),
    path('clientes/atualizar-dados/<pk>', views.ClientUpdate.as_view(), name='update_client_data'),
    path('redes-sociais/atualizar-metrica/<pk>', views.SocialMediaMetricUpdate.as_view(), name='update_sm_metric'),
    path('campanhas/atualizar-metrica/<pk>', views.CampaignMetricUpdate.as_view(), name='update_campaign_metric'),
    path('contratos/atualizar-dados/<pk>', views.ContractUpdate.as_view(), name='update_contract_data'),
    path('membros/atualizar-dados/<pk>', views.MemberUpdate.as_view(), name='update_member_data'),
    path('projetos/atualizar-dados/<pk>', views.ServiceUpdate.as_view(), name='update_service_data'),
    path('empresas/atualizar-dados/<pk>', views.CompanyUpdate.as_view(), name='update_company_data'),
    path('leads/atualizar-diagnostico/<pk>', views.DiagnosticUpdate.as_view(), name='update_diagnostic'),
    path('leads/atualizar-proposta/<pk>', views.PropositionUpdate.as_view(), name='update_proposition'),

    path('leads/excluir-dados/<pk>', views.LeadDelete.as_view(), name='delete_lead'),
    path('clientes/excluir-dados/<pk>', views.ClientDelete.as_view(), name='delete_client_data'),
    path('redes-sociais/excluir-metrica/<pk>', views.SocialMediaMetricDelete.as_view(), name='delete_sm_metric'),
    path('campanhas/excluir-metrica/<pk>', views.CampaignMetricDelete.as_view(), name='delete_campaign_metric'),
    path('contratos/excluir-dados/<pk>', views.ContractDelete.as_view(), name='delete_contract_data'),
    path('membros/excluir-dados/<pk>', views.MemberDelete.as_view(), name='delete_member_data'),
    path('projetos/excluir-dados/<pk>', views.ServiceDelete.as_view(), name='delete_service_data'),
    path('empresas/excluir-dados/<pk>', views.CompanyDelete.as_view(), name='delete_company_data'),
    path('leads/excluir-diagnostico/<pk>', views.DiagnosticDelete.as_view(), name='delete_diagnostic'),
    path('leads/excluir-proposta/<pk>', views.PropositionDelete.as_view(), name='delete_proposition'),
    
    path('leads/pesquisar-leads', csrf_exempt(views.search_lead), name='search_lead'),
    path('clientes/pesquisar-clientes', csrf_exempt(views.search_client), name='search_client'),
    path('empresas/pesquisar-empresas', csrf_exempt(views.search_company), name='search_company'),
    path('contratos/pesquisar-contratos', csrf_exempt(views.search_contract), name='search_contract'),
    path('campanhas/pesquisar-campanhas', csrf_exempt(views.search_campaign), name='search_campaign'),
    path('redes-sociais/pesquisar-metricas', csrf_exempt(views.search_social_media), name='search_social_media'),
    path('membros/pesquisar-membros', csrf_exempt(views.search_member), name='search_member'),
    path('servicos/pesquisar-servicos', csrf_exempt(views.search_project), name='search_project'),
    
    
    path('leads/exportar-leads-csv', views.export_leads_csv, name='export_leads_csv'),
    path('clientes/exportar-clientes-csv', views.export_clients_csv, name='export_clients_csv'),
    path('empresas/exportar-empresas-csv', views.export_companies_csv, name='export_companies_csv'),
    path('contratos/exportar-contratos-csv', views.export_contracts_csv, name='export_contracts_csv'),
    path('campanhas/exportar-campanhas-csv', views.export_campaigns_csv, name='export_campaigns_csv'),
    path('redes-sociais/exportar-redes-csv', views.export_sm_metrics_csv, name='export_sm_metrics_csv'),
    path('membros/exportar-membros-csv', views.export_members_csv, name='export_members_csv'),
    path('servicos/exportar-servicos-csv', views.export_services_csv, name='export_services_csv'),
    
    path('leads/lead/<pk>', views.LeadDetail.as_view(), name="lead_detail"),
    path('clientes/cliente/<pk>', views.ClientDetail.as_view(), name="client_detail"),
    
    path('relatorios/comercial', views.SalesReports.as_view(), name='reports_sales'),
    
    path('gerar-analise-publico-alvo', views.generate_target_analysis, name='generate_target_analysis'),
    path('gerar-analise-funil-de-vendas', views.generate_funnel_analysis, name='generate_funnel_analysis'),
    
    path('update_lead/', csrf_exempt(views.update_lead), name='update_lead'),
    path('get_lead_status/<int:lead_id>/', views.get_lead_status, name='get_lead_status'),
    
    path('leads/funil-de-vendas', views.Funnel.as_view(), name='funnel'),
    
    
    path('ajuda/saiba-mais', views.LearnMore.as_view(), name="learn_more"),
]