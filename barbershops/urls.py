from django.urls import path
from . import views

app_name = 'barbershops'

urlpatterns = [
    path('services/', views.services_manage, name='services_manage'),
    path('services/add/', views.service_add, name='service_add'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:service_id>/delete/', views.service_delete, name='service_delete'),
    
    path('employees/', views.employees_manage, name='employees_manage'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:employee_id>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),

    path('schedule/', views.schedule_manage, name='schedule_manage'),
    path('schedule/add/', views.schedule_add, name='schedule_add'),
    path('schedule/<int:operation_id>/edit/', views.schedule_edit, name='schedule_edit'),
    path('schedule/<int:operation_id>/delete/', views.schedule_delete, name='schedule_delete'),

    path('settings/', views.settings_manage, name='settings_manage'),
]