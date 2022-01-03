import logging

from django.db import models


logger = logging.getLogger(__name__)


class CategorySetManager(models.Manager):
    """
    Loads CategorySet instances by their camp year category set, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, category_set, group_type):
        logger.debug(
            "GET BY NATURAL KEY %s: (category_set: %s (%s), group_type: %s (%s))",
            "CategorySet",
            category_set,
            type(category_set).__name__,
            group_type,
            type(group_type).__name__,
        )

        if type(group_type).__name__ == "ScoutsGroupType":
            return self.get(
                category_set__camp_year__year=category_set, group_type=group_type
            )

        return self.get(
            category_set__camp_year__year=category_set,
            group_type__group_type=group_type,
        )
