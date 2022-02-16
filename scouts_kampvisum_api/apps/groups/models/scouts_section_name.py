import logging

from django.db import models
from safedelete.models import HARD_DELETE

from apps.groups.managers import ScoutsSectionNameManager

from scouts_auth.inuits.models import AbstractBaseModel, Gender
from scouts_auth.inuits.models.fields import (
    RequiredCharField,
    DefaultCharField,
    DefaultIntegerField,
)

# FIXTURE: scouts_section_names
# Taken from https://nl.wikipedia.org/wiki/Tak_(scouting)
# https://en.wikipedia.org/wiki/Age_groups_in_Scouting_and_Guiding#History


logger = logging.getLogger(__name__)


class ScoutsSectionName(AbstractBaseModel):
    """
    A simple string model to represent a scouts section name.

    This can be used to provide a consistent list of section names to
    choose from.
    """

    objects = ScoutsSectionNameManager()

    # Setting to HARD_DELETE because a section name may be incorrect
    _safedelete_policy = HARD_DELETE

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
                fields=["name", "gender", "age_group"],
                name="unique_name_gender_and_age_group",
            )
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        if not self.gender:
            self.gender = Gender.UNKNOWN
        if not self.age_group:
            self.age_group = 0
        return (self.name, self.gender, self.age_group)

    def __str__(self):
        return "OBJECT ScoutsSectionName: name({}), gender({}), age_group({}), hidden({})".format(
            self.name, self.gender, self.age_group, self.hidden
        )
