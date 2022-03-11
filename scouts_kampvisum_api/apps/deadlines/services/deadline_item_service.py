from typing import List

from django.db import transaction
from django.core.exceptions import ValidationError

from apps.deadlines.models import (
    Deadline,
    DeadlineItem,
    DeadlineFlag,
)
from apps.deadlines.models.enums import DeadlineItemType
from apps.deadlines.services import DeadlineFlagService

from apps.visums.models import SubCategory, Check


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineItemService:

    deadline_flag_service = DeadlineFlagService()

    @transaction.atomic
    def create_or_update_deadline_items(
        self, request, deadline: Deadline, items: List[dict]
    ) -> List[DeadlineItem]:
        results = []
        for item in items:
            results.append(
                self.create_or_update_deadline_item(request, deadline=deadline, **item)
            )

        return results

    @transaction.atomic
    def create_or_update_deadline_item(self, request, deadline, **item) -> DeadlineItem:
        instance = DeadlineItem.objects.safe_get(deadline=deadline, **item)

        if instance:
            instance: DeadlineItem = self.update_deadline_item(
                request=request, instance=instance, **item
            )
        else:
            instance: DeadlineItem = self.create_deadline_item(
                request=request, deadline=deadline, **item
            )

        return instance

    @transaction.atomic
    def create_deadline_item(
        self, request, deadline: Deadline, **fields
    ) -> DeadlineItem:
        logger.debug("ITEM: %s", fields)
        sub_category: dict = fields.get("item_sub_category", None)
        check: dict = fields.get("item_check", None)
        flag: dict = fields.get("item_flag", None)

        instance = DeadlineItem()

        instance.deadline = deadline
        instance.index = fields.get("index", 0)

        if sub_category:
            instance.deadline_item_type = DeadlineItemType.LINKED_SUB_CATEGORY
            item_sub_category: SubCategory = SubCategory.objects.get_by_natural_key(
                name=sub_category[0], category=sub_category[1]
            )
            if not item_sub_category:
                raise ValidationError(
                    "SubCategory not found: {}".format(sub_category[0])
                )

            instance.item_sub_category = item_sub_category
        elif check:
            instance.deadline_item_type = DeadlineItemType.LINKED_CHECK
            item_check = Check.objects.get_by_natural_key(
                name=check[0], sub_category=check[1]
            )
            if not item_check:
                raise ValidationError("Check not found: {}".format(check[0]))

            instance.item_check = item_check
        elif flag:
            instance.deadline_item_type = DeadlineItemType.DEADLINE
            instance.item_flag = self.deadline_flag_service.get_or_create_flag(**flag)
        else:
            raise ValidationError(
                "A DeadlineItem needs to be linked to a DeadlineFlag, a SubCategory or a Check instance"
            )

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update_deadline_item(
        self, request, instance: DeadlineItem, **fields
    ) -> DeadlineItem:
        sub_category: SubCategory = fields.get("item_sub_category", None)
        check: Check = fields.get("item_check", None)
        flag: DeadlineFlag = fields.get("item_flag", None)

        instance.index = fields.get("index", 0)

        if sub_category:
            instance.item_check = None
            instance.item_flag = None

            instance.deadline_item_type = DeadlineItemType.LINKED_SUB_CATEGORY
            instance.item_sub_category = SubCategory.objects.get_by_natural_key(
                name=sub_category[0], category=sub_category[1]
            )
        elif check:
            instance.item_sub_category = None
            instance.item_flag = None

            instance.deadline_item_type = DeadlineItemType.LINKED_CHECK
            instance.item_check = Check.objects.get_by_natural_key(
                name=check[0], sub_category=check[1]
            )
        elif flag:
            instance.item_sub_category = None
            instance.item_check = None

            instance.deadline_item_type = DeadlineItemType.DEADLINE
            instance.item_flag = self.deadline_flag_service.get_or_create_flag(**flag)
        else:
            raise ValidationError(
                "A DeadlineItem needs to be linked to a DeadlineFlag, a SubCategory or a Check instance"
            )

        instance.full_clean()
        instance.save()

        return instance
