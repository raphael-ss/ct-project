from django.db import models
from django.contrib.auth.models import User
import datetime
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
    
    
class SocialMediaMetric(models.Model):
    #timestamp = models.TimeField
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
    date = models.DateField(null=False, default=datetime.datetime.now)
    network = models.CharField(max_length=2, choices=NETWORKS, null=False)
    followers = models.IntegerField(null=False)
    impressions = models.IntegerField()
    reach = models.IntegerField()
    engagement = models.IntegerField()
    visits = models.IntegerField()
    notes = models.CharField(max_length=100)

    def __srt__(self):
        return f"{self.network} - {self.date}"

    class Meta:
        ordering: ['-date']


