from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
# Create your views here.

class Registration(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST,
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, "Sua senha deve ter mais de 8 caracteres!")
                    return render(request, 'authentication/register.html', context=context)

                else:

                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Conta criada com sucesso!")
                    return redirect('home')


        return render(request, 'authentication/register.html')
    
class ValidateUsername(View):
    def post(self, request):

        data = json.loads(request.body)

        username = data['username']

        if not str(username).isascii():
            return JsonResponse({'username_error': 'Nome de usuário só pode ser composto de caracteres ASCII!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Nome de usuário já está em uso'}, status=409)
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
            return JsonResponse({'email_error': 'Use o email da CT Junior!'}, status=400)
        return JsonResponse({'email_valid': True})

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                name = user.username.split(".")[0].title()
                messages.success(request, f"{name} está conectado(a)!")
                return redirect('home')

            messages.error(request, "Credenciais Inválidas! Tente novamente...")
            return render(request, "authentication/login.html")

        messages.error(request, "Insira seus dados de login!")
        return render(request, "authentication/login.html")

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return redirect('login')
