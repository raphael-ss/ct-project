from django.db import models
from django.contrib.auth.models import AbstractUser
class SystemUser(AbstractUser):
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
    RH = "RH"
    ADMFIN = "Financeiro"
    CON = "Consultoria"
    DIR = "DirEx"
    SECTORS = [
        (TEC, "Tecnologia"),
        (CIV, "Construção Civil"),
        (COM, "Comercial"),
        (RH, "Recursos Humanos"),
        (ADMFIN, "Adminstrativo Financeiro"),
        (CON, "Consultoria"),
        (DIR, "Diretoria Executiva"),
    ]
    
    full_name = models.CharField(max_length=100, null=False)
    cpf = models.CharField(max_length=14, null=False)
    rg = models.CharField(max_length=9, null=False)
    role = models.CharField(max_length=20, choices=ROLE)
    sector = models.CharField(max_length=20, choices=SECTORS)