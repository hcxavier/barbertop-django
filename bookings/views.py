from django.shortcuts import render
from .models import Booking

def booking_list(request, user_id):
    bookings_confirmed = Booking.objects.filter(customer_id=user_id, status='CONFIRMADO')
    bookings_finished = Booking.objects.filter(customer_id=user_id, status='CONCLUIDO')

    selected_booking = None
    if bookings_confirmed:
        selected_booking = bookings_confirmed[0]
    elif bookings_finished:
        selected_booking = bookings_finished[0]
    else:
        selected_booking = None
    return render(request, 'pages/bookings/booking_list.html', {'user_id': user_id, 'bookings_confirmed': bookings_confirmed, 'bookings_finished': bookings_finished, 'selected_booking': selected_booking  })