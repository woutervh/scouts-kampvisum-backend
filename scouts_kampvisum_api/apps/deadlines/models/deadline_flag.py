from django.db import models

from apps.deadlines.models import DefaultDeadlineFlag
from apps.deadlines.managers import DeadlineFlagManager

from scouts_auth.inuits.models import AuditedBaseModel

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineFlag(AuditedBaseModel):

    objects = DeadlineFlagManager()

    parent = models.ForeignKey(DefaultDeadlineFlag, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)
