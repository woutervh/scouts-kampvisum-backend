from django.db import models

from apps.deadlines.models import DeadlineFlag
from apps.deadlines.managers import LinkedDeadlineFlagManager

from scouts_auth.inuits.models import AuditedBaseModel

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineFlag(AuditedBaseModel):

    objects = LinkedDeadlineFlagManager()

    parent = models.ForeignKey(DeadlineFlag, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)
