import logging

from django.db import models

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.managers import DeadlineFlagManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Indexable, Translatable


logger = logging.getLogger(__name__)


class DeadlineFlag(Indexable, Translatable, AbstractBaseModel):

    objects = DeadlineFlagManager()

    default_deadline = models.ForeignKey(
        DefaultDeadline, on_delete=models.CASCADE, related_name="flags"
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
        return (self.name,)

    def get_by_natural_key(self, default_deadline, name):
        logger.debug(
            "GET BY NATURAL KEY %s: (default_deadline: %s (%s),  name: %s (%s))",
            "DefaultDeadline",
            default_deadline,
            type(default_deadline).__name__,
            name,
            type(name).__name__,
        )

        return self.get(default_deadline, name=name)
