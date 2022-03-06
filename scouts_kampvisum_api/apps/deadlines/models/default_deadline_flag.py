from django.db import models

from apps.deadlines.managers import DefaultDeadlineFlagManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Indexable, Translatable


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultDeadlineFlag(Indexable, Translatable, AbstractBaseModel):

    objects = DefaultDeadlineFlagManager()

    name = RequiredCharField()
    flag = models.BooleanField(default=False)

    class Meta:
        ordering = ["index", "name"]
        constraints = [
            # models.UniqueConstraint(
            #     fields=["default_deadline_item", "name"],
            #     name="unique_default_deadline_item_and_name_for_flag",
            # )
            models.UniqueConstraint(
                fields=["name"], name="unique_default_deadline_flag_name"
            )
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED DefaultDeadlineFlag")
        return (self.name,)
