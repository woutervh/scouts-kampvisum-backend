from django.db import models

from ..models import CampVisumSubCategory, CampVisumLinkedCategory
from apps.base.models import BaseModel
from inuits.models import OptionalTextField


class CampVisumLinkedSubCategory(BaseModel):

    category = models.ForeignKey(
        CampVisumLinkedCategory, on_delete=models.CASCADE)
    # Reference
    origin = models.ForeignKey(
        CampVisumSubCategory, on_delete=models.SET_NULL, null=True)
    # Deep copy
    sub_category = models.ForeignKey(
        CampVisumSubCategory,
        related_name="linked_sub_categories",
        on_delete=models.CASCADE)

    def get_status(self):
        pass
