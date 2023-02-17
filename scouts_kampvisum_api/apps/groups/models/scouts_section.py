from django.db import models

from apps.groups.managers import ScoutsSectionManager

from scouts_auth.groupadmin.models.fields import GroupAdminIdField
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

    group = GroupAdminIdField()
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

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED ScoutsSection")
        return (self.group, self.name, self.gender, self.age_group)

    def __str__(self):
        return (
            f"group ({self.group}), name ({self.name}), gender ({self.gender}), age_group ({self.age_group}), hidden ({self.hidden})"
        )
