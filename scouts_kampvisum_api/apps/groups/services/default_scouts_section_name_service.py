import logging
from typing import List

from django.db.models import Q

from apps.groups.models import DefaultScoutsSectionName


logger = logging.getLogger(__name__)


class DefaultScoutsSectionNameService:
    def load_for_type(self, request, group_type: str) -> List[DefaultScoutsSectionName]:
        """
        Loads default names based on group type or the parent group type.
        """
        logger.debug(
            "Loading DefaultScoutsSectionName instances for type '%s'",
            group_type.group_type,
        )
        types = DefaultScoutsSectionName.objects.filter(
            group_type__group_type=group_type
        ).distinct()

        if not types or types.count() == 0:
            types = DefaultScoutsSectionName.objects.filter(
                group_type__parent__group_type=group_type
            ).distinct()

        return types
