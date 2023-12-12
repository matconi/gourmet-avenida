from django.urls import path
from . import views

app_name = 'produto'
urlpatterns = [
    path('', views.index, name="index"), 
    path('<slug:category_slug>', views.index_category, name="index_category"),
    path('<slug:category_slug>/<slug:unit_slug>', views.view, name="view"),
    path('carrinho/', views.cart, name="cart"),
    path('adicionar-ao-carrinho/', views.add_to_cart, name="add_to_cart"),
    path('adicionar-item-ao-carrinho/', views.add_from_list_to_cart, name="add_from_list_to_cart"),
    path('carrinho/incrementar/', views.increment_cart, name="increment_cart"),
    path('carrinho/decrementar/', views.decrement_cart, name="decrement_cart"),
    path('carrinho/limpar/', views.clean_cart, name="clean_cart"),
    path('carrinho/remover/', views.remove_from_cart, name="remove_from_cart")
 ]
