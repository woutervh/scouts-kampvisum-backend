from django.db import models

from ..models import SubCategory, ConcernType
from apps.base.models import BaseModel, Translatable, Linkable, Explainable
from inuits.models import RequiredCharField


class Concern(Translatable, Linkable, Explainable, BaseModel):

    name = RequiredCharField(max_length=64)
    sub_category = models.ForeignKey(
        SubCategory, related_name="concerns", on_delete=models.CASCADE
    )
    type = models.ForeignKey(ConcernType, on_delete=models.CASCADE)
    is_default = False

    class Meta:
        ordering = ["name"]
