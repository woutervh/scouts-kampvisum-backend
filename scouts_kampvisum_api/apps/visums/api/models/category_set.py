from django.db import models

from ..models import CampVisumCategory, CampVisumCategorySetPriority
from apps.base.models import BaseModel
from apps.camps.models import CampYear
from apps.groups.api.models import GroupType


class CampVisumCategorySet(BaseModel):
    """
    A list of categories for a certain group type with a certain priority.
    """

    # Indicates the hierarchical source and thereby specifies precedence.
    priority = models.ForeignKey(
        CampVisumCategorySetPriority,
        on_delete=models.CASCADE,
        default=None,
    )
    type = models.ForeignKey(GroupType, on_delete=models.CASCADE)
    categories = models.ManyToManyField(CampVisumCategory)
    camp_year = models.ForeignKey(CampYear, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["camp_year"]

    def has_categories(self):
        return len(self.categories) > 0
