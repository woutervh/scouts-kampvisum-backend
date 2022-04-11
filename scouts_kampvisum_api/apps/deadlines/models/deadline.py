from django.db import models

from apps.camps.models import CampYear, CampType

from apps.deadlines.managers import DeadlineManager

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.mixins import (
    Describable,
    Explainable,
    Indexable,
    Translatable,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Deadline(Describable, Explainable, Indexable, Translatable, AuditedBaseModel):

    objects = DeadlineManager()

    name = RequiredCharField()
    is_important = models.BooleanField(default=False)
    is_camp_registration = models.BooleanField(default=False)
    camp_year = models.ForeignKey(
        CampYear, on_delete=models.CASCADE, related_name="deadline_set"
    )
    camp_types = models.ManyToManyField(CampType, related_name="deadlines")

    class Meta:
        ordering = [
            "index",
            "due_date__date_year",
            "due_date__date_month",
            "due_date__date_day",
            "is_important",
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "camp_year"],
                name="unique_name__camp_year",
            )
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED Deadline")
        return (self.name, self.camp_year)

    def __str__(self) -> str:
        return "id ({}), name ({}), camp_year({}), camp_types ({}), is_important ({}), is_camp_registration ({}), label ({}), description ({}), explanation ({})".format(
            self.id,
            self.name,
            self.camp_year.year,
            ",".join(
                camp_type.to_readable_str() for camp_type in self.camp_types.all()
            ),
            self.is_important,
            self.is_camp_registration,
            self.label,
            self.description,
            self.explanation,
        )
