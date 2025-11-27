from django import forms
from .models import BarbershopService

class BarbershopServiceForm(forms.ModelForm):
    class Meta:
        model = BarbershopService
        fields = ['name', 'description', 'price', 'imageUrl']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do serviço'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'imageUrl': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
