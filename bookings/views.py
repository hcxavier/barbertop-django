from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Booking
from barbershops.models import Barbershop, BarbershopService

@login_required
def booking_list(request, user_id):
    if request.user.id != user_id:
        return redirect('home')
        
    if request.user.is_owner:
        return redirect('home')

    bookings_confirmed = Booking.objects.filter(customer_id=user_id, status='CONFIRMADO').order_by('schedule')
    bookings_finished = Booking.objects.filter(customer_id=user_id, status='CONCLUIDO').order_by('schedule')

    selected_booking = None
    if bookings_confirmed:
        selected_booking = bookings_confirmed.last()
    elif bookings_finished:
        selected_booking = bookings_finished.last()
    else:
        selected_booking = None
    return render(request, 'pages/bookings/booking_list.html', {'user_id': user_id, 'bookings_confirmed': bookings_confirmed, 'bookings_finished': bookings_finished, 'selected_booking': selected_booking  })

@login_required
def booking_create(request):
    if request.method == 'POST':
        barbershop_id = request.POST.get('barbershop_id')
        service_id = request.POST.get('service_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        try:
            barbershop = get_object_or_404(Barbershop, id=barbershop_id)
            service = get_object_or_404(BarbershopService, id=service_id)
            
            # Combine date and time
            schedule_str = f"{date_str} {time_str}"
            schedule = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")
            
            # Make it timezone aware (naive datetime warning fix)
            schedule = timezone.make_aware(schedule)

            # Create booking
            Booking.objects.create(
                customer=request.user,
                barbershop=barbershop,
                service=service,
                schedule=schedule,
                status='CONFIRMADO' # Auto confirm for MVP or 'PENDENTE'
            )
            
            messages.success(request, 'Agendamento realizado com sucesso!')
            return redirect('bookings:booking_list', user_id=request.user.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao agendar: {str(e)}')
            return redirect('home')
            
    return redirect('home')

@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if request.method == 'POST':
        if not booking.can_cancel:
            messages.error(request, 'Não é possível cancelar agendamentos com menos de 24h de antecedência.')
            return redirect('bookings:booking_list', user_id=request.user.id)

        # Em vez de soft delete, vamos fazer delete real para contar como CRUD Delete
        booking.delete()
        messages.success(request, 'Agendamento cancelado/removido com sucesso!')
    
    return redirect('bookings:booking_list', user_id=request.user.id)