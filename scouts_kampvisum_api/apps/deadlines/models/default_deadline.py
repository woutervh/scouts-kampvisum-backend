import logging

from django.db import models

from apps.camps.models import CampYear, CampType

from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.managers import DefaultDeadlineManager

from apps.visums.models import SubCategory, Check


from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, DefaultCharField
from scouts_auth.inuits.models.interfaces import Describable, Explainable, Translatable


logger = logging.getLogger(__name__)


class DefaultDeadline(Describable, Explainable, Translatable, AuditedBaseModel):

    objects = DefaultDeadlineManager()

    name = RequiredCharField()
    is_important = models.BooleanField(default=False)
    deadline_type = DefaultCharField(
        choices=DeadlineType.choices,
        default=DeadlineType.DEADLINE,
        max_length=1,
    )
    camp_year = models.ForeignKey(
        CampYear, on_delete=models.CASCADE, related_name="default_deadline_set"
    )
    camp_types = models.ManyToManyField(CampType, related_name="deadlines")
    sub_categories = models.ManyToManyField(SubCategory)
    checks = models.ManyToManyField(Check)

    class Meta:
        ordering = [
            "due_date__date_year",
            "due_date__date_month",
            "due_date__date_day",
            "is_important",
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "deadline_type", "camp_year"],
                name="unique_name__deadline_type__camp_year",
            )
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED DefaultDeadline")
        return (self.name, self.deadline_type, self.camp_year)

    def is_deadline(self):
        return self.deadline_type == DeadlineType.DEADLINE

    def is_sub_category_deadline(self):
        return self.deadline_type == DeadlineType.LINKED_SUB_CATEGORY

    def has_sub_categories(self):
        return (
            (self.is_sub_category_deadline() or self.is_mixed_deadline())
            and self.sub_categories
            and len(self.sub_categories) > 0
        )

    def is_check_deadline(self):
        return self.deadline_type == DeadlineType.LINKED_CHECK

    def has_checks(self):
        return (
            (self.is_check_deadline() or self.is_mixed_deadline())
            and self.checks
            and len(self.checks) > 0
        )

    def is_mixed_deadline(self):
        return self.deadline_type == DeadlineType.MIXED

    def has_flags(self):
        return self.is_deadline() and self.flags and len(self.flags) > 0

    def __str__(self) -> str:
        return "id ({}), name ({}), deadline_type ({}), camp_year({}), camp_types ({}), is_important ({}), label ({}), description ({}), explanation ({})".format(
            self.id,
            self.name,
            self.deadline_type,
            self.camp_year.year,
            ",".join(camp_type.to_readable_str() for camp_type in self.camp_types),
            self.is_important,
            self.label,
            self.description,
            self.explanation,
        )
