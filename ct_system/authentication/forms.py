from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SystemUser

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = SystemUser
        fields = [
            'full_name',
            'cpf',
            'rg',
            'role',
            'sector',
            'username',
            'email',
            'password',  # Note: Handle password fields securely, consider using PasswordInput widget
        ]
