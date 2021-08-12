
from django.db import models
from ...base.models import BaseModel

from .managers import ScoutsCampVisumCategoryManager

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


class ScoutsCampVisumSubCategory(BaseModel):
    
    category = models.ForeignKey(
        ScoutsCampVisumCategory, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=128)
    
    class Meta:
        #@TODO order by category, then name ?
        ordering = ['name']
        unique_together = (('category', 'name'))
    
    def clean(self):
        pass

