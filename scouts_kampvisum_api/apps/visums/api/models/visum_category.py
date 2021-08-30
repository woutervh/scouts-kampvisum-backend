from django.db import models

from ..models import CampVisumCategory
from apps.base.models import BaseModel
from apps.camps.models import Camp


class CampVisumLinkedCategory(BaseModel):

    camp = models.ForeignKey(
        Camp,
        related_name="categories",
        on_delete=models.CASCADE)
    # Reference
    origin = models.ForeignKey(
        CampVisumCategory, on_delete=models.SET_NULL, null=True)
    # Deep copy
    category = models.ForeignKey(
        CampVisumCategory,
        related_name="linked_categories",
        on_delete=models.CASCADE)
