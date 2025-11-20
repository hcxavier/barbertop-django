from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/client', views.registerClient, name='registerClient'),
    path('register/barber', views.registerBarber, name='registerBarber'),
    path('api/register-barbershop/', views.registerBarbershopApi, name='registerBarbershopApi'),
]
