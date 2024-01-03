from django.contrib import admin
from .models import Order
from .models import OrderUnit
from usuario.models import Payment 
from pedido.admin_forms import OrderAdminForm, OrderUnitAdminForm
from django import forms
from produto.templatetags.produto_pipe import currencyformat
from django.core.validators import ValidationError

class PayInTimeFilter(admin.SimpleListFilter):
    title = 'Pago na hora'
    parameter_name = 'payintime'
    
    def lookups(self, request, model_admin):
        return [
            ("1", "Sim"),
            ("0", "Não"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.exclude(payment=None)
        if self.value() == "0":
            return queryset.filter(payment=None)

class OrderUnitInline(admin.TabularInline):
    model = OrderUnit
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    inlines = [OrderUnitInline]
    list_display = ['id', 'customer', 'date_time', 'get_total_price', 'status']
    list_filter = ['status', 'date_time', PayInTimeFilter]
    search_fields = ('customer__name', 'customer__user__email', 'customer__user__phone', 'id',)

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormRequest

    def save_formset(self, request, form: OrderAdminForm, formset, change):
        if not formset.cleaned_data:
            raise ValidationError("Por favor, adicione as unidades referentes ao pedido.")

        instances = formset.save()
        if instances:
            form.set_totals(instances)
            form.instance.save()
        form.bind_payment()
        form.buy_bill()
    
    @admin.display(ordering='total_price', description='Total')
    def get_total_price(self, order: Order):
        return currencyformat(order.get_sold_price())

class OrderUnitAdmin(admin.ModelAdmin):
    form = OrderUnitAdminForm
    list_display = ['get_order_id', 'unit', 'get_price', 'quantity', 'get_quantity_price']
    list_filter = ['order__status', 'order__date_time']
    search_fields = (
        'order__customer__name', 'order__customer__user__email', 'order__customer__user__phone', 'order__id',
    )

    @admin.display(ordering='id', description='Id Pedido')
    def get_order_id(self, order_unit: OrderUnit):
        return order_unit.order.id

    @admin.display(ordering='price', description='Preço')
    def get_price(self, order_unit: OrderUnit):
        return currencyformat(order_unit.price)

    @admin.display(ordering='price', description='Subtotal')
    def get_quantity_price(self, order_unit: OrderUnit):
        return currencyformat(order_unit.quantity_price())

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUnit, OrderUnitAdmin)
