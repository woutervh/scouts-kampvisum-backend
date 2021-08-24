import logging
from django.db.models import Q

from ..models import ScoutsDefaultSectionName


logger = logging.getLogger(__name__)


class ScoutsDefaultSectionNameService:
    
    def load_for_type(self, type):
        """
        Loads default names based on group type or the parent group type.
        """
        logger.debug(
            "Loading ScoutsDefaultSectionName instances for type '%s'",
            type.type)
        return ScoutsDefaultSectionName.objects.filter(
            Q(type=type) | Q(type__parent=type)).distinct()

