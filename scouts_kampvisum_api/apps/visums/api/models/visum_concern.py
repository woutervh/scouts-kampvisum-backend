from django.db import models

from ..models import (
    CampVisumConcern, CampVisumConcernType, CampVisumLinkedSubCategory
)
from apps.base.models import BaseModel
from apps.camps.models import Camp


class CampVisumLinkedConcern(BaseModel):

    sub_category = models.ForeignKey(
        CampVisumLinkedSubCategory,
        related_name="concerns",
        on_delete=models.CASCADE
    )
    origin = models.ForeignKey(CampVisumConcern, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
