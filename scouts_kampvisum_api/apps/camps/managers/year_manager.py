from django.db import models


import logging

logger = logging.getLogger(__name__)


class CampYearManager(models.Manager):
    """
    Loads CampYear instances by their integer year, not their id/uuid.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, year):
        logger.trace(
            "GET BY NATURAL KEY %s: (year: %s (%s))",
            "CampYear",
            year,
            type(year).__name__,
        )
        return self.get(year=year)
