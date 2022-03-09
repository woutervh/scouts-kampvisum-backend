from typing import List

from django.conf import settings

from scouts_auth.groupadmin.models import (
    AbstractScoutsGroup,
    ScoutsGroup,
    AbstractScoutsFunction,
    ScoutsFunction,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunctionService:
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

                user.persisted_scouts_functions.add(scouts_function)

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

        if scouts_function:
            return self.update_scouts_function(
                updated_by=user,
                scouts_function=scouts_function,
                abstract_function=abstract_function,
                abstract_group=abstract_group,
            )
        else:
            return self.create_scouts_function(
                created_by=user,
                abstract_function=abstract_function,
                abstract_group=abstract_group,
            )

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
            group_admin_id=abstract_group.group_admin_id, raise_error=True
        )

        scouts_function: ScoutsFunction = ScoutsFunction()

        scouts_function.group_admin_id = abstract_function.group_admin_id
        scouts_function.code = abstract_function.code
        scouts_function.type = abstract_function.type
        scouts_function.description = abstract_function.description
        scouts_function.group = scouts_group
        scouts_function.begin = abstract_function.begin
        scouts_function.end = abstract_function.end
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
            "Updating scouts function with group_admin_id %s and code %s for group %s",
            abstract_function.group_admin_id,
            abstract_function.code,
            abstract_group.group_admin_id,
        )

        if abstract_function.end and abstract_function.end != scouts_function.end:
            scouts_function.group_admin_id = (
                abstract_function.group_admin_id
                if abstract_function.group_admin_id
                else scouts_function.group_admin_id
            )
            scouts_function.code = (
                abstract_function.code
                if abstract_function.code
                else scouts_function.code
            )
            scouts_function.type = (
                abstract_function.type
                if abstract_function.type
                else scouts_function.type
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
