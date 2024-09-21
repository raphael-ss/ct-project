from django.db import models
from django.utils.timezone import now

class Member(models.Model):
    ADVISOR = "Assessor"
    CONSULTANT = "Consultor"
    MANAGER = "Gerente"
    DIRECTOR = "Diretor"
    PRESIDENT = "Presidente"
    ROLE = [
        (ADVISOR, "Assessor(a)"),
        (CONSULTANT, "Consultor(a)"),
        (MANAGER, "Gerente"),
        (DIRECTOR, "Diretor(a)"),
        (PRESIDENT, "Presidente"),
    ]
    
    TEC = "Tecnologia"
    CIV = "Civil"
    COM = "Comercial"
    RH = "Recursos Humanos"
    ADMFIN = "Adm-Fin"
    CON = "Consultoria"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (COM, "Comercial"),
        (RH, "Recursos Humanos"),
        (ADMFIN, "Adminstrativo Financeiro"),
        (CON, "Consultoria"),
    ]
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    sector = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    date_of_entry = models.DateField(null=False)
    date_of_leave = models.DateField(null=True)
    professional_email = models.CharField(max_length=80)
    academic_email = models.CharField(max_length=80, null=True)
    phone = models.CharField(max_length=16)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=9)
    degree = models.CharField(max_length=50,null=True)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=300, null=True)
    notes = models.CharField(max_length=150, default="...")

    def get_absolute_url(self):
        return "/membros"

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    
    class Meta:
        ordering: ['-date_of_entry']
        
class Lead(models.Model):
    MALE = "Homem"
    FEMALE = "Mulher"
    GENDER = [
        (MALE, "Homem"),
        (FEMALE, "Mulher")
    ]
    INDICATION = "Indicação"
    FACEBOOKADS = "Facebook Ads"
    GOOGLEADS = "Google Ads"
    ACTIVE = "Ativa"
    PASSIVE = "Passiva"
    SOURCE = [
        (INDICATION, "Indicação"),
        (FACEBOOKADS, "Facebook Ads"),
        (GOOGLEADS, "Google Ads"),
        (ACTIVE, "Prospecção Ativa"),
        (PASSIVE, "Prospecção Passiva"),
    ]
    
    PRED = "PRÉ-DIAGNÓSTICO"
    PPD = "PERDIDO PRÉ-DIAG"
    PREP = "PRÉ-PROPOSTA"
    PPREP = "PERDIDO PRÉ-PROP"
    POSTP = "PÓS-PROPOSTA"
    PPOSP = "PERDIDO PÓS-PROP"
    CLOSED = "CONTRATO FECHADO"
    STATUS = [
        (PRED, "Pré-Diagnóstico"),
        (PPD, "Perdido Pré-Diagnóstico"),
        (PREP, "Pré-Proposta"),
        (PPREP, "Perdido Pré-Proposta"),
        (POSTP, "Pós-Proposta"),
        (PPOSP, "Perdido Pós-Proposta"),
        (CLOSED, "Contrato Fechado"),
    ]
    TEC = "Tecnologia"
    CIV = "Civil"
    CON = "Consultoria"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (CON, "Consultoria"),
    ]
    member_id = models.ForeignKey(Member, limit_choices_to={
        'sector': 'Comercial'
    }, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    sector = models.CharField(max_length=15, choices=SECTORS, default=TEC)
    gender = models.CharField(max_length=10, choices=GENDER)
    status = models.CharField(max_length=20, choices=STATUS, default=PRED)
    source = models.CharField(max_length=20, choices=SOURCE)
    email = models.CharField(max_length=80, null=True)
    phone = models.CharField(max_length=16, default="")
    field_of_action = models.CharField(max_length=30, default="", null=True)
    arrival_date = models.DateField()
    notes = models.CharField(max_length=300, default="...")
    
    def get_absolute_url(self):
        return "/leads"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"
    
    def to_json(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'sector': self.sector,
            'gender': self.gender,
            'status': self.status,
            'source': self.source,
            'email': self.email,
            'phone': self.phone,
            'field_of_action': self.field_of_action,

            'notes': self.notes,
        }

        return data
    
    def get_score(self):
        object = self.diagnostic_set
        return object.first().score if object.exists() else '-'
    class Meta:
        ordering: ['-date']
        
class Diagnostic(models.Model):
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE)
    budget = models.IntegerField(null=True)
    authority = models.IntegerField(null=True)
    need = models.IntegerField(null=True)
    timing = models.IntegerField(null=True)
    time_to_respond = models.IntegerField(null=True)
    behavior = models.IntegerField(null=True)
    score = models.CharField(max_length=1)
    date = models.DateField()
    estimated_price = models.FloatField()
    notes = models.CharField(max_length=300, default="...")
    
    def __str__(self):
        return f"{self.lead_id.first_name} {self.lead_id.last_name} - {self.date}"
    
