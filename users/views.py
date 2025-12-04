from django.shortcuts import render, redirect
from .forms import ClientSignUpForm, BarbershopSignUpForm, CustomLoginForm, UserProfileForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def logout_view(request):
    logout(request)
    return redirect('users:login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

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

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'pages/users/profile.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('home')
    return redirect('users:profile')
