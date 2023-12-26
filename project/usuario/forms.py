from django import forms
from .models.Customer import Customer
from django.core.validators import ValidationError
from .models.User import User
from .domain.repositories import user_repository
from .domain.services import user_service

class ProfileForm(forms.ModelForm):   
    email = forms.CharField(max_length=320, label='Email', required=True,
        help_text='Gmail obrigatório.<br>Pelo email, é possível entrar com um clique pelo Google,'
        ' recuperar senhas e ter um canal de contato.',
        widget=forms.TextInput(
            attrs={
                "placeholder": "exemplo@gmail.com"
            }
        )
    )

    first_name = forms.CharField(max_length=50, label='Primeiro nome', required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Primeiro nome"
            }
        )
    )
    last_name = forms.CharField(max_length=120, label='Último nome', required=False, 
        widget=forms.TextInput(
            attrs={
                "placeholder": "Último nome(opcional)"
            }
        )
    )
    phone = forms.CharField(max_length=14, label='Celular', required=True,
        help_text='Digite apenas números.<br>Com o número de telefone podemos identificá-lo(a) mais facilmente'
        ' e estabelecer uma comunicação mais direta.',
        widget=forms.TextInput(
            attrs={
                "placeholder": "(12)12345-1234"
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email != self.instance.email:
            user_service.email_in_use(email)
        return email

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')
