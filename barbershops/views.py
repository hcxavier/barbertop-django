from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Avg
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Barbershop, BarbershopService, Employee, Operation
from .forms import BarbershopServiceForm, BarbershopForm, AddressForm, EmployeeForm, OperationForm
from bookings.models import Booking
import calendar
from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Avg, Count, Q
from .models import Barbershop

def home(request):
    # recomendadas - barbearias com as notas acima de 4.5 em relação a media de avaliações
    barbers_recommended = Barbershop.objects.filter(rating__gte=4.5).order_by('-rating')

    # populares - barbearias com maior número de avaliações
    barbers_popular = Barbershop.objects.filter(ratings_count__gt=6).order_by('-ratings_count')

    # mais visitados - barbearias com maior número de agendamentos finalizados
    barbers_most_visited = Barbershop.objects.annotate(
        completed_bookings=Count(
            'bookings', 
            filter=Q(bookings__status='CONCLUIDO')
        )
    ).filter(completed_bookings__gt=5).order_by('-completed_bookings')

    context = {
        'barbers_recommended': barbers_recommended,
        'barbers_popular': barbers_popular,
        'barbers_most_visited': barbers_most_visited
    }

    return render(request, 'pages/home.html', context)

def is_barbershop_owner(user):
    return user.is_authenticated and user.is_owner

@user_passes_test(is_barbershop_owner)
def dashboard(request):
    user = request.user
    
    if not hasattr(user, 'barbershop_profile'):
        # Se for dono mas não tiver perfil de barbearia, redirecionar para criar?
        # Por enquanto, apenas renderiza o dashboard vazio ou erro
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

@user_passes_test(is_barbershop_owner)
def employees_manage(request):
    barbershop = request.user.barbershop_profile
    employees = Employee.objects.filter(barbershop=barbershop)
    
    context = {
        'barbershop': barbershop,
        'employees': employees,
        'form': EmployeeForm() # Formulário para o modal de adicionar
    }
    return render(request, 'pages/dashboard-employees.html', context)

@user_passes_test(is_barbershop_owner)
def employee_add(request):
    barbershop = request.user.barbershop_profile
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.barbershop = barbershop
            employee.save()
            messages.success(request, 'Funcionário adicionado com sucesso!')
            return redirect('barbershops:employees_manage')
    else:
        form = EmployeeForm()
    
    context = {
        'barbershop': barbershop,
        'form': form,
        'title': 'Novo Funcionário'
    }
    return render(request, 'pages/employee-form.html', context)

@user_passes_test(is_barbershop_owner)
def employee_edit(request, employee_id):
    barbershop = request.user.barbershop_profile
    employee = get_object_or_404(Employee, id=employee_id, barbershop=barbershop)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('barbershops:employees_manage')
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'barbershop': barbershop,
        'form': form,
        'title': f'Editar Funcionário: {employee.name}'
    }
    return render(request, 'pages/employee-form.html', context)

@user_passes_test(is_barbershop_owner)
def employee_delete(request, employee_id):
    barbershop = request.user.barbershop_profile
    employee = get_object_or_404(Employee, id=employee_id, barbershop=barbershop)
    
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Funcionário removido com sucesso!')
        return redirect('barbershops:employees_manage')
    
    return redirect('barbershops:employees_manage')

@user_passes_test(is_barbershop_owner)
def services_manage(request):
    barbershop = request.user.barbershop_profile
    services = BarbershopService.objects.filter(barbershop=barbershop)
    
    context = {
        'barbershop': barbershop,
        'services': services,
        'form': BarbershopServiceForm() # Formulário para o modal de adicionar
    }
    return render(request, 'pages/dashboard-services.html', context)

@user_passes_test(is_barbershop_owner)
def service_add(request):
    barbershop = request.user.barbershop_profile
    
    if request.method == 'POST':
        form = BarbershopServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.barbershop = barbershop
            service.save()
            messages.success(request, 'Serviço adicionado com sucesso!')
            return redirect('barbershops:services_manage')
    else:
        form = BarbershopServiceForm()
    
    context = {
        'barbershop': barbershop,
        'form': form,
        'title': 'Novo Serviço'
    }
    return render(request, 'pages/service-form.html', context)

@user_passes_test(is_barbershop_owner)
def service_edit(request, service_id):
    barbershop = request.user.barbershop_profile
    service = get_object_or_404(BarbershopService, id=service_id, barbershop=barbershop)
    
    if request.method == 'POST':
        form = BarbershopServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('barbershops:services_manage')
    else:
        form = BarbershopServiceForm(instance=service)
    
    context = {
        'barbershop': barbershop,
        'form': form,
        'title': f'Editar Serviço: {service.name}'
    }
    return render(request, 'pages/service-form.html', context)

