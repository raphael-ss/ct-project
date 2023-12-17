from ..models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member, Lead
from datetime import datetime
import numpy as np
import pandas as pd

def revenue_per_sector():
    civil_total = 0
    tec_total = 0
    con_total = 0
      
    for contract in Contract.objects.filter(sector="CIV"):
      civil_total += contract.total_value
    for contract in Contract.objects.filter(sector="TEC"):
      tec_total += contract.total_value
    for contract in Contract.objects.filter(sector="CON"):
      con_total += contract.total_value
      
    return [tec_total, civil_total, con_total]

def total_leads():
    df = pd.DataFrame.from_records(Lead.objects.values())
    df['date'] = pd.to_datetime(df['date'])
    current_year_leads = df[df['date'].dt.year == datetime.now().year].shape[0]

    return current_year_leads
    
def average_ticket_per_sector():
    df = pd.DataFrame.from_records(Contract.objects.values())
    revenue_by_sector = df.groupby('sector').total_value.mean().reset_index()
    sectors = list(revenue_by_sector.sector)
    average = list(revenue_by_sector.total_value)
    return average, sectors
        
def average_ticket():
    df = pd.DataFrame.from_records(Service.objects.values())
    avg_ticket = df.price.mean()
    return round(avg_ticket, 2)
    
def leads_per_sector():
    df = pd.DataFrame.from_records(Lead.objects.values())
    revenue_by_sector = df.groupby('sector').first_name.count().reset_index()
    sectors = list(revenue_by_sector.sector)
    revenue = list(revenue_by_sector.first_name)
    return revenue, sectors

def cpl():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    cost_per_lead = campaigns.weekly_cost.sum() / leads.shape[0]
    return cost_per_lead

def cpl_per_platform():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    cost_per_platform = campaigns.groupby('platform').weekly_cost.sum().reset_index()
    leads_per_platform = leads.loc[leads.source == 'GOOGLEADS' | leads.source == 'FBADS'].groupby('source').first_name.count().reset_index()
    
    return 
    
    
def revenue_per_month():
    revenue = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
      sum = 0
      contracts_in_month = Contract.objects.filter(date__month=month)
      if contracts_in_month.count() is 0:
         if revenue:
            revenue.append(revenue[-1])
         else:
            revenue.append(0)
      else:
         for contract in contracts_in_month:
            sum = revenue[-1]
            sum += contract.total_value
            revenue.append(sum)
            
    return revenue


def total_revenue():
    total_revenue = 0
    for contract in Contract.objects.filter(date__year=datetime.now().date().year):
       total_revenue += contract.total_value
    return round(total_revenue)
    
    
def cac():
    pass

def lead_scoring(object):
    score = 0

    budget = object.budget
    authority = object.authority
    need = object.need
    timing = object.timing
    
    takes_time_to_respond = object.time_to_respond 
    bad_behavior = object.behavior

    params = [budget, authority, need, timing, takes_time_to_respond, bad_behavior]
    
    for parameter in params:
        score += parameter
    
    score /= len(params)
    
    if 8.5 < score <= 10:
        return 'A'
    
    elif 7 < score <= 8.5:
        return 'B'
    
    elif 6 < score <= 7:
        return 'C'
    
    else:
        return 'D'
        
    
        
        