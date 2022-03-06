from django.db import models

from apps.deadlines.models import DefaultDeadlineItem, DeadlineFlag

from apps.visums.models import LinkedSubCategory, LinkedCheck

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.interfaces import Indexable


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineItem(AbstractBaseModel, Indexable):

    parent = models.ForeignKey(
        DefaultDeadlineItem, on_delete=models.CASCADE, related_name="deadline_item"
    )

    linked_sub_category = models.ForeignKey(
        LinkedSubCategory,
        on_delete=models.CASCADE,
        related_name="deadline_items",
        null=True,
        blank=True,
    )
    linked_check = models.ForeignKey(
        LinkedCheck,
        on_delete=models.CASCADE,
        related_name="deadline_items",
        null=True,
        blank=True,
    )
    flag = models.ForeignKey(
        DeadlineFlag,
        on_delete=models.CASCADE,
        related_name="deadline_item",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["index"]

    def is_deadline(self):
        return self.parent.is_deadline()

    def is_sub_category_deadline(self):
        return self.parent.is_sub_category_deadline()

    def is_check_deadline(self):
        return self.parent.is_check_deadline()
