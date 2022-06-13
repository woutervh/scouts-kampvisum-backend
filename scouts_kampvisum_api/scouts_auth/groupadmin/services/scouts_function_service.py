from typing import List

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import (
    AbstractScoutsGroup,
    ScoutsGroup,
    AbstractScoutsFunctionDescription,
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

    def create_or_update_scouts_functions_for_user(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        # logger.debug("PRESENT FUNCTIONS: %s", user.functions, user=user)
        abstract_function_descriptions: List[
            AbstractScoutsFunctionDescription
        ] = self.groupadmin.get_function_descriptions(
            active_user=user
        ).function_descriptions
        unique_function_descriptions = {}
        unique_function_descriptions_list = []

        for abstract_function_description in abstract_function_descriptions:
            if abstract_function_description.description not in unique_function_descriptions or abstract_function_description.end is None:
                unique_function_descriptions[abstract_function_description.description] = abstract_function_description
                unique_function_descriptions_list.append(abstract_function_description)

        user.function_descriptions = unique_function_descriptions_list

        for abstract_function in user.functions:
            for key in unique_function_descriptions.keys():
                if (
                    unique_function_descriptions[key].group_admin_id
                    == abstract_function.function
                ):

                    scouts_function: ScoutsFunction = (
                        self.create_or_update_scouts_function(
                            user=user,
                            abstract_function=abstract_function,
                            abstract_function_description=unique_function_descriptions[key],
                            abstract_scouts_groups=[abstract_function.scouts_group],
                        )
                    )

        return user

    def create_or_update_scouts_function(
        self,
        user: settings.AUTH_USER_MODEL,
        abstract_function: AbstractScoutsFunction,
        abstract_function_description: AbstractScoutsFunctionDescription,
        abstract_scouts_groups: List[AbstractScoutsGroup],
    ) -> ScoutsFunction:
        scouts_function: ScoutsFunction = ScoutsFunction.objects.safe_get(
            user=user,
            group_admin_id=abstract_function_description.group_admin_id,
        )

        if scouts_function:
            scouts_function: ScoutsFunction = self.update_scouts_function(
                updated_by=user,
                instance=scouts_function,
                abstract_function=abstract_function,
                abstract_function_description=abstract_function_description,
                abstract_scouts_groups=abstract_scouts_groups,
            )
        else:
            scouts_function: ScoutsFunction = self.create_scouts_function(
                created_by=user,
                abstract_function=abstract_function,
                abstract_function_description=abstract_function_description,
                abstract_scouts_groups=abstract_scouts_groups,
            )

        user.persisted_scouts_functions.add(scouts_function)

        return scouts_function

    @transaction.atomic
    def create_scouts_function(
        self,
        created_by: settings.AUTH_USER_MODEL,
        abstract_function: AbstractScoutsFunction,
        abstract_function_description: AbstractScoutsFunctionDescription,
        abstract_scouts_groups: List[AbstractScoutsGroup],
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
        name = abstract_function_description.get_groupings_name() if abstract_function_description.get_groupings_name() else ""
        begin = abstract_function.begin if abstract_function.begin else None
        end = abstract_function.end if abstract_function.end else None

        # logger.debug(
        #     "Creating scouts function with group_admin_id %s and code %s for groups %s",
        #     group_admin_id,
        #     code,
        #     ", ".join(
        #         abstract_scouts_group.group_admin_id
        #         for abstract_scouts_group in abstract_scouts_groups
        #     ),
        # )

        scouts_function: ScoutsFunction = ScoutsFunction()

        scouts_function.user = created_by
        scouts_function.group_admin_id = group_admin_id
        scouts_function.code = code
        scouts_function.type = type
        scouts_function.description = description
        scouts_function.name = name
        scouts_function.begin = begin
        scouts_function.end = end
        scouts_function.created_by = created_by

        scouts_function.full_clean()
        scouts_function.save()

        self.set_groups_for_function(
            instance=scouts_function, abstract_scouts_groups=abstract_scouts_groups
        )

        return scouts_function

    @transaction.atomic
    def update_scouts_function(
        self,
        updated_by: settings.AUTH_USER_MODEL,
        instance: ScoutsFunction,
        abstract_function: AbstractScoutsFunction,
        abstract_function_description: AbstractScoutsFunctionDescription,
        abstract_scouts_groups: List[AbstractScoutsGroup],
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
        name = (
            abstract_function_description.get_groupings_name()
            if abstract_function_description.get_groupings_name()
            else ""
        )
        begin = (
            abstract_function_description.begin
            if abstract_function_description.begin
            else abstract_function.begin
            if abstract_function.begin
            else instance.begin
        )

        # if abstract_function.end and (
        #     not instance.end or abstract_function.end != instance.end
        # ):
        #     logger.debug(
        #         "Not updating ScoutsFunction %s (%s, %s), no end date or end date already set (%s)",
        #         instance.id,
        #         instance.code,
        #         instance.description,
        #         instance.end,
        #     )

        # logger.debug(
        #     "Updating scouts function with group_admin_id %s and code %s for group %s (existing function end date: %s - abstract function end date: %s)",
        #     group_admin_id,
        #     code,
        #     group_admin_id,
        #     instance.end,
        #     end,
        # )

        instance.group_admin_id = group_admin_id
        instance.code = code
        instance.type = type
        instance.description = description
        instance.name = name
        instance.begin = begin
        instance.end = abstract_function.end if abstract_function.end else None
        instance.updated_by = updated_by

        instance.full_clean()
        instance.save()

        self.set_groups_for_function(
            instance=instance, abstract_scouts_groups=abstract_scouts_groups
        )

        return instance

    @transaction.atomic
    def set_groups_for_function(
        self,
        instance: ScoutsFunction,
        abstract_scouts_groups: List[AbstractScoutsGroup],
    ):
        for abstract_scouts_group in abstract_scouts_groups:
            scouts_group: ScoutsGroup = ScoutsGroup.objects.safe_get(
                group_admin_id=abstract_scouts_group.group_admin_id
            )
            # Users can have a function in a group that they're no longer a member of.
            # If it's an inactive function, ignore, otherwise raise an exception
            if not scouts_group:
                if not instance.end:
                    raise ValidationError(
                        "Encountered an active ScoutsFunction %s (%s %s) for group %s and the user doesn't belong to that group".format(
                            instance.group_admin_id,
                            instance.code,
                            instance.description,
                            abstract_scouts_group.group_admin_id,
                        )
                    )
            else:
                instance.scouts_groups.add(scouts_group)
