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
        logger.debug("Checking %d groups for fix #92074", len(groups))
        logger.debug(
            "Found %d DefaultScoutsSectionName instance(s)",
            DefaultScoutsSectionName.objects.count(),
        )
        for group in groups:
            if group.default_sections_loaded:
                sections: List[ScoutsSection] = group.sections.all()
                sections_to_remove: List[ScoutsSection] = []
                sections_to_create: List[ScoutsSection] = []

                # Remove unlinked sections
                for section in sections:
                    camps: List[Camp] = list(
                        Camp.objects.all().filter(sections__in=[section])
                    )
                    if not camps or len(camps) == 0:
                        sections_to_remove.append(section)
                for section in sections_to_remove:
                    self.remove_section(section=section)

                # Create sections with default names if there are no sections for the default gender and age group sections
                default_scouts_section_names: List[
                    DefaultScoutsSectionName
                ] = self.default_section_name_service.load_for_group(
                    request=None, group=group
                )
                for default_scouts_section_name in default_scouts_section_names:
                    sections: List[ScoutsSection] = ScoutsSection.objects.all().filter(
                        group=group,
                        gender=default_scouts_section_name.gender,
                        age_group=default_scouts_section_name.age_group,
                    )

                    if not sections or len(sections) == 0:
                        self.create_section(
                            group=group,
                            default_scouts_section_name=default_scouts_section_name,
                        )

    def update_section(
        self,
        section: ScoutsSection,
        group: ScoutsGroup,
        name: str,
        gender: Gender,
        age_group: int,
    ) -> ScoutsSection:

        current_group = section.group
        current_name = section.name
        current_gender = section.gender
        current_age_group = section.age_group

        recreated_sections: List[ScoutsSection] = list(
            ScoutsSection.objects.all().filter(
                group=group,
                name=name,
                gender=gender,
                age_group=age_group,
            )
        )
        logger.debug(
            "IN UPDATE: Found %d recreated sections for default name %s (current section name: %s)",
            len(recreated_sections),
            name,
            section.name,
        )

        logger.debug(
            "Updating SECTION (%s) in GROUP %s: name (%s) -> (%s)",
            section.id,
            section.group.group_admin_id,
            section.name,
            name,
        )

        section.group = group
        section.name = name
        section.gender = gender
        section.age_group = age_group

        try:
            section.full_clean()
            section.save()
        except:
            raise ValidationError(
                "Unable to update ScoutsSection {} (group: {}, name: {}, gender: {}, age_group: {}) with values (group: {}, name: {}, gender: {}, age_group: {})".format(
                    section.id,
                    current_group,
                    current_name,
                    current_gender,
                    current_age_group,
                    group,
                    name,
                    gender,
                    age_group,
                )
            )

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
