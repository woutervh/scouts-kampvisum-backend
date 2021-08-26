from django.db import models
from safedelete.models import HARD_DELETE

from apps.base.models import BaseModel
from ..models import Group, SectionName


class Section(BaseModel):
    """
    A model for a scouts section, linked to their scouts group and name.
    """
    
    group = models.ForeignKey(
        Group,
        related_name='sections',
        on_delete = models.CASCADE)
    name = models.ForeignKey(
        SectionName,
        on_delete = models.DO_NOTHING)
    hidden = models.BooleanField(default=False)
    
    class Meta:
        ordering = [ 'name__age_group' ]

