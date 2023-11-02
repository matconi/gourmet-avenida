from django.urls import path
from . import views

app_name = 'pedido'
urlpatterns = [
    path('', views.index, name="index"), 
    path('adicionar/', views.save, name="save")
 ]