@user_passes_test(is_barbershop_owner)
def service_delete(request, service_id):
    barbershop = request.user.barbershop_profile
    service = get_object_or_404(BarbershopService, id=service_id, barbershop=barbershop)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Serviço removido com sucesso!')
        return redirect('barbershops:services_manage')
    
    # Se não for POST, apenas redireciona (segurança)
    return redirect('barbershops:services_manage')

@user_passes_test(is_barbershop_owner)
def settings_manage(request):
    barbershop = request.user.barbershop_profile
    
    # Inicializa os formulários com as instâncias atuais (para GET ou se o POST falhar)
    barbershop_form = BarbershopForm(instance=barbershop)
    address_form = AddressForm(instance=barbershop.address)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'general':
            barbershop_form = BarbershopForm(request.POST, instance=barbershop)
            if barbershop_form.is_valid():
                barbershop_form.save()
                messages.success(request, 'Informações da barbearia atualizadas!')
                return redirect('barbershops:settings_manage')
        
        elif form_type == 'address':
            # Se barbershop.address for None, o form cria um novo. Se existir, atualiza.
            address_form = AddressForm(request.POST, instance=barbershop.address)
            if address_form.is_valid():
                address = address_form.save()
                # Se não tinha endereço vinculado, vincula agora
                if not barbershop.address:
                    barbershop.address = address
                    barbershop.save()
                messages.success(request, 'Endereço atualizado!')
                return redirect('barbershops:settings_manage')

    context = {
        'barbershop': barbershop,
        'barbershop_form': barbershop_form,
        'address_form': address_form,
    }
    return render(request, 'pages/dashboard-settings.html', context)

@user_passes_test(is_barbershop_owner)
def schedule_manage(request):
    barbershop = request.user.barbershop_profile
    operations = Operation.objects.filter(barbershop=barbershop).order_by('weekDay')
    
    # Mapeamento para exibir nomes dos dias na view se necessário, ou usar no template
    # O form já tem choices, mas para listar é bom ter o display name
    days_map = {
        0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira',
        3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'
    }
    
    # Anexar nome do dia ao objeto (apenas para display)
    for op in operations:
        op.day_display = days_map.get(op.weekDay, 'Dia desconhecido')

    context = {
        'barbershop': barbershop,
        'operations': operations,
    }
    return render(request, 'pages/dashboard-schedule.html', context)

@user_passes_test(is_barbershop_owner)
def schedule_add(request):
    barbershop = request.user.barbershop_profile
    
    if request.method == 'POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            # Verificar se já existe horário para este dia
            week_day = form.cleaned_data['weekDay']
            if Operation.objects.filter(barbershop=barbershop, weekDay=week_day).exists():
                messages.error(request, 'Já existe um horário configurado para este dia.')
            else:
                operation = form.save(commit=False)
                operation.barbershop = barbershop
                operation.save()
                messages.success(request, 'Horário adicionado com sucesso!')
                return redirect('barbershops:schedule_manage')
    else:
        form = OperationForm()
    
    context = {
        'barbershop': barbershop,
        'form': form,
        'title': 'Novo Horário'
    }
    return render(request, 'pages/schedule-form.html', context)

@user_passes_test(is_barbershop_owner)
def schedule_edit(request, operation_id):
    barbershop = request.user.barbershop_profile
    operation = get_object_or_404(Operation, id=operation_id, barbershop=barbershop)
    
    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation)
        if form.is_valid():
            # Verificar colisão de dias se o usuário mudar o dia
            new_week_day = form.cleaned_data.get('weekDay')
            # Se mudou o dia E já existe outro registro com esse novo dia
            if str(new_week_day) != str(operation.weekDay) and Operation.objects.filter(barbershop=barbershop, weekDay=new_week_day).exists():
                 messages.error(request, 'Já existe um horário configurado para este dia.')
            else:
                form.save()
                messages.success(request, 'Horário atualizado com sucesso!')
                return redirect('barbershops:schedule_manage')
    else:
        form = OperationForm(instance=operation)
    
    context = {
        'barbershop': barbershop,
        'form': form,
        'title': 'Editar Horário'
    }
    return render(request, 'pages/schedule-form.html', context)

@user_passes_test(is_barbershop_owner)
def schedule_delete(request, operation_id):
    barbershop = request.user.barbershop_profile
    operation = get_object_or_404(Operation, id=operation_id, barbershop=barbershop)
    
    if request.method == 'POST':
        operation.delete()
        messages.success(request, 'Horário removido com sucesso!')
        return redirect('barbershops:schedule_manage')
    
    return redirect('barbershops:schedule_manage')
