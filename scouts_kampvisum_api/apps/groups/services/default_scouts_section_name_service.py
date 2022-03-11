from typing import List

from apps.groups.models import DefaultScoutsSectionName, ScoutsGroupType


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultScoutsSectionNameService:
    def load_for_type(
        self, request, group_type: ScoutsGroupType
    ) -> List[DefaultScoutsSectionName]:
        """
        Loads default names based on group type or the parent group type.
        """
        logger.debug(
            "Loading DefaultScoutsSectionName instances for type '%s'",
            group_type.group_type,
        )
        names: List[
            DefaultScoutsSectionName
        ] = DefaultScoutsSectionName.objects.safe_get_list(group_type=group_type)

        if not names or names.count() == 0:
            names: List[
                DefaultScoutsSectionName
            ] = DefaultScoutsSectionName.objects.safe_get_list(
                group_type=group_type.parent
            )

        return names
