import datetime

from django.db import models
from django.utils import timezone

from apps.deadlines.models import Deadline
from apps.deadlines.managers import DeadlineDateManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import (
    OptionalIntegerField,
    DatetypeAwareDateField,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineDate(AbstractBaseModel):

    objects = DeadlineDateManager()

    deadline = models.OneToOneField(
        Deadline, on_delete=models.CASCADE, related_name="due_date"
    )
    date_day = OptionalIntegerField()
    date_month = OptionalIntegerField()
    date_year = OptionalIntegerField()
    calculated_date = DatetypeAwareDateField()

    class Meta:
        ordering = ["date_year", "date_month", "date_day"]
        constraints = [
            models.UniqueConstraint(fields=["deadline"], name="unique_deadline")
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED DeadlineDate")
        return (self.deadline,)

    def to_date(self) -> datetime.date:
        day = self.date_day if self.date_day else 1
        month = self.date_month if self.date_month else 1
        year = self.date_year if self.date_year else timezone.now().date().year

        return datetime.date(year, month, day)
