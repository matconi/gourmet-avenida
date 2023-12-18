from django.urls import path
from . import views

app_name = 'pedido'
urlpatterns = [
    path('', views.index, name="index"), 
    path('reservar/', views.book, name="book")
 ]
