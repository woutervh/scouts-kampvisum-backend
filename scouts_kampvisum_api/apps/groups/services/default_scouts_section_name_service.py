import logging
from django.db.models import Q

from apps.groups.models import DefaultScoutsSectionName


logger = logging.getLogger(__name__)


class DefaultScoutsSectionNameService:
    def load_for_type(self, type):
        """
        Loads default names based on group type or the parent group type.
        """
        logger.debug(
            "Loading DefaultScoutsSectionName instances for type '%s'", type.type
        )
        return DefaultScoutsSectionName.objects.filter(
            Q(type=type) | Q(type__parent=type)
        ).distinct()
