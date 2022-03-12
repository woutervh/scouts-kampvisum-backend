from django.db import models

from apps.deadlines.managers import DeadlineFlagManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, OptionalCharField
from scouts_auth.inuits.models.interfaces import Changeable, Indexable, Translatable


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineFlag(Changeable, Indexable, Translatable, AbstractBaseModel):

    objects = DeadlineFlagManager()

    name = RequiredCharField()
    flag = models.BooleanField(default=False)

    class Meta:
        ordering = ["index", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_deadline_flag_name")
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED DeadlineFlag")
        return (self.name,)
