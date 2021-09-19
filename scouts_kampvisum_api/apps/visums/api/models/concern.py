from django.db import models

from ..models import SubCategory, ConcernType
from apps.base.models import BaseModel, Translatable, Linkable, Explainable


class Concern(Translatable, Linkable, Explainable, BaseModel):

    name = models.CharField(max_length=64, default="")
    sub_category = models.ForeignKey(
        SubCategory, related_name="concerns", on_delete=models.CASCADE
    )
    type = models.ForeignKey(ConcernType, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "sub_category")
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_name")]
