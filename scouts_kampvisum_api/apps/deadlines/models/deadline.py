from django.db import models

from apps.deadlines.models import DefaultDeadline, DeadlineItem
from apps.deadlines.managers import DeadlineManager

from apps.visums.models import CampVisum


from scouts_auth.inuits.models import AuditedBaseModel


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Deadline(AuditedBaseModel):

    objects = DeadlineManager()

    parent = models.ForeignKey(
        DefaultDeadline, on_delete=models.CASCADE, related_name="deadline"
    )
    visum = models.ForeignKey(
        CampVisum, on_delete=models.CASCADE, related_name="deadlines"
    )
    items = models.ManyToManyField(DeadlineItem)

    class Meta:
        unique_together = ("parent", "visum")

    def __str__(self):
        return "visum ({}), parent({})".format(self.visum.id, self.parent)


class DeadlineFactory:
    @staticmethod
    def get_deadline_fields(default_deadline: DefaultDeadline) -> dict:
        return {
            "name": default_deadline.name,
            "label": default_deadline.label,
            "description": default_deadline.description,
            "explanation": default_deadline.explanation,
            "is_important": default_deadline.is_important,
            "deadline_type": default_deadline.deadline_type,
        }
