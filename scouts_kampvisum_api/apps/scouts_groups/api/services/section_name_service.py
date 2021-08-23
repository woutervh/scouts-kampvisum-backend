import logging
from django.db.models import Q

from ..models import ScoutsSectionName


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

