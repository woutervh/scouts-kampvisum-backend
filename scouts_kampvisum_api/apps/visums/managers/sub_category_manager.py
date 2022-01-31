import logging

from django.db import models


logger = logging.getLogger(__name__)


class SubCategoryManager(models.Manager):
    """
    Loads Category instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name, category):
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s), category: %s (%s))",
            "SubCategory",
            name,
            type(name).__name__,
            category,
            type(category).__name__,
        )

        if isinstance(category, list):
            return self.get(
                name=name,
                category__name=category[0],
                category__camp_year__year=category[1],
            )

        return self.get(name=name, category=category)
