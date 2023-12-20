from django.urls import path
from . import views

app_name = 'pedido'
urlpatterns = [
    path('', views.index, name="index"), 
    path('reservar/', views.book, name="book"),
    path('cancelar/', views.cancel_book, name="cancel_book")
 ]
