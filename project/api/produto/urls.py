from . import views
from django.urls import path


app_name = 'api_produto'
urlpatterns = [
    path('<slug:slug>', views.view_product, name='view_product' )
]
