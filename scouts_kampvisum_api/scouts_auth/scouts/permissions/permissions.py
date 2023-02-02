from rest_framework import permissions


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class IsLeaderForGroup(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        logger.debug(
            f"LEADER GROUPS: {request.user.get_scouts_leader_group_names()}")
        return request.GET.get("group") in request.user.get_scouts_leader_group_names()
