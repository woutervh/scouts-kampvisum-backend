from django.db import models

from apps.visums.managers import ConcernTypeManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField


class ConcernType(AbstractBaseModel):

    type = RequiredCharField(max_length=32)

    objects = ConcernTypeManager()

    class Meta:
        ordering = ["type"]
        constraints = [models.UniqueConstraint(fields=["type"], name="unique_type")]

    def natural_key(self):
        return (self.type,)
