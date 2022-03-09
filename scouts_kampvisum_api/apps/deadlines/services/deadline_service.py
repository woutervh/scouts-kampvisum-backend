from typing import List

from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.camps.models import CampYear, CampType

from apps.deadlines.models import (
    DefaultDeadline,
    DeadlineDate,
    Deadline,
    DeadlineItem,
)
from apps.deadlines.services import DefaultDeadlineService, DeadlineItemService

from apps.visums.models import (
    CampVisum,
    SubCategory,
    LinkedSubCategory,
    Check,
    LinkedCheck,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineService:

    default_deadline_service = DefaultDeadlineService()
    deadline_item_service = DeadlineItemService()

    @transaction.atomic
    def create_or_update_deadline(
        self,
        request,
        default_deadline: DefaultDeadline = None,
        visum: CampVisum = None,
        **fields
    ) -> Deadline:
        if not default_deadline or not isinstance(default_deadline, DefaultDeadline):
            default_deadline = (
                self.default_deadline_service.get_or_create_default_deadline(
                    request=request, **fields.get("parent", {})
                )
            )

        instance = Deadline.objects.safe_get(parent=default_deadline, visum=visum)
        if instance:
            return self.update_deadline(
                request=request,
                instance=instance,
                default_deadline=default_deadline,
                **fields
            )
        else:
            return self.create_deadline(
                request=request,
                default_deadline=default_deadline,
                visum=visum,
                **fields
            )

    @transaction.atomic
    def create_deadline(
        self,
        request,
        default_deadline: DefaultDeadline = None,
        visum: CampVisum = None,
        **fields
    ) -> Deadline:
        instance = Deadline()

        instance.parent = default_deadline
        if not (visum and isinstance(visum, CampVisum)):
            visum = CampVisum.objects.safe_get(
                id=fields.get("visum", {}).get("id", None)
            )

        logger.debug(
            "Creating a %s instance for visum with id %s, with name %s",
            "Deadline",
            visum.id,
            instance.parent.name,
        )

        instance.visum = visum
        instance.created_by = request.user

        instance.full_clean()
        instance.save()

        items: List[
            DeadlineItem
        ] = self.deadline_item_service.create_or_update_deadline_items(
            request=request, deadline=instance
        )

        if len(items) == 0:
            raise ValidationError(
                "No DeadlineItem instances found to link to Deadline %s !",
                instance.parent.name,
            )

        for item in items:
            instance.items.add(item)

        return instance

    def get_deadline(self, deadline_id):
        try:
            return Deadline.objects.get(id=deadline_id)
        except Deadline.DoesNotExist:
            logger.error("Deadline with id %s not found", deadline_id)
            raise ValidationError("Deadline with id {} not found".format(deadline_id))

    @transaction.atomic
    def update_deadline(self, request, instance: Deadline, **fields):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        parent: DefaultDeadline = self.default_deadline_service.update_default_deadline(
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
        due_date: DeadlineDate = self.default_deadline_service.update_deadline_date(
            request=request,
            instance=instance.parent.due_date,
            **fields.get("due_date", None)
        )

        return instance

    @transaction.atomic
    def link_to_visum(self, request, visum: CampVisum):
        camp_year: CampYear = visum.camp.year
        camp_types: List[CampType] = visum.camp_types.all()

        default_deadlines: List[DefaultDeadline] = DefaultDeadline.objects.safe_get(
            camp_year=camp_year, camp_types=camp_types
        )

        if len(default_deadlines) == 0:
            raise ValidationError("No deadlines found to link to visum")

        logger.debug(
            "Found %d DefaultDeadline instances with camp year %s and camp types %s",
            len(default_deadlines),
            camp_year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
        )
        for default_deadline in default_deadlines:
            self._link_deadline_to_visum(
                request=request, default_deadline=default_deadline, visum=visum
            )

    def _link_deadline_to_visum(
        self, request, default_deadline: DefaultDeadline, visum: CampVisum
    ):
        logger.debug(
            "Setting up Deadline %s (%s) for visum %s",
            default_deadline.name,
            default_deadline.id,
            visum.id,
        )
        deadline: Deadline = self.create_or_update_deadline(
            request=request, default_deadline=default_deadline, visum=visum
        )

        return deadline

    def _link_sub_categories_to_deadline(
        self, default_deadline: DefaultDeadline, visum: CampVisum, deadline
    ):
        sub_categories: List[SubCategory] = default_deadline.sub_categories.all()
        logger.debug(
            "Found %d SubCategory instances linked to DefaultDeadline %s",
            len(sub_categories),
            default_deadline.name,
        )
        for sub_category in sub_categories:
            logger.trace(
                "SUB CATEGORY: %s (%s), CATEGORY: %s (%s)",
                sub_category.id,
                sub_category.name,
                sub_category.category.id,
                sub_category.category.name,
            )
            linked_sub_category: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
                parent=sub_category, visum=visum, raise_error=True
            )
            logger.trace(
                "FOUND LINKED SUB CATEGORY: %s (%s)",
                linked_sub_category.id,
                linked_sub_category.parent.name,
            )
            deadline.linked_sub_categories.add(linked_sub_category)

    def _link_checks_to_deadline(
        self, default_deadline: DefaultDeadline, visum: CampVisum, deadline
    ):
        checks: List[Check] = default_deadline.checks.all()
        logger.debug(
            "Found %d Check instances linked to DefaultDeadline %s",
            len(checks),
            default_deadline.name,
        )
        for check in checks:
            linked_check: LinkedCheck = LinkedCheck.objects.safe_get(
                parent=check, visum=visum
            )
            if not linked_check:
                raise ValidationError(
                    "Unable to find LinkedCheck with parent Check id {}".format(
                        check.id
                    )
                )
            deadline.linked_checks.add(linked_check)

    def list_for_visum(self, visum: CampVisum) -> List[Deadline]:
        return Deadline.objects.filter(visum=visum)

    def get_visum_deadline(self, deadline: Deadline) -> Deadline:
        return Deadline.objects.get(id=deadline.id)
