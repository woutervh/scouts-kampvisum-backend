import logging

from django.db import models

from apps.visums.managers import CategorySetPriorityManager

from scouts_auth.inuits.models import AbstractBaseModel


logger = logging.getLogger(__name__)


class CategorySetPriority(AbstractBaseModel):

    objects = CategorySetPriorityManager()

    owner = models.CharField(max_length=32, unique=True, default="Verbond")
    priority = models.IntegerField(default=100)

    class Meta:
        ordering = ["priority"]
        constraints = [
            models.UniqueConstraint(fields=["owner"], name="unique_owner"),
            models.UniqueConstraint(fields=["priority"], name="unique_priority"),
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED CategorySetPriority")
        return (self.owner,)

    def __str__(self):
        return "OBJECT CategorySetPriority: owner({}), priority({})".format(
            self.owner, self.priority
        )
