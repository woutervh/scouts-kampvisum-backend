from django.db import models

from scouts_auth.inuits.models.fields import DefaultIntegerField


class Indexable(models.Model):
    """Provides an index to order a list of objects (field name: index)"""

    index = DefaultIntegerField(default=0)

    class Meta:
        abstract = True

    def has_index(self) -> bool:
        return self.index >= 0
