from django.urls import path

from scouts_auth.auth.views import (
    CurrentUserView,
    PermissionsViewSet,
    OIDCAuthCodeView,
    OIDCRefreshView,
    LogoutView,
)

permissions = PermissionsViewSet.as_view({"get": "get"})

urlpatterns = [
    # The infamous 'me' call
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/permissions/", permissions, name="permissions"),
    # Authenticate with OIDC
    path("oidc/token/", OIDCAuthCodeView.as_view(), name="token"),
    # Refresh the OIDC authentication
    path("oidc/refresh/", OIDCRefreshView.as_view(), name="refresh"),
]
