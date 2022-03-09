from typing import List

from django.core.exceptions import ValidationError

from apps.deadlines.models import (
    DefaultDeadline,
    DefaultDeadlineItem,
    DefaultDeadlineFlag,
)
from apps.deadlines.models.enums import DeadlineItemType
from apps.deadlines.services import DefaultDeadlineFlagService

from apps.visums.models import SubCategory, Check


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultDeadlineItemService:

    default_deadline_flag_service = DefaultDeadlineFlagService()

    def create_or_update_default_deadline_items(
        self, request, default_deadline: DefaultDeadline, items: List[dict]
    ) -> List[DefaultDeadlineItem]:
        current_items: List[DefaultDeadlineItem] = default_deadline.items.all()

        default_deadline.items.clear()

        results = []
        for item in items:
            instance = DefaultDeadlineItem.objects.safe_get(**item)

            if instance:
                instance: DefaultDeadlineItem = self.update_default_deadline_item(
                    request=request, instance=instance, **item
                )
            else:
                instance: DefaultDeadlineItem = self.create_default_deadline_item(
                    request=request, **item
                )

            results.append(instance)

            default_deadline.items.add(instance)

        return results

    def create_default_deadline_item(
        self, request, default_deadline: DefaultDeadline, **fields
    ) -> DefaultDeadlineItem:
        logger.debug("ITEM: %s", fields)
        sub_category: SubCategory = fields.get("item_sub_category", None)
        check: Check = fields.get("item_check", None)
        flag: DefaultDeadlineFlag = fields.get("item_flag", None)

        item: DefaultDeadlineItem = DefaultDeadlineItem()

        item.index = fields.get("index", 0)

        if sub_category:
            item.deadline_item_type = DeadlineItemType.LINKED_SUB_CATEGORY
            item.item_sub_category = SubCategory.objects.get_by_natural_key(
                name=sub_category[0], category=sub_category[1]
            )
        elif check:
            item.deadline_item_type = DeadlineItemType.LINKED_CHECK
            item.item_check = Check.objects.get_by_natural_key(
                name=check[0], sub_category=check[1]
            )
        elif flag:
            item.deadline_item_type = DeadlineItemType.DEADLINE
            item.item_flag = (
                self.default_deadline_flag_service.get_or_create_default_flag(**flag)
            )
        else:
            raise ValidationError(
                "A DefaultDeadlineItem needs to be linked to a DefaultDeadlineFlag, a SubCategory or a Check instance"
            )

        item.full_clean()
        item.save()

        return item

    def update_default_deadline_item(
        self, request, instance: DefaultDeadlineItem, **fields
    ) -> DefaultDeadlineItem:
        return instance
