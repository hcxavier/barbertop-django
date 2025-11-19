from django.shortcuts import render, redirect
from .forms import ClientSignUpForm, BarbershopSignUpForm
from django.contrib.auth import login

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

    if request.method == 'POST':
        barbershop_form = BarbershopSignUpForm(request.POST)
        if barbershop_form.is_valid():
            user = barbershop_form.save()
            login(request, user)
            return redirect('admin:index')
         
    return render(request, 'users/barber-form.html', {'barbershop_form': barbershop_form})