from django.contrib import admin
from .models.User import User
from .models.Customer import Customer
from .models.Payment import Payment
from .admin_forms import UserAdminForm, CustomerAdminForm

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
        
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm

admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Payment)