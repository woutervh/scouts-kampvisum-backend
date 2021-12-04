from django.db import models

from apps.visums.models import Category
from apps.visums.managers import CategoryManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Linkable, Explainable


class SubCategory(Linkable, Explainable, AbstractBaseModel):

    category = models.ForeignKey(
        Category,
        related_name="sub_categories",
        on_delete=models.CASCADE,
    )
    name = RequiredCharField(max_length=128)
    is_default = models.BooleanField(default=False)

    objects = CategoryManager()

    class Meta:
        ordering = ["name"]

    def natural_key(self):
        return (self.name,)
