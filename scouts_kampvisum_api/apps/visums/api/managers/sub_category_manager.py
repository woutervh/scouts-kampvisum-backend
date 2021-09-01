from django.db import models


class SubCategoryManager(models.Manager):
    """
    Loads Category instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name):
        return self.get(name=name)
