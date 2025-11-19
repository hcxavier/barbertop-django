from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser
from barbershops.models import Barbershop, Address

class ClientSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['phone'].required = True

        # Configuração das Senhas
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirme sua Senha"
        self.fields['password1'].help_text = "" # Remove texto de ajuda padrão do Django

        # --- Injeção de Estilos (CSS) ---
        
        # Username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-dark', 
            'placeholder': 'Digite seu nome de usuário'
        })
        
        # Email
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-dark',
            'placeholder': 'seu@email.com'
        })
        
        # Phone
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control form-control-dark',
            'placeholder': '(11) 99999-9999'
        })

        # cpf
        self.fields['cpf'].widget.attrs.update({
            'class': 'form-control form-control-dark',
            'placeholder': '000.000.000-00'
        })

        # Senhas
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-dark',
            'placeholder': 'Mínimo 6 caracteres'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-dark',
            'placeholder': 'Confirme sua senha'
        })

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'cpf') 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.CLIENT # Define como Cliente
        if commit:
            user.save()
        return user

class BarbershopSignUpForm(UserCreationForm):
    shop_name = forms.CharField(max_length=255, label="Nome da Barbearia")
    description = forms.CharField(
        max_length=300, 
        label="Descrição da barbearia", 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 3})
    )
    
    # Campos de Endereço
    street = forms.CharField(max_length=255, label="Rua")
    number = forms.IntegerField(label="Número")
    city = forms.CharField(max_length=255, label="Cidade")
    neighbourhood = forms.CharField(max_length=255, label="Bairro")
    state = forms.CharField(max_length=2, label="UF")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone', 'cpf') 

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.OWNER # Define como Dono
        user.save()

        address = Address.objects.create(
            street=self.cleaned_data['street'],
            number=self.cleaned_data['number'],
            city=self.cleaned_data['city'],
            neighbourhood=self.cleaned_data['neighbourhood'],
            state=self.cleaned_data['state']
        )

        Barbershop.objects.create(
            owner=user,
            address=address,
            name=self.cleaned_data['shop_name'],
            description=self.cleaned_data.get('description', '')
        )

        return user