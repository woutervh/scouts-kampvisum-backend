from django.db import models

from ..models import Category, CategorySet
from apps.base.models import BaseModel
from apps.camps.models import CampYear
from apps.groups.api.models import GroupType


class LinkedCategorySet(BaseModel):
    """
    A list of categories for a certain group type with a certain priority.
    """

    origin = models.ForeignKey(CategorySet, on_delete=models.CASCADE)

    class Meta:
        ordering = ["origin__camp_year"]

    def has_categories(self):
        return len(self.categories) > 0
