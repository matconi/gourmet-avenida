from django import forms
from .models.Customer import Customer
from django.core.validators import ValidationError
from .models.User import User
from .domain.repositories import user_repository

class ProfileForm(forms.ModelForm):   
    email = forms.CharField(max_length=320, label='Email', required=True,
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
        help_text='Digite apenas números',
        widget=forms.TextInput(
            attrs={
                "placeholder": "(12)12345-1234"
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email != self.instance.email:
            if user_repository.exists_by_email(email):
                raise forms.ValidationError('Um usuário já foi registrado com este endereço de e-mail.')
        return email

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')
