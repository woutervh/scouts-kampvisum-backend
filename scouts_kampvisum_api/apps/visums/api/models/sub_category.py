from django.db import models

from ..models import CampVisumCategory
from ..managers import CampVisumCategoryManager
from apps.base.models import BaseModel
from inuits.models import RequiredCharField


class CampVisumSubCategory(BaseModel):

    category = models.ForeignKey(
        CampVisumCategory,
        related_name="sub_categories",
        on_delete=models.CASCADE,
    )
    name = RequiredCharField(max_length=128)
    is_default = models.BooleanField(default=False)

    objects = CampVisumCategoryManager()

    class Meta:
        ordering = ["name"]
        unique_together = ("category", "name")

    def natural_key(self):
        return (self.name,)
