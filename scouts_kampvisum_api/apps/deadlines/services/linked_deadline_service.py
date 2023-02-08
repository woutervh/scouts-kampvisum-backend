from typing import List

from django.utils import timezone
from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.camps.models import CampYear, CampType

from apps.deadlines.models import (
    Deadline,
    DeadlineDate,
    LinkedDeadline,
    LinkedDeadlineItem,
)
from apps.deadlines.services import DeadlineService, LinkedDeadlineItemService

from apps.visums.models import (
    CampVisum,
    SubCategory,
    LinkedSubCategory,
    Check,
    LinkedCheck,
)
from apps.visums.settings import VisumSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineService:

    deadline_service = DeadlineService()
    linked_deadline_item_service = LinkedDeadlineItemService()

    def get_camp_registration_deadline(self, visum: CampVisum) -> LinkedDeadline:
        return LinkedDeadline.objects.safe_get(
            parent_name=VisumSettings.get_camp_registration_deadline_name(),
            visum=visum,
            raise_error=True,
        )

    def are_camp_registration_deadline_items_checked(self, visum: CampVisum) -> bool:
        linked_deadline: LinkedDeadline = self.get_camp_registration_deadline(
            visum=visum
        )

        items: List[LinkedDeadlineItem] = linked_deadline.items.all()

        for item in items:
            if not item.is_checked():
                logger.debug(
                    "ITEM: %s (%s) - %s", type(item).__name__, item.id, item.name
                )
                return False

        return True

    @transaction.atomic
    def create_or_update_linked_deadline(
        self, request, deadline: Deadline = None, visum: CampVisum = None, **fields
    ) -> LinkedDeadline:
        if not deadline or not isinstance(deadline, Deadline):
            deadline = self.deadline_service.get_or_create_deadline(
                request=request, **fields.get("parent", {})
            )

        instance = LinkedDeadline.objects.safe_get(
            parent=deadline, visum=visum)
        if instance:
            return self.update_linked_deadline(
                request=request, instance=instance, deadline=deadline, **fields
            )
        else:
            return self.create_linked_deadline(
                request=request, deadline=deadline, visum=visum, **fields
            )

    @transaction.atomic
    def create_linked_deadline(
        self, request, deadline: Deadline = None, visum: CampVisum = None, **fields
    ) -> LinkedDeadline:
        instance = LinkedDeadline()

        instance.parent = deadline
        if not (visum and isinstance(visum, CampVisum)):
            visum = CampVisum.objects.safe_get(
                id=fields.get("visum", {}).get("id", None), raise_error=True
            )

        logger.debug(
            "Creating a %s instance for visum %s (%s), with name %s",
            "LinkedDeadline",
            visum.camp.name,
            visum.id,
            instance.parent.name,
        )

        instance.visum = visum
        instance.created_by = request.user

        instance.full_clean()
        instance.save()

        logger.debug(f"LINKED DEADLINE: {instance}")

        items: List[
            LinkedDeadlineItem
        ] = self.linked_deadline_item_service.create_or_update_linked_deadline_items(
            request=request, linked_deadline=instance
        )

        if len(items) == 0:
            raise ValidationError(
                "No LinkedDeadlineItem instances found to link to LinkedDeadline %s !",
                instance.parent.name,
            )

        # logger.debug(
        #     "Linking %d LinkedDeadlineItem instance(s) to LinkedDeadline %s",
        #     len(items),
        #     instance.parent.name,
        # )
        # for item in items:
        #     instance.items.add(item)

        return instance

    def get_linked_deadline(self, linked_deadline_id):
        return LinkedDeadline.objects.safe_get(id=linked_deadline_id, raise_error=True)

    @transaction.atomic
    def update_linked_deadline(self, request, instance: LinkedDeadline, **fields):
        logger.debug(
            "Updating %s instance with id %s", type(
                instance).__name__, instance.id
        )

        parent: Deadline = self.deadline_service.update_deadline(
            request=request, instance=instance.parent, **fields.get("parent", {})
        )

        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        if not (
            fields
            and isinstance(fields, dict)
            and "due_date" in fields
            and isinstance(fields.get("due_date"), dict)
        ):
            fields["due_date"] = dict()
        due_date: DeadlineDate = self.deadline_service.update_deadline_date(
            request=request,
            instance=instance.parent.due_date,
            **fields.get("due_date", None)
        )

        return instance

    @transaction.atomic
    def link_to_visum(self, request, visum: CampVisum):
        camp_year: CampYear = visum.camp.year
        camp_types: List[CampType] = visum.camp_types.all()

        deadlines: List[Deadline] = Deadline.objects.safe_get(
            camp_year=camp_year, camp_types=camp_types
        )

        if len(deadlines) == 0:
            raise ValidationError("No deadlines found to link to visum")

        logger.debug(
            "Found %d Deadline instances with camp year %s and camp types %s",
            len(deadlines),
            camp_year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
        )
        for deadline in deadlines:
            logger.debug(
                "Setting up LinkedDeadline %s (%s) for visum %s",
                deadline.name,
                deadline.id,
                visum.id,
            )
            linked_deadline: LinkedDeadline = self.create_or_update_linked_deadline(
                request=request, deadline=deadline, visum=visum
            )

    def list_for_visum(self, visum: CampVisum) -> List[LinkedDeadline]:
        return LinkedDeadline.objects.filter(visum=visum)

    def get_visum_deadline(self, linked_deadline: LinkedDeadline) -> LinkedDeadline:
        if linked_deadline and isinstance(linked_deadline, LinkedDeadline):
            return LinkedDeadline.objects.get(id=linked_deadline.id)

        return LinkedDeadline.objects.get(id=linked_deadline)

    @transaction.atomic
    def delete_linked_deadlines_for_visum(self, request, visum: CampVisum):
        linked_deadlines: List[LinkedDeadline] = visum.deadlines.all()

        for linked_deadline in linked_deadlines:
            linked_deadline.delete()
