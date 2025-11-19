from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Home temporária só para não dar erro 404 no redirecionamento
def home_view(request):
    return HttpResponse("<h1>Página Inicial - Cadastro Sucesso!</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', home_view, name='home'),
    path('barbershops/', include('barbershops.urls')),
    path('bookings/', include('bookings.urls'))
]
