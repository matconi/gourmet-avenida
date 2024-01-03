from django.contrib import admin
from .models import User, Customer, Payment
from .admin_forms import UserAdminForm, CustomerAdminForm, PaymentAdminForm
from .templatetags.usuario_pipe import get_bill, currencyformat
from django.db.models import Q
from typing import List

class CustomerGroupFilter(admin.SimpleListFilter):
    title = 'Grupo'
    parameter_name = 'group'
    
    def lookups(self, request, model_admin):
        return [
            ("u", "Possui usuário"),
            ("pu", "Possui usuário Premium"),
            ("nu", "Não possui usuário"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "u":
            return queryset.filter(
                Q(user__groups__in=[User.CUSTOMER_ROLE]) |
                Q(user__is_superuser=True)
            )
        if self.value() == "pu":
            return queryset.filter(
                Q(user__groups__in=[User.CUSTOMER_PREMIUM_ROLE]) | 
                Q(user__is_superuser=True)
            )
        if self.value() == "nu":
            return queryset.filter(user=None)

class UserGroupFilter(admin.SimpleListFilter):
    title = 'Grupo'
    parameter_name = 'group'
    
    def lookups(self, request, model_admin):
        return [
            ("c", "Cliente"),
            ("pc", "Cliente Premium"),
            ("nc", "Não possui cliente"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "c":
            return queryset.filter(
                Q(groups__in=[User.CUSTOMER_ROLE]) |
                Q(is_superuser=True)
            )
        if self.value() == "pc":
            return queryset.filter(
                Q(groups__in=[User.CUSTOMER_PREMIUM_ROLE]) | 
                Q(is_superuser=True)
            )
        if self.value() == "nc":
            return queryset.filter(groups=None)

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['first_name', 'email', 'phone']
    list_filter = ['is_active', 'is_staff', 'is_superuser', UserGroupFilter]
    search_fields = ('first_name', 'email', 'phone',)

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(UserAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormRequest
        
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = ['name', 'get_phone', 'get_bill', 'get_limit']
    list_filter = ['gender', CustomerGroupFilter]
    search_fields = ('name', 'user__email', 'user__phone',)

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(CustomerAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormRequest

    def get_queryset(self, request):
        return super(CustomerAdmin, self).get_queryset(request).select_related('user')
   
    @admin.display(ordering='name', description='Cel.')
    def get_phone(self, customer: Customer):
        return customer.user.phone if customer.user else None

    @admin.display(ordering='bill', description='Conta')
    def get_bill(self, customer: Customer):
        return get_bill(customer.bill) if customer.is_premium() else None

    @admin.display(ordering='limit', description='Limite')
    def get_limit(self, customer: Customer):
        return currencyformat(customer.limit) if customer.is_premium() else None

class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm 
    list_display = ['amount', 'customer', 'date_time']
    list_filter = ['method', 'date_time']
    search_fields = ('customer__name',)

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(PaymentAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormRequest

admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Payment, PaymentAdmin)