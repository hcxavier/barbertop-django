from django.shortcuts import render, redirect
from .forms import ClientSignUpForm, BarbershopSignUpForm
from django.contrib.auth import login

def register(request):
    client_form = ClientSignUpForm()
    barbershop_form = BarbershopSignUpForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'client':
            client_form = ClientSignUpForm(request.POST)
            if client_form.is_valid():
                user = client_form.save()
                login(request, user) 
                return redirect('home') 
        elif form_type == 'barbershop':
            barbershop_form = BarbershopSignUpForm(request.POST)
            if barbershop_form.is_valid():
                user = barbershop_form.save()
                login(request, user)
                return redirect('admin:index')
    return render(request, 'pages/registration.html', {'client_form': client_form, 'barbershop_form': barbershop_form})