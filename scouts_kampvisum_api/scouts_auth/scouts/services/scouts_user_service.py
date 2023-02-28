import pytz
from typing import List, Tuple
from datetime import datetime

from django.conf import settings

from apps.groups.services import ScoutsSectionService

from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.groupadmin.models import (
    AbstractScoutsMember,
    AbstractScoutsGroup,
    AbstractScoutsFunctionDescription,
    AbstractScoutsFunction,
    ScoutsGroup,
    ScoutsFunction,
    ScoutsUser
)
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.groupadmin.settings import GroupAdminSettings
from scouts_auth.inuits.utils import ListUtils
from scouts_auth.scouts.services import ScoutsPermissionService, ScoutsUserSessionService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserService:

    groupadmin = GroupAdminMemberService()
    permission_service = ScoutsPermissionService()
    section_service = ScoutsSectionService()
    session_service = ScoutsUserSessionService()

    def get_scouts_user(self, active_user: settings.AUTH_USER_MODEL, abstract_member: AbstractScoutsMember) -> settings.AUTH_USER_MODEL:
        # Clear any lingering data
        active_user.clear_data()

        # #######
        # 1. MEMBER PROFILE (rest-ga/lid/profiel)
        #
        # Get the member profile from groepsadmin
        #
        # This contains:
        # - basic user data (username, first_name, phone number, ...)
        # - a list of scouts functions, for a particular group
        # abstract_user: AbstractScoutsMember = self.group_admin.get_member_profile(
        #     active_user=active_user)
        #
        # -- Already done by the authentication backend
        logger.debug(
            f"[AUTHENTICATION/AUTHORISATION] Constructing a ScoutsUser object", user=active_user)

        # #######
        # 2. FUNCTION DESCRIPTIONS (rest-ga/functie)
        #
        # Get the list of function descriptions for which the user has rights
        #
        # This contains all the functions the user can see, including
        # - active functions
        # - inactive functions
        # - functions the user doesn't have, but can see the description of
        # - functions that denote leadership status ("Leiding")
        abstract_function_descriptions: List[AbstractScoutsFunctionDescription] = self.groupadmin.get_function_descriptions(
            active_user=active_user).function_descriptions

        # #######
        # 3. GROUPS (rest-ga/groep)
        #
        # Get the list of scouts groups for which the user has rights
        #
        # This contains all the scouts groups the user is allowed to see
        # An AbstractScoutsGroup contains:
        # - The group's group admin id
        # - The group's name
        abstract_groups: List[AbstractScoutsGroup] = self.groupadmin.get_groups(
            active_user=active_user).scouts_groups
        user_groups = self.process_groups(abstract_groups=abstract_groups)

        if ScoutsUser.has_administrator_groups(user_groups=user_groups):
            from apps.visums.models import CampVisum

            groups = CampVisum.objects.get_queryset().get_linked_groups()
            for group in groups:
                if group[0] not in [user_group.group_admin_id for user_group in user_groups]:
                    admin_group = ScoutsGroup()

                    admin_group.group_admin_id = group[0]
                    admin_group.name = group[1]

                    user_groups.append(admin_group)

        # #######
        # 4. PROCESS FUNCTIONS
        #
        # Result of this should be:
        # - A list of abstract functions we want to persist
        # - A list of scouts groups for which the user has an included function
        #
        # The following settings apply:
        # - INCLUDE_INACTIVE_FUNCTIONS_IN_PROFILE
        # - INCLUDE_ONLY_LEADER_FUNCTIONS_IN_PROFILE
        # - LEADERSHIP_STATUS_IDENTIFIER
        user_functions = self.process_functions(
            active_user=active_user,
            user_groups=user_groups,
            abstract_member=abstract_member,
            abstract_function_descriptions=abstract_function_descriptions)

        for scouts_function in user_functions:
            active_user.add_scouts_function(scouts_function)

        # #######
        # 5. PROCESS GROUPS
        #
        #
        #
        #
        for scouts_group in user_groups:
            active_user.add_scouts_group(scouts_group=scouts_group)

        logger.info(active_user.to_descriptive_string())

        logger.debug(
            f"[AUTHENTICATION/AUTHORISATION] Updating user authorisations", user=active_user)
        self.permission_service.update_user_authorizations(user=active_user)

        logger.debug(
            f"[AUTHENTICATION/AUTHORISATION] Setting up default scouts sections", user=active_user)
        self.section_service.setup_default_sections(user=active_user)

        logger.debug(
            f"[AUTHENTICATION/AUTHORISATION] ScoutsUser object initialised", user=active_user)

        return active_user

    def process_groups(self, abstract_groups: List[AbstractScoutsGroup]) -> List[ScoutsGroup]:
        user_groups: List[ScoutsGroup] = []

        # First construct a list of ScoutsGroup instances
        for abstract_group in abstract_groups:
            user_groups.append(
                ScoutsGroup.from_abstract_scouts_group(abstract_group=abstract_group))

        return self.process_child_groups(user_groups=user_groups, abstract_groups=abstract_groups)

    def process_child_groups(self, user_groups: List[ScoutsGroup], abstract_groups: List[AbstractScoutsGroup]) -> List[ScoutsGroup]:
        # Now loop over the list and find child groups, filtering out groups that weren't in the group call
        # (this is because groups may be listed as underlying groups, without them having any activity)
        for parent_group in user_groups:
            for abstract_group in abstract_groups:
                if abstract_group.child_groups and len(abstract_group.child_groups) > 0:
                    for child_group in abstract_group.child_groups:
                        for scouts_group in user_groups:
                            if scouts_group.group_admin_id == child_group:
                                parent_group.add_child_group(child_group)

        return user_groups

    # #######
    # LEADER:
    # To definitively find out if a user is a leader, the function description
    # must be queried. This is because the scouts maintain a flexible approach
    # to section naming.
    # A code like GVL (gidsen-verkennerleiding) in the function list of the
    # profile call is not sufficient, because a scouts group might not have
    # that section (gidsen/verkenners). To know for sure, the function
    # description must be queried. If it contains the word "Leiding" under the
    # key "naam" in the element "groeperingen", then you know it's a leader
    # function.
    # Required calls:
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie

    # GROUP LEADER:
    # These functions do follow a convention that can be derived from the
    # profile call: if the function code is GRL (groepsleider), AGRL (adjunct
    # groepsleider) or GRLP (groepsleidingsploeg), then the user is a group
    # leader.
    # Required calls:
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel

    # DISTRICT COMMISSIONER:
    # DC is different yet again. When a user is a DC, it could be that only 1
    # group is listed in the profile call. Usually however, a DC has
    # responsibilities for more than 1 group. A list of these groups can be
    # derived by looking at the underlying and upper groups (keys
    # "onderliggendeGroepen" and "bovenliggendeGroep") in a group call.
    # This follows a convention that if someone is DC for group A1234B, that
    # user is also a DC for all groups that have a name starting with A12.

    # SHIRE PRESIDENT:
    # A shire president (gouwvoorzitter) more or less follows the logic for a DC,
    # but the underlying groups are DC groups.
    # To get the complete list of scouts groups under the responsibility of the
    # shire president, there is currently no other option than to make separate calls
    # for every underlying group of every DC group.

    # Required calls:
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/<GROUP NAME>
    #
    def process_functions(
        self,
        active_user: ScoutsUser,
        user_groups: List[ScoutsGroup],
        abstract_member: AbstractScoutsMember,
        abstract_function_descriptions: List[AbstractScoutsFunctionDescription]
    ) -> List[AbstractScoutsFunction]:
        user_functions: List[ScoutsFunction] = []

        now = pytz.utc.localize(datetime.now())

        include_inactive = GroupAdminSettings.include_inactive_functions_in_profile()
        include_only_leader_functions = GroupAdminSettings.include_only_leader_functions_in_profile()
        leadership_status_identifier = GroupAdminSettings.get_leadership_status_identifier()

        for abstract_function in abstract_member.functions:
            # logger.debug(
            #     f"USER FUNCTION: {abstract_function.scouts_group.group_admin_id} {abstract_function.description} {abstract_function.code}", user=active_user)
            # Ignore inactive functions ?
            if not include_inactive and abstract_function.end and abstract_function.end <= now:
                # logger.debug(
                #     f"- IGNORING: include_inactive is {include_inactive} and end date has passed ({abstract_function.end})")
                continue

            user_functions = self.process_function(
                active_user=active_user,
                user_groups=user_groups,
                user_functions=user_functions,
                abstract_function=abstract_function,
                abstract_function_descriptions=abstract_function_descriptions,
                leadership_status_identifier=leadership_status_identifier,
                include_only_leader_functions=include_only_leader_functions,
            )

        return user_functions

    def process_function(
        self,
        active_user: ScoutsUser,
        user_groups: List[ScoutsGroup],
        user_functions: List[ScoutsFunction],
        abstract_function: AbstractScoutsFunction,
        abstract_function_descriptions: List[AbstractScoutsFunctionDescription],
        leadership_status_identifier: str,
        include_only_leader_functions: bool = False,
    ) -> List[AbstractScoutsFunction]:
        is_leader_function = False
        for abstract_function_description in abstract_function_descriptions:
            if abstract_function_description.group_admin_id == abstract_function.function:
                for grouping in abstract_function_description.groupings:
                    if grouping.name == leadership_status_identifier:
                        is_leader_function = True
                        break

        # Ignore non-leader functions ?
        if not include_only_leader_functions or is_leader_function:
            user_functions.append(self.create_scouts_function(
                active_user=active_user,
                user_groups=user_groups,
                abstract_function=abstract_function,
                abstract_function_description=abstract_function_description,
                is_leader=is_leader_function))
            # logger.debug(
            #     f"- INCLUDING: {abstract_function.scouts_group.group_admin_id} {abstract_function.code} {abstract_function.description}")
        # else:
            # logger.debug(
            #     f"- IGNORING: include_only_leader_functions is set to {include_only_leader_functions} or is_leader_function is {is_leader_function}")

        return user_functions

    def create_scouts_function(
            self,
            active_user: ScoutsUser,
            user_groups: List[ScoutsGroup],
            abstract_function: AbstractScoutsFunction,
            abstract_function_description: AbstractScoutsFunctionDescription,
            is_leader: bool = False) -> ScoutsFunction:
        scouts_function = ScoutsFunction.from_abstract_function(
            abstract_function=abstract_function, abstract_function_description=abstract_function_description)

        scouts_group: ScoutsGroup = None
        for user_group in user_groups:
            if user_group.group_admin_id == abstract_function.scouts_group.group_admin_id:
                scouts_group = user_group

        if not scouts_group:
            raise ScoutsAuthException(
                f"[{active_user.username}] Scouts group {abstract_function.scouts_group.group_admin_id} is not registered for user")

        scouts_function.scouts_group = scouts_group.group_admin_id
        scouts_function.is_leader = is_leader

        return scouts_function
