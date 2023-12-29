from django.contrib import admin
from .models import User, Customer, Payment
from .admin_forms import UserAdminForm, CustomerAdminForm, PaymentAdminForm

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(UserAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormRequest
        
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(CustomerAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormRequest

class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm
    
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