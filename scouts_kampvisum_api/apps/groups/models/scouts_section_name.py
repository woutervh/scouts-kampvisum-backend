from django.db import models
from safedelete.models import HARD_DELETE

from apps.groups.managers import ScoutsSectionNameManager

from scouts_auth.groupadmin.scouts import AgeGroup
from scouts_auth.inuits.models import AbstractBaseModel, Gender
from scouts_auth.inuits.models.fields import RequiredCharField, DefaultCharField

# FIXTURE: scouts_section_names
# Taken from https://nl.wikipedia.org/wiki/Tak_(scouting)
# https://en.wikipedia.org/wiki/Age_groups_in_Scouting_and_Guiding#History


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
        choices=Gender,
        default=Gender.UNKNOWN,
        max_length=1,
    )
    age_group = DefaultCharField(
        choices=AgeGroup, default=AgeGroup.AGE_GROUP_UNKNOWN, max_length=3
    )
    hidden = models.BooleanField(default=False)

    class Meta:
        unique_together = ("name", "gender", "age_group")
        ordering = ["age_group"]

    def natural_key(self):
        return (self.name,)
