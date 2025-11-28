from django import forms
from .models import BarbershopService, Barbershop, Address, Employee, Operation

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

class BarbershopForm(forms.ModelForm):
    class Meta:
        model = Barbershop
        fields = ['name', 'description', 'imageUrl']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Barbearia'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição sobre a barbearia'}),
            'imageUrl': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL da Imagem/Logo'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'number', 'neighbourhood', 'state']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'neighbourhood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'urlProfilePhoto']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do funcionário'}),
            'urlProfilePhoto': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL da foto de perfil'}),
        }

class OperationForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    weekDay = forms.ChoiceField(choices=DAYS_OF_WEEK, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Operation
        fields = ['weekDay', 'timeInitial', 'timeFinal']
        widgets = {
            'timeInitial': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'timeFinal': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
