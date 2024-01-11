from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SystemUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = SystemUser
        fields = '__all__'