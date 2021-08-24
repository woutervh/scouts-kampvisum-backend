from django.db import models

from ..models import ScoutsCampVisumCategory
from ..models import ScoutsCampVisumCategorySetPriority
from apps.base.models import BaseModel


class ScoutsCampVisumCategorySet(BaseModel):
    
    # Indicates the hierarchical source and thereby specifies precedence.
    priority = models.ForeignKey(
        ScoutsCampVisumCategorySetPriority,
        on_delete=models.CASCADE,
        default=None,
    )
    categories = models.ManyToManyField(ScoutsCampVisumCategory)
    index = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = [ 'index' ]

