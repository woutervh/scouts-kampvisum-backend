import logging
import warnings
from django.shortcuts import get_object_or_404

from apps.groups.models import (
    ScoutsSectionName,
    ScoutsSection,
)
from apps.groups.services import ScoutsSectionNameService

from scouts_auth.groupadmin.models import AbstractScoutsGroup


logger = logging.getLogger(__name__)


class ScoutsSectionService:

    section_name_service = ScoutsSectionNameService()

    def section_create_or_update(
        self, group=None, name=None, hidden=False, **fields
    ) -> ScoutsSection:
        """
        Creates or updates a ScoutsSection instance.
        """
        logger.debug(
            "GROUP ('%s'), NAME ('%s'), HIDDEN: %s", group.name, name.name, hidden
        )
        if not isinstance(group, AbstractScoutsGroup):
            from ..services import ScoutsGroupService

            group = ScoutsGroupService().get_group(group)

        name_instance = None
        if not isinstance(name, ScoutsSectionName):
            name_instance = self.section_name_service.name_get(name=name)

        if name_instance is None:
            qs = ScoutsSection.objects.filter(group=group, name__name=name)
        else:
            qs = ScoutsSection.objects.filter(group=group, name=name)
        count = qs.count()

        if count > 0:
            warnings.warn("Attempted to create or update multiple objects")
            return None

        if count == 0:
            logger.debug("Creating ScoutsSection with name '%s'", name)
            return self._section_create(group, name, hidden, **fields)
        if count == 1:
            instance = qs[0]
            logger.debug("Updating ScoutsSection with name '%s'", instance.name.name)
            return self._section_update(instance, group, name, hidden, **fields)

    def _section_create(
        self, group=None, name=None, hidden=False, **fields
    ) -> ScoutsSection:
        if name is None or not isinstance(name, ScoutsSectionName):
            name = self.section_name_service.name_create(name=name)
        instance = ScoutsSection()

        instance.group = group
        instance.name = name
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def _section_update(
        self,
        instance: ScoutsSection,
        group: AbstractScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden=False,
        **fields
    ) -> ScoutsSection:
        """
        Updates an existing Section instance.
        """
        logger.debug("Updating Section with name '%s'", instance.name.name)

        instance.group = group
        instance.name = name
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def section_read(self, *args, **fields) -> ScoutsSection:
        """
        Retrieves a Section by uuid or SectionName.

        If uuid or name are lists, then lists will be returned.
        If uuid is None, then the group argument must be presented.
        """
        group = fields.get("group", None)
        uuid = fields.get("uuid", None)
        name = fields.get("name", None)

        logger.debug("SECTION FIELDS: %s", fields)

        if uuid is None and name is None:
            return ScoutsSection.objects.all()

        if uuid is not None and not isinstance(uuid, dict):
            if isinstance(uuid, list):
                return list(ScoutsSection.objects.filter(uuid__in=uuid).values_list())

            if isinstance(uuid, uuid.UUID):
                return get_object_or_404(ScoutsSection, uuid=uuid)

        if name is not None and not isinstance(name, dict):
            if isinstance(name, list):
                return list(
                    ScoutsSection.objects.filter(
                        group=group, name__name__in=name
                    ).values_list()
                )

            if isinstance(name, str):
                return list(ScoutsSection.objects.filter(group=group, name__name=name))

        logger.debug("No Section instances found with the given args")

        return None
