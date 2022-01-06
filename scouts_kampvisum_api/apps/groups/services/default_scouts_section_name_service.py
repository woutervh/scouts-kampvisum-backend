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
        return DefaultScoutsSectionName.objects.filter(
            Q(group_type=group_type) | Q(group_type__parent=group_type)
        ).distinct()
