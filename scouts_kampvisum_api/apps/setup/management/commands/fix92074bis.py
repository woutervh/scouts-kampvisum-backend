import os
from pathlib import Path
from typing import List

from django.db import transaction
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from apps.camps.models import Camp

from apps.groups.models import (
    ScoutsSectionName,
    DefaultScoutsSectionName,
    ScoutsSection,
)
from apps.groups.services import DefaultScoutsSectionNameService

from scouts_auth.groupadmin.models import ScoutsGroup

from scouts_auth.inuits.models import Gender


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 92074 https://redmine.inuits.eu/issues/92074"
    exception = False

    default_section_name_service = DefaultScoutsSectionNameService()

    BASE_PATH = "apps/groups/fixtures"
    DEFAULT_SECTION_NAMES = "default_scouts_section_names.json"

    # fix for https://redmine.inuits.eu/issues/92074 for groups that were already registered
    @transaction.atomic
    def handle(self, *args, **kwargs):

        # First remove all existing DefaultScoutsSectionName instances
        DefaultScoutsSectionName.objects.all().delete()

        # Reload DefaultScoutsSectionName instances from the fixture, to be sure, to be sure
        parent_path = Path(settings.BASE_DIR)
        data_path = "{}/{}".format(self.BASE_PATH, self.DEFAULT_SECTION_NAMES)
        path = os.path.join(parent_path, data_path)
        logger.debug("Reloading DefaultScoutsSectionName instances from %s", path)
        call_command("loaddata", path)

        # Now fix existing groups: reset section names to their defaults
        groups: List[ScoutsGroup] = ScoutsGroup.objects.all()
        logger.debug("Checking %d groups for fix #92074bis", len(groups))
        logger.debug(
            "Found %d DefaultScoutsSectionName instance(s)",
            DefaultScoutsSectionName.objects.count(),
        )
        for group in groups:
            if group.default_sections_loaded:
                sections: List[ScoutsSection] = group.sections.all()
                sections_to_update: List[ScoutsSection] = []

                for section in sections:
                    section_name: ScoutsSectionName = (
                        ScoutsSectionName.objects.safe_get(id=section.name)
                    )

                    if section_name:
                        default_scouts_section_name: DefaultScoutsSectionName = (
                            self.default_section_name_service.load_name_for_group(
                                request=None,
                                group=group,
                                gender=section_name.gender,
                                age_group=section_name.age_group,
                            )
                        )

                        if default_scouts_section_name:
                            sections_to_update.append(section)

                for section in sections_to_update:
                    self.update_section(
                        section=section,
                        group=group,
                        name=default_scouts_section_name.name,
                        gender=default_scouts_section_name.gender,
                        age_group=default_scouts_section_name.age_group,
                        hidden=default_scouts_section_name.hidden,
                    )

    def update_section(
        self,
        section: ScoutsSection,
        group: ScoutsGroup,
        name: str,
        gender: Gender,
        age_group: int,
        hidden: bool,
    ) -> ScoutsSection:
        recreated_sections: List[ScoutsSection] = list(
            ScoutsSection.objects.all().filter(
                group=group,
                name=name,
                gender=gender,
                age_group=age_group,
            )
        )
        sections_to_remove: List[ScoutsSection] = []
        if recreated_sections:
            if len(recreated_sections) > 0:
                for recreated_section in recreated_sections:
                    camps: List[Camp] = Camp.objects.all().filter(
                        sections__in=[recreated_section]
                    )
                    if not camps or len(camps) == 0:
                        sections_to_remove.append(recreated_section)
                for removable_section in sections_to_remove:
                    self.remove_section(removable_section)

            if len(recreated_sections) != len(sections_to_remove):
                logger.warn(
                    "Some sections were recreated and linked, not removing, not updating current section"
                )
                return section

        section.group = group
        section.name = name
        section.gender = gender
        section.age_group = age_group
        section.hidden = hidden

        section.full_clean()
        section.save()

        return section

    def remove_section(self, section: ScoutsSection):
        # The section could have already been removed -> check
        section: ScoutsSection = ScoutsSection.objects.safe_get(id=section.id)

        if not section:
            logger.debug("Section (%d) was already removed", section.id)
            return

        # Double check that the section is not linked to any camp
        camps: List[Camp] = list(Camp.objects.all().filter(sections__in=[section]))
        if camps and len(camps) != 0:
            logger.error(
                "The section %s (%s) was linked to a camp, doing nothing",
                section.name,
                section.id,
            )
        else:
            logger.debug("Removing section %s", section.name)
            section.delete()

    def create_section(
        self, group: ScoutsGroup, default_scouts_section_name: DefaultScoutsSectionName
    ) -> ScoutsSection:
        instance = ScoutsSection()

        instance.group = group
        instance.name = default_scouts_section_name.name
        instance.gender = default_scouts_section_name.gender
        instance.age_group = default_scouts_section_name.age_group
        instance.hidden = default_scouts_section_name.hidden

        instance.full_clean()
        instance.save()

        return instance
