from django.urls import path
from . import views

app_name = 'usuario'
urlpatterns = [
    path('perfil/', views.profile, name="profile"),
    path('pagamentos/', views.payments, name="payments"),
    path('favoritos/', views.favorites, name="favorites"),
    path('favoritos/adicionar/', views.add_favorive, name="add_favorite"),
    path('favoritos/remover/', views.remove_favorive, name="remove_favorite")
 ]
