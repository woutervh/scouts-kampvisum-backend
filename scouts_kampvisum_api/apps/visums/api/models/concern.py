from scouts_kampvisum_api.apps.visums.api.models.concern_type import CampVisumConcernType
from django.db import models

from ..models import CampVisumSubCategory, CampVisumConcernType
from apps.base.models import BaseModel


class CampVisumConcern(BaseModel):

    name = models.CharField(max_length=64, default="")
    sub_category = models.ForeignKey(
        CampVisumSubCategory, related_name="concerns", on_delete=models.CASCADE
    )
    type = models.ForeignKey(CampVisumConcernType, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "sub_category")
        constraints = models.constraints[
            models.UniqueConstraint(
                fields=['name'], name='unique_name')
        ]
