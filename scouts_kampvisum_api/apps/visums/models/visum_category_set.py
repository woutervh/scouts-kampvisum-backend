from django.db import models

from apps.visums.models import CategorySet

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategorySet(AbstractBaseModel):
    """
    A list of categories for a certain group type with a certain priority.
    """

    origin = models.ForeignKey(CategorySet, on_delete=models.CASCADE)

    class Meta:
        ordering = ["origin__camp_year"]

    def has_categories(self):
        return len(self.categories) > 0
