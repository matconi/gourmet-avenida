from django import forms
from allauth.account.forms import SignupForm
from .models.Customer import Customer
from allauth.account.forms import PasswordField
from django.core.validators import RegexValidator, ValidationError
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from .models.User import User
from .domain.repositories import user_repository

def get_password_pattern() -> RegexValidator:
    return RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)((?=.*[\W_]))*.*$',
        'A senha deve conter pelo menos 1 número, 1 letra maiúscula e 1 minúscula, totalizando no mínimo 8 caracteres.'
    )

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Senha', autocomplete="new-password",
            help_text="Mínimo de 8 caracteres, incluindo números, letras maiúsculas e minúsculas",
            validators=[get_password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )
        self.fields['email'].widget.attrs.update(
           {"placeholder": "exemplo@gmail.com"}
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

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()
        customer = Customer.objects.create(user=user)
        return user

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
            if user_repository.get_by_email(email):
                raise forms.ValidationError('Um usuário já foi registrado com este endereço de e-mail')
        return email

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')
