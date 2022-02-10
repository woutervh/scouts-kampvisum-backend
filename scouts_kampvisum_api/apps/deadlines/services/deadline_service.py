import logging
from typing import List

from django.http import Http404
from django.utils import timezone

from apps.deadlines.models import (
    DefaultDeadline,
    Deadline,
    LinkedSubCategoryDeadline,
    LinkedCheckDeadline,
    DeadlineDependentDeadline,
)
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.services import DeadlineDateService

from apps.visums.models import CampVisum, LinkedSubCategory, LinkedCheck


logger = logging.getLogger(__name__)


class DeadlineService:

    deadline_date_service = DeadlineDateService()

    def create_deadline(self, request, **fields) -> Deadline:
        instance = Deadline()

        instance.visum = CampVisum.objects.safe_get(
            id=fields.get("visum", {}).get("id", None)
        )
        instance.deadline_type = DeadlineType.DEADLINE
        instance.name = fields.get("name", None)
        instance.label = fields.get("label", None)
        instance.description = fields.get("description", None)
        instance.explanation = fields.get("explanation", None)
        instance.is_important = fields.get("is_important", False)
        instance.due_date = self.deadline_date_service.create_deadline_date(
            request, **fields.get("due_date", None)
        )
        instance.created_by = request.user

        instance.full_clean()
        instance.save()

        return instance

    def get_deadline(self, deadline_id):
        try:
            return Deadline.objects.get(id=deadline_id)
        except Deadline.DoesNotExist:
            logger.error("Deadline with id %s not found", deadline_id)
            raise Http404

    def update_deadline(self, request, instance: Deadline, **fields):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        instance.name = fields.get("name", instance.name)
        instance.label = fields.get("label", instance.label)
        instance.description = fields.get("description", instance.description)
        instance.explanation = fields.get("explanation", instance.description)
        instance.is_important = fields.get("is_important", instance.is_important)
        instance.due_date = self.deadline_date_service.update_deadline_date(
            request, instance.due_date, **fields.get("due_date", None)
        )
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        return instance

    def create_sub_category_deadline(
        self, request, **fields
    ) -> LinkedSubCategoryDeadline:
        instance = LinkedSubCategoryDeadline()

        instance.visum = CampVisum.objects.safe_get(
            id=fields.get("visum", {}).get("id", None)
        )
        instance.deadline_type = DeadlineType.LINKED_SUB_CATEGORY
        instance.name = fields.get("name", None)
        instance.label = fields.get("label", None)
        instance.description = fields.get("description", None)
        instance.explanation = fields.get("explanation", None)
        instance.is_important = fields.get("is_important", False)
        instance.due_date = self.deadline_date_service.create_deadline_date(
            request, **fields.get("due_date", None)
        )
        instance.linked_sub_category = LinkedSubCategory.objects.safe_get(
            id=fields.get("linked_sub_category", {}).get("id", None)
        )
        instance.created_by = request.user

        instance.full_clean()
        instance.save()

        return instance

    def get_sub_category_deadline(self, deadline_id):
        try:
            return LinkedSubCategoryDeadline.objects.get(deadline_ptr=deadline_id)
        except LinkedSubCategoryDeadline.DoesNotExist:
            raise Http404

    def create_check_deadline(self, request, **fields) -> LinkedCheckDeadline:
        instance = LinkedCheckDeadline()

        instance.visum = CampVisum.objects.safe_get(
            id=fields.get("visum", {}).get("id", None)
        )
        instance.deadline_type = DeadlineType.LINKED_CHECK
        instance.name = fields.get("name", None)
        instance.label = fields.get("label", None)
        instance.description = fields.get("description", None)
        instance.explanation = fields.get("explanation", None)
        instance.is_important = fields.get("is_important", False)
        instance.due_date = self.deadline_date_service.create_deadline_date(
            request, **fields.get("due_date", None)
        )
        instance.linked_check = LinkedCheck.objects.safe_get(
            id=fields.get("linked_check", {}).get("id", None)
        )
        instance.created_by = request.user

        instance.full_clean()
        instance.save()

        return instance

    def get_check_deadline(self, deadline_id):
        try:
            return LinkedCheckDeadline.objects.get(deadline_ptr=deadline_id)
        except LinkedCheckDeadline.DoesNotExist:
            raise Http404

    def update_check_deadline(self, instance: LinkedCheckDeadline, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_deadline_dependent_deadline(self, deadline_id):
        try:
            return DeadlineDependentDeadline.objects.get(linkedcheck_ptr=deadline_id)
        except DeadlineDependentDeadline.DoesNotExist:
            raise Http404

    def update_deadline_dependent_deadline(
        self, instance: DeadlineDependentDeadline, **data
    ):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def list_for_visum(self, visum) -> List[DefaultDeadline]:
        deadlines: List[DefaultDeadline] = DefaultDeadline.objects.filter(
            deadline__visum=visum
        )
        results = list()

        for deadline in deadlines:
            if deadline.is_deadline():
                results.append(Deadline.objects.get(defaultdeadline_ptr=deadline.id))
            elif deadline.is_sub_category_deadline():
                results.append(
                    LinkedSubCategoryDeadline.objects.get(
                        defaultdeadline_ptr=deadline.id
                    )
                )
            elif deadline.is_check_deadline():
                results.append(
                    LinkedCheckDeadline.objects.get(defaultdeadline_ptr=deadline.id)
                )

        return results
