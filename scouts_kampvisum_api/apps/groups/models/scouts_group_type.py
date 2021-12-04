from django.db import models

from apps.groups.managers import ScoutsGroupTypeManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField


class ScoutsGroupType(AbstractBaseModel):
    """
    Specifies the type of scouts group (e.g. AKABE, zeescouts, ...).
    """

    objects = ScoutsGroupTypeManager()

    type = RequiredCharField(max_length=64)
    parent = models.ForeignKey("ScoutsGroupType", null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ["type"]

    def natural_key(self):
        return (self.type,)
