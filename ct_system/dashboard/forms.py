from django import forms
from .models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member, Lead, Diagnostic, PostSales, Proposition, ServiceTag, Installment, Team
#from crispy_forms.layout import Layout, Submit, Field
from .utils.analysis_utils import lead_scoring
from django.template.loader import render_to_string
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import PrependedText

class BaseCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

class LeadCreateForm(BaseCreateForm): 
    class Meta:
        model = Lead
        fields = '__all__'
        
class DiagnosticCreateForm(BaseCreateForm):
    def save(self, commit=True):
        instance = super(DiagnosticCreateForm, self).save(commit=False)
        instance.score = lead_scoring(instance)
        if commit:
            instance.save()
        return instance   
    class Meta:
        model = Diagnostic
        fields = '__all__'
        exclude = ['score']
             
class PropositionCreateForm(BaseCreateForm): 
    class Meta:
        model = Proposition
        fields = '__all__'
        
class ClientCreateForm(BaseCreateForm):
    class Meta:
        model = Client
        fields = '__all__'

class CompanyCreateForm(BaseCreateForm):
    class Meta:
        model = Company
        fields = '__all__'
       
class ContractCreateForm(BaseCreateForm):
    class Meta:
        model = Contract
        fields = '__all__'
        
class InstallmentCreateForm(BaseCreateForm): 
    class Meta:
        model = Installment
        fields = '__all__'
        
class MemberCreateForm(BaseCreateForm):
    class Meta:
        model = Member
        fields = '__all__'

class ServiceTagCreateForm(BaseCreateForm): 
    class Meta:
        model = ServiceTag
        fields = '__all__'
        
class ServiceCreateForm(BaseCreateForm):
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['tags']

class TeamCreateForm(BaseCreateForm): 
    class Meta:
        model = Team
        fields = '__all__'
        
class PostSalesCreateForm(BaseCreateForm): 
    class Meta:
        model = PostSales
        fields = '__all__'
        
class CampaignMetricCreateForm(BaseCreateForm):
    class Meta:
        model = CampaignMetric
        fields = '__all__'

class SocialMediaMetricCreateForm(BaseCreateForm):
    class Meta:
        model = SocialMediaMetric
        fields = '__all__'
        
