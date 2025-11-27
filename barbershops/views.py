from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Avg
from django.contrib.auth.decorators import user_passes_test
from .models import Barbershop
from bookings.models import Booking
import calendar
from datetime import datetime, timedelta

def home(request):
    # TODO: buscar barbearias de cada categoria
    barbershops = Barbershop.objects.all()
    context = {
        'barbershops': barbershops
    }

    return render(request, 'pages/home.html', context)

def is_barbershop_owner(user):
    return user.is_authenticated and user.is_owner

@user_passes_test(is_barbershop_owner)
def dashboard(request):
    user = request.user
    
    if not hasattr(user, 'barbershop_profile'):
        return render(request, 'pages/dashboard.html')
    
    barbershop = user.barbershop_profile
    
    today = timezone.localdate()
    yesterday = today - timezone.timedelta(days=1)
    
    # --- Lógica do Calendário ---
    
    # 1. Data Selecionada (Filtro)
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today
            selected_date_str = today.strftime('%Y-%m-%d')
    else:
        selected_date = today
        selected_date_str = today.strftime('%Y-%m-%d')

    # 2. Navegação Mês/Ano
    try:
        cal_year = int(request.GET.get('year', selected_date.year))
        cal_month = int(request.GET.get('month', selected_date.month))
    except ValueError:
        cal_year = selected_date.year
        cal_month = selected_date.month

    # Ajuste de navegação (overflow de meses)
    if cal_month > 12:
        cal_month = 1
        cal_year += 1
    elif cal_month < 1:
        cal_month = 12
        cal_year -= 1
        
    current_month_display = datetime(cal_year, cal_month, 1)

    # 3. Dados do Calendário
    cal = calendar.Calendar(firstweekday=6) # Começa Domingo
    month_days = cal.monthdatescalendar(cal_year, cal_month)
    
    # Buscar dias que têm agendamento para marcar no calendário
    start_visible = month_days[0][0]
    end_visible = month_days[-1][-1]
    
    bookings_in_view = Booking.objects.filter(
        service__barbershop=barbershop,
        schedule__date__range=[start_visible, end_visible]
    ).values_list('schedule__date', flat=True).distinct()
    
    booking_dates_set = set(bookings_in_view)
    
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            is_current_month = (day.month == cal_month)
            week_data.append({
                'day': day.day,
                'date_str': day.strftime('%Y-%m-%d'),
                'is_today': (day == today),
                'is_current_month': is_current_month,
                'has_appointments': (day in booking_dates_set),
                'is_selected': (day == selected_date)
            })
        calendar_data.append(week_data)

    # Links Próximo/Anterior Mês
    prev_m = (current_month_display - timedelta(days=1))
    next_m = (current_month_display + timedelta(days=32)).replace(day=1)

    # --- Agendamentos (Lista) ---
    
    status_filter = request.GET.get('status')
    
    appointments_query = Booking.objects.filter(service__barbershop=barbershop)
    
    # Filtro de data (Sempre aplicado agora)
    appointments_query = appointments_query.filter(schedule__date=selected_date)
    
    if selected_date == today:
        list_title = "Agendamentos de Hoje"
    else:
        list_title = f"Agendamentos em {selected_date.strftime('%d/%m')}"

    if status_filter:
        appointments_query = appointments_query.filter(status=status_filter)

    upcoming_appointments = appointments_query.order_by('schedule')

    # --- Métricas (existentes) ---
    
    # Agendamentos Hoje e Ontem
    appointments_today = Booking.objects.filter(
        service__barbershop=barbershop,
        schedule__date=today
    ).count()
    
    appointments_yesterday = Booking.objects.filter(
        service__barbershop=barbershop,
        schedule__date=yesterday
    ).count()
    
    appointments_diff = appointments_today - appointments_yesterday

    # Agendamentos Pendentes
    pending_appointments_count = Booking.objects.filter(
        service__barbershop=barbershop,
        status='PENDENTE'
    ).count()

    # Receita do Mês Atual (Datas fixas no mês atual real, não do calendário visualizado)
    start_month_real = today.replace(day=1)
    last_month_real = start_month_real - timedelta(days=1)
    start_last_month_real = last_month_real.replace(day=1)

    revenue_current_month = Booking.objects.filter(
        service__barbershop=barbershop,
        schedule__gte=start_month_real,
        status='CONCLUIDO'
    ).aggregate(Sum('service__price'))['service__price__sum'] or 0

    revenue_last_month = Booking.objects.filter(
        service__barbershop=barbershop,
        schedule__gte=start_last_month_real,
        schedule__lt=start_month_real,
        status='CONCLUIDO'
    ).aggregate(Sum('service__price'))['service__price__sum'] or 0

    if revenue_last_month > 0:
        revenue_growth = ((revenue_current_month - revenue_last_month) / revenue_last_month) * 100
    else:
        revenue_growth = 100 if revenue_current_month > 0 else 0

    # Avaliação
    avg_rating_val = barbershop.ratings.aggregate(Avg('ratingNumber'))['ratingNumber__avg'] or 0
    total_ratings = barbershop.ratings.count()

    context = {
        'barbershop': barbershop,
        'appointments_today': appointments_today,
        'appointments_diff': appointments_diff,
        'pending_appointments_count': pending_appointments_count,
        'revenue_current_month': f"{revenue_current_month:.2f}",
        'revenue_growth': revenue_growth,
        'revenue_growth_display': f"{abs(revenue_growth):.1f}",
        'average_rating': f"{avg_rating_val:.1f}".replace('.', ','),
        'total_ratings': total_ratings,
        
        # Novos dados
        'upcoming_appointments': upcoming_appointments,
        'status_choices': Booking.StatusChoices.choices,
        'current_status': status_filter,
        'calendar_data': calendar_data,
        'current_month_display': current_month_display,
        'prev_year': prev_m.year,
        'prev_month': prev_m.month,
        'next_year': next_m.year,
        'next_month': next_m.month,
        'list_title': list_title,
        'selected_date': selected_date_str, # Para manter estado na view se precisar
    }

    return render(request, 'pages/dashboard.html', context)
