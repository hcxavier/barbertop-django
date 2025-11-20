from django.shortcuts import render, redirect
from .forms import ClientSignUpForm, BarbershopSignUpForm
from django.contrib.auth import login
from django.db import transaction
from .models import CustomUser
from django.http import JsonResponse
from barbershops.models import Barbershop, Address, BarbershopService, Employee
import json
from django.views.decorators.http import require_POST

def register(request):            
    return render(request, 'pages/registration.html')

def registerClient(request):
    client_form = ClientSignUpForm()

    if request.method == 'POST':
        client_form = ClientSignUpForm(request.POST)
        if client_form.is_valid():
            user = client_form.save()
            login(request, user) 
            return redirect('home')
         
    return render(request, 'users/client-form.html', {'client_form': client_form})

def registerBarber(request):
    barbershop_form = BarbershopSignUpForm()         
    return render(request, 'users/barber-form.html', {'barbershop_form': barbershop_form})

@require_POST
def registerBarbershopApi(request):
    # O request.FILES é crucial para a imagem funcionar
    form = BarbershopSignUpForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            # O form.save() agora faz TUDO (User, Address, Barbearia, Serviços, Equipe)
            user = form.save()
            
            # Loga o usuário automaticamente
            login(request, user)
            
            return JsonResponse({'message': 'Cadastro realizado com sucesso!'}, status=201)
        except Exception as e:
            return JsonResponse({'message': f'Erro ao salvar: {str(e)}'}, status=500)
    else:
        # Retorna os erros de validação (ex: senha fraca, usuário existente)
        return JsonResponse({'message': 'Dados inválidos', 'errors': form.errors}, status=400)
