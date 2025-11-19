from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):    
    # Campos customizados do seu schema
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Telefone"
    )
    
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        blank=True, 
        null=True, # Permitir NULL/BLANK para flexibilidade na criação inicial
        verbose_name="CPF"
    )

    # O campo 'updatedAt' do seu schema
    updatedAt = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    def __str__(self):
        return self.username