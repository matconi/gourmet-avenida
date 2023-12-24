from django import forms
from django.contrib.auth.models import Group
from django.core.validators import ValidationError
from .domain.repositories import customer_repository, user_repository, role_repository
from .models import User, Customer

class UserAdminForm(forms.ModelForm):
    def save(self, **kwargs):
        user: User = super(UserAdminForm, self).save(**kwargs)
        customer_role = role_repository.get_by_id(User.CUSTOMER_ROLE)

        if self.__added_role_without_customer(user, customer_role):
            customer_repository.create_by_user(user)
        elif self.__customer_without_added_role(user, customer_role):
            raise ValidationError('Para retirar o grupo "Cliente" é necessário excluir ou desvincular o cliente deste usuário.')

        return user

    def __is_customer(self, user: User) -> bool:
        return hasattr(user, 'user_customer')

    def __added_role_without_customer(self, user, customer_role: Group) -> bool:
        return not self.__is_customer(user) and customer_role in self.cleaned_data["groups"]

    def __customer_without_added_role(self, user, customer_role: Group) -> bool:
        return self.__is_customer(user) and customer_role not in self.cleaned_data["groups"]

    class Meta:
        exclude = ('user_permissions',)

class CustomerAdminForm(forms.ModelForm):
    def save(self, **kwargs):
        customer: Customer = super(CustomerAdminForm, self).save(**kwargs)

        if customer.user:
            customer_role = role_repository.get_by_id(User.CUSTOMER_ROLE)
            
            if customer_role not in customer.user.groups.all():
                customer.user.groups.add(customer_role)

        elif self.__user_was_removed():
            user: User = user_repository.get_by_id(self.initial["user"])
            customer_role = role_repository.get_by_id(User.CUSTOMER_ROLE)

            if customer_role in user.groups.all():
                user.groups.remove(customer_role)

        return customer
    
    def __user_was_removed(self) -> bool:
        return (self.initial.get("user") is not None) and (self.cleaned_data["user"] is None)