from django.db import models

from ..managers import CampVisumConcernTypeManager
from apps.base.models import BaseModel
from inuits.models import RequiredCharField


class CampVisumConcernType(BaseModel):

    type = RequiredCharField(max_length=32)

    objects = CampVisumConcernTypeManager()

    class Meta:
        ordering = ["type"]
        constraints = [
            models.UniqueConstraint(
                fields=['type'], name='unique_type')
        ]

    def natural_key(self):
        return (self.type,)
