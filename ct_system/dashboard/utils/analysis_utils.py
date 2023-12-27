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
    if not df.empty:
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            current_year_leads = df[df['date'].dt.year == datetime.now().year].shape[0]
            return current_year_leads
    return 0
    
def leads_per_gender():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        leads_by_gender = df.groupby('gender').first_name.count().reset_index()
        leads = list(leads_by_gender.first_name)
        return leads
    return 0
    
def leads_per_time():
    leads_over_time = list()
    
    months = ['01', '02', '03', '04', 
               '05', '06', '07', '08', 
               '09', '10', '11', '12']
        
    for month in months:
        sum = 0
        leads_in_month = Lead.objects.filter(date__month=month)
        if leads_in_month.count() == 0:
            if leads_over_time:
                leads_over_time.append(leads_over_time[-1])
            else:
                leads_over_time.append(0)
        else:
            for lead in leads_in_month:
                if leads_over_time: sum = leads_over_time[-1]
                sum += 1
                leads_over_time.append(sum)    
                
    return leads_over_time
     
def leads_goal(goal:int):
    leads_goal_monthly = list()
    for i in range(13):
        if i == 0:
            continue
        leads_goal_monthly.append(goal*i)
    return leads_goal_monthly      
        
def average_ticket_per_sector():
    df = pd.DataFrame.from_records(Contract.objects.values())
    if not df.empty:
        revenue_by_sector = df.groupby('sector').total_value.mean().reset_index()
        average = list(revenue_by_sector.total_value)
        return average
    return 0
        
def average_ticket(sector=None):
    services = pd.DataFrame.from_records(Service.objects.values())
    contracts = pd.DataFrame.from_records(Contract.objects.values())
    if not services.empty and not contracts.empty:
        if sector == None:
            avg_ticket = services.price.mean()
            return round(avg_ticket)
        else:
            contracts.rename(columns={
            'id': 'contract_id_id'},
            inplace=True)
            df = services.merge(contracts, how="inner", on="contract_id_id")
            if sector == "TEC":
                tec = df.loc[df.sector == "TEC"].shape[0]
                avg_ticket = df.loc[df.sector == "TEC"].price.sum() / tec if tec != 0 else 0
                if not pd.isna(avg_ticket):
                    return round(avg_ticket)
            elif sector == "CIV":
                civ = df.loc[df.sector == "CIV"].shape[0]
                avg_ticket = df.loc[df.sector == "CIV"].price.sum() / civ if civ != 0 else 0
                if not pd.isna(avg_ticket):
                    return round(avg_ticket)
            elif sector == "CON":
                con = df.loc[df.sector == "CON"].shape[0]
                avg_ticket = df.loc[df.sector == "CON"].price.sum() / con if con != 0 else 0
                if not pd.isna(avg_ticket):
                    return round(avg_ticket)
    return 0
        
def leads_per_sector():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        leads_by_sector = df.groupby('sector').first_name.count().reset_index()
        leads = list(leads_by_sector.first_name)
        return leads
    return 0

def leads_per_source():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        leads_by_sector = df.groupby('source').first_name.count().reset_index()
        leads = list(leads_by_sector.first_name)
        leads_by_sector.sort_values(by=['source'])
        return leads
    return 0

def cpl():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not campaigns.empty and not leads.empty:
        cost_per_lead = campaigns.weekly_cost.sum() / leads.loc[(leads.source == "GOOGLEADS") | (leads.source == "FBADS")].shape[0]
        return round(cost_per_lead, 2)
    return 0

def most_frequent_lead_score():
    lead_df = pd.DataFrame.from_records(Lead.objects.values())
    if not lead_df.empty:
        scores = lead_df['score'].value_counts()
        most_frequent_score = scores.idxmax()
        return most_frequent_score
    return 0

def most_frequent_lead_source():
    lead_df = pd.DataFrame.from_records(Lead.objects.values())
    if not lead_df.empty:
        sources = lead_df['source'].value_counts()
        most_frequent_source = sources.idxmax()
        return most_frequent_source.lower().title()
    return 0

def conversion_rate_diagnostic_to_proposition():
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty:
        diagnostic = leads.loc[(leads.status == "PRÉ-DIAGNÓSTICO") | (leads.status == "PERDIDO PRÉ-DIAG") | (leads.status == "PRÉ-PROPOSTA") | (leads.status == "PERDIDO PRÉ-PROP")].shape[0]
        proposition = leads.loc[(leads.status == "PÓS-PROPOSTA")].shape[0]
        if diagnostic > 0:
            return round(proposition/diagnostic, 1)*100
    return 0

