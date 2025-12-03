from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.booking_create, name='booking_create'),
    path('<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('<int:user_id>/', views.booking_list, name='booking_list'),
]
