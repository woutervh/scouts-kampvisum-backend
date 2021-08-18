import logging
from django.db.models import Q

from ..groups.models import ScoutsGroup
from .models import ScoutsSection, ScoutsSectionName, ScoutsDefaultSectionName


logger = logging.getLogger(__name__)


class ScoutsSectionNameService:
    def name_create(self, *, name, gender) -> ScoutsSectionName:
        """
        Saves a ScoutsTroopName object to the DB.
        """
        
        instance = ScoutsSectionName(
            name = name,
            gender = gender
        )
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    def name_update(
            self, *,
            instance: ScoutsSectionName, **fields) -> ScoutsSectionName:
        """
        Updates an existing ScoutsSectionName object in the DB.
        """
        
        instance.name = fields.get('name', instance.name)
        
        instance.full_clean()
        instance.save()
        
        return instance


class ScoutsDefaultSectionNameService:
    
    def load_for_type(self, type):
        return ScoutsDefaultSectionName.objects.filter(
            Q(type=type) | Q(type__parent=type)
        )


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
