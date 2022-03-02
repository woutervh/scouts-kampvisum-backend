from typing import List

from django.conf import settings

from scouts_auth.auth.services import AuthorizationService

from scouts_auth.groupadmin.models import AbstractScoutsGroup, AbstractScoutsFunction
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.groupadmin.settings import GroupadminSettings

from scouts_auth.inuits.utils import GlobalSettingsUtil

import logging

logger = logging.getLogger(__name__)


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

    def load_user_scouts_groups(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        scouts_groups: List[AbstractScoutsGroup] = self.service.get_groups(
            active_user=user
        ).scouts_groups

        user.scouts_groups = scouts_groups

        user = self.update_user_scouts_groups(user)

        return user

    def update_user_scouts_groups(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        """
        Updates the authenticated user with the groups he/she belongs to.

        The groupadmin call for groups can only be made after the user has been authenticated.
        """
        user: settings.AUTH_USER_MODEL = self.update_user_authorizations(user)

        user.full_clean()
        user.save()

        return user

    def update_user_authorizations(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        logger.debug(
            "SCOUTS AUTHORIZATION: updating user authorizations for %s", user.username
        )
        # Initialize authorizations we can derive from membership of a scouts group
        if user.has_role_administrator():
            user = self.add_user_as_admin(user)

        if user.has_role_district_commissioner():
            user = self.add_user_to_group(
                user, ScoutsAuthorizationService.DISTRICT_COMMISSIONER
            )

        if GroupadminSettings.is_debug():
            test_groups = GroupadminSettings.get_test_groups()
            if any(group in user.get_group_names() for group in test_groups):
                logger.debug(
                    "User %s is member of a test group and DEBUG is set to True, adding user as administrator",
                    user.username,
                )
                GlobalSettingsUtil.instance().is_test = True
                user = self.add_user_as_admin(user)

        return user

    def add_user_as_admin(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        return self.add_user_to_group(user, ScoutsAuthorizationService.ADMINISTRATOR)

    def add_user_to_group(
        self, user: settings.AUTH_USER_MODEL, role: str
    ) -> settings.AUTH_USER_MODEL:
        if role not in self.known_roles:
            raise ValueError("Role " + role + " is not a known scouts role")

        super().add_user_to_group(user, group_name=role)

        return user

    def load_user_functions(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        functions: List[AbstractScoutsFunction] = self.service.get_functions(
            active_user=user
        ).functions

        logger.debug(
            "SCOUTS AUTHORIZATION SERVICE: Found %d function(s) for user %s",
            len(functions),
            user.username,
        )

        for user_function in user.functions:
            for function in functions:
                if function.group_admin_id == user_function.function:
                    for grouping in function.groupings:
                        if (
                            grouping.name
                            == GroupadminSettings.get_section_leader_identifier()
                        ):
                            logger.debug(
                                "Setting user as section leader for group %s",
                                user_function.scouts_group.group_admin_id,
                            )
                            user_function.groups_section_leader[
                                user_function.scouts_group.group_admin_id
                            ] = True

        user.full_clean()
        user.save()

        return user
