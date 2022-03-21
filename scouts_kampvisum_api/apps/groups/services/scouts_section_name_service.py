from apps.groups.models import ScoutsSectionName

from scouts_auth.inuits.models import Gender


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionNameService:
    def create_or_update_name(
        self,
        request,
        instance: ScoutsSectionName = None,
        name: str = None,
        gender: Gender = Gender.MIXED,
        age_group: int = 0,
        hidden: bool = False,
    ):
        """Creates or updates a ScoutsSectionName."""
        if instance and isinstance(instance, ScoutsSectionName):
            instance = ScoutsSectionName.objects.safe_get(id=instance.id)

        if not instance:
            return self._create_name(
                request=request,
                name=name,
                gender=gender,
                age_group=age_group,
                hidden=hidden,
            )
        else:
            return self._update_name(
                request=request,
                instance=instance,
                updated_instance=ScoutsSectionName(
                    name=name, gender=gender, age_group=age_group, hidden=hidden
                ),
            )

    def _create_name(
        self,
        request,
        name: str = None,
        gender: Gender = Gender.MIXED,
        age_group: int = 0,
        hidden: bool = False,
    ) -> ScoutsSectionName:
        logger.debug(
            "Creating a ScoutsSectionName with name '%s', gender %s, age_group %s and hidden %s",
            name,
            gender,
            age_group,
            hidden,
            user=request.user,
        )

        instance = ScoutsSectionName()

        instance.name = name
        instance.gender = gender
        instance.age_group = age_group
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def _update_name(
        self,
        request,
        instance: ScoutsSectionName,
        updated_instance: ScoutsSectionName = None,
        **fields
    ) -> ScoutsSectionName:
        """
        Updates an existing SectionName object in the DB.
        """
        name = (
            updated_instance.name
            if updated_instance and updated_instance.name
            else fields.get("name", instance.name)
        )
        gender = (
            updated_instance.gender
            if updated_instance and updated_instance.gender
            else fields.get("gender", instance.gender)
        )
        age_group = (
            updated_instance.age_group
            if updated_instance and updated_instance.age_group
            else fields.get("age_group", instance.age_group)
        )
        hidden = updated_instance.hidden if updated_instance.hidden else instance.hidden

        logger.debug(
            "Updating ScoutsSectionName %s with name '%s', gender %s, age_group %s and hidden %s",
            instance.id,
            name,
            gender,
            age_group,
            hidden,
            user=request.user,
        )

        instance.name = name
        instance.gender = gender
        instance.age_group = age_group
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance
