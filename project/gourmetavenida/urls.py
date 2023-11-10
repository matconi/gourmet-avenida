from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")), #TODO debugtoolbar
    path('produtos/', include('produto.urls', namespace='produto')),
    path('api/produtos/', include('api.produto.urls', namespace='api_produtos')),
    path('pedidos/', include('pedido.urls', namespace='pedido')),
    path('accounts/', include('usuario.allauth.urls',)),
    path('usuarios/', include('usuario.urls', namespace='usuario')),
    path(settings.ADMIN_PATH, admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )