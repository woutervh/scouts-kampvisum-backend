from typing import List

from django.conf import settings

from scouts_auth.groupadmin.models import (
    AbstractScoutsGroup,
    ScoutsGroup,
    AbstractScoutsFunction,
    ScoutsFunction,
)
from scouts_auth.groupadmin.services import ScoutsGroupService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunctionService:
    scouts_group_service = ScoutsGroupService()

    def create_or_update_scouts_functions(
        self, user: settings.AUTH_USER_MODEL
    ) -> List[ScoutsFunction]:
        for abstract_function in user.functions:
            for abstract_group in abstract_function.scouts_groups:
                scouts_function: ScoutsFunction = self.create_or_update_scouts_function(
                    user=user,
                    abstract_function=abstract_function,
                    abstract_group=abstract_group,
                )

        return user.persisted_scouts_functions.all()

    def create_or_update_scouts_function(
        self,
        user: settings.AUTH_USER_MODEL,
        abstract_function: AbstractScoutsFunction,
        abstract_group: AbstractScoutsGroup,
    ) -> ScoutsFunction:
        scouts_function: ScoutsFunction = ScoutsFunction.objects.safe_get(
            group_admin_id=abstract_function.group_admin_id,
            code=abstract_function.code,
            group_group_admin_id=abstract_group.group_admin_id,
        )

        # for user_function in user.functions:
        #     for function in functions:
        #         if function.group_admin_id == user_function.function:
        #             for grouping in function.groupings:
        #                 if (
        #                     grouping.name
        #                     == GroupadminSettings.get_section_leader_identifier()
        #                 ):
        #                     logger.debug(
        #                         "Setting user as section leader for group %s",
        #                         user_function.scouts_group.group_admin_id,
        #                     )
        #                     user_function.groups_section_leader[
        #                         user_function.scouts_group.group_admin_id
        #                     ] = True

        # user.full_clean()
        # user.save()

        if scouts_function:
            if abstract_function.end and (
                not scouts_function.end or abstract_function.end != scouts_function.end
            ):
                scouts_function: ScoutsFunction = self.update_scouts_function(
                    updated_by=user,
                    scouts_function=scouts_function,
                    abstract_function=abstract_function,
                    abstract_group=abstract_group,
                )
        else:
            scouts_function: ScoutsFunction = self.create_scouts_function(
                created_by=user,
                abstract_function=abstract_function,
                abstract_group=abstract_group,
            )
            user.persisted_scouts_functions.add(scouts_function)

        return scouts_function

    def create_scouts_function(
        self,
        created_by: settings.AUTH_USER_MODEL,
        abstract_function: AbstractScoutsFunction,
        abstract_group: AbstractScoutsGroup,
    ) -> ScoutsFunction:
        logger.debug(
            "Creating scouts function with group_admin_id %s and code %s for group %s",
            abstract_function.group_admin_id,
            abstract_function.code,
            abstract_group.group_admin_id,
        )

        scouts_group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=abstract_group.group_admin_id
        )
        if not scouts_group:
            # User has a function in a group that isn't the user's group list anymore
            scouts_group: ScoutsGroup = self.scouts_group_service.create_scouts_group(
                created_by=created_by, group_admin_id=abstract_group.group_admin_id
            )

        scouts_function: ScoutsFunction = ScoutsFunction()

        scouts_function.group_admin_id = abstract_function.group_admin_id
        scouts_function.code = abstract_function.code if abstract_function.code else ""
        scouts_function.type = abstract_function.type if abstract_function.type else ""
        scouts_function.description = (
            abstract_function.description if abstract_function.description else ""
        )
        scouts_function.group = scouts_group
        scouts_function.begin = (
            abstract_function.begin if abstract_function.begin else None
        )
        scouts_function.end = abstract_function.end if abstract_function.end else None
        scouts_function.created_by = created_by

        scouts_function.full_clean()
        scouts_function.save()

        return scouts_function

    def update_scouts_function(
        self,
        updated_by: settings.AUTH_USER_MODEL,
        scouts_function: ScoutsFunction,
        abstract_function: AbstractScoutsFunction,
        abstract_group: AbstractScoutsGroup,
    ) -> ScoutsFunction:
        logger.debug(
            "Updating scouts function with group_admin_id %s and code %s for group %s (existing function end date: %s - abstract function end date: %s",
            abstract_function.group_admin_id,
            abstract_function.code,
            abstract_group.group_admin_id,
            scouts_function.end,
            abstract_function.end,
        )
        scouts_function.group_admin_id = (
            abstract_function.group_admin_id
            if abstract_function.group_admin_id
            else scouts_function.group_admin_id
        )
        scouts_function.code = (
            abstract_function.code if abstract_function.code else scouts_function.code
        )
        scouts_function.type = (
            abstract_function.type if abstract_function.type else scouts_function.type
        )
        scouts_function.description = (
            abstract_function.description
            if abstract_function.description
            else scouts_function.description
        )
        scouts_function.begin = (
            abstract_function.begin
            if abstract_function.begin
            else scouts_function.begin
        )
        scouts_function.end = (
            abstract_function.end if abstract_function.end else scouts_function.end
        )
        scouts_function.updated_by = updated_by

        scouts_function.full_clean()
        scouts_function.save()

        return scouts_function
