from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from scouts_auth.groupadmin.models import ScoutsGroup, ScoutsFunction 

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)

class AuthenticationHelper:
    @staticmethod
    def load_groups(user: settings.AUTH_USER_MODEL) -> List[str]:
        leader_functions: List[ScoutsFunction] = list(
            ScoutsFunction.objects.get_leader_functions(user=user)
        ) 

        group_admin_ids = []
        for leader_function in leader_functions:
            for group in leader_function.scouts_groups.all():
                group_admin_ids.append(group.group_admin_id)

                if user.has_role_district_commissioner():
                    underlyingGroups: List[ScoutsGroup] = list(
                        ScoutsGroup.objects.get_groups_with_parent(
                            parent_group_admin_id=group.group_admin_id
                        )
                    )

                    for underlyingGroup in underlyingGroups:
                        if leader_functions.is_district_commissioner_for_group(scouts_group=underlyingGroup):
                            group_admin_ids.append(underlyingGroup.group_admin_id)
        return group_admin_ids

    @staticmethod
    def has_rights_for_group(user: settings.AUTH_USER_MODEL, group_admin_id: str = None) -> bool: 
        logger.debug("&&&&&&&&&&&&& %s", AuthenticationHelper.load_groups(user=user))
        logger.debug("&&&&&&&&&&&&& %s", group_admin_id)

        if not group_admin_id in AuthenticationHelper.load_groups(user=user):
            raise PermissionDenied(
                {
                    "message": "You don't have permission to this request for group {}".format(
                        group_admin_id
                    )
                }
            )

        return True