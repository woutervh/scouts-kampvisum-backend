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

from scouts_auth.groupadmin.models import AbstractScoutsGroup
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
        group_group_admin_id: str = None,
        name: ScoutsSectionName = None,
        hidden: bool = False,
    ) -> ScoutsSection:
        """
        Creates or updates a ScoutsSection instance.
        """
        if not user:
            user = request.user

        scouts_group = self.group_admin.get_group(
            active_user=user, group_group_admin_id=group_group_admin_id
        )
        if not scouts_group:
            raise ValidationError(
                "Invalid group admin id {} for scouts group".format(
                    group_group_admin_id
                )
            )
        logger.debug(
            "GROUP ('%s'), NAME ('%s'), HIDDEN: %s",
            scouts_group.name,
            name.name,
            hidden,
        )

        name_instance = ScoutsSectionName.objects.safe_get(
            id=name.id, name=name.name, gender=name.gender, age_group=name.age_group
        )

        logger.debug(
            "Querying existing ScoutsSection instances with group admin id %s and name %s (%s)",
            scouts_group.group_admin_id,
            name,
            type(name).__name__,
        )
        if name_instance is None:
            qs = ScoutsSection.objects.filter(
                group_group_admin_id=scouts_group.group_admin_id, name__name=name
            )
        else:
            qs = ScoutsSection.objects.filter(
                group_group_admin_id=scouts_group.group_admin_id, name=name
            )
        count = qs.count()

        if count > 0:
            warnings.warn("Attempted to create or update multiple objects")
            return None

        if count == 0:
            logger.debug("Creating ScoutsSection with name '%s'", name)
            return self._section_create(request, user, scouts_group, name, hidden)
        if count == 1:
            instance = qs[0]
            logger.debug("Updating ScoutsSection with name '%s'", instance.name.name)
            return self._section_update(
                request, user, instance, scouts_group, name, hidden
            )

    def _section_create(
        self,
        request=None,
        user: settings.AUTH_USER_MODEL = None,
        group: AbstractScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden: bool = False,
    ) -> ScoutsSection:
        if not user:
            user = request.user

        instance = ScoutsSection()

        instance.group_group_admin_id = group.group_admin_id
        instance.name = self.section_name_service.get_or_create_name(
            request=request, section_name=name
        )
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def update_section(self, request, instance: ScoutsSection, **data) -> ScoutsSection:
        # logger.debug("SCOUTS SECTION SERVICE UPDATE DATA: %s", data)
        group_group_admin_id = data.get(
            "group_group_admin_id", instance.group_group_admin_id
        )
        name = self.section_name_service.update_name(
            request,
            instance=ScoutsSectionName.objects.safe_get(
                id=data.get("name").id, raise_error=True
            ),
            updated_instance=data.get("name"),
        )

        instance = ScoutsSection.objects.safe_get(
            id=instance.id, group_group_admin_id=group_group_admin_id, name=name
        )

        instance.group_group_admin_id = group_group_admin_id
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
        group: AbstractScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden=False,
    ) -> ScoutsSection:
        """
        Updates an existing Section instance.
        """
        if not user:
            user = request.user

        logger.debug("Updating Section with name '%s'", instance.name.name)

        instance.group_group_admin_id = group.group_admin_id
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

        groups = user.scouts_groups
        created_sections = list()

        for group in groups:
            logger.debug(
                "Linking sections to GROUP: %s (%s)", group.group_admin_id, group.name
            )

            sections = ScoutsSection.objects.all().filter(
                group_group_admin_id=group.group_admin_id
            )

            # @TODO update if necessary
            logger.debug(
                "Found %d SECTIONS to link to group %ss", sections.count(), group.name
            )
            if sections.count() == 0:
                group_type = ScoutsGroupType.objects.get(group_type=group.type)
                default_scouts_section_names: List[
                    DefaultScoutsSectionName
                ] = self.default_section_name_service.load_for_type(request, group_type)

                logger.debug(
                    "Found %d default section NAMES", len(default_scouts_section_names)
                )
                for name in default_scouts_section_names:
                    logger.debug("Linking section NAME: %s", name.name)
                    created_sections.append(
                        self.section_create_or_update(
                            request=request,
                            user=user,
                            group_group_admin_id=group.group_admin_id,
                            name=name.name,
                            hidden=name.name.hidden,
                        )
                    )

        return created_sections
