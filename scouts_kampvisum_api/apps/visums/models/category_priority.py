from django.db import models

from apps.visums.managers import CategoryPriorityManager

from scouts_auth.inuits.models import AbstractBaseModel


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CategoryPriority(AbstractBaseModel):

    objects = CategoryPriorityManager()

    owner = models.CharField(max_length=32, unique=True, default="Verbond")
    priority = models.IntegerField(default=10)

    class Meta:
        ordering = ["priority"]
        constraints = [
            models.UniqueConstraint(fields=["owner"], name="unique_owner"),
            models.UniqueConstraint(fields=["priority"], name="unique_priority"),
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED CategoryPriority")
        return (self.owner,)

    def __str__(self):
        return "OBJECT CategoryPriority: owner({}), priority({})".format(
            self.owner, self.priority
        )
