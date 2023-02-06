from typing import List

from apps.groups.models import (
    DefaultScoutsSectionName,
    ScoutsSectionName,
    ScoutsGroupType,
)

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.inuits.models import Gender


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultScoutsSectionNameService:

    def load_for_group(
        self, request, group: ScoutsGroup
    ) -> List[DefaultScoutsSectionName]:
        """
        Loads default names based on group type or the parent group type.
        """
        group_type = ScoutsGroupType.objects.safe_get(
            group_type=group.type, is_default=True, raise_error=True
        )
        logger.debug(
            f"Loading DefaultScoutsSectionName instances for group {group.group_admin_id} (group_type {group_type.group_type})")
        names: List[
            DefaultScoutsSectionName
        ] = DefaultScoutsSectionName.objects.safe_get_list(
            group_type=group_type, gender=group.gender
        )

        if not names or names.count() == 0:
            names: List[
                DefaultScoutsSectionName
            ] = DefaultScoutsSectionName.objects.safe_get_list(
                group_type=group_type.parent, gender=group.gender
            )

        return names

    def load_name_for_group(
        self, request, group: str, gender: Gender, age_group: int
    ) -> DefaultScoutsSectionName:
        """
        Load the default name based on group type or the parent group type.
        """
        group_type = ScoutsGroupType.objects.safe_get(
            group_type=group.type, is_default=True, raise_error=True
        )
        # logger.debug(
        #     "Loading DefaultScoutsSectionName instances for group %s (group_type '%s')",
        #     group.group_admin_id,
        #     group_type.group_type,
        # )
        name: DefaultScoutsSectionName = DefaultScoutsSectionName.objects.safe_get(
            group_type=group_type, gender=gender, age_group=age_group
        )

        if not name:
            name: DefaultScoutsSectionName = DefaultScoutsSectionName.objects.safe_get(
                group_type=group_type.parent,
                name=name,
                gender=gender,
                age_group=age_group,
            )

        return name
