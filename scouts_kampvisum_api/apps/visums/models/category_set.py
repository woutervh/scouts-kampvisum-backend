import logging

from django.db import models

from apps.groups.models import ScoutsGroupType
from apps.visums.managers import CategorySetManager
from apps.visums.models import CampYearCategorySet, CategorySetPriority

from scouts_auth.inuits.models import AuditedBaseModel


logger = logging.getLogger(__name__)


class CategorySet(AuditedBaseModel):
    """
    A list of categories for a certain group type with a certain priority.
    """

    objects = CategorySetManager()

    category_set = models.ForeignKey(
        CampYearCategorySet, on_delete=models.CASCADE, related_name="category_sets"
    )
    group_type = models.ForeignKey(ScoutsGroupType, on_delete=models.CASCADE)
    # Indicates the hierarchical source and thereby specifies precedence.
    priority = models.ForeignKey(
        CategorySetPriority,
        on_delete=models.CASCADE,
        default=None,
    )

    class Meta:
        ordering = ["category_set__camp_year__year"]
        constraints = [
            models.UniqueConstraint(
                fields=["category_set", "group_type"],
                name="unique_set_for_category_set_and_group_type",
            ),
        ]

    def has_categories(self):
        return len(self.categories) > 0

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        return (self.category_set.camp_year.year, self.group_type)

    def __str__(self):
        return (
            "OBJECT CategorySet: category_set({}), group_type({}), priority({})".format(
                str(self.category_set), str(self.group_type), str(self.priority)
            )
        )

    def to_simple_str(self):
        return "CategorySet ({})".format(self.id)
