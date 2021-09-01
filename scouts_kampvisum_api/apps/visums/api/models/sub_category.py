from django.db import models

from ..models import Category
from ..managers import CategoryManager
from apps.base.models import BaseModel
from inuits.models import RequiredCharField


class SubCategory(BaseModel):

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
        unique_together = ("category", "name")

    def natural_key(self):
        return (self.name,)
