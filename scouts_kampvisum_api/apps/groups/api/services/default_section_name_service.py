import logging
from django.db.models import Q

from ..models import DefaultSectionName


logger = logging.getLogger(__name__)


class DefaultSectionNameService:
    def load_for_type(self, type):
        """
        Loads default names based on group type or the parent group type.
        """
        logger.debug("Loading DefaultSectionName instances for type '%s'", type.type)
        return DefaultSectionName.objects.filter(
            Q(type=type) | Q(type__parent=type)
        ).distinct()
