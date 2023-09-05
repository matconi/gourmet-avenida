from django.contrib import admin
from .models.User import User
from .models.Customer import Customer
from .models.Payment import Payment

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Payment)