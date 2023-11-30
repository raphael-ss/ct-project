from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

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
    first_name = models.CharField(max_length=32, default="")
    last_name = models.CharField(max_length=32, default="")
    gender = models.CharField(max_length=1, choices=GENDER, default="")
    source = models.CharField(max_length=10, choices=SOURCE, default="")
    email = models.CharField(max_length=80, default="")
    phone = models.CharField(max_length=16, default="")
    profession = models.CharField(max_length=30, default="")


class Client(models.Model):
    EFCOMPLETE = "EF-COMPLETO"
    EMINCOMPLETE = "EM-INCOMPLETO"
    ESINCOMPLETE = "ES-INCOMPLETO"
    ESCOMPLETE = "ES-COMPLETO"
    EDUCATION = [
        (EFCOMPLETE, "Ensino Fundamental Completo"),
        (EMINCOMPLETE, "Ensino Médio Incompleto"),
        (ESINCOMPLETE, "Ensino Superior Incompleto"),
        (ESCOMPLETE, "Ensino Superior Completo"),
    ]
    SINGLE = "SOLTEIRO"
    MARRIED = "CASADO"
    DIVORCED = "DIVORCIADO"
    WIDOWED = "VIÚVO"
    DATING = "UNIÃO ESTÁVEL"
    STATUS = [
        (SINGLE, 'Solteiro(a)'),
        (MARRIED, "Casado(a)"),
        (DIVORCED, "Divorciado(a)"),
        (WIDOWED, "Viúvo(a)"),
        (DATING, "União Estável"),
    ]
    UPTO_1 = "1"
    UPTO_1_5 = "1,5"
    UPTO_6_5 = "6,5"
    UPTO_9 = "9"
    ABOVE_9 = "+9"

    INCOME = [
        (UPTO_1, "Até 1 salário mínimo"),
        (UPTO_1_5, "Até 1,5 salários mínimos"),
        (UPTO_6_5, "Até 6,5 salários mínimos"),
        (UPTO_9, "Até 9 salários mínimos"),
        (ABOVE_9, "Acima de 9 salários mínimos"),
    ]

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    SCORE = [
        (A, "A"),
        (B, "B"),
        (C, "C"),
        (D, "D"),
        (E, "E"),
    ]
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, default="123-456-789-12")
    birth_date = models.DateField(null=False, default=datetime.datetime.now)
    education = models.CharField(max_length=15, choices=EDUCATION, default=ESCOMPLETE)
    marital_status = models.CharField(max_length=15, choices=STATUS, default=SINGLE)
    monthly_income = models.CharField(max_length=5, choices=INCOME, default=UPTO_6_5)
    funnel_time = models.PositiveIntegerField(default=20)
    score = models.CharField(default=A, choices=SCORE)
    notes = models.CharField(max_length=100, default="-")

    def get_absolute_url(self):
        return "/clientes"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

    
class Company(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=80)
    cnpj = models.CharField(max_length=18)
    field_of_action = models.CharField(max_length=100)
    annual_revenue = models.FloatField()
    n_of_locations = models.PositiveSmallIntegerField()
    n_of_employees = models.PositiveSmallIntegerField()
    proof_of_registration_link = models.CharField(max_length=150)
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/empresas"

    def __srt__(self):
        return f"{self.client_id.first_name} - {self.client_id.last_name} - {self.company_name}"

class Contract(models.Model):
    TEC = "TEC"
    CIV = "CIV"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil")
    ]
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    sector = models.CharField(max_length=3, choices=SECTORS)
    total_value = models.FloatField(null=False)
    n_of_services = models.PositiveSmallIntegerField()
    date = models.DateField()
    link_of_contract = models.CharField(max_length=150)
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/contratos"

    def __str__(self):
        return f"{self.client_id.first_name} {self.client_id.last_name} - {self.sector}" 

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
    email = models.CharField(max_length=80)
    phone = models.CharField(max_length=16)
    cpf = models.CharField(max_length=14)
    degree = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=3, choices=ROLE)
    date_of_entry = models.DateField(null=False)
    date_of_leave = models.DateField(null=True)
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/membros"

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

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
    ]
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, default="")
    project = models.CharField(max_length=18, choices=SER)
    estimated_time = models.PositiveSmallIntegerField(null=False)
    actual_time = models.PositiveSmallIntegerField()
    n_of_consultants = models.PositiveSmallIntegerField()
    price = models.FloatField()
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/servicos"

    def __str__(self):
        return f"{self.client_id.first_name} {self.client_id.last_name} - {self.project}"
    
class CampaignMetric(models.Model):

    TEC = "TEC"
    CIV = "CIV"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil")
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
    POSITION = [
        (HIGH, "Topo de Funil"),
        (MEDIUM, "Meio de Funil"),
        (LOW, "Fundo de Funil"),
    ]
    date = models.DateField(null=False, default=datetime.datetime.now, primary_key=True)
    platform = models.CharField(max_length=10, choices=PLATFORM)
    campaign_sector = models.CharField(max_length=3, choices=SECTORS)
    funnel_position = models.CharField(max_length=5, choices=POSITION)
    weekly_cost = models.FloatField()
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/campanhas"

    def __srt__(self):
        return f"{self.platform} - {self.date}"


    
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
    date = models.DateField(null=False, default=datetime.datetime.now, primary_key=True)
    network = models.CharField(max_length=2, choices=NETWORKS, null=False)
    followers = models.PositiveIntegerField(null=False)
    impressions = models.PositiveIntegerField()
    reach = models.PositiveIntegerField()
    engagement = models.PositiveIntegerField()
    visits = models.PositiveIntegerField()
    notes = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/redes-sociais"

    def __srt__(self):
        return f"{self.network} - {self.date}"

    class Meta:
        ordering: ['-date']


