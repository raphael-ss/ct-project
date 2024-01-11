from django.contrib import admin
from .models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member, Lead, Diagnostic, PostSales, Proposition, ServiceTag, Installment, Team
# Register your models here.

admin.site.register(Client)
admin.site.register(Lead)
admin.site.register(Company)
admin.site.register(Contract)
admin.site.register(Member)
admin.site.register(Service)
admin.site.register(CampaignMetric)
admin.site.register(SocialMediaMetric)
admin.site.register(Diagnostic)
admin.site.register(PostSales)
admin.site.register(Proposition)
admin.site.register(ServiceTag)
admin.site.register(Installment)
admin.site.register(Team)
