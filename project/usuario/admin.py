from django.contrib import admin
from .models import User, Customer, Payment
from .admin_forms import UserAdminForm, CustomerAdminForm, PaymentAdminForm
from .templatetags.usuario_pipe import get_bill, currencyformat

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['first_name', 'email', 'phone']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
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
    list_filter = ['gender']
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
        user = customer.user
        return get_bill(customer.bill) if user and user.has_perm('usuario.buy_in_term') else None

    @admin.display(ordering='limit', description='Limite')
    def get_limit(self, customer: Customer):
        user = customer.user
        return currencyformat(customer.limit) if user and user.has_perm('usuario.buy_in_term') else None

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