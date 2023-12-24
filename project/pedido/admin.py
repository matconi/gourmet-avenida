from django.contrib import admin
from .models import Order
from .models import OrderUnit
from usuario.models import Payment 
from pedido.admin_forms import OrderAdminForm
from django import forms

class OrderUnitInline(admin.TabularInline):
    model = OrderUnit
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    inlines = [
        OrderUnitInline
    ]

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormRequest

    def save_formset(self, request, form, formset, change):
        try:
            order_unit_form = formset[0]
        except IndexError as e:
            raise forms.ValidationError("Por favor, adicione as unidades referentes ao pedido.")
        return formset.save()

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUnit)
