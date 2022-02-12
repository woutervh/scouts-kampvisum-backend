import logging
import datetime

from django.db import models
from django.utils import timezone

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.managers import DeadlineDateManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalIntegerField


logger = logging.getLogger(__name__)


class DeadlineDate(AbstractBaseModel):

    objects = DeadlineDateManager()

    default_deadline = models.OneToOneField(
        DefaultDeadline, on_delete=models.CASCADE, related_name="due_date"
    )
    date_day = OptionalIntegerField()
    date_month = OptionalIntegerField()
    date_year = OptionalIntegerField()

    class Meta:
        ordering = ["date_year", "date_month", "date_day"]
        constraints = [
            models.UniqueConstraint(
                fields=["default_deadline"], name="unique_default_deadline"
            )
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED DeadlineDate")
        return (self.default_deadline,)

    def to_date(self) -> datetime.date:
        day = self.day if self.day else 1
        month = self.month if self.month else 1
        year = self.year if self.year else timezone.now().date().year

        return datetime.date(year, month, day)
