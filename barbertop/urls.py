from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from barbershops.views import home
from barbershops.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('users/', include('users.urls')),
    path('barbershops/', include('barbershops.urls')),
    path('bookings/', include('bookings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
