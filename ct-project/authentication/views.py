from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
# Create your views here.

class Registration(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
class ValidateUsername(View):
    def post(self, request):

        data = json.loads(request.body)

        username = data['username']

        if not str(username).isascii():
            return JsonResponse({'username_error': 'Nome de usuário só pode ser composto de caracteres ASCII!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'nome de usuário já está em uso'}, status=409)
        return JsonResponse({'username_valid': True})

class ValidateEmail(View):
    def post(self, request):

        data = json.loads(request.body)

        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Esse não é um email válido!'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email já está em uso!'}, status=409)
        if email.split("@")[1] != "ctjunior.com.br":
            return JsonResponse({'email_error': 'Use o email da CT Junior!'})
        return JsonResponse({'email_valid': True})