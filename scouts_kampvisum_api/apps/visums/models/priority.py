from django.db import models

from apps.visums.managers import PriorityManager

from scouts_auth.inuits.models import AbstractBaseModel


class CategorySetPriority(AbstractBaseModel):

    owner = models.CharField(max_length=32, unique=True, default="Verbond")
    priority = models.IntegerField(default=100)

    objects = PriorityManager()

    class Meta:
        ordering = ["priority"]
        constraints = [
            models.UniqueConstraint(fields=["owner"], name="unique_owner"),
            models.UniqueConstraint(fields=["priority"], name="unique_priority"),
        ]

    def natural_key(self):
        return (self.owner,)
