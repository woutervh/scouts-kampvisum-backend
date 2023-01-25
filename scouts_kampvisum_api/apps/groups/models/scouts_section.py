from django.db import models

from apps.groups.models import ScoutsSectionName
from apps.groups.managers import ScoutsSectionManager

from scouts_auth.groupadmin.models import ScoutsGroup

from scouts_auth.inuits.models import AbstractBaseModel, Gender
from scouts_auth.inuits.models.fields import (
    DefaultCharField,
    RequiredCharField,
    DefaultIntegerField,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSection(AbstractBaseModel):
    """
    A model for a scouts section, linked to their scouts group and name.
    """

    objects = ScoutsSectionManager()

    group = models.ForeignKey(
        ScoutsGroup, on_delete=models.CASCADE, related_name="sections"
    )
    section_name = models.ForeignKey(
        ScoutsSectionName, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    name = RequiredCharField(max_length=128)
    gender = DefaultCharField(
        choices=Gender.choices,
        default=Gender.UNKNOWN,
        max_length=1,
    )
    age_group = DefaultIntegerField(default=0)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["age_group"]
        constraints = [
            models.UniqueConstraint(
                fields=["group", "name", "gender", "age_group"],
                name="unique_group_name_gender_age_group_for_section",
            )
        ]
        permissions = [
            ("create_section", "User can create a group section"),
            ("read_section", "User can view a group section"),
            ("update_section", "User can edit a group section"),
            ("delete_section", "User can delete a group section"),
            ("list_section", "User can list sections for his/her group"),
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED ScoutsSection")
        return (self.group, self.name, self.gender, self.age_group)
