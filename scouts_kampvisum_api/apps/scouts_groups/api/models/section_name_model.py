from django.db import models
from safedelete.models import HARD_DELETE

from apps.base.models import BaseModel
from apps.groupadmin.api import MemberGender
from ..managers import ScoutsSectionNameManager

# FIXTURE: scouts_section_names
# Taken from https://nl.wikipedia.org/wiki/Tak_(scouting)
# https://en.wikipedia.org/wiki/Age_groups_in_Scouting_and_Guiding#History
class ScoutsSectionName(BaseModel):
    """
    A simple string model to represent a scouts section name.
    
    This can be used to provide a consistent list of section names to
    choose from.
    """
    
    # Setting to HARD_DELETE because a section name may be incorrect
    _safedelete_policy = HARD_DELETE
    
    name = models.CharField(
        max_length=128)
    gender = models.CharField(
        max_length=12,
        choices=MemberGender.choices,
        default=MemberGender.MIXED
    )

    objects = ScoutsSectionNameManager()

    class Meta:
        unique_together = (('name', 'gender'))

    def natural_key(self):
        return (self.name, )
    
    def clean(self):
        pass

