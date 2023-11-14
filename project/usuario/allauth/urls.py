from django.urls import path, re_path
from allauth.account import views
from allauth.socialaccount import views as sa_views
from usuario.allauth import views as custom_views
from django.conf import settings
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount.providers.google.provider import GoogleProvider

urlpatterns = [
    path("signup/", views.signup, name="account_signup"),
    path("login/", views.login, name="account_login"),
    path("logout/", views.logout, name="account_logout"),
    path("inactive/", views.account_inactive, name="account_inactive"),
    path(
        "password/change/",
        views.password_change,
        name="account_change_password"
    ),
    path("password/set/", views.password_set, name="account_set_password"),
    # password reset
    path("password/reset/", views.password_reset, name="account_reset_password"),
    path(
        "password/reset/done/",
        custom_views.password_reset_done,
        name="account_reset_password_done"
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key"
    ),
    path(
        "password/reset/key/done/",
        custom_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done"
    )
]

if settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += default_urlpatterns(GoogleProvider)
    urlpatterns += [
        path("social/connections/", sa_views.connections, name="socialaccount_connections"),
        path("login/error/", sa_views.login_error, name="socialaccount_login_error")
    ]