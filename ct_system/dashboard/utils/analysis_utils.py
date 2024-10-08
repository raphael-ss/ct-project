from ..models import SocialMediaMetric, Client, Company, Contract, CampaignMetric, Service, Member, Lead, Diagnostic, PostSales, Proposition, ServiceTag, Installment, Team
from datetime import datetime
import numpy as np
import pandas as pd

current_year = datetime.now().year

def revenue_per_sector(goal=127000):
    civil_total = 0
    tec_total = 0
    con_total = 0
    gp_total = 0
    ko_total = 0
    
    for contract in Contract.objects.filter(sector="Civil", date__year=current_year):
      civil_total += contract.total_value
    for contract in Contract.objects.filter(sector="Tecnologia", date__year=current_year):
      tec_total += contract.total_value
    for contract in Contract.objects.filter(sector="Consultoria", date__year=current_year):
      con_total += contract.total_value
    for contract in Contract.objects.filter(sector="Gestão de Pessoas", date__year=current_year):
      gp_total += contract.total_value
    for contract in Contract.objects.filter(sector="Comercial", date__year=current_year):
      ko_total += contract.total_value
      
    total = goal - (civil_total + tec_total + con_total + gp_total + ko_total)
      
    return [tec_total, civil_total, con_total, gp_total, ko_total, total]

def revenue_per_sector_legend(goal=127000):
        revenue = {}
        revenue['Civil'] = 0
        revenue['Tecnologia'] = 0
        revenue['Consultoria'] = 0
        revenue['Em Falta'] = 0
            
        for contract in Contract.objects.filter(sector="Civil", date__year=current_year):
            revenue['Civil'] += contract.total_value
        for contract in Contract.objects.filter(sector="Tecnologia", date__year=current_year):
            revenue['Tecnologia'] += contract.total_value
        for contract in Contract.objects.filter(sector="Consultoria", date__year=current_year):
            revenue['Consultoria'] += contract.total_value
            
        revenue['Em Falta'] = goal - (revenue['Civil'] + revenue['Tecnologia'] + revenue['Consultoria'])
        
        sorted_revenue = sorted(revenue.items(), key=lambda x: x[1], reverse=True)
        sorted_keys = [item[0] for item in sorted_revenue]
            
        return sorted_keys

def total_leads():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        if 'arrival_date' in df.columns:
            df['date'] = pd.to_datetime(df['arrival_date'])
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
        leads_in_month = Lead.objects.filter(arrival_date__month=month, arrival_date__year=current_year)
        if leads_in_month.count() == 0:
            if leads_over_time:
                leads_over_time.append(leads_over_time[-1])
            else:
                leads_over_time.append(0)
        else:
            if leads_over_time: 
                sum = leads_over_time[-1]
            for lead in leads_in_month:
                sum += 1
            leads_over_time.append(sum)    
    print(leads_over_time)
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
        if sector is None:
            avg_ticket = services.price.mean()
            return round(avg_ticket)
        else:
            contracts.rename(columns={
            'id': 'contract_id_id'},
            inplace=True)
            df = services.merge(contracts, how="inner", on="contract_id_id")
            if sector == "Tecnologia":
                tec = df.loc[df.sector == "Tecnologia"].shape[0]
                avg_ticket = df.loc[df.sector == "Tecnologia"].price.sum() / tec if tec != 0 else 0
                if not pd.isna(avg_ticket):
                    return round(avg_ticket)
            elif sector == "Civil":
                civ = df.loc[df.sector == "Civil"].shape[0]
                avg_ticket = df.loc[df.sector == "Civil"].price.sum() / civ if civ != 0 else 0
                if not pd.isna(avg_ticket):
                    return round(avg_ticket)
            elif sector == "Consultoria":
                con = df.loc[df.sector == "Consultoria"].shape[0]
                avg_ticket = df.loc[df.sector == "Consultoria"].price.sum() / con if con != 0 else 0
                if not pd.isna(avg_ticket):
                    return round(avg_ticket)
    return 0
        
def leads_per_sector():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        leads_by_sector = df.groupby('sector').first_name.count().reset_index()
        try:
            civ = list(leads_by_sector.loc[leads_by_sector.sector == "Civil"].first_name)[0]
        except IndexError:
            civ = 0
            
        try:
            con = list(leads_by_sector.loc[leads_by_sector.sector == "Consultoria"].first_name)[0]
        except IndexError:
            con = 0
            
        try:
            tec = list(leads_by_sector.loc[leads_by_sector.sector == "Tecnologia"].first_name)[0]
        except IndexError:
            tec = 0
        leads = [civ, con, tec]
        return leads
    return [0,0,0]

