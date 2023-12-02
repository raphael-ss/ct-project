from django.contrib import admin
from .models import SocialMediaMetric, Client, CampaignMetric, Company, Contract, Member, Service, Lead
# Register your models here.

admin.site.register(Client)
admin.site.register(Lead)
admin.site.register(Company)
admin.site.register(Contract)
admin.site.register(Member)
admin.site.register(Service)
admin.site.register(CampaignMetric)
admin.site.register(SocialMediaMetric)
