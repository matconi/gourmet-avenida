from django.contrib import admin
from .models.Category import Category
from .models.Product import Product
from .models.Variant import Variant
from .models.Variation import Variation
from .models.Unit import Unit

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [
        UnitInline
    ]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Unit)
admin.site.register(Variant)
admin.site.register(Variation)
