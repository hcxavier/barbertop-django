from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Address(models.Model):
    city = models.CharField(max_length=255)
    number = models.IntegerField()
    neighbourhood = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}"

class Barbershop(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='barbershop_profile' # Permite acessar via user.barbershop_profile
    )

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    # endereço vinculado a uma barbearia
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    imageUrl = models.TextField(blank=True, null=True)
    
    # Novos campos para avaliação
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    ratings_count = models.IntegerField(default=0)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Operation(models.Model):
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name="operations")
    weekDay = models.SmallIntegerField(help_text="0=Segunda, 6=Domingo")
    timeInitial = models.TimeField()
    timeFinal = models.TimeField()

    class Meta:
        unique_together = ('barbershop', 'weekDay')
        verbose_name = "Horário de Funcionamento"

    def __str__(self):
        return f"{self.barbershop.name} - Dia {self.weekDay}"

class Employee(models.Model):
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name="employees")
    name = models.CharField(max_length=255)
    urlProfilePhoto = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class BarbershopService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    imageUrl = models.URLField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Decimal
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name="services")
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name="ratings")
    ratingNumber = models.IntegerField() 
    ratingDescription = models.TextField(blank=True, null=True) #
    createdAt = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Rating {self.ratingNumber} para {self.barbershop.name}"

# Signals para atualizar a média de avaliações automaticamente
@receiver(post_save, sender=Rating)
@receiver(post_delete, sender=Rating)
def update_barbershop_rating(sender, instance, **kwargs):
    barbershop = instance.barbershop
    data = Rating.objects.filter(barbershop=barbershop).aggregate(
        avg_rating=Avg('ratingNumber'),
        count_rating=Count('id')
    )
    
    barbershop.rating = data['avg_rating'] or 0.0
    barbershop.ratings_count = data['count_rating'] or 0
    barbershop.save()
