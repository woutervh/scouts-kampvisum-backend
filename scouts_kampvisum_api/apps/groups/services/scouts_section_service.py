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


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionService:

    group_admin = GroupAdmin()
    default_section_name_service = DefaultScoutsSectionNameService()
    section_name_service = ScoutsSectionNameService()

    def section_create_or_update(
        self,
        request=None,
        user: settings.AUTH_USER_MODEL = None,
        group: ScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden: bool = False,
    ) -> ScoutsSection:
        """
        Creates or updates a ScoutsSection instance.
        """
        if not user:
            user = request.user

        logger.debug(
            "Querying existing ScoutsSection instances with group admin id %s and name %s (%s)",
            group.group_admin_id,
            name,
            type(name).__name__,
        )
        name_instance = ScoutsSectionName.objects.safe_get(
            id=name.id, name=name.name, gender=name.gender, age_group=name.age_group
        )
        if name_instance is None:
            qs = ScoutsSection.objects.filter(group=group, name__name=name)
        else:
            qs = ScoutsSection.objects.filter(group=group, name=name_instance)
        count = qs.count()

        if count > 0:
            warnings.warn("Attempted to create or update multiple objects")
            return None

        if count == 0:
            logger.debug(
                "Creating ScoutsSection with name '%s' for group %s",
                name,
                group.group_admin_id,
            )
            return self._section_create(request, user, group, name, hidden)
        if count == 1:
            instance = qs[0]
            logger.debug(
                "Updating ScoutsSection with name '%s' for group %s",
                instance.name.name,
                group.group_admin_id,
            )
            return self._section_update(request, user, instance, group, name, hidden)

    def _section_create(
        self,
        request=None,
        user: settings.AUTH_USER_MODEL = None,
        group: ScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden: bool = False,
    ) -> ScoutsSection:
        if not user:
            user = request.user

        instance = ScoutsSection()

        instance.group = group
        instance.name = self.section_name_service.get_or_create_name(
            request=request, section_name=name
        )
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def update_section(self, request, instance: ScoutsSection, **data) -> ScoutsSection:
        logger.debug("SCOUTS SECTION SERVICE UPDATE DATA: %s", data)
        group: ScoutsGroup = data.get("group")
        name: ScoutsSectionName = self.section_name_service.update_name(
            request,
            instance=ScoutsSectionName.objects.safe_get(
                id=data.get("name").id, raise_error=True
            ),
            updated_instance=data.get("name"),
        )

        instance = ScoutsSection.objects.safe_get(
            id=instance.id, group=group, name=name
        )

        instance.group = group
        instance.name = name
        instance.hidden = data.get("hidden", instance.hidden)

        instance.full_clean()
        instance.save()

        return instance

    def _section_update(
        self,
        request=None,
        user: settings.AUTH_USER_MODEL = None,
        instance: ScoutsSection = None,
        group: ScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden=False,
    ) -> ScoutsSection:
        """
        Updates an existing Section instance.
        """
        if not user:
            user = request.user

        logger.debug("Updating Section with name '%s'", instance.name.name)

        instance.group = group
        instance.name = name
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
            user: settings.AUTH_USER_MODEL = request.user

        groups: List[ScoutsGroup] = user.persisted_scouts_groups.all()
        created_sections = list()

        for group in groups:
            if group.default_sections_loaded:
                logger.debug(
                    "Default sections for group %s already loaded (%d section(s))",
                    group.group_admin_id,
                    group.sections.count(),
                )
                return created_sections

            logger.debug(
                "Linking sections to GROUP: %s (%s)",
                group.group_admin_id,
                group.name,
            )
            group_type = ScoutsGroupType.objects.get(group_type=group.group_type)
            default_scouts_section_names: List[
                DefaultScoutsSectionName
            ] = self.default_section_name_service.load_for_type(request, group_type)

            logger.debug(
                "Found %d default section NAMES", len(default_scouts_section_names)
            )
            for name in default_scouts_section_names:
                logger.debug(
                    "Linking DefaultSectionName %s to group %s",
                    name.name,
                    group.group_admin_id,
                )
                created_sections.append(
                    self.section_create_or_update(
                        request=request,
                        user=user,
                        group=group,
                        name=name.name,
                        hidden=name.name.hidden,
                    )
                )

            group.default_sections_loaded = True
            group.full_clean()
            group.save()

        return created_sections
