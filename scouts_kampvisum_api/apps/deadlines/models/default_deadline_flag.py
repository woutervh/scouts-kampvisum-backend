from django.db import models

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.managers import DefaultDeadlineFlagManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Indexable, Translatable


import logging

logger = logging.getLogger(__name__)


class DefaultDeadlineFlag(Indexable, Translatable, AbstractBaseModel):

    objects = DefaultDeadlineFlagManager()

    default_deadline = models.ForeignKey(
        DefaultDeadline, on_delete=models.CASCADE, related_name="default_flags"
    )
    name = RequiredCharField()
    flag = models.BooleanField(default=False)

    class Meta:
        ordering = ["index", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["default_deadline", "name"],
                name="unique_default_deadline_and_name_for_flag",
            )
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED DefaultDeadlineFlag")
        return (self.name,)

    def get_by_natural_key(self, default_deadline, name):
        logger.trace(
            "GET BY NATURAL KEY %s: (default_deadline: %s (%s),  name: %s (%s))",
            "DefaultDeadline",
            default_deadline,
            type(default_deadline).__name__,
            name,
            type(name).__name__,
        )

        return self.get(default_deadline, name=name)
