from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from .forms import RegistrationForm
from dashboard.models import Member
from .models import SystemUser
# Create your views here.

class Registration(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'authentication/register.html', {'form': form})

    def post(self, request):     
        form = RegistrationForm(request.POST)
        if form.is_valid():
 
            name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            rg = form.cleaned_data['rg']
            cpf = form.cleaned_data['cpf']
            role = form.cleaned_data['role']
            sector = form.cleaned_data['sector']

            context = {
                'fieldValues': request.POST,
            }

            if not SystemUser.objects.filter(username=username).exists():
                if not SystemUser.objects.filter(email=email).exists():
                    if len(password) < 8:
                        messages.error(request, "Sua senha deve ter mais de 8 caracteres!")
                        return render(request, 'authentication/register.html', context=context)

                    else:
                        if str(password).isnumeric():
                            messages.error(request, "Sua senha não pode ser completamente numérica!")
                            return render(request, 'authentication/register.html', context=context)
                        
                        if (Member.objects.filter(rg=rg).exists()) and (Member.objects.filter(cpf=cpf).exists()):
                            member = Member.objects.get(rg=rg)
                            print(member.role, role)
                            if str(member.role) == str(role):
                                user = SystemUser.objects.create_user(username=username, email=email, rg=rg, 
                                                                    cpf=cpf, role=role, sector=sector, full_name=name)
                                user.set_password(password)
                                user.save()
                                messages.success(request, "Conta criada com sucesso!")
                                return redirect('login')
                            else:
                                messages.error(request, "Cargo selecionado não condiz ao cadastrado!")
                                return render(request, 'authentication/register.html', context=context)
                                
                        else:
                            messages.error(request, "Dados pessoais (CPF ou RG) não estão cadastrados!")
                            return render(request, 'authentication/register.html', context=context)


        return render(request, 'authentication/register.html')
    
class ValidateUsername(View):
    def post(self, request):

        data = json.loads(request.body)

        username = data['username']

        if not str(username).isascii():
            return JsonResponse({'username_error': 'Nome de usuário só pode ser composto de caracteres ASCII!'}, status=400)
        if SystemUser.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Nome de usuário já está em uso'}, status=409)
        return JsonResponse({'username_valid': True})

class ValidateEmail(View):
    def post(self, request):

        data = json.loads(request.body)

        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Esse não é um email válido!'}, status=400)
        if SystemUser.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email já está em uso!'}, status=409)
        if email.split("@")[1] != "ctjunior.com.br":
            return JsonResponse({'email_error': 'Use o email da CT Junior!'}, status=400)
        return JsonResponse({'email_valid': True})

class LoginView(View):
    
    model = SystemUser
    
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                name = user.full_name
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
