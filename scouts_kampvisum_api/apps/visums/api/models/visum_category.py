from django.db import models

from ..models import Category
from apps.base.models import BaseModel
from apps.camps.models import Camp


class LinkedCategory(BaseModel):

    # Parent camp
    camp = models.ForeignKey(Camp, related_name="categories", on_delete=models.CASCADE)
    # Reference
    origin = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # Deep copy
    category = models.ForeignKey(
        Category, related_name="linked_categories", on_delete=models.CASCADE
    )
