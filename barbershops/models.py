from django.db import models
from django.conf import settings

class Address(models.Model):
    city = models.CharField(max_length=255)
    number = models.IntegerField()
    neighbourhood = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}"

class Barbershop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    imageUrl = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Operation(models.Model):
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name="operations")
    weekDay = models.SmallIntegerField()
    timeInitial = models.TimeField()
    timeFinal = models.TimeField()

    class Meta:
        unique_together = ('barbershop', 'weekDay')

    def __str__(self):
        return f"{self.barbershop.name} - Dia {self.weekDay}"

class Employee(models.Model):
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name="employees")
    username = models.CharField(max_length=255)
    urlProfilePhoto = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

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