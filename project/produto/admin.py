from django.contrib import admin
from .models import Category, Unit, Product, Variety, Variation
from .admin_forms import UnitAdminForm
from django import forms
from .templatetags.produto_pipe import currencyformat
from django.core.validators import ValidationError

class UnitInline(admin.StackedInline):
    model = Unit
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [UnitInline]
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ('name',)
    
    def save_formset(self, request, form, formset, change):
        if not formset.cleaned_data:
            raise ValidationError("Por favor, adicione as unidades referentes ao produto.")
            
        instances = formset.save(commit=False)
        for instance in instances:
            self.__set_images(formset, instance)
        formset.save_m2m()

    def __set_images(self, formset, instance):
        for inline_form in formset:
            if 'image_lg' in inline_form.changed_data:
                unit_form = UnitAdminForm(instance=instance)
                cleaned_data = (
                    list(filter(lambda attr: attr["id"] == instance, formset.cleaned_data))[0] 
                    if instance.id else inline_form.cleaned_data
                )
                setattr(unit_form, 'cleaned_data', cleaned_data)
                unit_form.thumb_images()
                instance.save()
                inline_form.changed_data.clear()
                return

class UnitAdmin(admin.ModelAdmin):
    form = UnitAdminForm
    list_display = ['name', 'get_price', 'stock', 'get_avaliable']
    list_filter = ['product__category', 'showcase', 'released']
    search_fields = ('name', 'product__name',)

    @admin.display(ordering='price', description='Preço')
    def get_price(self, unit: Unit):
        return currencyformat(unit.price)

    @admin.display(ordering='booked', description='Disponível')
    def get_avaliable(self, unit: Unit):
        return unit.avaliable()

class VariationAdmin(admin.ModelAdmin):
    list_display = ['name', 'variety']
    list_filter = ['variety']
    search_fields = ('name',)

class VarietyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Variety, VarietyAdmin)
admin.site.register(Variation, VariationAdmin)
