from django.contrib import admin
from .models.Order import Order
from .models.OrderUnit import OrderUnit

class OrderUnitInline(admin.TabularInline):
    model = OrderUnit
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderUnitInline
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUnit)
