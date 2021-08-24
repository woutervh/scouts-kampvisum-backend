from django.db import models

from apps.base.models import BaseModel
from ..models import ScoutsCampVisumCategory

class ScoutsCampVisumSubCategory(BaseModel):
    
    category = models.ForeignKey(
        ScoutsCampVisumCategory,
        related_name='sub_categories',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=128)
    
    class Meta:
        ordering = ['name']
        unique_together = (('category', 'name'))
    
    def clean(self):
        pass

