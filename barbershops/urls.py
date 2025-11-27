from django.urls import path
from . import views

app_name = 'barbershops'

urlpatterns = [
    path('services/', views.services_manage, name='services_manage'),
    path('services/add/', views.service_add, name='service_add'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:service_id>/delete/', views.service_delete, name='service_delete'),
    path('settings/', views.settings_manage, name='settings_manage'),
]