def leads_per_source():
    df = pd.DataFrame.from_records(Lead.objects.all().values())
    if not df.empty:
        leads_by_source = df.groupby('source').first_name.count().reset_index()
        
        try:
            ativa = list(leads_by_source.loc[leads_by_source.source == "Ativa"].first_name)[0]
        except IndexError:
            ativa = 0
            
        try:
            passiva = list(leads_by_source.loc[leads_by_source.source == "Passiva"].first_name)[0]
        except IndexError:
            passiva = 0
            
        try:
            google = list(leads_by_source.loc[leads_by_source.source == "Google Ads"].first_name)[0]
        except IndexError:
            google = 0
            
        try:
            face = list(leads_by_source.loc[leads_by_source.source == "Facebook Ads"].first_name)[0]
        except IndexError:
            face = 0
            
        try:
            indicacao = list(leads_by_source.loc[leads_by_source.source == "Indicação"].first_name)[0]
        except:
            indicacao = 0
            
        leads = [ativa,face,google,indicacao,passiva]
        return leads
    return [0,0,0,0,0]

def cpl():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not campaigns.empty and not leads.empty:
        traffic_leads = leads.loc[(leads.source == "GOOGLEADS") | (leads.source == "FBADS")]
        if not traffic_leads.empty:
            cost_per_lead = campaigns.weekly_cost.sum() / traffic_leads.shape[0]
            return round(cost_per_lead, 1)
    return '-'

