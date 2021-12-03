from django.db import models

from ..models import SubCategory, LinkedCategory
from apps.base.models import BaseModel, Commentable


class LinkedSubCategory(Commentable, BaseModel):

    # Parent category
    category = models.ForeignKey(LinkedCategory, on_delete=models.CASCADE)
    # Reference
    origin = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    # Deep copy
    sub_category = models.ForeignKey(
        SubCategory, related_name="linked_sub_categories", on_delete=models.CASCADE
    )

    def get_status(self):
        pass
