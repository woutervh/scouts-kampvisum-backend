from django.urls import path

from scouts_auth.auth.views import (
    CurrentUserView,
    PermissionsViewSet,
    OIDCAuthCodeView,
    OIDCRefreshView,
)

permissions = PermissionsViewSet.as_view({"get": "get"})
permissions_for_group = PermissionsViewSet.as_view({"get": "get_for_group"})

urlpatterns = [
    # The infamous 'me' call
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    path("auth/permissions/", permissions, name="permissions"),
    path(
        "auth/permissions/<str:group_admin_id>",
        permissions_for_group,
        name="permissions_for_group",
    ),
    # Authenticate with OIDC
    path("oidc/token/", OIDCAuthCodeView.as_view(), name="token"),
    # Refresh the OIDC authentication
    path("oidc/refresh/", OIDCRefreshView.as_view(), name="refresh"),
]
