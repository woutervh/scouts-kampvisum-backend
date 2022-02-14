import logging

from django.db import models

from apps.camps.models import CampYear, CampType

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.managers import DefaultDeadlineSetManager

from scouts_auth.inuits.models import AuditedBaseModel


logger = logging.getLogger(__name__)


class DefaultDeadlineSet(AuditedBaseModel):

    objects = DefaultDeadlineSetManager()

    camp_year = models.ForeignKey(
        CampYear, on_delete=models.CASCADE, related_name="default_deadline_set"
    )
    camp_type = models.ForeignKey(
        CampType, on_delete=models.CASCADE, related_name="default_deadline_set"
    )
    default_deadlines = models.ManyToManyField(DefaultDeadline)

    class Meta:
        unique_together = ("camp_year", "camp_type")

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED DefaultDeadlineSet")
        return (self.camp_year, self.camp_type)