def most_frequent_lead_score():
    diagnostics = pd.DataFrame.from_records(Diagnostic.objects.values())
    if not diagnostics.empty:
        scores = diagnostics['score'].value_counts()
        most_frequent_score = scores.idxmax()
        return most_frequent_score
    return "-"

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
        diagnostic = leads.loc[(leads.status == "PRÉ-DIAGNÓSTICO") | (leads.status == "PERDIDO PRÉ-DIAG") | (leads.status == "PRÉ-PROPOSTA")].shape[0]
        proposition = leads.loc[(leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP")].shape[0]
        if diagnostic > 0:
            return round(proposition/diagnostic, 1)*100
    return 0

def conversion_rate_proposition_to_closed():
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty:
        proposition = leads.loc[(leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP")|(leads.status == "CONTRATO FECHADO")].shape[0]
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

def projects_sold():
    contracts = Contract.objects.filter(date__year=current_year)
    projects = 0
    for contract in contracts:
        projects += contract.n_of_services
    return projects

def cumulative_contract_amount(current_year):
    # Initialize cumulative amounts to zero for each day of the year
    cumulative_amount = [0] * 365
    # Get contracts for the specified year
    contracts = Contract.objects.filter(date__year=current_year).order_by('date')

    previous_amount = 0
    current_day = 0
    
    for contract in contracts:
        day_of_year = contract.date.timetuple().tm_yday
        
        # Update all days from the last updated day to the current contract day
        while current_day < day_of_year:
            cumulative_amount[current_day] = previous_amount
            current_day += 1
        
        # Update the cumulative amount for the current contract day
        previous_amount += contract.total_value
        cumulative_amount[day_of_year - 1] = previous_amount
    
    # Fill the remaining days of the year with the last cumulative amount
    while current_day < 365:
        cumulative_amount[current_day] = previous_amount
        current_day += 1
    
    return cumulative_amount

def goal():
    monthly = [22000,22000,22000,22000,22000,22000,22000,22000,22000,22000,22000,22000]
    year_revenue = [0] * 365
    
    for i in range (0, 365):
        if i < 31:
            year_revenue[i] = monthly[0] / 31 * (i+1)
        elif i <= 59:
            year_revenue[i] = (monthly[1] / 29 * (i-30)) + monthly[0]
        elif i <= 91:
            year_revenue[i] = (monthly[2] / 31 * (i-59)) + monthly[1] + monthly[0]
        elif i < 121:
            year_revenue[i] = (monthly[3] / 30 * (i-90)) + monthly[2] + monthly[1] + monthly[0]
        elif i < 152:
            year_revenue[i] = (monthly[4] / 31 * (i-120)) + monthly[3] + monthly[2] + monthly[1] + monthly[0]
        elif i < 182:
            year_revenue[i] = (monthly[5] / 30 * (i-151)) + monthly[4] + monthly[3] + monthly[2] + monthly[1] + monthly[0]
        elif i < 213:
            year_revenue[i] = (monthly[6] / 31 * (i-181)) + monthly[5] + monthly[4] + monthly[3] + monthly[2] + monthly[1] + monthly[0]
        elif i < 244:
            year_revenue[i] = (monthly[7] / 31 * (i-212)) + monthly[6] + monthly[5] + monthly[4] + monthly[3] + monthly[2] + monthly[1] + monthly[0]
        elif i < 274:
            year_revenue[i] = (monthly[8] / 30 * (i-243)) + monthly[7] + monthly[6] + monthly[5] + monthly[4] + monthly[3] + monthly[2] + monthly[1] + monthly[0]
        elif i < 305:
            year_revenue[i] = (monthly[9] / 31 * (i-273)) + monthly[8] + monthly[7] + monthly[6] + monthly[5] + monthly[4] + monthly[3] + monthly[2] + monthly[1] + monthly[0]
        elif i < 335:
            year_revenue[i] = (monthly[10] / 30 * (i-304)) + monthly[9] + monthly[8] + monthly[7] + monthly[6] + monthly[5] + monthly[4] + monthly[3] + monthly[2] + monthly[1] + monthly[0]
        else:
            year_revenue[i] = (monthly[11] / 31 * (i-334)) + monthly[10] + monthly[9] + monthly[8] + monthly[7] + monthly[6] + monthly[5] + monthly[4] + monthly[3] + monthly[2] + monthly[1] + monthly[0]
            
        
    return year_revenue
   
def revenue_per_month():
    revenue = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        contracts_in_month = Contract.objects.filter(date__month=month, date__year=current_year)
        if contracts_in_month.count() == 0:
            if revenue:
                revenue.append(revenue[-1])
            else:
                revenue.append(0)
        else:
            if revenue:
                sum = revenue[-1]
            for contract in contracts_in_month:
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
    
    elif 7.5 < score <= 8.5:
        return 'B'
    
    elif 6.5 < score <= 7.5:
        return 'C'
    
    elif 5 < score <= 6.5:
        return 'D'
    
    else:
        return 'F'
         
def sales_funnel():
    
    leads = pd.DataFrame.from_records(Lead.objects.all().values())
    if not leads.empty:
        pre_diagnostic = leads.loc[(leads.status == "PRÉ-DIAGNÓSTICO")].shape[0]
        pre_proposition = leads.loc[(leads.status == "PRÉ-PROPOSTA")].shape[0]
        post_proposition = leads.loc[(leads.status == "PÓS-PROPOSTA")].shape[0]
        closed = leads.loc[leads.status == "CONTRATO FECHADO"].shape[0]
        
        return [pre_diagnostic, pre_proposition, post_proposition, closed]
    return []
    
def leads_per_score():
    
    diagnostics = pd.DataFrame.from_records(Diagnostic.objects.values())
    if not diagnostics.empty:
        a_score = diagnostics.loc[diagnostics.score == "A"].shape[0]
        b_score = diagnostics.loc[diagnostics.score == "B"].shape[0]
        c_score = diagnostics.loc[diagnostics.score == "C"].shape[0]
        d_score = diagnostics.loc[diagnostics.score == "D"].shape[0]
        f_score = diagnostics.loc[diagnostics.score == "F"].shape[0]
        return [a_score, b_score, c_score, d_score, f_score]
    return 0

def client_education_distribution():
    EFCOMPLETE = "Fundamental Completo"
    EMCOMPLETE = "Médio Completo"
    ESCOMPLETE = "Superior Completo"
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
    SINGLE = "Solteiro"
    MARRIED = "Casado"
    DIVORCED = "Divorciado"
    OTHER = "Outro"
    DATING = "União Estável"
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
    clients_df = pd.DataFrame.from_records(Client.objects.filter(lead_id__arrival_date__year=current_year).values())
    
    if not clients_df.empty:
        return clients_df.shape[0]
    
    return 0

def conversion_rate_general(string:bool):
    leads = pd.DataFrame.from_records(Lead.objects.values())
    
    if not leads.empty:
        all_statuses = leads.shape[0]
        closed = leads.loc[(leads.status == "CONTRATO FECHADO")].shape[0]
        
        if all_statuses > 0:
            if string: return str((closed / all_statuses) * 100)[:5]
            else: return (closed / all_statuses) * 100
    
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
        avg = companies.employees.sum() / companies.shape[0]
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
            
            if most_frequent_sector == 'Tecnologia':
                return "Tecnologia"
            elif most_frequent_sector == 'Civil':
                return "Civil"
            if most_frequent_sector == 'Consultoria':
                return "Consultoria"
        
        return "-"
    return "-"

def most_frequent_company_field():
    companies = pd.DataFrame.from_records(Company.objects.values())
    
    if not companies.empty:
        fields = companies['field_of_action'].value_counts()
        most_frequent_field = fields.idxmax()
        return most_frequent_field.lower().title()
    
    return "-"

def most_frequent_area_in_closing_leads():
    clients = pd.DataFrame.from_records(Client.objects.values())
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty and not clients.empty:
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
    if not leads.empty and not clients.empty:
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
    all_leads = Diagnostic.objects.all()

    if all_leads:
        mean_scores = np.mean([
            [lead.budget, lead.authority, lead.need, lead.timing, lead.time_to_respond, lead.behavior]
            for lead in all_leads
        ], axis=0)

        return mean_scores
    
    return []

def get_lead_scoring_data():
    leads = Diagnostic.objects.all()

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
        micro = companies.loc[companies.employees <= 9].shape[0]
        small = companies.loc[(companies.employees <= 49) & (companies.employees > 9)].shape[0]
        medium = companies.loc[(companies.employees <= 99) & (companies.employees > 49)].shape[0]
        big = companies.loc[(companies.employees > 99)].shape[0]
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
        return round((conversions/clicks)*100,2) if clicks != 0 else 0
    return 0

def most_efficient_platform():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    if not campaigns.empty:
        google = campaigns.loc[campaigns.platform == "Google Ads"]
        facebook = campaigns.loc[campaigns.platform == "Facebook Ads"]
        if (facebook.empty) or (google.empty):
            if facebook.empty:
                return "Google"
            elif google.empty:
                return "Face"
        conversion_google = google.conversions.sum() / google.clicks.sum()
        conversion_face = facebook.conversions.sum() / facebook.clicks.sum()
        if conversion_google > conversion_face:
            return "Google"
        else:
            return "Face"
    return "-"

def avg_weekly_cost():
    campaigns = pd.DataFrame.from_records(CampaignMetric.objects.values())
    if not campaigns.empty:
        cost = campaigns.weekly_cost.sum()
        total = campaigns.shape[0]
        return round(cost/total,1) if total != 0 else 0
    return 0

def google_clicks_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        campaigns_in_month = CampaignMetric.objects.filter(platform="Google Ads", date__month=month, date__year=current_year)
        if campaigns_in_month.count() == 0:
            value.append(0)
        else:
            for i,campaign in enumerate(campaigns_in_month):
                sum += campaign.clicks
                num = i
            value.append(sum)
    return value

def fb_clicks_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        campaigns_in_month = CampaignMetric.objects.filter(platform="Facebook Ads", date__month=month, date__year=current_year)
        if campaigns_in_month.count() == 0:
            value.append(0)
        else:
            for i,campaign in enumerate(campaigns_in_month):
                sum += campaign.clicks
                num = i
            value.append(sum)
    return value

def google_conversion_rate_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        campaigns_in_month = CampaignMetric.objects.filter(platform="Google Ads",date__month=month, date__year=current_year)
        if campaigns_in_month.count() == 0:
            value.append(0)
        else:
            for i,campaign in enumerate(campaigns_in_month):
                clicks = campaign.clicks
                conversions = campaign.conversions
                conv = round(conversions/clicks,2)*100 if clicks != 0 else 0
                sum += conv
                num = i
            sum /= num+1
            value.append(sum)
    return value

def fb_conversion_rate_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        campaigns_in_month = CampaignMetric.objects.filter(platform="Facebook Ads",date__month=month, date__year=current_year)
        if campaigns_in_month.count() == 0:
            value.append(0)
        else:
            for i,campaign in enumerate(campaigns_in_month):
                clicks = campaign.clicks
                conversions = campaign.conversions
                conv = round(conversions/clicks,2)*100 if clicks != 0 else 0
                sum += conv
                num = i
            sum /= num+1
            value.append(sum)
    return value

def google_cpc_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        campaigns_in_month = CampaignMetric.objects.filter(platform="Google Ads",date__month=month, date__year=current_year)
        if campaigns_in_month.count() == 0:
            value.append(0)
        else:
            for i,campaign in enumerate(campaigns_in_month):
                clicks = campaign.clicks
                cost = campaign.weekly_cost
                conv = round(cost/clicks,2) if clicks != 0 else 0
                sum += conv
                num = i
            sum /= num+1
            value.append(sum)
    return value

def fb_cpc_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        campaigns_in_month = CampaignMetric.objects.filter(platform="Facebook Ads",date__month=month, date__year=current_year)
        if campaigns_in_month.count() == 0:
            value.append(0)
        else:
            for i,campaign in enumerate(campaigns_in_month):
                clicks = campaign.clicks
                cost = campaign.weekly_cost
                conv = round(cost/clicks,2) if clicks != 0 else 0
                sum += conv
                num = i
            sum /= num+1
            value.append(sum)
    return value


#-SOCIAL MEDIA
def total_followers():
    sm_metrics = pd.DataFrame.from_records(SocialMediaMetric.objects.values())
    total = 0
    if not sm_metrics.empty:
        instagram = sm_metrics.loc[sm_metrics.network == "Instagram"].followers.values
        linkedin = sm_metrics.loc[sm_metrics.network == "LinkedIn"].followers.values
        tiktok = sm_metrics.loc[sm_metrics.network == "TikTok"].followers.values
        facebook = sm_metrics.loc[sm_metrics.network == "Facebook"].followers.values
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
        instagram = sm_metrics.loc[sm_metrics.network == "Instagram"].reach.values
        linkedin = sm_metrics.loc[sm_metrics.network == "LinkedIn"].reach.values
        tiktok = sm_metrics.loc[sm_metrics.network == "TikTok"].reach.values
        facebook = sm_metrics.loc[sm_metrics.network == "Facebook"].reach.values
        network_list = [instagram, linkedin, tiktok, facebook]
        current_reachs = [net[-1] if net.any() else 0 for net in network_list]
        last_reachs = []
        for i, net in enumerate(network_list):
            if net.any():
                try:
                    last_reachs.append(net[-2] if len(net) > 1 else net[-1])
                except IndexError:
                    last_reachs.append(current_reachs[i])
                    
            else:
                last_reachs.append(0)
                
        for i, reach in enumerate(current_reachs):
            growth.append(1 - (reach / last_reachs[i]) if last_reachs[i] != 0 else 0)
                
        for percent in growth:
            mean_growth += percent
            
        return round(mean_growth/len(growth), 2)*100 if len(growth) > 0 else 0
    return 0
    
def mean_engagement():
    sm_metrics = pd.DataFrame.from_records(SocialMediaMetric.objects.values())
    if not sm_metrics.empty:
        return round(sm_metrics.engagement.sum() / sm_metrics.shape[0])
    return 0

def most_impact_network():
    sm_metrics = pd.DataFrame.from_records(SocialMediaMetric.objects.values())
    if not sm_metrics.empty:
        instagram = sm_metrics.loc[sm_metrics.network == "Instagram"].reach.sum()
        linkedin = sm_metrics.loc[sm_metrics.network == "LinkedIn"].reach.sum()
        tiktok = sm_metrics.loc[sm_metrics.network == "TikTok"].reach.sum()
        facebook = sm_metrics.loc[sm_metrics.network == "Facebook"].reach.sum()
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
    return "-"

def ig_followers_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="Instagram",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].followers)
        else:
            for i,metric in enumerate(metrics_in_month):
                followers = metric.followers
                sum += followers
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def face_followers_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="Facebook",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].followers)
        else:
            for i,metric in enumerate(metrics_in_month):
                followers = metric.followers
                sum += followers
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def linkedin_followers_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="LinkedIn",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].followers)
        else:
            for i,metric in enumerate(metrics_in_month):
                followers = metric.followers
                sum += followers
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def tiktok_followers_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="TikTok",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].followers)
        else:
            for i,metric in enumerate(metrics_in_month):
                followers = metric.followers
                sum += followers
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def ig_reach_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="Instagram",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].reach)
        else:
            for i,metric in enumerate(metrics_in_month):
                reach = metric.reach
                sum += reach
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def face_reach_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="Facebook",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].reach)
        else:
            for i,metric in enumerate(metrics_in_month):
                reach = metric.reach
                sum += reach
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def linkedin_reach_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="LinkedIn",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].reach)
        else:
            for i,metric in enumerate(metrics_in_month):
                reach = metric.reach
                sum += reach
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def tiktok_reach_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="TikTok",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].reach)
        else:
            for i,metric in enumerate(metrics_in_month):
                reach = metric.reach
                sum += reach
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def ig_engagement_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="Instagram",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].engagement)
        else:
            for i,metric in enumerate(metrics_in_month):
                engagement = metric.engagement
                sum += engagement
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def face_engagament_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="Facebook",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].engagement)
        else:
            for i,metric in enumerate(metrics_in_month):
                engagement = metric.engagement
                sum += engagement
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def linkedin_engagement_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="LinkedIn",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].engagement)
        else:
            for i,metric in enumerate(metrics_in_month):
                engagement = metric.engagement
                sum += engagement
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

