import logging

from apps.groups.models import ScoutsSectionName

from scouts_auth.groupadmin.scouts import AgeGroup
from scouts_auth.inuits.models import Gender


logger = logging.getLogger(__name__)


class ScoutsSectionNameService:
    def name_get(self, request, name: str) -> ScoutsSectionName:
        """
        Retrieves a SectionName instance based on the name.
        """
        logger.debug("Retrieving ScoutsSectionName with name %s", name)
        qs = ScoutsSectionName.objects.filter(name=name).values_list()
        count = qs.count()

        if count == 0:
            return None
        if count == 1:
            return qs[0]

        return list(qs)

    def name_create(
        self,
        request,
        name: str,
        gender=Gender.MIXED,
        age_group=AgeGroup.AGE_GROUP_UNKNOWN,
    ) -> ScoutsSectionName:
        """
        Saves a SectionName object to the DB.
        """

        instance = ScoutsSectionName(name=name, gender=gender, age_group=age_group)

        instance.full_clean()
        instance.save()

        return instance

    def name_update(
        self, request, instance: ScoutsSectionName, **fields
    ) -> ScoutsSectionName:
        """
        Updates an existing SectionName object in the DB.
        """

        instance.name = fields.get("name", instance.name)
        instance.gender = fields.get("gender", instance.gender)
        instance.age_group = fields.get("age_group", instance.age_group)

        instance.full_clean()
        instance.save()

        return instance
