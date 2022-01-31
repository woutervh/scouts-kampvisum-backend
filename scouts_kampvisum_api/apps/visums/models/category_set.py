import logging

from django.db import models

from apps.visums.managers import CategorySetManager
from apps.visums.models import CampYearCategorySet, CategorySetPriority

from scouts_auth.inuits.models import AuditedBaseModel


logger = logging.getLogger(__name__)


class CategorySet(AuditedBaseModel):
    """
    A list of categories for a certain group type with a certain priority.
    """

    objects = CategorySetManager()

    camp_year_category_set = models.ForeignKey(
        CampYearCategorySet, on_delete=models.CASCADE, related_name="category_sets"
    )
    # Indicates the hierarchical source and thereby specifies precedence.
    priority = models.ForeignKey(
        CategorySetPriority,
        on_delete=models.CASCADE,
        default=None,
    )

    class Meta:
        ordering = ["camp_year_category_set__camp_year__year"]
        constraints = [
            models.UniqueConstraint(
                fields=["camp_year_category_set"],
                name="unique_set_for_camp_year_category_set",
            ),
        ]

    def has_categories(self):
        return len(self.categories) > 0

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        return (self.category_set.camp_year.year)

    def __str__(self):
        return (
            "OBJECT CategorySet: camp_year_category_set({}), priority({})".format(
                self.camp_year_category_set, self.priority
            )
        )

    def to_simple_str(self):
        return "CategorySet ({})".format(self.id)
