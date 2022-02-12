import logging

from django.db import models

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
        unique_together = ("name", "deadline_type")

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED DefaultDeadline")
        return (self.name, self.deadline_type)

    def is_deadline(self):
        return self.deadline_type == DeadlineType.DEADLINE

    def is_sub_category_deadline(self):
        return self.deadline_type == DeadlineType.LINKED_SUB_CATEGORY

    def has_sub_categories(self):
        return (
            self.is_sub_category_deadline()
            and self.sub_categories
            and len(self.sub_categories) > 0
        )

    def is_check_deadline(self):
        return self.deadline_type == DeadlineType.LINKED_CHECK

    def has_checks(self):
        return self.is_check_deadline() and self.checks and len(self.checks) > 0

    def has_flags(self):
        return self.is_deadline() and self.flags and len(self.flags) > 0

    def __str__(self) -> str:
        return "id ({}), name ({}), deadline_type ({}), is_important ({}), label ({}), description ({}), explanation ({})".format(
            self.id,
            self.name,
            self.deadline_type,
            self.is_important,
            self.label,
            self.description,
            self.explanation,
        )
