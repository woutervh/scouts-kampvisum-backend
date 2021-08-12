from django.db import models

from ....base.models import BaseModel
from ..categories.models import ScoutsCampVisumCategory

class ScoutsCampVisumSubCategory(BaseModel):
    
    category = models.ForeignKey(
        ScoutsCampVisumCategory, on_delete=models.CASCADE,
        related_name='sub_categories')
    name = models.CharField(
        max_length=128)
    
    class Meta:
        #@TODO order by category, then name ?
        ordering = ['name']
        unique_together = (('category', 'name'))
    
    def clean(self):
        pass

