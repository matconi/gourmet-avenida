from django.contrib import admin
from .models.Category import Category
from .models.Product import Product
from .models.Variant import Variant
from .models.Variation import Variation
from .models.Unit import Unit
from .admin_forms import UnitAdminForm

class UnitInline(admin.StackedInline):
    model = Unit
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [UnitInline]
    
    def save_formset(self, request, form, formset, change):
        initial_unit_form = formset[0].initial
        instances = formset.save(commit=False)
        
        for instance in instances:
            if isinstance(instance, Unit):
                unit_form = UnitAdminForm(instance=instance, initial=initial_unit_form) 

                setattr(unit_form, 'cleaned_data', formset.cleaned_data[0])
                unit_form.cleaned_data["image_lg"] = instance.image_lg

                unit_form.thumb_images()
            instance.save()

class UnitAdmin(admin.ModelAdmin):
    form = UnitAdminForm

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Variant)
admin.site.register(Variation)