def conversion_rate_proposition_to_closed():
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty:
        proposition = leads.loc[(leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP") | (leads.status == "CONTRATO FECHADO")].shape[0]
        closed = leads.loc[(leads.status == "CONTRATO FECHADO")].shape[0]
        if proposition > 0:
            return round(closed/proposition, 1)*100
    return 0

def cpl_per_platform():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not campaigns.empty and not leads.empty:
        cost_per_platform = campaigns.groupby('platform').weekly_cost.sum().reset_index()
        leads_per_platform = leads.loc[(leads.source == 'GOOGLEADS') | (leads.source == 'FBADS')].groupby('source').first_name.count().reset_index()
        return cost_per_platform, leads_per_platform
    return 0

def revenue_per_month():
    revenue = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        contracts_in_month = Contract.objects.filter(date__month=month)
        if contracts_in_month.count() == 0:
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

def lead_scoring(object):
    score = 0

    budget = object.budget
    authority = object.authority
    need = object.need
    timing = object.timing
    
    time_to_respond = object.time_to_respond 
    behavior = object.behavior

    params = [budget, authority, need, timing, time_to_respond, behavior]
    
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
         
def sales_funnel():
    
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty:
        pre_diagnostic = leads.loc[(leads.status == "PRÉ-DIAGNÓSTICO") | (leads.status == "PERDIDO PRÉ-DIAG")].shape[0]
        pre_proposition = leads.loc[(leads.status == "PRÉ-PROPOSTA") | (leads.status == "PERDIDO PRÉ-PROP")].shape[0]
        post_proposition = leads.loc[(leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP")].shape[0]
        closed = leads.loc[leads.status == "CONTRATO FECHADO"].shape[0]
        
        return [pre_diagnostic, pre_proposition, post_proposition, closed]
    return []
    
def leads_per_score():
    
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty:
        a_score = leads.loc[leads.score == "A"].shape[0]
        b_score = leads.loc[leads.score == "B"].shape[0]
        c_score = leads.loc[leads.score == "C"].shape[0]
        d_score = leads.loc[leads.score == "D"].shape[0]
        return [a_score, b_score, c_score, d_score]
    return 0

def client_education_distribution():
    EFCOMPLETE = "EF-COMPLETO"
    EMCOMPLETE = "EM-COMPLETO"
    ESCOMPLETE = "ES-COMPLETO"
    clients_df = pd.DataFrame.from_records(Client.objects.values())
    if not clients_df.empty:
        bin_1 = clients_df.loc[clients_df.education == EFCOMPLETE].shape[0]
        bin_2 = clients_df.loc[clients_df.education == EMCOMPLETE].shape[0]
        bin_3 = clients_df.loc[clients_df.education == ESCOMPLETE].shape[0]
        return [bin_1, bin_2, bin_3]
    return 0

def client_income_distribution():
    UPTO_3 = "3"
    UPTO_6 = "6"
    UPTO_9 = "9"
    ABOVE_9 = "+9"
    clients_df = pd.DataFrame.from_records(Client.objects.values())
    if not clients_df.empty:
        bin_1 = clients_df.loc[clients_df.income == UPTO_3].shape[0]
        bin_2 = clients_df.loc[clients_df.income == UPTO_6].shape[0]
        bin_3 = clients_df.loc[clients_df.income == UPTO_9].shape[0]
        bin_4 = clients_df.loc[clients_df.income == ABOVE_9].shape[0]
        return [bin_1, bin_2, bin_3, bin_4]
    return 0

def client_civil_state_distribution():
    SINGLE = "SOLTEIRO"
    MARRIED = "CASADO"
    DIVORCED = "DIVORCIADO"
    OTHER = "OUTRO"
    DATING = "UNIÃO ESTÁVEL"
    clients_df = pd.DataFrame.from_records(Client.objects.values())
    if not clients_df.empty:
        bin_1 = clients_df.loc[clients_df.marital_status == SINGLE].shape[0]
        bin_2 = clients_df.loc[clients_df.marital_status == MARRIED].shape[0]
        bin_3 = clients_df.loc[clients_df.marital_status == DIVORCED].shape[0]
        bin_4 = clients_df.loc[clients_df.marital_status == DATING].shape[0]
        bin_5 = clients_df.loc[clients_df.marital_status == OTHER].shape[0]
        return [bin_1, bin_2, bin_3, bin_4, bin_5]
    return 0

def client_age_distribution():
    clients_df = pd.DataFrame.from_records(Client.objects.values())
    if not clients_df.empty:
        clients_df['age'] = datetime.now().date() - clients_df.birth_date
        clients_df['age_in_years'] = clients_df['age'] / pd.Timedelta(days=365)
        bin_1 = clients_df.loc[clients_df.age_in_years <= 25].shape[0]
        bin_2 = clients_df.loc[(clients_df.age_in_years <= 40) & (clients_df.age_in_years > 25)].shape[0]
        bin_3 = clients_df.loc[(clients_df.age_in_years <= 60) & (clients_df.age_in_years > 40)].shape[0]
        bin_4 = clients_df.loc[(clients_df.age_in_years > 60)].shape[0]
        return [bin_1, bin_2, bin_3, bin_4]
    return 0

def cac():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    clients_df = pd.DataFrame.from_records(Client.objects.values())
    if not campaigns.empty and not clients_df.empty:
        clients = clients_df.shape[0]
        cost = campaigns.weekly_cost.sum()
        return round(cost/clients, 2)
    return 0

def client_mean_funnel_time():
    clients_df = pd.DataFrame.from_records(Client.objects.values())
    
    if not clients_df.empty:
        return round(clients_df.funnel_time.mean())
    
    return 0

def client_count():
    clients_df = pd.DataFrame.from_records(Client.objects.values())
    
    if not clients_df.empty:
        return clients_df.shape[0]
    
    return 0

def conversion_rate_general():
    leads = pd.DataFrame.from_records(Lead.objects.values())
    
    if not leads.empty:
        all_statuses = leads.loc[(leads.status != "CONTRATO FECHADO")].shape[0]
        closed = leads.loc[(leads.status == "CONTRATO FECHADO")].shape[0]
        
        if all_statuses > 0:
            return round(closed / all_statuses, 1) * 100
    
    return 0

def average_company_revenue():
    companies = pd.DataFrame.from_records(Company.objects.values())
    
    if not companies.empty:
        avg = companies.annual_revenue.sum() / companies.shape[0]
        return round(avg)
    
    return 0

def average_company_size():
    companies = pd.DataFrame.from_records(Company.objects.values())
    
    if not companies.empty:
        avg = companies.n_of_employees.sum() / companies.shape[0]
        return round(avg)
    
    return 0

def most_frequent_sector_for_companies():
    companies = pd.DataFrame.from_records(Company.objects.values())
    clients = pd.DataFrame.from_records(Client.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if (not companies.empty) and (not clients.empty) and (not leads.empty):
        clients.rename(columns={
            'id': 'client_id_id'},
            inplace=True)
        leads.rename(columns={
            'id': 'lead_id_id'},
            inplace=True)
        df = companies.merge(clients, how="left", on='client_id_id').merge(leads, how="left", on='lead_id_id')

        if not df.empty:
            sectors = df['sector'].value_counts()
            most_frequent_sector = sectors.idxmax()
            
            if most_frequent_sector == 'TEC':
                return "Tecnologia"
            elif most_frequent_sector == 'CIV':
                return "Civil"
            if most_frequent_sector == 'CON':
                return "Consultoria"
        
        return ""
    return ""

def most_frequent_company_field():
    companies = pd.DataFrame.from_records(Company.objects.values())
    
    if not companies.empty:
        fields = companies['field_of_action'].value_counts()
        most_frequent_field = fields.idxmax()
        return most_frequent_field.lower().title()
    
    return ""

def most_frequent_area_in_closing_leads():
    clients = pd.DataFrame.from_records(Client.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    leads.rename(columns={
        'id': 'lead_id_id'},
        inplace=True)
    df = clients.merge(leads, how="left", on='lead_id_id')

    if not df.empty:
        field = df['field_of_action'].value_counts()
        most_frequent_fields = field.head(3).index.tolist()
        most_frequent_fields = [area.lower().title() for area in most_frequent_fields]
        return most_frequent_fields
    
    return []

def most_frequent_area_in_closing_leads_count():
    clients = pd.DataFrame.from_records(Client.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    leads.rename(columns={
        'id': 'lead_id_id'},
        inplace=True)
    df = clients.merge(leads, how="left", on='lead_id_id')

    if not df.empty:
        field = df['field_of_action'].value_counts()
        counts_of_most_frequent_areas = field.head(3).tolist()
        return counts_of_most_frequent_areas
    
    return []

def lead_scoring_radar_data():
    all_leads = Lead.objects.all()

    if all_leads:
        # Calculate the mean of each lead scoring attribute
        mean_scores = np.mean([
            [lead.budget, lead.authority, lead.need, lead.timing, lead.time_to_respond, lead.behavior]
            for lead in all_leads
        ], axis=0)

        return mean_scores
    
    return []

def get_lead_scoring_data():
    leads = Lead.objects.all()

    if leads:
        # Initialize lists to store attribute values
        budget_values = []
        authority_values = []
        need_values = []
        timing_values = []
        time_to_respond_values = []
        behavior_values = []

        for lead in leads:
            budget_values.append(lead.budget)
            authority_values.append(lead.authority)
            need_values.append(lead.need)
            timing_values.append(lead.timing)
            time_to_respond_values.append(lead.time_to_respond)
            behavior_values.append(lead.behavior)

        # Create a dictionary to store the attribute values
        data = {
            'budget_values': budget_values,
            'authority_values': authority_values,
            'need_values': need_values,
            'timing_values': timing_values,
            'time_to_respond_values': time_to_respond_values,
            'behavior_values': behavior_values,
        }

        return data
    
    return {}

#-EMPRESAS
def most_frequent_companies_areas():
    companies = pd.DataFrame.from_records(Company.objects.values())
    if not companies.empty:
        field = companies['field_of_action'].value_counts()
        most_frequent_fields = field.head(3).index.tolist()
        most_frequent_fields = [area.lower().title() for area in most_frequent_fields]
        return most_frequent_fields
    
    return []

def most_frequent_companies_areas_count():
    companies = pd.DataFrame.from_records(Company.objects.values())
    if not companies.empty:
        field = companies['field_of_action'].value_counts()
        counts_of_most_frequent_areas = field.head(3).tolist()
        return counts_of_most_frequent_areas
    
    return []

def company_size_distribution():
    companies = pd.DataFrame.from_records(Company.objects.values())
    if not companies.empty:
        micro = companies.loc[companies.n_of_employees <= 9].shape[0]
        small = companies.loc[(companies.n_of_employees <= 49) & (companies.n_of_employees > 9)].shape[0]
        medium = companies.loc[(companies.n_of_employees <= 99) & (companies.n_of_employees > 49)].shape[0]
        big = companies.loc[(companies.n_of_employees > 99)].shape[0]
        return [micro, small, medium, big]
    
    return []
    

#-CAMPANHAS
def cpc():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    if not campaigns.empty:
        clicks = campaigns.clicks.sum()
        cost = campaigns.weekly_cost.sum()
        return round(cost/clicks,2) if clicks != 0 else 0
    return 0

def conversion_rate_campaign():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    if not campaigns.empty:
        clicks = campaigns.clicks.sum()
        conversions = campaigns.conversions.sum()
        return round(conversions/clicks,2)*100 if clicks != 0 else 0
    return 0

def most_efficient_platform():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    if not campaigns.empty:
        google = campaigns.loc[campaigns.platform == "GOOGLEADS"]
        facebook = campaigns.loc[campaigns.platform == "FBADS"]
        if (facebook.empty) or (google.empty):
            if facebook.empty:
                return "Google"
            elif google.empty:
                return "Facebook"
        conversion_google = google.clicks.sum() / google.conversions.sum()
        conversion_face = facebook.clicks.sum() / facebook.conversions.sum()
        if conversion_google > conversion_face:
            return "Google"
        else:
            return "Facebook"
    return 0

def avg_weekly_cost():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    if not campaigns.empty:
        cost = campaigns.weekly_cost.sum()
        total = campaigns.shape[0]
        return round(cost/total,2) if total != 0 else 0
    return 0

#-SOCIAL MEDIA
def total_followers():
    sm_metrics = pd.DataFrame.from_records(SocialMediaMetric.objects.values())
    total = 0
    if not sm_metrics.empty:
        instagram = sm_metrics.loc[sm_metrics.network == "IG"].followers.values
        linkedin = sm_metrics.loc[sm_metrics.network == "LI"].followers.values
        tiktok = sm_metrics.loc[sm_metrics.network == "TK"].followers.values
        facebook = sm_metrics.loc[sm_metrics.network == "FC"].followers.values
        network_list = [instagram, linkedin, tiktok, facebook]
        followers = [net[-1] for net in network_list if net.any()]
        for value in followers:
            total += value
        return total
    return 0

def social_media_growth():
    sm_metrics = pd.DataFrame.from_records(SocialMediaMetric.objects.values())
    growth = []
    mean_growth = 0
    if not sm_metrics.empty:
        instagram = sm_metrics.loc[sm_metrics.network == "IG"].reach.values
        linkedin = sm_metrics.loc[sm_metrics.network == "LI"].reach.values
        tiktok = sm_metrics.loc[sm_metrics.network == "TK"].reach.values
        facebook = sm_metrics.loc[sm_metrics.network == "FC"].reach.values
        network_list = [instagram, linkedin, tiktok, facebook]
        current_reachs = [net[-1] for net in network_list if net.any()]
        last_reachs = []
        for i,net in enumerate(network_list):
            if net.any():
                try:
                    last_reachs.append(net[-2])
                except IndexError:
                    last_reachs.append(current_reachs[i])
                
        for i, reach in enumerate(current_reachs):
                growth.append(1 - (reach / last_reachs[i]))
                
        for percent in growth:
            mean_growth += percent
            
        return round(mean_growth/len(growth), 2)*100
    return 0
    
def mean_engagement():
    sm_metrics = pd.DataFrame.from_records(SocialMediaMetric.objects.values())
    if not sm_metrics.empty:
        return round(sm_metrics.engagement.sum() / sm_metrics.shape[0])
    return 0

def most_impact_network():
    sm_metrics = pd.DataFrame.from_records(SocialMediaMetric.objects.values())
    if not sm_metrics.empty:
        instagram = sm_metrics.loc[sm_metrics.network == "IG"].reach.sum()
        linkedin = sm_metrics.loc[sm_metrics.network == "LI"].reach.sum()
        tiktok = sm_metrics.loc[sm_metrics.network == "TK"].reach.sum()
        facebook = sm_metrics.loc[sm_metrics.network == "FC"].reach.sum()
        network_list = [instagram, linkedin, tiktok, facebook]
        network_list.sort()
        most_impact = network_list[-1]
        if most_impact == instagram:
            return "Instagram"
        elif most_impact == linkedin:
            return "LinkedIn"
        elif most_impact == tiktok:
            return "TikTok"
        elif most_impact == facebook:
            return "Facebook"
    return ""


#-PROJETOS
def mean_delay():
    projects = pd.DataFrame.from_records(Service.objects.values())
    if not projects.empty:
        projects['delay'] = projects.actual_time - projects.estimated_time
        return round(projects.delay.mean(), 1)
    return 0

def real_mean_deadline():
    projects = pd.DataFrame.from_records(Service.objects.values())
    if not projects.empty:
        return round(projects.actual_time.mean())
    return 0

def projects_on_time():
    projects = pd.DataFrame.from_records(Service.objects.values())
    if not projects.empty:
        projects_inside_deadline = projects.loc[projects.actual_time <= projects.estimated_time].shape[0]
        all_projects = projects.shape[0]
        return round(projects_inside_deadline / all_projects, 1)*100
    return 0
    

#-CONTRATOS

def contract_ticket_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        contracts_in_month = Contract.objects.filter(date__month=month)
        if contracts_in_month.count() == 0:
            value.append(0)
        else:
            for i,contract in enumerate(contracts_in_month):
                sum += contract.total_value
                num = i
            sum /= num+1
            value.append(sum)
    return value

def tec_contract_ticket_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        contracts_in_month = Contract.objects.filter(date__month=month, sector="TEC")
        if contracts_in_month.count() == 0:
            value.append(0)
        else:
            for i,contract in enumerate(contracts_in_month):
                sum += contract.total_value
                num = i
            sum /= num+1
            value.append(sum)
    return value
    
def civ_contract_ticket_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        contracts_in_month = Contract.objects.filter(date__month=month, sector="CIV")
        if contracts_in_month.count() == 0:
            value.append(0)
        else:
            for i,contract in enumerate(contracts_in_month):
                sum += contract.total_value
                num = i
            sum /= num+1
            value.append(sum)
    return value

def con_contract_ticket_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        contracts_in_month = Contract.objects.filter(date__month=month, sector="CON")
        if contracts_in_month.count() == 0:
            value.append(0)
        else:
            for i,contract in enumerate(contracts_in_month):
                sum += contract.total_value
                num = i
            sum /= num+1
            value.append(sum)
    return value
    