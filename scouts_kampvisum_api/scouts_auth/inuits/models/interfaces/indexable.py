from django.db import models

from scouts_auth.inuits.models.fields import DefaultIntegerField


class Indexable(models.Model):

    index = DefaultIntegerField(default=0)

    class Meta:
        abstract = True

    def has_index(self) -> bool:
        return self.index >= 0
