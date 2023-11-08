from django import forms
from allauth.account.forms import SignupForm, ChangePasswordForm, SetPasswordForm, ResetPasswordKeyForm
from usuario.models.Customer import Customer
from allauth.account.forms import PasswordField
from django.core.validators import RegexValidator
from usuario.models.User import User

def get_password_pattern() -> RegexValidator:
    return RegexValidator(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)((?=.*[\W_]))*.*$",
        'A senha deve conter pelo menos 1 número, 1 letra maiúscula e 1 minúscula, totalizando no mínimo 8 caracteres.'
    )

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Senha', autocomplete="new-password",
            help_text="Mínimo de 8 caracteres, incluindo números, letras maiúsculas e minúsculas.",
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

class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Nova Senha', autocomplete="new-password",
            help_text="Mínimo de 8 caracteres, incluindo números, letras maiúsculas e minúsculas",
            validators=[get_password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Senha', autocomplete="new-password",
            help_text="Mínimo de 8 caracteres, incluindo números, letras maiúsculas e minúsculas",
            validators=[get_password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )

class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Nova Senha', autocomplete="new-password",
            help_text="Mínimo de 8 caracteres, incluindo números, letras maiúsculas e minúsculas",
            validators=[get_password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )