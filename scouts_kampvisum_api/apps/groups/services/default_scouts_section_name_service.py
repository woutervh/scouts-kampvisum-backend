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
        types = DefaultScoutsSectionName.objects.filter(
            group_type=group_type
        ).distinct()

        if not types or types.count() == 0:
            types = DefaultScoutsSectionName.objects.filter(
                group_type__parent=group_type
            ).distinct()

        return types
