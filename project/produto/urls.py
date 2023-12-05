from django.urls import path
from . import views

app_name = 'produto'
urlpatterns = [
    path('', views.index, name="index"), 
    path('<slug:category_slug>', views.index_category, name="index_category"),
    path('adicionar-ao-carrinho/<int:pk>', views.add_one_to_cart, name="add_one_to_cart"),
    path('<slug:category_slug>/<slug:unit_slug>', views.view, name="view"),
    path('adicionar-ao-carrinho/', views.add_to_cart, name="add_to_cart"),
    path('carrinho/', views.cart, name="cart"),
    path('carrinho/esvaziar/', views.clear_cart, name="clear_cart"),
    path('carrinho/remover/', views.remove_from_cart, name="remove_from_cart"),
 ]
