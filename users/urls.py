from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [ 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/client', views.registerClient, name='registerClient'),
    path('register/barber', views.registerBarber, name='registerBarber'),
    path('api/register-barbershop/', views.registerBarbershopApi, name='registerBarbershopApi'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/delete/', views.delete_account_view, name='delete_account'),
]
