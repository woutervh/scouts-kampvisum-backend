from django.db import models

from ..models import (
    Concern, ConcernType, LinkedSubCategory
)
from apps.base.models import BaseModel
from apps.camps.models import Camp


class LinkedConcern(BaseModel):

    sub_category = models.ForeignKey(
        LinkedSubCategory,
        related_name="concerns",
        on_delete=models.CASCADE
    )
    origin = models.ForeignKey(Concern, on_delete=models.CASCADE)
    type = models.ForeignKey(ConcernType, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
