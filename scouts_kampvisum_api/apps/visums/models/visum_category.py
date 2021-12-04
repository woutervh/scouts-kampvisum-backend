from django.db import models

from apps.visums.models import Category
from apps.camps.models import Camp

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategory(AbstractBaseModel):

    # Parent camp
    camp = models.ForeignKey(Camp, related_name="categories", on_delete=models.CASCADE)
    # Reference
    origin = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # Deep copy
    category = models.ForeignKey(
        Category, related_name="linked_categories", on_delete=models.CASCADE
    )
