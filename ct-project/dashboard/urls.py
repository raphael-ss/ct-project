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
    path('redes-sociais/adicionar-metrica', views.add_sm_metric, name='add_sm_metric'),
]