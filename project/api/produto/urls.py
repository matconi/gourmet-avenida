from . import views
from django.urls import path


app_name = 'api_produto'
urlpatterns = [
    path('<slug:slug>', views.view_product, name='view_product'),
    path('load-more/', views.load_more, name='load_more'),
    path('load-more-category/<slug:category_slug>', views.load_more_category, name='load_more_category')
]
