from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import AbstractScoutsGroup, ScoutsGroup
from scouts_auth.groupadmin.services import GroupAdmin


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupService:

    groupadmin = GroupAdmin()

    def create_or_update_scouts_groups_for_user(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        abstract_groups: List[AbstractScoutsGroup] = self.groupadmin.get_groups(
            active_user=user
        ).scouts_groups
        user.scouts_groups = abstract_groups

        logger.debug(
            "SCOUTS GROUP SERVICE: Found %d groups(s) for user %s",
            len(abstract_groups),
            user.username,
            user=user,
        )

        self.create_or_update_scouts_groups(user=user)

        return user

    def create_or_update_scouts_groups(
        self, user: settings.AUTH_USER_MODEL
    ) -> List[ScoutsGroup]:
        for abstract_group in user.scouts_groups:
            scouts_group: ScoutsGroup = self.create_or_update_scouts_group(
                user=user, abstract_group=abstract_group
            )
            logger.debug(f"Created scouts group {scouts_group.group_admin_id}")

            user.add_group(scouts_group)
            logger.debug(f"Added scouts group {scouts_group.group_admin_id} for user {user.username}")

        return user.persisted_scouts_groups

    def create_or_update_scouts_group(
        self, user: settings.AUTH_USER_MODEL, abstract_group: AbstractScoutsGroup
    ) -> ScoutsGroup:
        scouts_group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=abstract_group.group_admin_id
        )

        if scouts_group:
            return self.update_scouts_group(
                updated_by=user,
                scouts_group=scouts_group,
                abstract_group=abstract_group,
            )
        else:
            return self.create_scouts_group(
                created_by=user, abstract_group=abstract_group
            )

    def create_scouts_group(
        self,
        created_by: settings.AUTH_USER_MODEL,
        abstract_group: AbstractScoutsGroup = None,
        group_admin_id=None,
    ) -> ScoutsGroup:
        if not abstract_group:
            if not group_admin_id:
                raise ValidationError(
                    "Can't load scouts group from GroupAdmin without a group_admin_id"
                )
            abstract_group: AbstractScoutsGroup = self.groupadmin.get_group(
                active_user=created_by, group_group_admin_id=group_admin_id
            )

        logger.debug(
            "Creating scouts group with group_admin_id %s and name %s",
            abstract_group.group_admin_id,
            abstract_group.name,
        )

        scouts_group: ScoutsGroup = ScoutsGroup.from_abstract_scouts_group(
            abstract_group=abstract_group
        )

        scouts_group.created_by = created_by

        scouts_group.full_clean()
        scouts_group.save()

        return scouts_group

    def update_scouts_group(
        self,
        updated_by: settings.AUTH_USER_MODEL,
        scouts_group: ScoutsGroup,
        abstract_group: AbstractScoutsGroup,
    ) -> ScoutsGroup:
        if not scouts_group.equals_abstract_scouts_group(abstract_group):
            logger.debug(
                "Updating scouts group with group_admin_id %s and name %s",
                abstract_group.group_admin_id,
                abstract_group.name,
            )

            scouts_group.group_admin_id = (
                abstract_group.group_admin_id
                if abstract_group.group_admin_id
                else scouts_group.group_admin_id
            )
            scouts_group.number = (
                abstract_group.number if abstract_group.number else scouts_group.number
            )
            scouts_group.name = (
                abstract_group.name if abstract_group.name else scouts_group.name
            )
            scouts_group.group_type = (
                abstract_group.type if abstract_group.type else scouts_group.group_type
            )
            scouts_group.updated_by = updated_by

            scouts_group.full_clean()
            scouts_group.save()

        return scouts_group
