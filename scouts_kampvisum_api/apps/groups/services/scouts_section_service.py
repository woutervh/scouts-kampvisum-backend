import logging, warnings, uuid
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

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


logger = logging.getLogger(__name__)


class ScoutsSectionService:

    group_admin = GroupAdmin()
    default_section_name_service = DefaultScoutsSectionNameService()
    section_name_service = ScoutsSectionNameService()

    def section_create_or_update(
        self,
        request,
        group_admin_id: str = None,
        name: ScoutsSectionName = None,
        hidden: bool = False,
    ) -> ScoutsSection:
        """
        Creates or updates a ScoutsSection instance.
        """
        scouts_group = self.group_admin.get_group(
            active_user=request.user, group_group_admin_id=group_admin_id
        )
        if not scouts_group:
            raise ValidationError(
                "Invalid group admin id {} for scouts group".format(group_admin_id)
            )
        logger.debug(
            "GROUP ('%s'), NAME ('%s'), HIDDEN: %s",
            scouts_group.name,
            name.name,
            hidden,
        )

        name_instance = None
        if not isinstance(name, ScoutsSectionName):
            name_instance = self.section_name_service.name_get(name=name)

        logger.debug(
            "Querying existing ScoutsSection instances with group admin id %s and name %s (%s)",
            scouts_group.group_admin_id,
            name,
            type(name).__name__,
        )
        if name_instance is None:
            qs = ScoutsSection.objects.filter(
                group_admin_id=scouts_group.group_admin_id, name__name=name
            )
        else:
            qs = ScoutsSection.objects.filter(
                group_admin_id=scouts_group.group_admin_id, name=name
            )
        count = qs.count()

        if count > 0:
            warnings.warn("Attempted to create or update multiple objects")
            return None

        if count == 0:
            logger.debug("Creating ScoutsSection with name '%s'", name)
            return self._section_create(request, scouts_group, name, hidden)
        if count == 1:
            instance = qs[0]
            logger.debug("Updating ScoutsSection with name '%s'", instance.name.name)
            return self._section_update(request, instance, scouts_group, name, hidden)

    def _section_create(
        self,
        request,
        group: AbstractScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden: bool = False,
    ) -> ScoutsSection:
        if name is None or not isinstance(name, ScoutsSectionName):
            name = self.section_name_service.name_create(name=name)
        instance = ScoutsSection()

        instance.group_admin_id = group.group_admin_id
        instance.group_type = ScoutsGroupType.objects.get(group_type=group.type)
        instance.name = name
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    def _section_update(
        self,
        request,
        instance: ScoutsSection,
        group: AbstractScoutsGroup = None,
        name: ScoutsSectionName = None,
        hidden=False,
    ) -> ScoutsSection:
        """
        Updates an existing Section instance.
        """
        logger.debug("Updating Section with name '%s'", instance.name.name)

        instance.group_admin_id = group.group_admin_id
        instance.name = name
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance

    # def section_read(self, request, **fields) -> ScoutsSection:
    #     """
    #     Retrieves a Section by uuid or SectionName.

    #     If uuid or name are lists, then lists will be returned.
    #     If uuid is None, then the group argument must be presented.
    #     """
    #     group = fields.get("group", None)
    #     id = fields.get("id", None)
    #     name = fields.get("name", None)

    #     logger.debug("SECTION FIELDS: %s", fields)

    #     if id is None and name is None:
    #         return ScoutsSection.objects.all()

    #     if id is not None and not isinstance(id, dict):
    #         if isinstance(id, list):
    #             return list(ScoutsSection.objects.filter(id__in=id).values_list())

    #         if isinstance(id, uuid.UUID):
    #             return get_object_or_404(ScoutsSection, id=id)

    #     if name is not None and not isinstance(name, dict):
    #         if isinstance(name, list):
    #             return list(
    #                 ScoutsSection.objects.filter(
    #                     group=group, name__name__in=name
    #                 ).values_list()
    #             )

    #         if isinstance(name, str):
    #             return list(ScoutsSection.objects.filter(group=group, name__name=name))

    #     logger.debug("No Section instances found with the given args")

    #     return None

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
            logger.debug("Linking sections to GROUP: %s (%s)", group, group.name)

            sections = ScoutsSection.objects.all().filter(
                group_admin_id=group.group_admin_id
            )

            # @TODO update if necessary
            logger.debug(
                "Found %d SECTIONS to link to group %s with type %s",
                sections.count(),
                group.name,
                group.type,
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
                            request, group.group_admin_id, name.name, name.name.hidden
                        )
                    )

        return created_sections

    # def add_section(self, instance: Group, **fields):
    #     """
    #     Adds Section instances to a Group.
    #     """
    #     logger.debug("FIELDS: %s", fields)
    #     sections = self.section_service.section_read(group=instance, **fields)

    #     if sections is None or len(sections) == 0:
    #         section = self.section_service.section_create_or_update(
    #             group=instance, **fields
    #         )
    #     else:
    #         section = sections[0]

    #     logger.debug("Section to add: %s", section)

    #     instance.sections.add(section)

    #     instance.full_clean()
    #     instance.save()

    #     return instance
