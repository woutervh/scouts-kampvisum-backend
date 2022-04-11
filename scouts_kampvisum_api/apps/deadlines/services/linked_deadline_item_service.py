from typing import List

from django.db import transaction
from django.core.exceptions import ValidationError

from apps.deadlines.models import (
    Deadline,
    LinkedDeadline,
    DeadlineItem,
    LinkedDeadlineItem,
    LinkedDeadlineFlag,
)
from apps.deadlines.services import LinkedDeadlineFlagService

from apps.visums.models import LinkedSubCategory, LinkedCheck


class LinkedDeadlineItemService:

    linked_deadline_flag_service = LinkedDeadlineFlagService()

    @transaction.atomic
    def create_or_update_linked_deadline_items(
        self, request, linked_deadline: LinkedDeadline
    ) -> List[LinkedDeadlineItem]:
        items: List[DeadlineItem] = linked_deadline.parent.items.all()
        if not items or len(items) == 0:
            raise ValidationError(
                "No DeadlineItem instances linked to Deadline {}".format(
                    linked_deadline.parent.name,
                )
            )

        results = []
        for item in items:
            results.append(
                self.create_linked_deadline_item(
                    request=request, linked_deadline=linked_deadline, deadline_item=item
                )
            )

        return results

    @transaction.atomic
    def create_linked_deadline_item(
        self, request, linked_deadline: LinkedDeadline, deadline_item: DeadlineItem
    ) -> LinkedDeadlineItem:
        linked_deadline_item = LinkedDeadlineItem()

        linked_deadline_item.parent = deadline_item
        linked_deadline_item.linked_deadline = linked_deadline
        linked_deadline_item.linked_deadline_fix = linked_deadline.id

        if deadline_item.item_sub_category:
            linked_deadline_item.linked_sub_category = (
                LinkedSubCategory.objects.safe_get(
                    parent=deadline_item.item_sub_category,
                    visum=linked_deadline.visum,
                    raise_error=True,
                )
            )
        elif deadline_item.item_check:
            linked_deadline_item.linked_check = LinkedCheck.objects.safe_get(
                parent=deadline_item.item_check,
                visum=linked_deadline.visum,
                raise_error=True,
            )
        elif deadline_item.item_flag:
            flag: LinkedDeadlineFlag = LinkedDeadlineFlag.objects.safe_get(
                parent=deadline_item.item_flag,
                linked_deadline=linked_deadline,
            )

            if not flag:
                flag: LinkedDeadlineFlag = self.linked_deadline_flag_service.get_or_create_linked_deadline_flag(
                    request=request,
                    linked_deadline=linked_deadline,
                    deadline_flag=deadline_item.item_flag,
                )

            linked_deadline_item.flag = flag

        linked_deadline_item.full_clean()
        linked_deadline_item.save()

        return linked_deadline_item
