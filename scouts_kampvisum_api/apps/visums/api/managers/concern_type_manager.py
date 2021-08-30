from django.db import models


class CampVisumConcernTypeManager(models.Manager):
    """
    Loads CampVisumConcernType instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, type):
        return self.get(type=type)