class Proposition(models.Model):
    lead_id = lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE)
    date = models.DateField()
    link = models.CharField(max_length=300)
    notes = models.CharField(max_length=300, default="...")
    
    def __str__(self):
        return f"{self.lead_id.first_name} {self.lead_id.last_name} - {self.date}"

class Client(models.Model):
    EFCOMPLETE = "Fundamental Completo"
    EMCOMPLETE = "Médio Completo"
    ESCOMPLETE = "Superior Completo"
    EDUCATION = [
        (EFCOMPLETE, "Ensino Fundamental Completo"),
        (EMCOMPLETE, "Ensino Médio Completo"),
        (ESCOMPLETE, "Ensino Superior Completo"),
    ]
    SINGLE = "Solteiro"
    MARRIED = "Casado"
    DIVORCED = "Divorciado"
    OTHER = "Outro"
    DATING = "União Estável"
    STATUS = [
        (SINGLE, 'Solteiro(a)'),
        (MARRIED, "Casado(a)"),
        (DIVORCED, "Divorciado(a)"),
        (DATING, "União Estável"),
        (OTHER, "Outro"),
    ]
    UPTO_3 = "3"
    UPTO_6 = "6"
    UPTO_9 = "9"
    ABOVE_9 = "+9"
    INCOME = [
        (UPTO_3, "Até 3 salários mínimos"),
        (UPTO_6, "Até 6 salários mínimos"),
        (UPTO_9, "Até 9 salários mínimos"),
        (ABOVE_9, "Acima de 9 salários mínimos"),
    ]

    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, limit_choices_to={
        'status': 'CONTRATO FECHADO'
    })
    cpf = models.CharField(max_length=14)
    birth_date = models.DateField(null=True)
    education = models.CharField(max_length=25, choices=EDUCATION, default=ESCOMPLETE, null=True)
    marital_status = models.CharField(max_length=15, choices=STATUS, default=SINGLE, null=True)
    income = models.CharField(max_length=5, choices=INCOME, null=True)
    funnel_time = models.PositiveIntegerField(default=15)
    notes = models.CharField(max_length=150, default="...")

    def get_absolute_url(self):
        return "/clientes"
    
    def __str__(self):
        return f"{self.lead_id.first_name} {self.lead_id.last_name}" 
    
    class Meta:
        ordering: ['-lead_id.date']
 
class Company(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=80)
    cnpj = models.CharField(max_length=18)
    field_of_action = models.CharField(max_length=100)
    annual_revenue = models.FloatField(null=True)
    locations = models.PositiveSmallIntegerField(null=True)
    employees = models.PositiveSmallIntegerField(null=True)
    registration_link = models.CharField(max_length=300, null=True)
    notes = models.CharField(max_length=150, default="...")

    def get_absolute_url(self):
        return "/empresas"

    def __srt__(self):
        return f"{self.company_name}"
    
    class Meta:
        ordering: ['-client_id.lead_id.date']
        
class Contract(models.Model):
    TEC = "Tecnologia"
    CIV = "Civil"
    CON = "Consultoria"
    GP = "Gestão de Pessoas"
    KO = "Comercial"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (CON, "Consultoria"),
        (GP, "Gestão de Pessoas"),
        (KO, "Comercial"),
    ]
    
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    sector = models.CharField(max_length=40, choices=SECTORS)
    total_value = models.FloatField(null=False)
    n_of_services = models.PositiveSmallIntegerField()
    date = models.DateField(default=now)
    deadline = models.DateField()
    contract_link = models.CharField(max_length=300)
    notes = models.CharField(max_length=150, default="...")

    def get_absolute_url(self):
        return "/contratos"

    def __str__(self):
        return f"{self.client_id.lead_id.first_name} {self.client_id.lead_id.last_name} - {self.sector}" 
    class Meta:
        ordering: ['-date']
        
class Installment(models.Model):
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField()
    paid_off = models.BooleanField()
        
class ServiceTag(models.Model):
    name = models.CharField(max_length=50, null=False)
    color = models.CharField(max_length=7, null=True, default="#000000")
    
class Service(models.Model):
    SYS = "Sistema"
    SITE = "Website"
    APP = "Aplicativo"
    LP = "Landing Page"
    PROTOTYPE = "Protótipo"
    ECOM = "E-Commerce"
    ARQ = "Arquitetônico"
    HID = "Hidrossanitário"
    ELE = "Elétrico"
    CAP = "Captação"
    INC = "Incêndio"
    MAP = "Mapeamento de Processos"
    EST = "Planejamento Estratégico"
    NEG = "Plano de Negócios"
    GEM = "Gestão de Marketing"
    GEF = "Gestão Financeira"
    GEE = "Gestão de Estoque"
    GEO = "Gestão Operacional"
    SER = [
        (SYS, "Sistema Web"),
        (SITE, "Website"),
        (APP, "Aplicativo"),
        (LP, "Landing Page"),
        (PROTOTYPE, "Protótipo"),
        (ECOM, "E-Commerce"),
        (ARQ, "Proj. Arquitetônico"),
        (HID, "Proj. Hidrossanitário"),
        (ELE, "Proj. Elétrico"),
        (CAP, "Proj. de Captação"),
        (INC, "Proj. de Combate à Incêndio"),
        (MAP, "Mapeamento de Processos"),
        (EST, "Planejamento Estratégico"),
        (NEG, "Plano de Negócios"),
    ]
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ServiceTag)
    project = models.CharField(max_length=40)
    consultants = models.PositiveSmallIntegerField()
    estimated_time = models.PositiveSmallIntegerField(null=False)
    actual_time = models.PositiveSmallIntegerField(null=True)
    price = models.FloatField()
    status = models.CharField(max_length=40, default="Não Iniciado")
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/servicos"

    def __str__(self):
        return f"{self.contract_id.client_id.lead_id.first_name} {self.contract_id.client_id.lead_id.last_name} - {self.project}"
    
    class Meta:
        ordering: ['-contract_id.date']  
        
