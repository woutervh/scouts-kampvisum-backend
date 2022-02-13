from django.db import models

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.managers import (
    DeadlineManager,
    LinkedSubCategoryDeadlineManager,
    LinkedCheckDeadlineManager,
    MixedDeadlineManager,
)

from apps.visums.models import CampVisum, LinkedSubCategory, LinkedCheck

from scouts_auth.inuits.models import AuditedBaseModel


class Deadline(AuditedBaseModel):

    objects = DeadlineManager()

    parent = models.ForeignKey(
        DefaultDeadline, on_delete=models.CASCADE, related_name="deadline"
    )
    visum = models.ForeignKey(
        CampVisum, on_delete=models.CASCADE, related_name="deadlines"
    )

    class Meta:
        unique_together = ("parent", "visum")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deadline_type = DeadlineType.DEADLINE

    def __str__(self):
        return "visum ({}), parent({})".format(self.visum.id, self.parent)


class LinkedSubCategoryDeadline(Deadline):

    objects = LinkedSubCategoryDeadlineManager()

    linked_sub_categories = models.ManyToManyField(LinkedSubCategory)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deadline_type = DeadlineType.LINKED_SUB_CATEGORY

    def __str__(self) -> str:
        return "{}, linked_sub_categories ({})".format(
            super().__str__(), str(self.linked_sub_categories)
        )


class LinkedCheckDeadline(Deadline):

    objects = LinkedCheckDeadlineManager()

    linked_checks = models.ManyToManyField(LinkedCheck)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deadline_type = DeadlineType.LINKED_CHECK

    def __str__(self) -> str:
        return "{}, linked_checks ({})".format(
            super().__str__(), str(self.linked_checks)
        )


class MixedDeadline(Deadline):

    objects = MixedDeadlineManager()

    linked_sub_categories = models.ManyToManyField(LinkedSubCategory)
    linked_checks = models.ManyToManyField(LinkedCheck)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deadline_type = DeadlineType.MIXED

    def __str__(self) -> str:
        return "{}, linked_sub_categories ({}), linked_checks ({})".format(
            super().__str__(), str(self.linked_sub_categories), str(self.linked_checks)
        )


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
