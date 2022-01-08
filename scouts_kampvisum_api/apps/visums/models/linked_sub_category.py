from django.db import models

from apps.visums.models import LinkedCategory, SubCategory

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedSubCategory(AbstractBaseModel):

    parent = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(
        LinkedCategory, on_delete=models.CASCADE, related_name="sub_categories"
    )

    class Meta:
        ordering = ["parent__index"]
