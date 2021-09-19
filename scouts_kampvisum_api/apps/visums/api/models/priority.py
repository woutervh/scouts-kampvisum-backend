from django.db import models

from ..managers import PriorityManager
from apps.base.models import BaseModel


class CategorySetPriority(BaseModel):

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
