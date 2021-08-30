from django.db import models

from ..models import Group, SectionName
from apps.base.models import BaseModel


class Section(BaseModel):
    """
    A model for a scouts section, linked to their scouts group and name.
    """

    group = models.ForeignKey(
        Group,
        related_name='sections',
        on_delete=models.CASCADE)
    name = models.ForeignKey(
        SectionName,
        on_delete=models.DO_NOTHING)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ['name__age_group']
