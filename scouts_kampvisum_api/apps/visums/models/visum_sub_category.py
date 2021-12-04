from django.db import models

from apps.visums.models import SubCategory, LinkedCategory

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.interfaces import Commentable


class LinkedSubCategory(Commentable, AbstractBaseModel):

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
