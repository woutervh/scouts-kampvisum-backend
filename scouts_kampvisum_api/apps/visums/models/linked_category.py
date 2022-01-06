from django.db import models

from apps.visums.models import Category, LinkedCategorySet

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategory(AbstractBaseModel):

    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_set = models.ForeignKey(
        LinkedCategorySet, on_delete=models.CASCADE, related_name="categories"
    )
