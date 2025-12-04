import json 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser
from barbershops.models import Barbershop, Address, BarbershopService, Employee
from django.contrib.auth.forms import AuthenticationForm

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
    telephone = forms.CharField(max_length=20, label="Telefone")
    description = forms.CharField(
        max_length=300, 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 3})
    )
    profile_image = forms.ImageField(required=False, label="Imagem de Perfil")

    # Campos de Endereço
    street = forms.CharField(max_length=255, label="Rua")
    number = forms.IntegerField(label="Número")
    city = forms.CharField(max_length=255, label="Cidade")
    neighbourhood = forms.CharField(max_length=255, label="Bairro")
    state = forms.CharField(max_length=2, label="UF")

    work_alone = forms.CharField(required=False, widget=forms.HiddenInput)

    services = forms.CharField(required=False, widget=forms.HiddenInput)
    employees = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante que email obrigatório
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super().clean()

        # 1. Validação de Serviços
        services_json = cleaned_data.get('services')
        try:
            services = json.loads(services_json) if services_json else []
            if len(services) == 0:
                self.add_error(None, "É obrigatório cadastrar pelo menos um serviço.")
        except json.JSONDecodeError:
            self.add_error(None, "Erro ao processar a lista de serviços.")
        
        # 2. Validação de Funcionários
        employees_json = cleaned_data.get('employees')
        is_working_alone = cleaned_data.get('work_alone') == 'true'

        try:
            employees = json.loads(employees_json) if employees_json else []
            # Regra: Se NÃO trabalha sozinho E a lista está vazia -> ERRO
            if not is_working_alone and len(employees) == 0:
                self.add_error(None, "Adicione funcionários ou marque a opção 'Trabalho Sozinho'.")
        except json.JSONDecodeError:
            self.add_error(None, "Erro ao processar a lista de funcionários.")
        
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        # 1. Cria o Usuário (Dono)
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

        # 3. Cria a Barbearia
        barbershop = Barbershop.objects.create(
            owner=user,
            address=address,
            name=self.cleaned_data['shop_name'],
            description=self.cleaned_data.get('description', ''),
            telephone=self.cleaned_data['telephone']
            # imageUrl=self.cleaned_data.get('profile_image') 
        )

        # 4. Processa os SERVIÇOS (JSON)
        services_data = self.cleaned_data.get('services')
        if services_data:
            try:
                items = json.loads(services_data)
                for item in items:
                    BarbershopService.objects.create(
                        barbershop=barbershop,
                        name=item['nome'],
                        price=float(item['preco']),
                        description=item.get('desc', '')
                    )
            except Exception as e:
                print(f"Erro ao salvar serviços: {e}")

        # 5. Processa a EQUIPE (JSON)
        employees_data = self.cleaned_data.get('employees')
        if employees_data:
            try:
                items = json.loads(employees_data)
                for item in items:
                    Employee.objects.create(
                        barbershop=barbershop,
                        name=item['nome']
                        # Se tiver foto do funcionário, trataria aqui
                    )
            except Exception as e:
                print(f"Erro ao salvar equipe: {e}")

        return user
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-dark',
        'placeholder': 'seu@email.com',
        'id': 'email'
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-dark',
        'placeholder': '******',
        'id': 'password'
    }))

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'cpf')