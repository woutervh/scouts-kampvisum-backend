import logging

from apps.groups.models import ScoutsSectionName

# from scouts_auth.groupadmin.scouts import AgeGroup
from scouts_auth.inuits.models import Gender


logger = logging.getLogger(__name__)


class ScoutsSectionNameService:
    def get_or_create_name(
        self,
        request,
        section_name: ScoutsSectionName = None,
        name: str = None,
        gender: Gender = Gender.MIXED,
        # age_group: AgeGroup = AgeGroup.AGE_GROUP_UNKNOWN,
        age_group: int = 0,
    ) -> ScoutsSectionName:
        """
        Saves a SectionName object to the DB.
        """
        if section_name and isinstance(section_name, ScoutsSectionName):
            name = section_name.name
            gender = section_name.gender
            age_group = section_name.age_group

            section_name = ScoutsSectionName.objects.safe_get(
                pk=section_name.id,
                name=name,
                gender=gender,
                age_group=age_group,
            )

        if section_name:
            return section_name

        instance = ScoutsSectionName(name=name, gender=gender, age_group=age_group)

        instance.full_clean()
        instance.save()

        return instance

    def update_name(
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
