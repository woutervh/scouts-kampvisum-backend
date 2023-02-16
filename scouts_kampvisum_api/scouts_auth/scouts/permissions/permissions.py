from rest_framework import permissions

from scouts_auth.auth.exceptions import ScoutsAuthException

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsGroup
from scouts_auth.groupadmin.settings import GroupAdminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CustomPermissionHelper:

    @staticmethod
    def has_required_permission(request, group_admin_id: ScoutsGroup, permission: str):
        permission_granted = request.user.has_role_leader(
            group_admin_id=group_admin_id)
        # logger.debug(
        #     f"PERMISSION {permission} FOR OBJECT IN GROUP {group_admin_id} ? {permission_granted}", user=request.user)

        if not permission_granted:
            return False

        for group in request.user.groups.all():
            if group.name in ['role_section_leader', 'role_group_leader']:
                if permission in group.permissions.all():
                    permission_granted = True
                    break

        # logger.debug(
        #     f"PERMISSION {permission} FOR OBJECT IN GROUP {group_admin_id} ? {permission_granted}", user=request.user)

        return permission_granted
