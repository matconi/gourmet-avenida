from django.contrib import admin
from .models import Order
from .models import OrderUnit
from usuario.models import Payment 
from pedido.admin_forms import OrderAdminForm
from django import forms
from produto.templatetags.produto_pipe import currencyformat

class OrderUnitInline(admin.TabularInline):
    model = OrderUnit
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    inlines = [OrderUnitInline]
    list_display = ['id', 'customer', 'date_time', 'get_total_price', 'status']
    list_filter = ['status', 'date_time']
    search_fields = ('customer__name', 'customer__user__email', 'customer__user__phone', 'id',)

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
        instances = formset.save()
        if order_unit_form.changed_data:
            form.set_totals(instances)
            form.instance.save()
        form.change_bill()
        form.bind_payment()
    
    @admin.display(ordering='total_price', description='Total')
    def get_total_price(self, order: Order):
        return currencyformat(order.get_sold_price())

class OrderUnitAdmin(admin.ModelAdmin):
    list_display = ['get_order_id', 'unit', 'quantity']
    list_filter = ['order__status', 'order__date_time']
    search_fields = (
        'order__customer__name', 'order__customer__user__email', 'order__customer__user__phone', 'order__id',
    )

    @admin.display(ordering='id', description='Id Pedido')
    def get_order_id(self, order_unit: OrderUnit):
        return order_unit.order.id

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUnit, OrderUnitAdmin)
