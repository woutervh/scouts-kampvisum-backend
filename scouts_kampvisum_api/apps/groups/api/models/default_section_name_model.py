from django.db import models

from apps.base.models import BaseModel
from ..models import SectionName, GroupType


class DefaultSectionName(BaseModel):
    """
    A model that configures default section names for a particular group type.

    Currently, if the group is not a zeescouts group, it is assumed the group
    type is 'Groep'.
    """

    type = models.ForeignKey(
        GroupType,
        null=True,
        on_delete=models.CASCADE)
    name = models.ForeignKey(
        SectionName,
        on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (('type', 'name'))

    def clean(self):
        pass
