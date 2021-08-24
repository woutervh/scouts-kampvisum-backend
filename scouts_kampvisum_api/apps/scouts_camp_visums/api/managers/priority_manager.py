from django.db import models

class PriorityManager(models.Manager):

    def get_by_natural_key(self, owner):
        return self.get(owner=owner)