def tiktok_engagement_over_time():
    value = []
    months = ['01', '02', '03', '04', 
              '05', '06', '07', '08', 
              '09', '10', '11', '12']
    
    for month in months:
        sum = 0
        num = 0
        metrics_in_month = SocialMediaMetric.objects.filter(network="TikTok",date__month=month, date__year=current_year)
        if metrics_in_month.count() == 0:
            value.append(0)
        elif metrics_in_month.count() == 1:
            value.append(metrics_in_month[0].engagement)
        else:
            for i,metric in enumerate(metrics_in_month):
                engagement = metric.engagement
                sum += engagement
            sum /= num+1 if num != 0 else num+2
            value.append(sum)
    return value

#-PROJETOS
def mean_delay():
    projects = pd.DataFrame.from_records(Service.objects.values())
    if not projects.empty:
        projects['delay'] = projects.actual_time - projects.estimated_time
        return round(projects.delay.mean())
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
    


#-CHARTS

def leads_per_sector_CHART():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        leads_by_sector = df.groupby('sector').first_name.count().reset_index()
        try:
            civ = list(leads_by_sector.loc[leads_by_sector.sector == "Civil"].first_name)[0]
        except IndexError:
            civ = 0
            
        try:
            con = list(leads_by_sector.loc[leads_by_sector.sector == "Consultoria"].first_name)[0]
        except IndexError:
            con = 0
            
        try:
            tec = list(leads_by_sector.loc[leads_by_sector.sector == "Tecnologia"].first_name)[0]
        except IndexError:
            tec = 0
        leads = {'Civil': civ, 'Consultoria': con, 'Tecnologia': tec}
        return leads.values()
    return [0,0,0]

