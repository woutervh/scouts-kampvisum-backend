from django.db import models


class CampYearManager(models.Manager):
    """
    Loads CampYear instances by their integer year, not their id/uuid.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, year):
        return self.get(year=year)
