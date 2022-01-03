import logging

from django.db import models

from apps.visums.managers import CheckTypeManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField


logger = logging.getLogger(__name__)


class CheckType(AbstractBaseModel):

    objects = CheckTypeManager()

    check_type = RequiredCharField(max_length=32)

    class Meta:
        ordering = ["check_type"]
        constraints = [
            models.UniqueConstraint(fields=["check_type"], name="unique_check_type")
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        return (self.check_type,)

    def __str__(self):
        return "OBJECT CheckType: check_type({})".format(self.check_type)
