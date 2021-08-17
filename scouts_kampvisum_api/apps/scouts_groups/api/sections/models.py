from apps.scouts_groups.api.sections.managers import ScoutsSectionNameManager
from django.db import models
from safedelete.models import HARD_DELETE

from ....base.models import BaseModel
from ....groupadmin.api import MemberGender
from ..groups.models import ScoutsGroupType, ScoutsGroup

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

    def natural_key(self):
        return (self.name, )
    
    def clean(self):
        pass


class ScoutsDefaultSectionName(BaseModel):
    """
    A model that configures default section names for a particular group type.
    
    Currently, if the group is not a zeescouts group, it is assumed the group
    type is 'Groep'.
    """
    
    type = models.ForeignKey(
        ScoutsGroupType,
        null=True,
        on_delete=models.CASCADE)
    name = models.ForeignKey(
        ScoutsSectionName,
        on_delete = models.DO_NOTHING)

    class Meta:
        unique_together = (('type', 'name'))
    
    def clean(self):
        pass


class ScoutsSection(BaseModel):
    """
    A model for a scouts section, linked to their scouts group and name.
    """
    
    group = models.ForeignKey(
        ScoutsGroup,
        on_delete = models.CASCADE)
    name = models.ForeignKey(
        ScoutsSectionName,
        on_delete = models.DO_NOTHING)
    
    def clean(self):
        pass

