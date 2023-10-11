from django.urls import path
from . import views

app_name = 'produto'
urlpatterns = [
    path('produtos/', views.index, name="index"), 
    path('produtos/<slug:slug>', views.view, name="view"),
    path('produtos/adicionar-ao-carrinho/', views.add_to_cart, name="add_to_cart"),
    path('produtos/adicionar-ao-carrinho/<int:pk>', views.add_one_to_cart, name="add_one_to_cart"),
    path('produtos/carrinho/', views.cart, name="cart"),
    path('produtos/carrinho/esvaziar/', views.clear_cart, name="clear_cart"),
    path('produtos/carrinho/remover/', views.remove_from_cart, name="remove_from_cart"),
 ]
