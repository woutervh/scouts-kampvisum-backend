from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.groups.models import (
    DefaultScoutsSectionName,
    ScoutsSection,
)
from apps.groups.services import DefaultScoutsSectionNameService

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.groupadmin.services import GroupAdmin

from scouts_auth.inuits.models import Gender


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionService:

    groupadmin = GroupAdmin()
    default_section_name_service = DefaultScoutsSectionNameService()

    def section_create_or_update(
        self,
        request=None,
        instance: ScoutsSection = None,
        group: ScoutsGroup = None,
        name: str = None,
        gender: Gender = Gender.MIXED,
        age_group: int = 0,
        hidden: bool = False,
        section: ScoutsSection = None,
    ) -> ScoutsSection:
        """
        Creates or updates a ScoutsSection instance.
        """
        if section:
            group = section.group
            name = section.name
            gender = section.gender
            age_group = section.age_group
            hidden = section.hidden

        if instance is None:
            instance = ScoutsSection.objects.safe_get(
                group=group,
                name=name,
                gender=gender,
                age_group=age_group,
            )

        if instance is None:
            return self._section_create(
                request=request,
                group=group,
                name=name,
                gender=gender,
                age_group=age_group,
                hidden=hidden,
            )
        else:
            return self._section_update(
                request=request,
                instance=instance,
                group=group,
                name=name,
                gender=gender,
                age_group=age_group,
                hidden=hidden,
            )

    def _section_create(
        self,
        request=None,
        group: ScoutsGroup = None,
        name: str = None,
        gender: Gender = Gender.MIXED,
        age_group: int = 0,
        hidden: bool = False,
    ) -> ScoutsSection:
        logger.debug(
            "Creating a ScoutsSection with name '%s', gender %s and age_group %s for group %s",
            name,
            gender,
            age_group,
            group.group_admin_id,
            user=request.user,
        )

        instance = ScoutsSection()

        instance.group = group
        instance.name = name
        instance.gender = gender
        instance.age_group = age_group
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def _section_update(
        self,
        request=None,
        instance: ScoutsSection = None,
        group: ScoutsGroup = None,
        name: str = None,
        gender: Gender = None,
        age_group: int = None,
        hidden=False,
    ) -> ScoutsSection:
        """
        Updates an existing Section instance.
        """
        name = name if name else instance.name
        gender = gender if gender else instance.gender
        age_group = age_group if age_group else instance.age_group

        logger.debug(
            "Updating Section with name '%s', gender %s and age_group %s in group %s",
            name,
            gender,
            age_group,
            group.group_admin_id,
            user=request.user,
        )

        instance.group = group
        instance.name = name
        instance.gender = gender
        instance.age_group = age_group
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def setup_default_sections(
        self, request=None, user: settings.AUTH_USER_MODEL = None
    ):
        """
        Links default sections to a group.
        """
        if not user:
            user = request.user

        groups: List[ScoutsGroup] = user.persisted_scouts_groups.all()
        created_sections = list()

        for group in groups:
            if group.default_sections_loaded:
                # logger.debug(
                #     "Default sections for group %s already loaded (%d section(s))",
                #     group.group_admin_id,
                #     group.sections.count(),
                # )
                continue

            logger.debug(
                "Linking sections to GROUP: %s (%s)",
                group.group_admin_id,
                group.name,
            )
            default_scouts_section_names: List[
                DefaultScoutsSectionName
            ] = self.default_section_name_service.load_for_group(
                request=request, group=group
            )

            if len(default_scouts_section_names) == 0:
                raise ValidationError(
                    "No DefaultScoutsSectionName instances found for group_type {}".format(
                        group.group_type
                    )
                )
            for default_name in default_scouts_section_names:
                logger.debug(
                    "Linking DefaultSectionName %s to group %s",
                    default_name.name,
                    group.group_admin_id,
                )
                created_sections.append(
                    self.section_create_or_update(
                        request=request,
                        group=group,
                        name=default_name.name,
                        gender=default_name.gender,
                        age_group=default_name.age_group,
                        hidden=default_name.hidden,
                    )
                )

            if len(created_sections) == 0:
                raise ValidationError("Attempted to create sections, but failed")

            group.default_sections_loaded = True
            group.full_clean()
            group.save()

        return created_sections
