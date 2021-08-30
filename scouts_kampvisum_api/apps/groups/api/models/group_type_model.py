from django.db import models

from apps.base.models import BaseModel
from ..managers import GroupTypeManager


class GroupType(BaseModel):
    """
    Specifies the type of scouts group (e.g. AKABE, zeescouts, ...).
    """

    type = models.CharField(
        max_length=64,
        null=False,
        blank=False)
    parent = models.ForeignKey(
        'GroupType',
        null=True,
        on_delete=models.CASCADE)

    objects = GroupTypeManager()

    class Meta:
        abstract = False
        ordering = ['type']

    def natural_key(self):
        return (self.type, )
