from django.urls import path
from . import views

app_name = 'usuario'
urlpatterns = [
    path('perfil/', views.profile, name="profile"),
    path('pagamentos/', views.payments, name="payments"),
    path('favoritos/', views.favorites, name="favorites")
 ]
