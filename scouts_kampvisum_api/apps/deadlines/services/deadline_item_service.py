from typing import List

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

    def create_or_update_deadline_items(
        self, request, deadline: Deadline, items: List[dict]
    ) -> List[DeadlineItem]:
        current_items: List[DeadlineItem] = deadline.items.all()

        deadline.items.clear()

        results = []
        for item in items:
            results.append(
                self.create_or_update_deadline_item(request, deadline=deadline, **item)
            )

        return results

    def create_or_update_deadline_item(self, request, deadline, **item) -> DeadlineItem:
        instance = DeadlineItem.objects.safe_get(**item)

        if instance:
            instance: DeadlineItem = self.update_deadline_item(
                request=request, instance=instance, **item
            )
        else:
            instance: DeadlineItem = self.create_deadline_item(
                request=request, deadline=deadline, **item
            )

        deadline.items.add(instance)

        return instance

    def create_deadline_item(
        self, request, deadline: Deadline, **fields
    ) -> DeadlineItem:
        # logger.debug("ITEM: %s", fields)
        sub_category: SubCategory = fields.get("item_sub_category", None)
        check: Check = fields.get("item_check", None)
        flag: DeadlineFlag = fields.get("item_flag", None)

        instance = DeadlineItem()

        instance.index = fields.get("index", 0)

        if sub_category:
            instance.deadline_item_type = DeadlineItemType.LINKED_SUB_CATEGORY
            instance.item_sub_category = SubCategory.objects.get_by_natural_key(
                name=sub_category[0], category=sub_category[1]
            )
        elif check:
            instance.deadline_item_type = DeadlineItemType.LINKED_CHECK
            instance.item_check = Check.objects.get_by_natural_key(
                name=check[0], sub_category=check[1]
            )
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
