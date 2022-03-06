from django.db import models

from apps.deadlines.models import DefaultDeadlineFlag
from apps.deadlines.models.enums import DeadlineItemType
from apps.deadlines.managers import DefaultDeadlineItemManager

from apps.visums.models import SubCategory, Check

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import DefaultCharField
from scouts_auth.inuits.models.interfaces import Indexable


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultDeadlineItem(Indexable, AbstractBaseModel):
    objects = DefaultDeadlineItemManager()

    deadline_item_type = DefaultCharField(
        choices=DeadlineItemType.choices,
        default=DeadlineItemType.DEADLINE,
        max_length=1,
    )
    item_flag = models.ForeignKey(
        DefaultDeadlineFlag,
        on_delete=models.CASCADE,
        related_name="default_deadline_item",
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
