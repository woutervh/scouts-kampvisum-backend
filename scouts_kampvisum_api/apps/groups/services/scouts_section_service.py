from typing import List
from types import SimpleNamespace

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
                group=group.group_admin_id,
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
            f"Creating a ScoutsSection with name {name}, gender {gender} and age_group {age_group} for group {group.group_admin_id}", user=request.user)

        instance = ScoutsSection()

        instance.group = group.group_admin_id
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
            f"Updating Section with name {name}, gender {gender} and age_group {age_group} in group {group.group_admin_id}", user=request.user)

        instance.group = group.group_admin_id
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
        if not request or not request.user:
            request = SimpleNamespace(user=user)

        created_sections = list()

        # logger.debug(
        #     f"Setting up default scouts sections for {len(user.get_scouts_groups())} group(s)", user=request.user)
        for group in user.get_scouts_groups():
            group_count = ScoutsSection.objects.filter(
                group=group.group_admin_id).count()
            # logger.debug(
            #     f"Found {group_count} scouts sections for group {group.group_admin_id}", user=request.user)

            if group_count == 0:
                # logger.debug(
                #     f"Linking sections to GROUP: {group.group_admin_id} ({group.name})", user=request.user)

                default_scouts_section_names: List[
                    DefaultScoutsSectionName
                ] = self.default_section_name_service.load_for_group(
                    request=request, group=group
                )

                if len(default_scouts_section_names) == 0:
                    raise ValidationError(
                        f"No DefaultScoutsSectionName instances found for group_type {group.type}")

                for default_name in default_scouts_section_names:
                    # logger.debug(
                    #     f"Linking DefaultSectionName {default_name.name} to group {group.group_admin_id}")

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
                    raise ValidationError(
                        "Attempted to create sections, but failed")

        return created_sections
