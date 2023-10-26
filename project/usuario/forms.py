from django import forms
from allauth.account.forms import SignupForm
from .models.Customer import Customer
from allauth.account.forms import PasswordField
from django.core.validators import RegexValidator
from django.utils import timezone
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from .models.User import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit
from crispy_forms.bootstrap import FormActions

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
                "placeholder": "Último nome"
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
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        
        self.helper.layout = Layout(
            Fieldset(
                'Informações do Perfil',
                Field('email', css_class='form-control', placeholder='Email'),
                Field('first_name', css_class='form-control', placeholder='Primeiro nome'),
                Field('last_name', css_class='form-control', placeholder='Último nome'),
                Field('phone', css_class='form-control', placeholder='(12)12345-1234')
            ),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-success')
            )
        )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']
