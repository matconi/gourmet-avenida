from django import forms
from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm, SetPasswordForm, ResetPasswordForm, ResetPasswordKeyForm
from usuario.models.Customer import Customer
from allauth.account.forms import PasswordField
from django.core.validators import RegexValidator
from usuario.models import User
from usuario.domain.repositories import user_repository
from usuario.domain.services import user_service

def password_pattern() -> RegexValidator:
    return RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)((?=.*[\W_]))*.{6,}$',
        'A senha deve conter pelo menos 1 número, 1 letra maiúscula e 1 minúscula, totalizando no mínimo 6 caracteres.'
    )

def phone_pattern() -> RegexValidator:
    return RegexValidator(
        r'^\([0-9]{2}\) [0-9]{5}-[0-9]{4}$',
        'Telefone inválido, padrão esperado: "(12) 12345-1234".'
    )
        
class CustomLoginForm(LoginForm):
    def clean_login(self):     
        user_service.block_user_by_password_err(self.cleaned_data["login"])
        return super(CustomLoginForm, self).clean_login()

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Senha', autocomplete="new-password",
            help_text="Mínimo de 6 caracteres, incluindo números, letras maiúsculas e minúsculas.",
            validators=[password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )
        self.fields['email'] = forms.CharField(max_length=320, label='Email', required=True,
            help_text='Gmail obrigatório.',
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
    phone = forms.CharField(max_length=15, label='Celular', required=True,
        help_text='Digite apenas números.',
        validators=[phone_pattern()],
        widget=forms.TextInput(
            attrs={
                "placeholder": "(12) 12345-1234",
                "class": "cel-input"
            }
        )
    )

    def clean_email(self):
        email = super(CustomSignupForm, self).clean_email()
        user_service.gmail_required(email)
        return email

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user

class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Nova Senha', autocomplete="new-password",
            help_text="Mínimo de 6 caracteres, incluindo números, letras maiúsculas e minúsculas.",
            validators=[password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Senha', autocomplete="new-password",
            help_text="Mínimo de 6 caracteres, incluindo números, letras maiúsculas e minúsculas.",
            validators=[password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )

class CustomResetPasswordForm(ResetPasswordForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            self.users = [user_repository.get_by_email_and_status(email)]
        except User.DoesNotExist:
            raise forms.ValidationError(f'Usuário não encontrado com e-mail "{email}".')
        return email

class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(
            label='Nova Senha', autocomplete="new-password",
            help_text="Mínimo de 6 caracteres, incluindo números, letras maiúsculas e minúsculas.",
            validators=[password_pattern()]
        )
        self.fields['password2'].widget.attrs.update(
           {"placeholder": "Repetir"}
        )