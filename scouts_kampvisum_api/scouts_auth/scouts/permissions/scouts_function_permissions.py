from rest_framework import permissions

from django.contrib.auth.models import Group, Permission

from scouts_auth.auth.exceptions import ScoutsAuthException

from scouts_auth.groupadmin.settings import GroupAdminSettings

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunctionPermissions(permissions.DjangoModelPermissions):

    authenticated_users_only = True
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
    base_auth_roles = GroupAdminSettings.get_base_auth_roles()

    def has_permission(self, request, view) -> bool:
        group_admin_id = self._validate_request(request, view)

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        required_permission = [perm % {'app_label': queryset.model._meta.app_label,
                                       'model_name': queryset.model._meta.model_name} for perm in self.perms_map[request.method]]

        permission = super().has_permission(request, view)
        # If the user doesn't have the required permission on any auth group, look no further
        if not permission:
            logger.warn(
                f"Permission {required_permission} not set on method {request.method} or for user", user=request.user)
            return False

        from scouts_auth.groupadmin.models import ScoutsUser
        user: ScoutsUser = request.user

        if user.has_role_administrator():
            return True

        for group in user.groups.all():
            # If the user role is not included in the base authentication roles, then ignore
            if group.name in self.base_auth_roles:
                for role in user.get_roles_for_group(group_admin_id=group_admin_id):
                    logger.debug(
                        f"ROLE FOR GROUP {group_admin_id}: {role}", user=user)
                    if (
                        # If the user role for the specified groups is not included in the base authentication roles, then ignore
                        role in self.base_auth_roles and role == group.name
                    ):
                        permissions: List[str] = [
                            permission.content_type.app_label + "." + permission.codename for permission in group.permissions.all()]
                        if any(perm in perms for perm in permissions):
                            return True

        logger.warn(
            f"Permission {required_permission} not granted for user", user=request.user)

        return False

    def _validate_request(self, request, view) -> str:
        if request and request.GET and request.GET.get("auth", None) and request.user:
            return request.GET.get("auth")

        if hasattr(view, "has_group_admin_id"):
            try:
                model = view.queryset.get(pk=view.kwargs.get("pk"))
                if model.group:
                    request.GET._mutable = True
                    request.GET['auth'] = model.group
                    request.GET._mutable = False
                return model.group
            except Exception:
                pass

        raise ScoutsAuthException(
            f"[{request.user.username}] {request.path}: Permissions can only be set if the group is passed as a GET param and the user object is present")
