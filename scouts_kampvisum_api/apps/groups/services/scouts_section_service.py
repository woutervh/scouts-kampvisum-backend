import warnings
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.groups.models import (
    DefaultScoutsSectionName,
    ScoutsGroupType,
    ScoutsSectionName,
    ScoutsSection,
)
from apps.groups.services import (
    DefaultScoutsSectionNameService,
    ScoutsSectionNameService,
)

from scouts_auth.groupadmin.models import AbstractScoutsGroup, ScoutsGroup
from scouts_auth.groupadmin.services import GroupAdmin

from scouts_auth.inuits.models import Gender


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionService:

    groupadmin = GroupAdmin()
    default_section_name_service = DefaultScoutsSectionNameService()
    section_name_service = ScoutsSectionNameService()

    def section_create_or_update(
        self,
        request=None,
        instance: ScoutsSection = None,
        group: ScoutsGroup = None,
        section_name: ScoutsSectionName = None,
        name: str = None,
        gender: Gender = Gender.MIXED,
        age_group: int = 0,
        hidden: bool = False,
    ) -> ScoutsSection:
        """
        Creates or updates a ScoutsSection instance.
        """
        self.fix_92074(request=request, group=group)

        if instance is None:
            instance = ScoutsSection.objects.safe_get(
                group=group, name=name, gender=gender, age_group=age_group
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
            self.fix_92074(request=request, group=group)
            if group.default_sections_loaded:
                logger.debug(
                    "Default sections for group %s already loaded (%d section(s))",
                    group.group_admin_id,
                    group.sections.count(),
                )
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
                    default_name.name.name,
                    group.group_admin_id,
                )
                created_sections.append(
                    self.section_create_or_update(
                        request=request,
                        group=group,
                        name=default_name.name.name,
                        gender=default_name.name.gender,
                        age_group=default_name.name.age_group,
                        hidden=default_name.name.hidden,
                    )
                )

            if len(created_sections) == 0:
                raise ValidationError("Attempted to create sections, but failed")

            group.default_sections_loaded = True
            group.full_clean()
            group.save()

        return created_sections

    def fix_92074(self, request, group: ScoutsGroup):
        # fix for https://redmine.inuits.eu/issues/92074 for groups that were already registered
        group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=group.group_admin_id
        )
        if group.default_sections_loaded:
            sections: List[ScoutsSection] = group.sections.all()

            for section in sections:
                section_name = section.section_name
                if section.name:
                    section_name = ScoutsSectionName.objects.safe_get(id=section.name)
                # logger.debug("SECTION NAME: %s (%s)", section.name, section_name)

                if not (section.name and section.gender and section.age_group):
                    logger.debug(
                        "Fixing #92074 for group %s and section %s",
                        group.group_admin_id,
                        section_name.name,
                        user=request.user,
                    )
                    section.name = section_name.name
                    section.gender = section_name.gender
                    section.age_group = section_name.age_group

                    section.full_clean()
                    section.save()
