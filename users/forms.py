from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.db import transaction
from barbershops.models import Barbershop, Address

class ClientSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirme sua Senha"
        self.fields['password1'].help_text = ""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'cpf', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.CLIENT # Definindo como cliente
        if commit:
            user.save()
        return user

class BarbershopSignUpForm(UserCreationForm):
    shop_name = forms.CharField(max_length=255, label="Nome da Barbearia")
    description = forms.CharField(max_length=300, label="Descrição da barbearia", required=False, widget=forms.Textarea(attrs={'rows': 3}))    # Campos de Endereço
    
    street = forms.CharField(max_length=255, label="Rua")
    number = forms.IntegerField(label="Número")
    city = forms.CharField(max_length=255, label="Cidade")
    neighbourhood = forms.CharField(max_length=255, label="Bairro")
    state = forms.CharField(max_length=2, label="UF")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone', 'cpf') # Dados do dono da barbearia

        @transaction.atomic
        def save(self, commit=True):
            user = super().save(commit=False)
            user.role = CustomUser.Role.OWNER
            user.save()

            # 2. Cria o Endereço
            address = Address.objects.create(
                street=self.cleaned_data['street'],
                number=self.cleaned_data['number'],
                city=self.cleaned_data['city'],
                neighbourhood=self.cleaned_data['neighbourhood'],
                state=self.cleaned_data['state']
            )

            # 3. Cria a barbearia (vinculando dono e endereço)
            Barbershop.objects.create(
                owner=user,
                address=address,
                name=self.cleaned_data['shop_name'],
                description=self.cleaned_data['description']
            )

            return user