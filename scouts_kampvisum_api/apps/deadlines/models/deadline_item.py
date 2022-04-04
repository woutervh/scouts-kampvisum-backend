from django.db import models
from django.db.models import Q

from apps.deadlines.models import Deadline, DeadlineFlag
from apps.deadlines.models.enums import DeadlineItemType
from apps.deadlines.managers import DeadlineItemManager

from apps.visums.models import SubCategory, Check

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import DefaultCharField
from scouts_auth.inuits.models.mixins import Indexable


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineItem(Indexable, AbstractBaseModel):
    objects = DeadlineItemManager()

    deadline = models.ForeignKey(
        Deadline, on_delete=models.CASCADE, related_name="items"
    )
    deadline_item_type = DefaultCharField(
        choices=DeadlineItemType.choices,
        default=DeadlineItemType.DEADLINE,
        max_length=1,
    )
    item_flag = models.ForeignKey(
        DeadlineFlag,
        on_delete=models.CASCADE,
        related_name="deadline_item",
        null=True,
        blank=True,
    )
    item_sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    item_check = models.ForeignKey(
        Check,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["index"]
        constraints = [
            models.UniqueConstraint(
                fields=["deadline", "deadline_item_type", "item_flag"],
                condition=(Q(item_sub_category=None) & Q(item_check=None)),
                name="unique_deadline_type_and_flag_if_null_sub_category_and_null_check",
            ),
            models.UniqueConstraint(
                fields=["deadline", "deadline_item_type", "item_sub_category"],
                condition=(Q(item_flag=None) & Q(item_check=None)),
                name="unique_deadline_type_and_sub_category_if_null_flag_and_null_check",
            ),
            models.UniqueConstraint(
                fields=["deadline", "deadline_item_type", "item_check"],
                condition=(Q(item_flag=None) & Q(item_sub_category=None)),
                name="unique_deadline_type_and_check_if_null_flag_and_null_sub_category",
            ),
        ]

    def is_deadline(self):
        return self.deadline_item_type == DeadlineItemType.DEADLINE

    def is_sub_category_deadline(self):
        return self.deadline_item_type == DeadlineItemType.LINKED_SUB_CATEGORY

    def is_check_deadline(self):
        return self.deadline_item_type == DeadlineItemType.LINKED_CHECK

    def is_mixed_deadline(self):
        return self.deadline_item_type == DeadlineItemType.MIXED

    def has_sub_categories(self):
        return (
            (self.is_sub_category_deadline() or self.is_mixed_deadline())
            and self.sub_categories
            and len(self.sub_categories) > 0
        )

    def has_checks(self):
        return (
            (self.is_check_deadline() or self.is_mixed_deadline())
            and self.checks
            and len(self.checks) > 0
        )

    def has_flags(self):
        return self.is_deadline() and self.flags and len(self.flags) > 0
