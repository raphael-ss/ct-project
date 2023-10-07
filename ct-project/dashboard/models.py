from django.db import models

# Create your models here.

class Client(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER = [
        (MALE, "Male"),
        (FEMALE, "Female")
    ]
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=GENDER)
    