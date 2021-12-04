from django.db import models


class ScoutsSectionNameManager(models.Manager):
    """
    Loads ScoutsSectionName instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name):
        return self.get(name=name)
