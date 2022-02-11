import logging

from django.db import models


logger = logging.getLogger(__name__)


class CheckManager(models.Manager):
    """
    Loads Check instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name, sub_category):
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s), sub_category: %s (%s))",
            "Check",
            name,
            type(name).__name__,
            sub_category,
            type(sub_category).__name__,
        )

        if isinstance(sub_category, list):
            return self.get(
                name=name,
                sub_category__name=sub_category[0],
                sub_category__category__name=sub_category[1][0],
                sub_category__category__camp_year__year=sub_category[1][1],
            )

        return self.get(name=name, sub_category=sub_category)
