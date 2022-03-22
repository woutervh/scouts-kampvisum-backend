import os
from pathlib import Path
from typing import List

from django.db import transaction
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from apps.groups.models import (
    DefaultScoutsSectionName,
    ScoutsSection,
)
from apps.groups.services import DefaultScoutsSectionNameService

from scouts_auth.groupadmin.models import ScoutsGroup


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
        for group in groups:
            if group.default_sections_loaded:
                sections: List[ScoutsSection] = group.sections.all()

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

                    section_name = section.section_name
                    if section.name:
                        # the migration has set the (now) string name with the (previous) foreign key on ScoutsSectionName
                        section_name = ScoutsSectionName.objects.safe_get(
                            id=section.name
                        )

                    if section.section_name or section_name:
                        name = section_name.name
                        gender = section_name.gender
                        age_group = section_name.age_group

                        logger.debug(
                            "Fixing #92074 for group %s and section %s",
                            group.group_admin_id,
                            name,
                        )
                        default_section_name: DefaultScoutsSectionName = (
                            self.default_section_name_service.load_name_for_group(
                                request=None,
                                group=group,
                                gender=gender,
                                age_group=age_group,
                            )
                        )
                        if not default_section_name:
                            logger.debug(
                                "No DefaultSectionName instance found with arguments (group (%s), gender (%s), age_group (%s))",
                                group.group_admin_id,
                                gender,
                                age_group,
                            )
                            # raise ValidationError(
                            #     "Couldn't find DefaultScoutsSectionName with group type %s, gender %s and age_group %s",
                            #     group.type,
                            #     gender,
                            #     age_group,
                            # )
                            section.section_name = None
                            section.name = name
                            section.gender = gender
                            section.age_group = age_group
                        else:
                            section.section_name = None
                            section.name = default_section_name.name
                            section.gender = default_section_name.gender
                            section.age_group = default_section_name.age_group

                        section.full_clean()
                        section.save()

                        logger.debug(
                            "FIXED SECTION: id (%s), group (%s), section_name (%s), name (%s), gender (%s), age_group (%s), hidden (%s)",
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
