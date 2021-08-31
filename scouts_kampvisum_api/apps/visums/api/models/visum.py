from django.db import models

from ..models import CampVisumCategorySet
from apps.base.models import BaseModel
from apps.camps.models import Camp


class CampVisum(BaseModel):

    camp = models.ForeignKey(
        Camp, on_delete=models.CASCADE)
    category_set = models.ForeignKey(
        CampVisumCategorySet, on_delete=models.CASCADE)

    class Meta:
        ordering = ["camp__sections__age_group"]
