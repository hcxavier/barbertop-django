from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from barbershops.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('users/', include('users.urls')),
    path('barbershops/', include('barbershops.urls')),
    path('bookings/', include('bookings.urls'))
]
