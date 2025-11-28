from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('<int:user_id>/', views.booking_list, name='booking_list'),
]
