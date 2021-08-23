from django.db import models

from apps.base.models import BaseModel
from ..managers import ScoutsCampVisumCategoryManager


class ScoutsCampVisumCategory(BaseModel):
    
    name = models.CharField(
        max_length=128, null=False, blank=False, unique=True)
    
    objects = ScoutsCampVisumCategoryManager()
    
    class Meta:
        ordering = ['name']
    
    def natural_key(self):
        return (self.name, )
    
    def clean(self):
        pass

