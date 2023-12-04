from . import views
from django.urls import path

app_name = 'api_usuario'
urlpatterns = [
    path('load-more-favorites/', views.load_more_favorites, name='load_more_favorites')
]
