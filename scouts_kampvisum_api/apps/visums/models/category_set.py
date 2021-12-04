from django.db import models

from apps.visums.models import Category, CategorySetPriority

from apps.camps.models import CampYear
from apps.groups.models import ScoutsGroupType

from scouts_auth.inuits.models import AuditedBaseModel


class CategorySet(AuditedBaseModel):
    """
    A list of categories for a certain group type with a certain priority.
    """

    # Indicates the hierarchical source and thereby specifies precedence.
    priority = models.ForeignKey(
        CategorySetPriority,
        on_delete=models.CASCADE,
        default=None,
    )
    type = models.ForeignKey(ScoutsGroupType, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    camp_year = models.ForeignKey(CampYear, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["camp_year"]

    def has_categories(self):
        return len(self.categories) > 0
