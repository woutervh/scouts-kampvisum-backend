from django.db import models
from safedelete.models import HARD_DELETE

from apps.base.models import BaseModel
from ..models import ScoutsSectionName, ScoutsGroupType


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

