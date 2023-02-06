from rest_framework import permissions

from scouts_auth.auth.exceptions import ScoutsAuthException

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsGroup
from scouts_auth.groupadmin.settings import GroupAdminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


def validate_request(request) -> bool:
    if request and request.GET and request.GET.get("group", None) and request.user:
        return True

    raise ScoutsAuthException(
        "Permissions can only be set if the group is passed as a GET param and the user object is present")


def has_role_leader(request, view) -> bool:
    has_role_leader = request.user.has_role_leader(
        group_admin_id=request.GET.get("group"),
        include_inactive=GroupAdminSettings.include_inactive_functions_in_profile())

    logger.debug(
        f"{view.__class__.__name__} permissions: LEADER in {request.GET.get('group')} ? {has_role_leader}", user=request.user)

    return has_role_leader


def has_role_section_leader(request, view) -> bool:
    has_role_section_leader = request.user.has_role_section_leader(
        group_admin_id=request.GET.get("group"),
        include_inactive=GroupAdminSettings.include_inactive_functions_in_profile())

    logger.debug(
        f"{view.__class__.__name__} permissions: SECTION LEADER in {request.GET.get('group')} ? {has_role_section_leader}", user=request.user)

    return has_role_section_leader


def has_role_group_leader(request, view) -> bool:
    has_role_group_leader = request.user.has_role_group_leader(
        group_admin_id=request.GET.get("group"),
        include_inactive=GroupAdminSettings.include_inactive_functions_in_profile())

    logger.debug(
        f"{view.__class__.__name__} permissions: GROUP LEADER in {request.GET.get('group')} ? {has_role_group_leader}", user=request.user)

    return has_role_group_leader


class IsLeader(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return validate_request(request) and has_role_leader(request, view)


class IsSectionLeader(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return validate_request(request) and has_role_section_leader(request, view)


class IsGroupLeader(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return validate_request(request) and has_role_group_leader(request, view)


class IsActiveLeaderInGroup(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return validate_request(request) and (has_role_leader(request, view) or has_role_section_leader(request, view) or has_role_group_leader(request, view))


class IsDistrictCommissioner(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return validate_request(request) and request.user.has_role_district_commissioner(
            group_admin_id=request.GET.get("group"), include_inactive=GroupAdminSettings.include_inactive_functions_in_profile())


class IsShirePresident(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return validate_request(request) and request.user.has_role_shire_president(
            group_admin_id=request.GET.get("group"), include_inactive=GroupAdminSettings.include_inactive_functions_in_profile())


class CustomPermissionHelper:

    @staticmethod
    def has_required_permission(request, group_admin_id: ScoutsGroup, permission: str):
        permission_granted = request.user.has_role_leader(
            group_admin_id=group_admin_id)
        logger.debug(
            f"PERMISSION {permission} FOR OBJECT IN GROUP {group_admin_id} ? {permission_granted}", user=request.user)

        if not permission_granted:
            return False

        for group in request.user.groups.all():
            if group.name in ['role_section_leader', 'role_group_leader']:
                if permission in group.permissions.all():
                    permission_granted = True
                    break

        logger.debug(
            f"PERMISSION {permission} FOR OBJECT IN GROUP {group_admin_id} ? {permission_granted}", user=request.user)

        return permission_granted
