from django.contrib import admin
from .models import Order
from .models import OrderUnit
from usuario.models import Payment 

class OrderUnitInline(admin.TabularInline):
    model = OrderUnit
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderUnitInline,
        PaymentInline
    ]

admin.site.register(Order)
admin.site.register(OrderUnit)