def leads_per_sector_LEGEND():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        leads_by_sector = df.groupby('sector').first_name.count().reset_index()
        try:
            civ = list(leads_by_sector.loc[leads_by_sector.sector == "Civil"].first_name)[0]
        except IndexError:
            civ = 0
            
        try:
            con = list(leads_by_sector.loc[leads_by_sector.sector == "Consultoria"].first_name)[0]
        except IndexError:
            con = 0
            
        try:
            tec = list(leads_by_sector.loc[leads_by_sector.sector == "Tecnologia"].first_name)[0]
        except IndexError:
            tec = 0
        leads = {'Civil': civ, 'Consultoria': con, 'Tecnologia': tec}
        
        sorted_leads = sorted(leads.items(), key=lambda x: x[1], reverse=True)
        sorted_keys = [item[0] for item in sorted_leads]
        
        return sorted_keys
    
    return [0, 0, 0]

def leads_per_source_LEGEND():
    df = pd.DataFrame.from_records(Lead.objects.values())
    if not df.empty:
        leads_by_source = df.groupby('source').first_name.count().reset_index()
        try:
            google = list(leads_by_source.loc[leads_by_source.source == "Google Ads"].first_name)[0]
        except IndexError:
            google = 0
            
        try:
            facebook = list(leads_by_source.loc[leads_by_source.source == "Facebook Ads"].first_name)[0]
        except IndexError:
            facebook = 0
            
        try:
            active = list(leads_by_source.loc[leads_by_source.source == "Ativa"].first_name)[0]
        except IndexError:
            active = 0
            
        try:
            passive = list(leads_by_source.loc[leads_by_source.source == "Passiva"].first_name)[0]
        except IndexError:
            passive = 0

        try:
            referral = list(leads_by_source.loc[leads_by_source.source == "Indicação"].first_name)[0]
        except IndexError:
            referral = 0
                        
        leads = {'Google Ads': google, 'Facebook Ads': facebook, 'Prosp. Ativa': active, 'Prosp. Passiva': passive, 'Indicação': referral}
        
        sorted_leads = sorted(leads.items(), key=lambda x: x[1], reverse=True)
        sorted_keys = [item[0] for item in sorted_leads]
        
        return sorted_keys
    
    return [0, 0, 0, 0]

