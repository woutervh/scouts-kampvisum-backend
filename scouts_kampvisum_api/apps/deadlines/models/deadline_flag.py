from django.db import models

from apps.deadlines.models import DefaultDeadlineFlag, Deadline
from apps.deadlines.managers import DeadlineFlagManager

from scouts_auth.inuits.models import AuditedBaseModel

import logging

logger = logging.getLogger(__name__)


class DeadlineFlag(AuditedBaseModel):

    objects = DeadlineFlagManager()

    parent = models.ForeignKey(DefaultDeadlineFlag, on_delete=models.CASCADE)
    deadline = models.ForeignKey(
        Deadline, on_delete=models.CASCADE, related_name="flags"
    )
    flag = models.BooleanField(default=False)

    class Meta:
        unique_together = ("parent", "deadline")
