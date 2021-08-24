from django.db import models

from ..models import ScoutsCampVisumCategory
from apps.base.models import BaseModel


class ScoutsCampVisumCategorySet(BaseModel):
    
    categories = models.ForeignKey(
        ScoutsCampVisumCategory, on_delete=models.CASCADE)

