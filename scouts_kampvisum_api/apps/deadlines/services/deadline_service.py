import logging, uuid

from django.http import Http404

from apps.deadlines.models import (Deadline, SubCategoryDeadline, CheckDeadline, DeadlineDependentDeadline)


logger = logging.getLogger(__name__)


class DeadlineService:
    
    def create_deadline(self, **fields) -> Deadline:
        instance = Deadline()
        
        instance.visum = fields.get("visum", None)
        instance.name = fields.get("name", None)
        instance.label = fields.get("label", None)
        instance.description = fields.get("description", None)
        instance.explanation = fields.get("explanation", None)
        instance.is_important = fields.get("is_important", None)
        instance.due_date = fields.get("due_date", None)

    def get_deadline(self, deadline_id):
        try:
            return Deadline.objects.get(linkedcheck_ptr=deadline_id)
        except Deadline.DoesNotExist:
            logger.error("Deadline with id %s not found", deadline_id)
            raise Http404
        

    def update_deadline(self, instance: Deadline, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_sub_category_deadline(self, deadline_id):
        try:
            return SubCategoryDeadline.objects.get(linkedcheck_ptr=deadline_id)
        except SubCategoryDeadline.DoesNotExist:
            raise Http404

    def update_check_deadline(self, instance: CheckDeadline, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_check_deadline(self, deadline_id):
        try:
            return CheckDeadline.objects.get(linkedcheck_ptr=deadline_id)
        except CheckDeadline.DoesNotExist:
            raise Http404

    def update_check_deadline(self, instance: CheckDeadline, **data):
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

    def update_deadline_dependent_deadline(self, instance: DeadlineDependentDeadline, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance