import logging
from django.db.models import Q

from ..models import (
    ScoutsSectionName,
    ScoutsGroup,
    ScoutsSection,
)


logger = logging.getLogger(__name__)


class ScoutsSectionService:
    
    def create(self,
            group: ScoutsGroup,
            name: ScoutsSectionName,
            hidden=False):
        instance = ScoutsSection()

        instance.group = group
        instance.name = name
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance
