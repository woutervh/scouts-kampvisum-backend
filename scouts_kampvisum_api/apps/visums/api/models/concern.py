from django.db import models

from ..models import CampVisumSubCategory
from apps.base.models import BaseModel


class CampVisumConcern(BaseModel):

    name = models.CharField(max_length=64, default="")
    sub_category = models.ForeignKey(
        CampVisumSubCategory, related_name="checks", on_delete=models.CASCADE
    )
