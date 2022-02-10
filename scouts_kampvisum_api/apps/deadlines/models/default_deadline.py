from django.db import models

from apps.deadlines.models import DeadlineDate
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.managers import DefaultDeadlineManager


from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, DefaultCharField
from scouts_auth.inuits.models.interfaces import Describable, Explainable, Translatable


class DefaultDeadline(Describable, Explainable, Translatable, AuditedBaseModel):

    objects = DefaultDeadlineManager()

    name = RequiredCharField()
    is_important = models.BooleanField(default=False)
    due_date = DeadlineDate()
    deadline_type = DefaultCharField(
        choices=DeadlineType.choices,
        default=DeadlineType.DEADLINE,
        max_length=1,
    )

    class Meta:
        unique_together = ("name", "deadline_type")

    def is_deadline(self):
        return self.deadline_type == DeadlineType.DEADLINE

    def is_sub_category_deadline(self):
        return self.deadline_type == DeadlineType.LINKED_SUB_CATEGORY

    def is_check_deadline(self):
        return self.deadline_type == DeadlineType.LINKED_CHECK

    def __str__(self) -> str:
        return "name ({}), important ({}), label ({}), description ({}), explanation ({})".format(
            self.name, self.important, self.label, self.description, self.explanation
        )
