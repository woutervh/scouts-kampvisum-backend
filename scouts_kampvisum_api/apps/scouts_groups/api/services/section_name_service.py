import logging
from django.db.models import Q

from ..models import ScoutsSectionName


logger = logging.getLogger(__name__)


class ScoutsSectionNameService:
    def name_create(self, *, name, gender, age_group) -> ScoutsSectionName:
        """
        Saves a ScoutsSectionName object to the DB.
        """
        
        instance = ScoutsSectionName(
            name=name,
            gender=gender,
            age_group=age_group
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
        instance.gender = fields.get('gender', instance.gender)
        instance.age_group = fields.get('age_group', instance.age_group)
        
        instance.full_clean()
        instance.save()
        
        return instance

