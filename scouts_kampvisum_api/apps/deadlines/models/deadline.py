from django.db import models

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.managers import DeadlineManager

from apps.visums.models import CampVisum, LinkedSubCategory, LinkedCheck


class Deadline(DefaultDeadline):

    objects = DeadlineManager()

    visum = models.ForeignKey(
        CampVisum, on_delete=models.CASCADE, related_name="deadlines"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deadline_type = DeadlineType.DEADLINE

    def __str__(self):
        return "visum ({}), {}".format(self.visum.id, super().__str__())


class LinkedSubCategoryDeadline(Deadline):

    linked_sub_category = models.ForeignKey(
        LinkedSubCategory, on_delete=models.CASCADE, related_name="deadline"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deadline_type = DeadlineType.LINKED_SUB_CATEGORY

    def __str__(self) -> str:
        return "{}, linked_sub_category ({})".format(
            super().__str__(), self.sub_category
        )


class LinkedCheckDeadline(Deadline):

    linked_check = models.ForeignKey(LinkedCheck, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deadline_type = DeadlineType.LINKED_CHECK

    def __str__(self) -> str:
        return "{}, linked_check ({})".format(super().__str__(), self.check)
