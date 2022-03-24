from typing import List

from django.conf import settings
from django.db import transaction

from scouts_auth.groupadmin.models import (
    AbstractScoutsGroup,
    ScoutsGroup,
    AbstractScoutsFunction,
    ScoutsFunction,
)
from scouts_auth.groupadmin.services import GroupAdmin, ScoutsGroupService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunctionService:

    groupadmin = GroupAdmin()
    scouts_group_service = ScoutsGroupService()

    @transaction.atomic
    def create_or_update_scouts_functions_for_user(
        self, user: settings.AUTH_USER_MODEL
    ):
        # logger.debug("PRESENT FUNCTIONS: %s", user.functions, user=user)
        abstract_function_descriptions: List[
            AbstractScoutsFunction
        ] = self.groupadmin.get_function_descriptions(active_user=user).functions
        user.function_descriptions = abstract_function_descriptions

        # for user_function in user.functions:
        #     logger.debug("FUNCTION: %s", user_function)

        logger.debug(
            "SCOUTS FUNCTION SERVICE: Found %d function(s) and %d function description(s)",
            len(user.functions),
            len(user.function_descriptions),
            user=user,
        )

        self.create_or_update_scouts_functions(
            user=user,
        )

        return user

    @transaction.atomic
    def create_or_update_scouts_functions(
        self,
        user: settings.AUTH_USER_MODEL,
        abstract_functions: List[AbstractScoutsFunction] = None,
        abstract_function_descriptions: List[AbstractScoutsFunction] = None,
    ) -> List[ScoutsFunction]:
        if not abstract_functions:
            abstract_functions = user.functions
        if not abstract_function_descriptions:
            abstract_function_descriptions = user.function_descriptions

        # for abstract_function_description in abstract_function_descriptions:
        #     logger.debug(
        #         "ABSTRACT FUNCTION DESCRIPTION: %s %s %s",
        #         abstract_function_description.group_admin_id,
        #         abstract_function_description.code,
        #         abstract_function_description.description,
        #     )

        # @TODO temporary fix: remove all existing scouts functions
        user.persisted_scouts_functions.clear()

        functions_without_description: List[AbstractScoutsFunction] = []
        for abstract_function in abstract_functions:
            for abstract_function_description in abstract_function_descriptions:
                if (
                    abstract_function_description.group_admin_id
                    == abstract_function.function
                ):
                    for abstract_group in abstract_function_description.scouts_groups:
                        scouts_function: ScoutsFunction = self.create_or_update_scouts_function(
                            user=user,
                            abstract_function=abstract_function,
                            abstract_function_description=abstract_function_description,
                            abstract_group=abstract_group,
                        )
                else:
                    if abstract_function.function not in [
                        function.function for function in functions_without_description
                    ]:
                        functions_without_description.append(abstract_function)

        # for function_without_description in functions_without_description:
        #     logger.debug(
        #         "NO FUNCTION DESCRIPTION FOR function %s %s %s %s",
        #         function_without_description.function,
        #         function_without_description.scouts_group.group_admin_id,
        #         function_without_description.code,
        #         function_without_description.description,
        #     )

        return user.persisted_scouts_functions.all()

    @transaction.atomic
    def create_or_update_scouts_function(
        self,
        user: settings.AUTH_USER_MODEL,
        abstract_function: AbstractScoutsFunction,
        abstract_function_description: AbstractScoutsFunction,
        abstract_group: AbstractScoutsGroup,
    ) -> ScoutsFunction:
        scouts_function: ScoutsFunction = ScoutsFunction.objects.safe_get(
            group_admin_id=abstract_function_description.group_admin_id,
            code=abstract_function_description.code,
            group_group_admin_id=abstract_group.group_admin_id,
            user=user,
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
                    instance=scouts_function,
                    abstract_function=abstract_function,
                    abstract_function_description=abstract_function_description,
                    abstract_group=abstract_group,
                )
        else:
            scouts_function: ScoutsFunction = self.create_scouts_function(
                created_by=user,
                abstract_function=abstract_function,
                abstract_function_description=abstract_function_description,
                abstract_group=abstract_group,
            )

        user.persisted_scouts_functions.add(scouts_function)

        return scouts_function

    @transaction.atomic
    def create_scouts_function(
        self,
        created_by: settings.AUTH_USER_MODEL,
        abstract_function: AbstractScoutsFunction,
        abstract_function_description: AbstractScoutsFunction,
        abstract_group: AbstractScoutsGroup,
    ) -> ScoutsFunction:
        group_admin_id = (
            abstract_function_description.group_admin_id
            if abstract_function_description.group_admin_id
            else abstract_function.function
            if abstract_function.function
            else ""
        )
        code = (
            abstract_function_description.code
            if abstract_function_description.code
            else abstract_function.code
            if abstract_function.code
            else ""
        )
        type = (
            abstract_function_description.type
            if abstract_function_description.type
            else abstract_function.type
            if abstract_function.type
            else ""
        )
        description = (
            abstract_function_description.description
            if abstract_function_description.description
            else abstract_function.description
            if abstract_function.description
            else ""
        )
        begin = abstract_function.begin if abstract_function.begin else None
        end = abstract_function.end if abstract_function.end else None

        scouts_group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=abstract_group.group_admin_id
        )
        if not scouts_group:
            # User has a function in a group that isn't the user's group list anymore
            scouts_group: ScoutsGroup = self.scouts_group_service.create_scouts_group(
                created_by=created_by, group_admin_id=abstract_group.group_admin_id
            )

        logger.debug(
            "Creating scouts function with group_admin_id %s and code %s for group %s",
            group_admin_id,
            code,
            scouts_group.group_admin_id,
        )

        scouts_function: ScoutsFunction = ScoutsFunction()

        scouts_function.group_admin_id = group_admin_id
        scouts_function.code = code
        scouts_function.type = type
        scouts_function.description = description
        scouts_function.group = scouts_group
        scouts_function.begin = begin
        scouts_function.end = end
        scouts_function.created_by = created_by

        scouts_function.full_clean()
        scouts_function.save()

        return scouts_function

    @transaction.atomic
    def update_scouts_function(
        self,
        updated_by: settings.AUTH_USER_MODEL,
        instance: ScoutsFunction,
        abstract_function: AbstractScoutsFunction,
        abstract_function_description: AbstractScoutsFunction,
        abstract_group: AbstractScoutsGroup,
    ) -> ScoutsFunction:
        group_admin_id = (
            abstract_function_description.group_admin_id
            if abstract_function_description.group_admin_id
            else abstract_function.function
            if abstract_function.function
            else instance.group_admin_id
        )
        code = (
            abstract_function_description.code
            if abstract_function_description.code
            else abstract_function.code
            if abstract_function.code
            else instance.code
        )
        type = (
            abstract_function_description.type
            if abstract_function_description.type
            else abstract_function.type
            if abstract_function.type
            else instance.type
        )
        description = (
            abstract_function_description.description
            if abstract_function_description.description
            else abstract_function.description
            if abstract_function.description
            else instance.description
        )
        begin = (
            abstract_function_description.begin
            if abstract_function_description.begin
            else abstract_function.begin
            if abstract_function.begin
            else instance.begin
        )
        end = abstract_function.end if abstract_function.end else instance.end

        logger.debug(
            "Updating scouts function with group_admin_id %s and code %s for group %s (existing function end date: %s - abstract function end date: %s",
            group_admin_id,
            code,
            group_admin_id,
            instance.end,
            end,
        )

        instance.group_admin_id = group_admin_id
        instance.code = code
        instance.type = type
        instance.description = description
        instance.begin = begin
        instance.end = abstract_function.end if abstract_function.end else instance.end
        instance.updated_by = updated_by

        instance.full_clean()
        instance.save()

        return instance
