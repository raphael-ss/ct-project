from django.db import models
from django.utils.timezone import now
class Lead(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER = [
        (MALE, "Homem"),
        (FEMALE, "Mulher")
    ]
    INDICATION = "INDICAÇÃO"
    FACEBOOKADS = "FBADS"
    GOOGLEADS = "GOOGLEADS"
    ACTIVE = "ATIVA"
    PASSIVE = "PASSIVA"
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
    TEC = "TEC"
    CIV = "CIV"
    CON = "CON"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (CON, "Consultoria"),
    ]
    first_name = models.CharField(max_length=32, default="")
    last_name = models.CharField(max_length=32, default="")
    sector = models.CharField(max_length=3, choices=SECTORS, default=TEC)
    gender = models.CharField(max_length=1, choices=GENDER, default="")
    status = models.CharField(max_length=20, choices=STATUS, default=PRED)
    source = models.CharField(max_length=10, choices=SOURCE, default="")
    email = models.CharField(max_length=80, default="", null=True)
    phone = models.CharField(max_length=16, default="")
    field_of_action = models.CharField(max_length=30, default="", null=True)
    score = models.CharField(max_length=1)
    date = models.DateField()
    notes = models.CharField(max_length=150, default="-")
    
    #-LEAD SCORING
    budget = models.IntegerField()
    authority = models.IntegerField()
    need = models.IntegerField()
    timing = models.IntegerField()
    time_to_respond = models.IntegerField()
    behavior = models.IntegerField()
    
    def get_absolute_url(self):
        return "/leads"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"
    
    class Meta:
        ordering: ['-date']
    
class Client(models.Model):
    EFCOMPLETE = "EF-COMPLETO"
    EMCOMPLETE = "EM-COMPLETO"
    ESCOMPLETE = "ES-COMPLETO"
    EDUCATION = [
        (EFCOMPLETE, "Ensino Fundamental Completo"),
        (EMCOMPLETE, "Ensino Médio Completo"),
        (ESCOMPLETE, "Ensino Superior Completo"),
    ]
    SINGLE = "SOLTEIRO"
    MARRIED = "CASADO"
    DIVORCED = "DIVORCIADO"
    OTHER = "OUTRO"
    DATING = "UNIÃO ESTÁVEL"
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
    }, null=True)
    cpf = models.CharField(max_length=14, default="")
    birth_date = models.DateField(null=False)
    education = models.CharField(max_length=15, choices=EDUCATION, default=ESCOMPLETE, null=True)
    marital_status = models.CharField(max_length=15, choices=STATUS, default=SINGLE, null=True)
    income = models.CharField(max_length=5, choices=INCOME, default="", null=True)
    funnel_time = models.PositiveIntegerField(default=15)
    notes = models.CharField(max_length=100, default="-")

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
    n_of_locations = models.PositiveSmallIntegerField(null=True)
    n_of_employees = models.PositiveSmallIntegerField(null=True)
    proof_of_registration_link = models.CharField(max_length=150)
    notes = models.CharField(max_length=10, default="-")

    def get_absolute_url(self):
        return "/empresas"

    def __srt__(self):
        return f"{self.client_id.first_name} - {self.client_id.last_name} - {self.company_name}"
    
    class Meta:
        ordering: ['-client_id.lead_id.date']

class Member(models.Model):
    ADVISOR = "ASS"
    CONSULTANT = "CON"
    MANAGER = "GER"
    DIRECTOR = "DIR"
    PRESIDENT = "PRE"
    ROLE = [
        (ADVISOR, "Assessor(a)"),
        (CONSULTANT, "Consultor(a)"),
        (MANAGER, "Gerente"),
        (DIRECTOR, "Diretor(a)"),
        (PRESIDENT, "Presidente"),
    ]
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
        (ADMFIN, "Adiminstrativo Financeiro"),
    ]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    sector = models.CharField(max_length=3, choices=SECTORS)
    role = models.CharField(max_length=3, choices=ROLE)
    date_of_entry = models.DateField(null=False)
    date_of_leave = models.DateField(null=True)
    professional_email = models.CharField(max_length=80)
    academic_email = models.CharField(max_length=80)
    phone = models.CharField(max_length=16)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=9)
    degree = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=300)
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/membros"

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    
    class Meta:
        ordering: ['-role']

