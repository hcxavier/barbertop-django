from django.db import models
from django.conf import settings

class Booking(models.Model):
    
    class StatusChoices(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        CONFIRMADO = 'CONFIRMADO', 'Confirmado'
        CANCELADO = 'CANCELADO', 'Cancelado'
        CONCLUIDO = 'CONCLUIDO', 'Concluído'

    customer = models.ForeignKey(
            settings.AUTH_USER_MODEL,  
            on_delete=models.CASCADE, 
            related_name="bookings"
        )    
        
    service = models.ForeignKey('barbershops.BarbershopService', on_delete=models.SET_NULL, null=True, related_name="bookings")    
    employee = models.ForeignKey('barbershops.Employee', on_delete=models.SET_NULL, null=True, related_name="bookings")
    
    schedule = models.DateTimeField() # Data e hora do agendamento
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE
    )
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Agendamento para {self.customer.username} em {self.schedule.strftime('%d/%m/%Y %H:%M')}"