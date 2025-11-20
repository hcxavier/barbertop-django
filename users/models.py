from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Definindo os papéis
    class Role(models.TextChoices):
        CLIENT = "CLIENT", "Cliente"
        OWNER = "OWNER", "Dono de Barbearia"

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.CLIENT,
        verbose_name="Tipo de Conta"
    )
    
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="CPF")
    
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_owner(self):
        return self.role == self.Role.OWNER