class Contract(models.Model):
    TEC = "TEC"
    CIV = "CIV"
    CON = "CON"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (CON, "Consultoria"),
    ]
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    sector = models.CharField(max_length=3, choices=SECTORS)
    total_value = models.FloatField(null=False)
    n_of_services = models.PositiveSmallIntegerField()
    date = models.DateField()
    link_of_contract = models.CharField(max_length=250)
    notes = models.CharField(max_length=100, default="-")

    def get_absolute_url(self):
        return "/contratos"

    def __str__(self):
        return f"{self.client_id.lead_id.first_name} {self.client_id.lead_id.last_name} - {self.sector}" 
    class Meta:
        ordering: ['-date']
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
    MAP = "Mapeamento"
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
    ]
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    project = models.CharField(max_length=18, choices=SER)
    estimated_time = models.PositiveSmallIntegerField(null=False)
    actual_time = models.PositiveSmallIntegerField(null=True)
    n_of_consultants = models.PositiveSmallIntegerField()
    price = models.FloatField()
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/servicos"

    def __str__(self):
        return f"{self.client_id.lead_id.first_name} {self.client_id.lead_id.last_name} - {self.project}"
    
    class Meta:
        ordering: ['-contract_id.date']
    
class CampaignMetric(models.Model):
    TEC = "TEC"
    CIV = "CIV"
    CON = "CON"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (CON, "Consultoria"),
    ]
    GOOGLE = "GOOGLEADS"
    FCBK = "FBADS"
    PLATFORM = [
        (GOOGLE, "Google Ads"),
        (FCBK, "Facebook Ads"),
    ]
    LOW = "FUNDO"    
    MEDIUM = "MEIO"
    HIGH = "TOPO"
    ALL = "GERAL"
    POSITION = [
        (HIGH, "Topo de Funil"),
        (MEDIUM, "Meio de Funil"),
        (LOW, "Fundo de Funil"),
        (ALL, "Geral")
    ]
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(null=False, default=now)
    platform = models.CharField(max_length=10, choices=PLATFORM)
    campaign_sector = models.CharField(max_length=3, choices=SECTORS)
    funnel_position = models.CharField(max_length=5, choices=POSITION)
    clicks = models.IntegerField()
    conversions = models.IntegerField()
    weekly_cost = models.FloatField()
    notes = models.CharField(max_length=100, default="-")

    def get_absolute_url(self):
        return "/campanhas"

    def __srt__(self):
        return f"{self.platform} - {self.date}"
    class Meta:
        ordering: ['-date']
   
class SocialMediaMetric(models.Model):
    INSTAGRAM = 'IG'
    LINKEDIN = 'LI'
    FACEBOOK = 'FC'
    TIKTOK = 'TK'
    NETWORKS=[
        (INSTAGRAM, "Instagram"),
        (LINKEDIN, "LinkedIn"),
        (FACEBOOK, "Facebook"),
        (TIKTOK, "TikTok"),
    ]
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(null=False, default=now)
    network = models.CharField(max_length=2, choices=NETWORKS, null=False)
    followers = models.PositiveIntegerField(null=False)
    impressions = models.PositiveIntegerField()
    reach = models.PositiveIntegerField()
    engagement = models.PositiveIntegerField()
    notes = models.CharField(max_length=100, default="-")

    def get_absolute_url(self):
        return "/redes-sociais"

    def __srt__(self):
        return f"{self.network} - {self.date}"

    class Meta:
        ordering: ['-date']

class CashMovement(models.Model):
    OUT = 'SAÍDA'
    IN = 'ENTRADA'
    FLOW=[
        (OUT, "Saída"),
        (IN, "Entrada"),
    ]
    EVENT = "EVENTO"
    TRAINING = "CAPACITAÇÃO"
    CATEGORIES = [
        (EVENT, "Evento"),
        (TRAINING, "Capacitação"),
    ]
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(default=now)
    amount = models.FloatField()
    flow = models.CharField(max_length=10, choices=FLOW)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.CharField(max_length=300, default="-")
    
    
    