class Team(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField()
    members = models.ManyToManyField(Member)    
    
class PostSales(models.Model):
    TS = "Totalmente Satisfeito"
    SA = "Satisfeito"
    NE = "Neutro"
    IN = "Insatisfeito"
    TI = "Totalmente Insatisfeito"
    SATISFACTION = [
        (TS, "Totalmente Satisfeito"),
        (SA, "Satisfeito"),
        (NE, "Neutro"),
        (IN, "Insatisfeito"),
        (TI, "Totalmente Insatisfeito"),
    ]
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    csat = models.CharField(max_length=30, choices=SATISFACTION)
    nps = models.PositiveSmallIntegerField()
    treatment = models.PositiveSmallIntegerField()
    
class CampaignMetric(models.Model):
    TEC = "Tecnologia"
    CIV = "Civil"
    CON = "Consultoria"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (CON, "Consultoria"),
    ]
    GOOGLE = "Google Ads"
    FCBK = "Facebook Ads"
    PLATFORM = [
        (GOOGLE, "Google Ads"),
        (FCBK, "Facebook Ads"),
    ]
    
    EXPOSURE = "Exposição"    
    SALES = "Vendas"
    OBJECTIVE = [
        (EXPOSURE, "Exposição de Marca"),
        (SALES, "Vendas"),
    ]
    date = models.DateField(default=now)
    platform = models.CharField(max_length=20, choices=PLATFORM)
    campaign_sector = models.CharField(max_length=30, choices=SECTORS)
    objective = models.CharField(max_length=20, choices=OBJECTIVE, default="Vendas")
    clicks = models.IntegerField()
    conversions = models.IntegerField()
    weekly_cost = models.FloatField()
    notes = models.CharField(max_length=150, default="...")

    def get_absolute_url(self):
        return "/campanhas"

    def __str__(self):
        return f"{self.platform} - {self.date}"
    class Meta:
        ordering: ['-date']
   
class SocialMediaMetric(models.Model):
    INSTAGRAM = 'Instagram'
    LINKEDIN = 'LinkedIn'
    FACEBOOK = 'Facebook'
    TIKTOK = 'TikTok'
    NETWORKS=[
        (INSTAGRAM, "Instagram"),
        (LINKEDIN, "LinkedIn"),
        (FACEBOOK, "Facebook"),
        (TIKTOK, "TikTok"),
    ]
    date = models.DateField(default=now)
    network = models.CharField(max_length=15, choices=NETWORKS)
    followers = models.PositiveIntegerField()
    impressions = models.PositiveIntegerField()
    reach = models.PositiveIntegerField()
    engagement = models.PositiveIntegerField(null=True)
    notes = models.CharField(max_length=150, default="...")

    def get_absolute_url(self):
        return "/redes-sociais"

    def __str__(self):
        return f"{self.network} - {self.date}"

    class Meta:
        ordering: ['-date']

'''
REMOVER QUANDO TERMINAR

class CashMovement(models.Model):
    OUT = 'Saída'
    IN = 'Entrada'
    FLOW=[
        (OUT, "Saída"),
        (IN, "Entrada"),
    ]
    date = models.DateField(default=now)
    amount = models.FloatField()
    flow = models.CharField(max_length=10, choices=FLOW)
    category = models.CharField(max_length=40)
    notes = models.CharField(max_length=300, default="...")
    
class TurnOver(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    term = models.BooleanField()
    reason = models.CharField(max_length=50)
    hours = models.IntegerField()
    months = models.FloatField()
    
class MoodTrack(models.Model):
    TEC = "TEC"
    CIV = "CIV"
    COM = "COM"
    RH = "RH"
    ADMFIN = "ADM"
    CON = "CON"

    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (COM, "Comercial"),
        (RH, "Recursos Humanos"),
        (ADMFIN, "Adminstrativo Financeiro"),
        (CON, "Consultoria"),
    ]
    date = models.DateField(default=now)
    score = models.FloatField()
    sector = models.CharField(max_length=3, choices=SECTORS)
    notes = models.CharField(max_length=100)
    
'''