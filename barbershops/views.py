from django.shortcuts import render
from .models import Barbershop

def home(request):
    # TODO: buscar barbearias de cada categoria
    barbershops = Barbershop.objects.all()
    context = {
        'barbershops': barbershops
    }

    return render(request, 'pages/home.html', context)

def dashboard(request):
    return render(request, 'pages/dashboard.html')
