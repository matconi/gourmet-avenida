from django.contrib import admin
from .models.User import User
from .models.Customer import Customer
from .models.Payment import Payment
from .admin_forms import UserAdminForm, CustomerAdminForm, PaymentAdminForm

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
        
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm

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