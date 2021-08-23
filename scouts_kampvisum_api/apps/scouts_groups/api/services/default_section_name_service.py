import logging
from django.db.models import Q

from ..models import ScoutsDefaultSectionName


logger = logging.getLogger(__name__)


class ScoutsDefaultSectionNameService:
    
    def load_for_type(self, type):
        return ScoutsDefaultSectionName.objects.filter(
            Q(type=type) | Q(type__parent=type)
        )

