from django.db import models

from ..models import CategorySet
from apps.base.models import BaseModel
from apps.camps.models import Camp


class CampVisum(BaseModel):

    camp = models.ForeignKey(
        Camp, related_name="visum", on_delete=models.CASCADE)
    category_set = models.ForeignKey(
        CategorySet, on_delete=models.CASCADE)
