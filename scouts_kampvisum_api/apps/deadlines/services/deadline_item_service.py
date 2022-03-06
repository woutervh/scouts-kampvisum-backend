from typing import List

from apps.deadlines.models import (
    DefaultDeadline,
    Deadline,
    DefaultDeadlineItem,
    DeadlineItem,
    DeadlineFlag,
)
from apps.deadlines.services import DeadlineFlagService

from apps.visums.models import LinkedSubCategory, LinkedCheck


class DeadlineItemService:

    deadline_flag_service = DeadlineFlagService()

    def create_or_update_deadline_items(
        self, request, deadline: Deadline
    ) -> List[DeadlineItem]:
        results = []
        for item in deadline.parent.items.all():
            results.append(
                self.create_deadline_item(
                    request=request, deadline=deadline, default_deadline_item=item
                )
            )

        return results

    def create_deadline_item(
        self, request, deadline: Deadline, default_deadline_item: DefaultDeadlineItem
    ) -> DeadlineItem:
        deadline_item: DeadlineItem = DeadlineItem()

        deadline_item.parent = default_deadline_item

        if default_deadline_item.item_sub_category:
            deadline_item.linked_sub_category = LinkedSubCategory.objects.safe_get(
                parent=default_deadline_item.item_sub_category,
                visum=deadline.visum,
                raise_error=True,
            )
        elif default_deadline_item.item_check:
            deadline_item.linked_check = LinkedCheck.objects.safe_get(
                parent=default_deadline_item.item_check,
                visum=deadline.visum,
                raise_error=True,
            )
        elif default_deadline_item.item_flag:
            flag: DeadlineFlag = DeadlineFlag.objects.safe_get(
                parent=default_deadline_item.item_flag,
                deadline=deadline,
            )

            if not flag:
                flag: DeadlineFlag = (
                    self.deadline_flag_service.get_or_create_deadline_flag(
                        request=request,
                        deadline=deadline,
                        default_deadline_flag=default_deadline_item.item_flag,
                    )
                )

            deadline_item.flag = flag

        deadline_item.full_clean()
        deadline_item.save()

        return deadline_item
