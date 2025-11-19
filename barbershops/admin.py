from django.contrib import admin
from .models import Barbershop, Address, BarbershopService, Operation, Employee, Rating

admin.site.register(Address)
admin.site.register(Barbershop)
admin.site.register(BarbershopService)
admin.site.register(Operation)
admin.site.register(Employee)
admin.site.register(Rating)