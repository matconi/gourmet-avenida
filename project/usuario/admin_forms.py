from django import forms
from django.contrib.auth.models import Group
from django.core.validators import ValidationError
from .domain.repositories import customer_repository, user_repository, role_repository
from .models import User, Customer, Payment
from .domain.services import messages_service, customer_service
from typing import List

class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.customer_roles_ids = Customer.get_customer_roles_ids()
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update({"class": "cel-input"})

    def clean(self):
        self.cleaned_data = super(UserAdminForm, self).clean()
        customer_roles = role_repository.get_by_ids(self.customer_roles_ids)
        self.__validate_added_role_without_customer(customer_roles)
        self.__validate_customer_without_added_role(customer_roles)

    def __validate_added_role_without_customer(self, customer_roles: List[Group]) -> None:
        if self.__added_role_without_customer(self.instance, customer_roles):
            raise ValidationError('Para adicionar uma permissão de cliente ao usuário, é necessário criar o cliente.')

    def __validate_customer_without_added_role(self, customer_roles: List[Group]) -> None:
        if self.__customer_without_added_role(self.instance, customer_roles):
            raise ValidationError('Para retirar os grupos de cliente, é necessário excluir ou desvincular o cliente deste usuário.')

    def __added_role_without_customer(self, user: User, customer_roles: List[Group]) -> bool:
        if not user.is_customer():
            for customer_role in customer_roles:
                if customer_role in self.cleaned_data["groups"]:
                    return True
        return False

    def __customer_without_added_role(self, user: User, customer_roles: List[Group]) -> bool:
        if user.is_customer():
            for customer_role in customer_roles:
                if customer_role not in self.cleaned_data["groups"]:
                    return True
        return False

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js',
            'js/admin-shared.js',
        )

    class Meta:
        exclude = ('user_permissions',)

class CustomerAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.customer_roles_ids = Customer.get_customer_roles_ids()
        super(CustomerAdminForm, self).__init__(*args, **kwargs)
        self.fields["bill"].help_text = 'Negativo indica "em haver".'
        self.fields["born_at"].widget.attrs.update({"class": "date-input"})

    def clean(self):
        self.cleaned_data = super(CustomerAdminForm, self).clean()
        customer_service.validate_limit(self.cleaned_data)

    def save(self, **kwargs):
        customer: Customer = super(CustomerAdminForm, self).save(**kwargs)

        if customer.has_user():
            customer_roles = role_repository.get_customer_by_user(customer.user, self.customer_roles_ids)
            self.__add_role(customer_roles, customer.user)
        elif self.__user_was_removed():
            user: User = user_repository.get_by_id(self.initial.get("user"))
            customer_roles = role_repository.get_customer_by_user(user, self.customer_roles_ids)
            self.__user_removed(customer_roles, user)     
        return customer

    def __add_role(self, customer_roles: List[Group], user: User) -> None:
        if not customer_roles:
            customer_role = role_repository.get_by_id(self.customer_roles_ids[0])
            role_repository.add(user, customer_role)
            messages_service.added_customer_role(self.request, customer_role, user)

    def __user_was_removed(self) -> bool:
        return (self.initial.get("user") is not None) and (self.cleaned_data["user"] is None)

    def __user_removed(self, customer_roles: List[Group], user: User) -> None:
        if customer_roles:
            for customer_role in customer_roles:
                role_repository.remove(user, customer_role)
            messages_service.removed_customer_roles(self.request, user)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js',
            'js/admin-shared.js',
        )

class PaymentAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PaymentAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data = super(PaymentAdminForm).clean()
        customer_service.validate_limit(self.cleaned_data)
        
    def save(self, **kwargs):
        customer: Customer = self.instance.customer
        if customer.is_premium():
            if not self.instance.id:                   
                customer: Customer = customer_repository.pay_bill(self.instance)
                messages_service.pay_bill(self.request, customer)
            else:
                diff = self.initial["amount"] - self.cleaned_data["amount"]
                customer: Customer = customer_repository.pay_bill(self.instance, diff)
                messages_service.update_pay_bill(self.request, customer, diff)
        return super(PaymentAdminForm, self).save(**kwargs)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js',
            'js/admin-shared.js',
        )