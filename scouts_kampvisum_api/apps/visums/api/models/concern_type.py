from django.db import models

from ..managers import ConcernTypeManager
from apps.base.models import BaseModel
from inuits.models import RequiredCharField


class ConcernType(BaseModel):

    type = RequiredCharField(max_length=32)

    objects = ConcernTypeManager()

    class Meta:
        ordering = ["type"]
        constraints = [models.UniqueConstraint(fields=["type"], name="unique_type")]

    def natural_key(self):
        return (self.type,)
