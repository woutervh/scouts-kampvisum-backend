from django.db import models

from apps.deadlines.models import Deadline, LinkedDeadlineItem
from apps.deadlines.managers import LinkedDeadlineManager

from apps.visums.models import CampVisum


from scouts_auth.inuits.models import AuditedBaseModel


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadline(AuditedBaseModel):

    objects = LinkedDeadlineManager()

    parent = models.ForeignKey(
        Deadline, on_delete=models.CASCADE, related_name="deadline"
    )
    visum = models.ForeignKey(
        CampVisum, on_delete=models.CASCADE, related_name="deadlines"
    )
    items = models.ManyToManyField(LinkedDeadlineItem, related_name="deadline")

    class Meta:
        unique_together = ("parent", "visum")

    def __str__(self):
        return "visum ({}), parent({})".format(self.visum.id, self.parent)
