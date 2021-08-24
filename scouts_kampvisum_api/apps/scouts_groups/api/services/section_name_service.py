import logging
from django.db.models import Q

from ..models import ScoutsSectionName
from apps.groupadmin.api import MemberGender, AgeGroup


logger = logging.getLogger(__name__)


class ScoutsSectionNameService:

    def name_get(self, name) -> ScoutsSectionName:
        """
        Retrieves a ScoutsSectionName instance based on the name.
        """
        qs = ScoutsSectionName.objects.filter(name=name).values_list()
        count = qs.count()

        if count == 0:
            return None
        if count == 1:
            return qs[0]
        
        return list(qs)

    def name_create(self,
        name,
        gender=MemberGender.MIXED,
        age_group=AgeGroup.AGE_GROUP_UNKNOWN, **fields) -> ScoutsSectionName:
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

