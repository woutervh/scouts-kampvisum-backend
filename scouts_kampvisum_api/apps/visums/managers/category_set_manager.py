import logging

from django.db import models


logger = logging.getLogger(__name__)


class CategorySetManager(models.Manager):
    """
    Loads CategorySet instances by their camp year category set, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, category_set):
        logger.debug(
            "GET BY NATURAL KEY %s: (category_set: %s (%s)",
            "CategorySet",
            category_set,
            type(category_set).__name__,
        )
        
        return self.get(
            category_set__camp_year__year=category_set
        )
