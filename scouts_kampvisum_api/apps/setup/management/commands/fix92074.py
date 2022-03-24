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
                sections_to_update: List[List[any]] = []
                sections_to_remove: List[ScoutsSection] = []

                for section in sections:
                    if not hasattr(section, "section_name"):
                        continue

                    logger.debug(
                        "CURRENT SECTION: id (%s), group (%s), section_name (%s), name (%s), gender (%s), age_group (%s), hidden (%s)",
                        section.id,
                        section.group.group_admin_id,
                        section.section_name.id
                        if hasattr(section.section_name, "id")
                        else section.section_name,
                        section.name,
                        section.gender,
                        section.age_group,
                        section.hidden,
                    )

                    from apps.groups.models import ScoutsSectionName

                    still_linked_to_section_name = False
                    section_name = (
                        section.section_name
                        if section.section_name
                        else section.name
                        if section.name
                        else None
                    )
                    if section_name:
                        # the migration has set the (now) string name with the (previous) foreign key on ScoutsSectionName
                        section_name = ScoutsSectionName.objects.safe_get(
                            id=section_name
                        )
                        if section_name:
                            still_linked_to_section_name = True

                    name = (
                        section_name.name
                        if still_linked_to_section_name
                        else section.name
                    )
                    gender = (
                        section_name.gender
                        if still_linked_to_section_name
                        else section.gender
                    )
                    age_group = (
                        section_name.age_group
                        if still_linked_to_section_name
                        else section.age_group
                    )

                    default_section_name: DefaultScoutsSectionName = (
                        self.default_section_name_service.load_name_for_group(
                            request=None,
                            group=group,
                            gender=gender,
                            age_group=age_group,
                        )
                    )
                    if default_section_name:
                        logger.debug(
                            "Found a DefaultScoutsSectionName instance for group type %s, gender %s and age_group %s: %s",
                            group.group_type,
                            gender,
                            age_group,
                            default_section_name.name,
                        )
                    else:
                        logger.debug(
                            "Couldn't find a DefaultScoutsSectionName instance for group type %s, gender %s and age_group %s",
                            group.group_type,
                            gender,
                            age_group,
                        )

                    if still_linked_to_section_name or (
                        default_section_name
                        and default_section_name.name != section.name
                    ):
                        logger.debug(
                            "Fixing #92074 for group %s and section %s",
                            group.group_admin_id,
                            name,
                        )

                        if not default_section_name:
                            logger.debug(
                                "No DefaultSectionName instance found with arguments (group (%s), gender (%s), age_group (%s))",
                                group.group_admin_id,
                                gender,
                                age_group,
                            )
                        else:
                            name = default_section_name.name
                            gender = default_section_name.gender
                            age_group = default_section_name.age_group

                        if not (
                            section.group == group
                            and section.name == name
                            and section.gender == gender
                            and section.age_group == age_group
                        ):
                            # The existing section has a non-default name
                            # OR
                            # the group has created a new section with the default name
                            #
                            # -> Check if a section with the default name was created
                            # -> If so, check if that section has been linked to a visum
                            #    -> If so, delete the current section
                            #    -> If not,
                            # Check if the group has recreated a section with the default name
                            recreated_sections: List[ScoutsSection] = list(
                                ScoutsSection.objects.all().filter(
                                    group=group,
                                    name=name,
                                    gender=gender,
                                    age_group=age_group,
                                )
                            )
                            logger.debug(
                                "Found %d recreated sections for default name %s (current section name: %s)",
                                len(recreated_sections),
                                name,
                                section.name,
                            )

                            # Easy: Default name sections were not recreated, safe to update
                            if not recreated_sections or len(recreated_sections) == 0:
                                logger.debug(
                                    "Found no recreated sections, updating the current section (%s -> %s)",
                                    section.name,
                                    name,
                                )
                                logger.debug("UPDATE ADD: %s -> %s", section.name, name)
                                sections_to_update.append(
                                    [section, group, name, gender, age_group]
                                )
                            # Default name sections were recreated, remove unlinked sections
                            else:
                                linked_sections: List[ScoutsSection] = []
                                unlinked_sections: List[ScoutsSection] = []
                                current_section_linked = False

                                camps: List[Camp] = list(
                                    Camp.objects.all().filter(sections__in=[section])
                                )
                                if camps and len(camps) != 0:
                                    logger.debug(
                                        "Current section %s is linked", section.name
                                    )
                                    current_section_linked = True

                                for recreated_section in recreated_sections:
                                    camps: List[Camp] = list(
                                        Camp.objects.all().filter(
                                            sections__in=[recreated_section]
                                        )
                                    )
                                    # The section under investigation is linked to a camp, investigate later
                                    if camps and len(camps) != 0:
                                        linked_sections.append(recreated_section)
                                    else:
                                        unlinked_sections.append(recreated_section)

                                    for camp in camps:
                                        logger.debug(
                                            "Recreated section(s) linked to camp %s: %s",
                                            camp.name,
                                            [
                                                section.name
                                                for section in camp.sections.all()
                                                if section in recreated_sections
                                            ],
                                        )

                                logger.debug(
                                    "Found %d linked recreated section(s) and %d unlinked",
                                    len(linked_sections),
                                    len(unlinked_sections),
                                )

                                if not current_section_linked:
                                    # Don't update, but remove the current section, because a recreated section exists that has been linked
                                    if len(linked_sections) > 0:
                                        # Don't touch the linked sections, but remove the current section
                                        logger.debug("REMOVE ADD: %s", section.name)
                                        sections_to_remove.append(section)
                                    # Don't remove, but update the current section and remove the unlinked sections
                                    else:
                                        logger.debug(
                                            "UPDATE ADD: %s -> %s", section.name, name
                                        )
                                        sections_to_update.append(
                                            [section, group, name, gender, age_group]
                                        )

                                        for unlinked_section in unlinked_sections:
                                            logger.debug(
                                                "REMOVE ADD: %s", unlinked_section.name
                                            )
                                            sections_to_remove.append(unlinked_section)
                                else:
                                    # Current section is linked, update it if there are no linked recreated sections
                                    if len(linked_sections) == 0:
                                        logger.debug(
                                            "UPDATE ADD: %s -> %s", section.name, name
                                        )
                                        sections_to_update.append(
                                            [section, group, name, gender, age_group]
                                        )

                                    # Remove the unlinked sections
                                    for unlinked_section in unlinked_sections:
                                        logger.debug(
                                            "REMOVE ADD: %s", unlinked_section.name
                                        )
                                        sections_to_remove.append(unlinked_section)

                logger.debug(
                    "Removing %d section(s) and updating %d",
                    len(sections_to_remove),
                    len(sections_to_update),
                )
                for section in sections_to_remove:
                    self.remove_section(section)
                for section in sections_to_update:
                    self.update_section(
                        section=section[0],
                        group=section[1],
                        name=section[2],
                        gender=section[3],
                        age_group=section[4],
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
