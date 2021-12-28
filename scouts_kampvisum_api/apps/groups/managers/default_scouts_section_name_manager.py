from django.db import models

# from apps.groups.models import ScoutsGroupType, ScoutsSectionName

class DefaultScoutsSectionNameManager(models.Manager):
    """
    Loads DefaultScoutsSectionName instances by their group type and name, not their id.

    This is useful for defining fixtures.
    """
    
    # def get_by_natural_key(self, type: ScoutsGroupType, name: ScoutsSectionName):
    def get_by_natural_key(self, type, name):
        return self.get(type=type, name=name)
    