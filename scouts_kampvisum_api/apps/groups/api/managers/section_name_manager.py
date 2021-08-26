from django.db import models


class SectionNameManager(models.Manager):
    """
    Loads SectionName instances by their name, not their id.
    
    This is useful for defining fixtures.
    """
    
    def get_by_natural_key(self, name):
        return self.get(name=name)

