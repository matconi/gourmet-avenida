from django import forms
from django.contrib.auth.models import Group
from django.core.validators import ValidationError
from .domain.repositories import customer_repository, user_repository, role_repository
from .models import User, Customer, Payment
from .domain.services import messages_service
from typing import List

class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.customer_roles_ids = [User.CUSTOMER_ROLE, User.CUSTOMER_PREMIUM_ROLE]
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update({"class": "cel-input"})

    def save(self, **kwargs):
        user: User = super(UserAdminForm, self).save(**kwargs)
        customer_roles = role_repository.get_by_ids(self.customer_roles_ids)

        if self.__added_role_without_customer(user, customer_roles):
            customer = customer_repository.create_by_user(user)
            messages_service.added_role_without_customer(self.request, customer)
        elif self.__customer_without_added_role(user, customer_roles):
            raise forms.ValidationError(f'Para retirar os grupos de cliente é necessário excluir ou desvincular o cliente deste usuário.')
        return user

    def __is_customer(self, user: User) -> bool:
        return hasattr(user, 'user_customer')

    def __added_role_without_customer(self, user, customer_roles: List[Group]) -> bool:
        if not self.__is_customer(user):
            for customer_role in customer_roles:
                if customer_role in self.cleaned_data["groups"]:
                    return True
        return False

    def __customer_without_added_role(self, user, customer_roles: List[Group]) -> bool:
        if self.__is_customer(user):
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
        self.customer_roles_ids = [User.CUSTOMER_ROLE, User.CUSTOMER_PREMIUM_ROLE]
        super(CustomerAdminForm, self).__init__(*args, **kwargs)
        self.fields["bill"].help_text = 'Negativo indica "em haver".'
        self.fields["born_at"].widget.attrs.update({"class": "date-input"})

    def save(self, **kwargs):
        customer: Customer = super(CustomerAdminForm, self).save(**kwargs)

        if customer.user:
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

    def save(self, **kwargs):
        customer: Customer = self.instance.customer
        if customer.user is not None and customer.user.has_perm('buy_in_term'):
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