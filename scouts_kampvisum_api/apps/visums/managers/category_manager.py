import logging

from django.db import models


logger = logging.getLogger(__name__)


class CategoryManager(models.Manager):
    """
    Loads Category instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name, category_set):
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s), category_set: %s (%s))",
            "Category",
            name,
            type(name).__name__,
            category_set,
            type(category_set).__name__,
        )

        if type(category_set).__name__ == "CategorySet":
            return self.get(name=name, category_set=category_set)

        if type(category_set).__name__ == "list":
            return self.get(
                name=name,
                category_set__category_set__camp_year__year=category_set[0]
            )

        return self.get(
            name=name, category_set__category_set__camp_year__year=category_set
        )
