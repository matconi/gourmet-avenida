from django import forms
from django.core.validators import ValidationError
from .models import User, Customer
from .domain.repositories import user_repository
from .domain.services import user_service
from usuario.auth.forms import phone_pattern

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
        ' e estabelecer<br> uma comunicação mais direta.',
        validators=[phone_pattern()],
        widget=forms.TextInput(
            attrs={
                "placeholder": "(12)12345-1234",
                "class": "w-50"
            }
        )
    )
    gender = forms.ChoiceField(choices=Customer.Gender.choices, label='Gênero')
    born = forms.DateField(input_formats=['%d/%m/%Y'], label='Data de nascimento', required=True,
        widget=forms.DateInput(
            attrs={
                "placeholder": "DD/MM/AAAA",
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')  
        if email != self.instance.email:
            user_service.email_in_use(email)

        user_service.gmail_required(email)
        return email

    def save(self):
        user = super(ProfileForm, self).save()
        if hasattr(user, 'user_customer'):
            customer = user.user_customer
            customer.gender = self.cleaned_data["gender"]
            customer.born = self.cleaned_data["born"]
            customer.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone',) 

