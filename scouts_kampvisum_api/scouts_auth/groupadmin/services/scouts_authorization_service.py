import pytz
from lib2to3.pgen2.token import EQUAL
from typing import List
from datetime import datetime

from django.conf import settings
from django.core.exceptions import PermissionDenied

from scouts_auth.auth.services import AuthorizationService

from scouts_auth.groupadmin.models import (
    AbstractScoutsGroup,
    ScoutsGroup,
    AbstractScoutsFunction,
    AbstractScoutsFunctionDescription,
    ScoutsFunction,
)
from scouts_auth.groupadmin.services import (
    GroupAdminMemberService,
    ScoutsGroupService,
    ScoutsFunctionService,
)
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.utils import GlobalSettingsUtil


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsAuthorizationService(AuthorizationService):
    """
    Fetches additional information from groupadmin, required to finetune user permissions.

    For a scouts user, the following sources are required for full authorization:
    0) Successfull authentication (provides partial scouts groups)
    1) Full user information, after a groupadmin call to /profiel (the "me" call)
    2) BASIC PERMISSIONS: Membership of groups, defined in roles.yaml and loaded by PermissionService, after successfull authentication
        -> load_user_scouts_groups
    3) ADMINISTRATOR: Membership of administrator groups, from the user informatiom (/profiel)
    4) SECTION LEADER: Section leader status, loaded after a groupadmin call for every function
        -> load_user_functions
    5) GROUP LEADER: Group leader status, from the function code in the profile response in 1)
    6) DISCTRICT COMMISSIONER: District commissioner status, from the function code in the profile response in 1)
    """

    USER = "role_user"
    SECTION_LEADER = "role_section_leader"
    GROUP_LEADER = "role_group_leader"
    DISTRICT_COMMISSIONER = "role_district_commissioner"
    ADMINISTRATOR = "role_administrator"

    known_roles = [
        USER,
        SECTION_LEADER,
        GROUP_LEADER,
        DISTRICT_COMMISSIONER,
        ADMINISTRATOR,
    ]

    service = GroupAdminMemberService()
    scouts_group_service = ScoutsGroupService()
    scouts_function_service = ScoutsFunctionService()

    def load_user_scouts_groups(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        logger.debug(
            "SCOUTS AUTHORIZATION SERVICE: loading user groups", user=user)
        user = self.scouts_group_service.create_or_update_scouts_groups_for_user(
            user=user
        )
        user = self.update_user_authorizations(user)

        user.full_clean()
        user.save()

        return user

    def update_user_authorizations(
        self, user: settings.AUTH_USER_MODEL, scouts_group: ScoutsGroup = None
    ) -> settings.AUTH_USER_MODEL:
        logger.debug(
            "SCOUTS AUTHORIZATION SERVICE: updating user authorizations", user=user
        )

        # Initialize authorizations we can derive from membership of a scouts group
        if user.has_role_administrator():
            user = self.add_user_as_admin(user)
            return user

        allowed = False
        if scouts_group:
            if user.has_role_district_commissioner(group=scouts_group):
                allowed = True

            if user.has_role_group_leader(group=scouts_group):
                allowed = True

            if user.has_role_section_leader(group=scouts_group):
                allowed = True

            if not allowed:
                logger.warn("Not allowed to retrieve data for group %s",
                            scouts_group.group_admin_id, user=user)
                raise PermissionDenied()

            if user.has_role_district_commissioner(group=scouts_group):
                user = self.add_user_to_group(
                    user,
                    ScoutsAuthorizationService.DISTRICT_COMMISSIONER,
                    scouts_group=scouts_group,
                )

            else:
                user = self.remove_user_from_group(
                    user,
                    ScoutsAuthorizationService.DISTRICT_COMMISSIONER,
                    scouts_group=scouts_group,
                )

            if user.has_role_group_leader(group=scouts_group):
                user = self.add_user_to_group(
                    user,
                    ScoutsAuthorizationService.GROUP_LEADER,
                    scouts_group=scouts_group,
                )

            else:
                user = self.remove_user_from_group(
                    user,
                    ScoutsAuthorizationService.GROUP_LEADER,
                    scouts_group=scouts_group,
                )

            if user.has_role_section_leader(group=scouts_group):
                user = self.add_user_to_group(
                    user,
                    ScoutsAuthorizationService.SECTION_LEADER,
                    scouts_group=scouts_group,
                )

            else:
                user = self.remove_user_from_group(
                    user,
                    ScoutsAuthorizationService.SECTION_LEADER,
                    scouts_group=scouts_group,
                )

        if GroupAdminSettings.is_debug():
            test_groups = GroupAdminSettings.get_test_groups()
            if any(group in user.get_group_names() for group in test_groups):
                logger.debug(
                    "User %s is member of a test group and DEBUG is set to True, adding user as administrator",
                    user.username,
                )
                # GlobalSettingsUtil.instance().is_test = True
                GlobalSettingsUtil.is_test = True
                user = self.add_user_as_admin(user)

        return user

    def add_user_as_admin(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        return self.add_user_to_group(user, ScoutsAuthorizationService.ADMINISTRATOR)

    def add_user_to_group(
        self,
        user: settings.AUTH_USER_MODEL,
        role: str,
        scouts_group: ScoutsGroup = None,
    ) -> settings.AUTH_USER_MODEL:
        if role not in self.known_roles:
            raise ValueError("Role " + role + " is not a known scouts role")

        logger.debug(f"Adding user {user.username} to permission group {role}")
        super().add_user_to_group(user, group_name=role)

        return user

    def remove_user_from_group(
        self,
        user: settings.AUTH_USER_MODEL,
        role: str,
        scouts_group: ScoutsGroup = None,
    ) -> settings.AUTH_USER_MODEL:
        if role not in self.known_roles:
            raise ValueError("Role " + role + " is not a known scouts role")

        logger.debug(f"Removing user {user.username} from permission group {role}")
        super().remove_user_from_group(user, group_name=role)

        return user

    def load_user_functions(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        logger.debug(
            "SCOUTS AUTHORIZATION SERVICE: loading user functions",
            user=user,
        )
        abstract_function_descriptions: List[AbstractScoutsFunctionDescription] = self.service.get_function_descriptions(
            active_user=user).function_descriptions
        active_leader_functions: List[AbstractScoutsFunction] = self.get_active_leader_functions(
            user=user, abstract_function_descriptions=abstract_function_descriptions)
        user = self.scouts_function_service.create_or_update_scouts_functions_for_user(
            user=user, abstract_functions=active_leader_functions, abstract_function_descriptions=abstract_function_descriptions
        )

        return user

    def get_active_leader_functions(self, user: settings.AUTH_USER_MODEL, abstract_function_descriptions: List[AbstractScoutsFunctionDescription] = None) -> List[AbstractScoutsFunction]:
        leader_functions: List[AbstractScoutsFunction()] = []

        if abstract_function_descriptions is None or len(abstract_function_descriptions) == 0:
            abstract_function_descriptions: List[AbstractScoutsFunctionDescription] = self.service.get_function_descriptions(
                active_user=user).function_descriptions
        now = pytz.utc.localize(datetime.now())

        for user_function in user.functions:
            function_end = user_function.end
            # if function_end and (not hasattr(function_end, "tzinfo") or function_end.tzinfo is None or function_end.tzinfo.utcoffset(function_end) is None):
            #     function_end = pytz.utc.localize(value)

            if function_end is None or function_end >= now:
                for abstract_function_description in abstract_function_descriptions:
                    if abstract_function_description.group_admin_id == user_function.group_admin_id or abstract_function_description.group_admin_id == user_function.function:
                        for grouping in abstract_function_description.groupings:
                            if grouping.name == GroupAdminSettings.get_section_leader_identifier():
                                leader_functions.append(user_function)
                                # if user_function.group_admin_id not in [f.group_admin_id for f in leader_functions]:
                                #     leader_functions.append(user_function)

        return leader_functions
