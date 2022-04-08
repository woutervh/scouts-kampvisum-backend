from django.urls import path

from scouts_auth.auth.views import (
    CurrentUserView,
    PermissionsView,
    OIDCAuthCodeView,
    OIDCRefreshView,
)

urlpatterns = [
    # The infamous 'me' call
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    path("auth/permissions/", PermissionsView.as_view(), name="permissions"),
    # Authenticate with OIDC
    path("oidc/token/", OIDCAuthCodeView.as_view(), name="token"),
    # Refresh the OIDC authentication
    path("oidc/refresh/", OIDCRefreshView.as_view(), name="refresh"),
]
