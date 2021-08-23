from django.db import models

from apps.base.models import BaseModel
from ..managers import ScoutsGroupTypeManager


class ScoutsGroupType(BaseModel):
    """
    Specifies the type of scouts group (e.g. AKABE, zeescouts, ...).
    """
    
    type = models.CharField(
        max_length=64,
        null=False,
        blank=False)
    parent = models.ForeignKey(
        'ScoutsGroupType',
        null=True,
        on_delete=models.CASCADE)
    
    objects = ScoutsGroupTypeManager()
    
    class Meta:
        abstract = False
        ordering = ['type']
    
    def natural_key(self):
        return (self.type, )
    
    def clean(self):
        pass