def sales_funnel_churn_rate(by_channel=False):
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty:
        if not by_channel:
            churn_rates = list()
            pre_diagnostic = leads.shape[0]
            lost_pre_diagnostic = leads.loc[(leads.status == "PERDIDO PRÉ-DIAG")].shape[0]
            if pre_diagnostic > 0:
                churn_rates.append(round((lost_pre_diagnostic / pre_diagnostic) * 100, 2))
            
            pre_proposal = leads.loc[(leads.status == "PRÉ-PROPOSTA") | (leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP") | (leads.status == "PERDIDO PRÉ-PROP") | (leads.status == "CONTRATO FECHADO")].shape[0]
            lost_pre_proposal = leads.loc[(leads.status == "PERDIDO PRÉ-PROP")].shape[0]
            if pre_proposal > 0:
                churn_rates.append(round((lost_pre_proposal / pre_proposal) * 100, 2))
                
            post_proposal = leads.loc[(leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP") | (leads.status == "CONTRATO FECHADO")].shape[0]
            lost_post_proposal = leads.loc[(leads.status == "PERDIDO PÓS-PROP")].shape[0]
            if post_proposal > 0:
                churn_rates.append(round((lost_post_proposal / post_proposal) * 100, 2))
                
            return churn_rates
        else:
            churn_rates_by_channel = dict()
            leads_by_source = leads.groupby('source')
            for source, group in leads_by_source:
                pre_diagnostic = group.shape[0]
                lost_pre_diagnostic = group.loc[(group.status == "PERDIDO PRÉ-DIAG")].shape[0]
                if pre_diagnostic > 0:
                    churn_rates_by_channel[source] = {'Pré-Diagnóstico':round((lost_pre_diagnostic / pre_diagnostic * 100), 2)} 
                else:
                    churn_rates_by_channel[source] = {'Pré-Diagnóstico': "SEM DADOS"}
                
                pre_proposal = group.loc[(group.status == "PRÉ-PROPOSTA") | (group.status == "PÓS-PROPOSTA") | (group.status == "PERDIDO PÓS-PROP") | (group.status == "PERDIDO PRÉ-PROP") | (group.status == "CONTRATO FECHADO")].shape[0]
                lost_pre_proposal = group.loc[(group.status == "PERDIDO PRÉ-PROP")].shape[0]
                
                if pre_proposal > 0:
                    if source in churn_rates_by_channel:
                        churn_rates_by_channel[source].update({"Pré-Proposta": round((lost_pre_proposal / pre_proposal) * 100, 2)})
                    else:
                        churn_rates_by_channel[source] = {"Pré-Proposta": round((lost_pre_proposal / pre_proposal * 100), 2)}
                else:
                    churn_rates_by_channel[source].update({"Pré-Proposta": "SEM DADOS"})
               
                post_proposal = group.loc[(group.status == "PÓS-PROPOSTA") | (group.status == "PERDIDO PÓS-PROP") | (group.status == "CONTRATO FECHADO")].shape[0]
                lost_post_proposal = group.loc[(group.status == "PERDIDO PÓS-PROP")].shape[0]
                
                if post_proposal > 0:
                    churn_rates_by_channel[source].update({"Pós-Proposta":round((lost_post_proposal / post_proposal * 100), 2)})
                else:
                    churn_rates_by_channel[source].update({"Pós-Proposta": "SEM DADOS"})
            
            sorted_churn_rates = dict(sorted(churn_rates_by_channel.items(), key=lambda x: x[0]))
            return list(sorted_churn_rates.values()),list(sorted_churn_rates.keys())
    
    return 0

def sales_funnel_conversion_rate(by_channel=False, by_salesman=False):
    leads = pd.DataFrame.from_records(Lead.objects.values())
    if not leads.empty:
        if not by_channel and not by_salesman:
            conversion_rates = list()
            diagnostic = leads.loc[(leads.status == "PRÉ-DIAGNÓSTICO") | (leads.status == "PERDIDO PRÉ-DIAG") | (leads.status == "PRÉ-PROPOSTA") | (leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP")].shape[0]
            proposition = leads.loc[(leads.status == "PÓS-PROPOSTA") | (leads.status == "PERDIDO PÓS-PROP") | (leads.status == "CONTRATO FECHADO")].shape[0]
            if diagnostic > 0:
                conversion_rates.append(round((proposition / diagnostic) * 100, 2))
            
            closed = leads.loc[(leads.status == "CONTRATO FECHADO")].shape[0]
            
            if proposition > 0:
                conversion_rates.append(round((closed / proposition) * 100, 2))
                
            return conversion_rates
        
        elif by_salesman:
            conversion_rates_by_salesman = dict()
            members = pd.DataFrame.from_records(Member.objects.values())
            members.drop(columns=['sector','role','date_of_entry','date_of_leave','professional_email','academic_email','phone','cpf','rg','degree','date_of_birth','address','notes'], inplace=True)
            members.rename(columns={
                'id': 'member_id_id'},
                inplace=True)
            leads_and_members = leads.merge(members, how="left", on='member_id_id')
            print(leads_and_members.head())
            leads_by_salesman = leads_and_members.groupby('first_name_y')
            
            for salesman, group in leads_by_salesman:
                diagnostic = group.loc[(group.status == "PRÉ-DIAGNÓSTICO") | (group.status == "PERDIDO PRÉ-DIAG") | (group.status == "PRÉ-PROPOSTA") | (group.status == "PÓS-PROPOSTA") | (group.status == "PERDIDO PÓS-PROP")].shape[0]
                proposition = group.loc[(group.status == "PÓS-PROPOSTA") | (group.status == "PERDIDO PÓS-PROP") | (group.status == "CONTRATO FECHADO")].shape[0]
                if diagnostic > 0:
                    conversion_rates_by_salesman[salesman] = {'Diagnóstico':round((proposition / diagnostic * 100), 2)} 
                else:
                    conversion_rates_by_salesman[salesman] = {'Diagnóstico': "SEM DADOS"}
                
                closed = group.loc[(group.status == "CONTRATO FECHADO")].shape[0]
                
                if proposition > 0:
                    if salesman in conversion_rates_by_salesman:
                        conversion_rates_by_salesman[salesman].update({"Proposta": round((closed / proposition) * 100, 2)})
                    else:
                        conversion_rates_by_salesman[salesman] = {"Proposta": round((closed / proposition * 100), 2)}
                else:
                    conversion_rates_by_salesman[salesman].update({"Proposta": "SEM DADOS"})
            
            leads_per_salesman_count = leads_and_members.groupby('first_name_y').id.count().reset_index()
            
            sorted_conversion_rates = dict(sorted(conversion_rates_by_salesman.items(), key=lambda x: x[0]))
            
            return list(sorted_conversion_rates.values()), list(sorted_conversion_rates.keys()), leads_per_salesman_count.first_name_y, leads_per_salesman_count.id
                      
        elif by_channel:
            conversion_rates_by_channel = dict()
            leads_by_source = leads.groupby('source')
            for source, group in leads_by_source:
                diagnostic = group.loc[(group.status == "PRÉ-DIAGNÓSTICO") | (group.status == "PERDIDO PRÉ-DIAG") | (group.status == "PRÉ-PROPOSTA") | (group.status == "PÓS-PROPOSTA") | (group.status == "PERDIDO PÓS-PROP")].shape[0]
                proposition = group.loc[(group.status == "PÓS-PROPOSTA") | (group.status == "PERDIDO PÓS-PROP") | (group.status == "CONTRATO FECHADO")].shape[0]
                if diagnostic > 0:
                    conversion_rates_by_channel[source] = {'Diagnóstico':round((proposition / diagnostic * 100), 2)} 
                else:
                    conversion_rates_by_channel[source] = {'Diagnóstico': "SEM DADOS"}
                
                closed = group.loc[(group.status == "CONTRATO FECHADO")].shape[0]
                
                if proposition > 0:
                    if source in conversion_rates_by_channel:
                        conversion_rates_by_channel[source].update({"Proposta": round((closed / proposition) * 100, 2)})
                    else:
                        conversion_rates_by_channel[source] = {"Proposta": round((closed / proposition * 100), 2)}
                else:
                    conversion_rates_by_channel[source].update({"Proposta": "SEM DADOS"})
            
            sorted_churn_rates = dict(sorted(conversion_rates_by_channel.items(), key=lambda x: x[0]))
            return list(sorted_churn_rates.values()),list(sorted_churn_rates.keys())









