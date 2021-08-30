import logging

from ..models import SectionName
from apps.groupadmin.api import MemberGender, AgeGroup


logger = logging.getLogger(__name__)


class SectionNameService:

    def name_get(self, name) -> SectionName:
        """
        Retrieves a SectionName instance based on the name.
        """
        qs = SectionName.objects.filter(name=name).values_list()
        count = qs.count()

        if count == 0:
            return None
        if count == 1:
            return qs[0]

        return list(qs)

    def name_create(self,
                    name,
                    gender=MemberGender.MIXED,
                    age_group=AgeGroup.AGE_GROUP_UNKNOWN, **fields) -> SectionName:
        """
        Saves a SectionName object to the DB.
        """

        instance = SectionName(
            name=name,
            gender=gender,
            age_group=age_group
        )

        instance.full_clean()
        instance.save()

        return instance

    def name_update(
            self, *,
            instance: SectionName, **fields) -> SectionName:
        """
        Updates an existing SectionName object in the DB.
        """

        instance.name = fields.get('name', instance.name)
        instance.gender = fields.get('gender', instance.gender)
        instance.age_group = fields.get('age_group', instance.age_group)

        instance.full_clean()
        instance.save()

        return instance
