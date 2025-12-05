from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.http import JsonResponse
from django.db.models import Q
from .models import Booking
from barbershops.models import Barbershop, BarbershopService, Employee

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

def _ensure_employee_exists(barbershop):
    if not barbershop.employees.exists() and barbershop.owner:
        owner_name = barbershop.owner.get_full_name() or barbershop.owner.username or "Profissional Principal"
        return Employee.objects.create(
            barbershop=barbershop,
            name=owner_name
        )
    return None

def get_available_times(request):
    barbershop_id = request.GET.get('barbershop_id')
    employee_id = request.GET.get('employee_id')
    date_str = request.GET.get('date')
    service_id = request.GET.get('service_id')

    if not all([barbershop_id, date_str, service_id]):
        return JsonResponse({'error': 'Parâmetros faltando'}, status=400)

    try:
        barbershop = Barbershop.objects.get(id=barbershop_id)
        
        _ensure_employee_exists(barbershop)
        
        service = BarbershopService.objects.get(id=service_id)
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Verifica se é dia de funcionamento
        week_day = selected_date.weekday()
        operation = barbershop.operations.filter(weekDay=week_day).first()
        
        if not operation:
             return JsonResponse({'available_times': [], 'message': 'Fechado neste dia'})

        service_duration = service.duration_minutes
        step_minutes = 30 
        
        # Determine target employees
        if employee_id:
            target_employees = [get_object_or_404(Employee, id=employee_id)]
        else:
            target_employees = barbershop.employees.all()

        final_available_slots = set()

        for emp in target_employees:
            bookings = Booking.objects.filter(
                barbershop=barbershop,
                schedule__date=selected_date,
                status__in=['PENDENTE', 'CONFIRMADO'],
                employee=emp
            )
            
            busy_slots = []
            for booking in bookings:
                local_schedule = timezone.localtime(booking.schedule)
                start_time = local_schedule.time()
                duration = booking.service.duration_minutes if booking.service else 30
                end_time_dt = local_schedule + timedelta(minutes=duration)
                busy_slots.append((start_time, end_time_dt.time()))

            current_dt = datetime.combine(selected_date, operation.timeInitial)
            closing_dt = datetime.combine(selected_date, operation.timeFinal)

            while current_dt < closing_dt:
                proposed_start = current_dt.time()
                proposed_end_dt = current_dt + timedelta(minutes=service_duration)
                proposed_end = proposed_end_dt.time()

                if proposed_end_dt > closing_dt:
                    break

                is_conflict = False
                for busy_start, busy_end in busy_slots:
                    if proposed_start < busy_end and proposed_end > busy_start:
                        is_conflict = True
                        break
                
                if not is_conflict:
                    final_available_slots.add(proposed_start.strftime("%H:%M"))

                current_dt += timedelta(minutes=step_minutes)

        sorted_slots = sorted(list(final_available_slots))
        return JsonResponse({'available_times': sorted_slots})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def booking_create(request):
    if request.method == 'POST':
        barbershop_id = request.POST.get('barbershop_id')
        service_id = request.POST.get('service_id')
        employee_id = request.POST.get('employee_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        try:
            barbershop = get_object_or_404(Barbershop, id=barbershop_id)
            
            _ensure_employee_exists(barbershop)
            
            service = get_object_or_404(BarbershopService, id=service_id)
            
            # Combine date and time
            schedule_str = f"{date_str} {time_str}"
            schedule = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")
            schedule = timezone.make_aware(schedule)
            
            employee = None
            if employee_id:
                employee = get_object_or_404(Employee, id=employee_id)
                
                # Validate availability for the selected employee
                cand_bookings = Booking.objects.filter(
                    employee=employee,
                    status__in=['PENDENTE', 'CONFIRMADO'],
                    schedule__date=schedule.date()
                )
                
                new_start = schedule
                new_end = schedule + timedelta(minutes=service.duration_minutes)
                
                for b in cand_bookings:
                    b_duration = b.service.duration_minutes if b.service else 30
                    b_start = b.schedule
                    b_end = b.schedule + timedelta(minutes=b_duration)
                    
                    if new_start < b_end and new_end > b_start:
                        messages.error(request, 'Este horário já foi reservado por outro cliente. Por favor, escolha outro horário.')
                        return redirect('barbershops:barbershop_detail', slug=barbershop.slug)
            else:
                candidates = barbershop.employees.all()
                for cand in candidates:
                    # Check conflicts for this candidate
                    is_busy = Booking.objects.filter(
                        employee=cand,
                        status__in=['PENDENTE', 'CONFIRMADO'],
                        schedule__lt=schedule + timedelta(minutes=service.duration_minutes),
                        schedule__gt=schedule - timedelta(minutes=30) # Approximate check, better to be precise
                    ).exists()
                    
                    cand_bookings = Booking.objects.filter(
                        employee=cand,
                        status__in=['PENDENTE', 'CONFIRMADO'],
                        schedule__date=schedule.date()
                    )
                    
                    conflict = False
                    new_start = schedule
                    new_end = schedule + timedelta(minutes=service.duration_minutes)
                    
                    for b in cand_bookings:
                        b_duration = b.service.duration_minutes if b.service else 30
                        b_start = b.schedule
                        b_end = b.schedule + timedelta(minutes=b_duration)
                        
                        if new_start < b_end and new_end > b_start:
                            conflict = True
                            break
                    
                    if not conflict:
                        employee = cand
                        break
                
                if not employee:
                    messages.error(request, 'Nenhum profissional disponível neste horário.')
                    return redirect('bookings:booking_list', user_id=request.user.id)

            # Create booking
            Booking.objects.create(
                customer=request.user,
                barbershop=barbershop,
                service=service,
                employee=employee,
                schedule=schedule,
                status='CONFIRMADO' 
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

        booking.status = 'CANCELADO'
        booking.save()
        messages.success(request, 'Agendamento cancelado/removido com sucesso!')
    
    return redirect('bookings:booking_list', user_id=request.user.id)