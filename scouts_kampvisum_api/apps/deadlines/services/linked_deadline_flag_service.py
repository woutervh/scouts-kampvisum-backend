from django.db import transaction

from apps.deadlines.models import LinkedDeadline, DeadlineFlag, LinkedDeadlineFlag
from apps.deadlines.services import DeadlineFlagService

from apps.visums.services import ChangeHandlerService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineFlagService:

    deadline_flag_service = DeadlineFlagService()
    change_handler_service = ChangeHandlerService()

    def notify_change(
        self, request, instance: LinkedDeadlineFlag, data_changed: bool = False
    ):
        if data_changed and instance.parent.has_change_handlers():
            self.change_handler_service.handle_changes(
                change_handlers=instance.parent.change_handlers,
                request=request,
                instance=instance,
            )

        return instance

    @transaction.atomic
    def get_or_create_linked_deadline_flag(
        self, request, linked_deadline: LinkedDeadline, deadline_flag: DeadlineFlag
    ) -> LinkedDeadlineFlag:
        instance = LinkedDeadlineFlag.objects.safe_get(
            parent=deadline_flag, linked_deadline=linked_deadline
        )
        if instance:
            return instance

        deadline_flag = self.deadline_flag_service.get_or_create_flag(
            instance=deadline_flag,
            **{
                "name": deadline_flag.name,
                "label": deadline_flag.label,
                "index": deadline_flag.index,
                "flag": deadline_flag.flag,
            },
        )

        instance = LinkedDeadlineFlag()

        instance.parent = deadline_flag
        instance.flag = deadline_flag.flag

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update_linked_deadline_flag(
        self, request, instance: LinkedDeadlineFlag, **data
    ) -> LinkedDeadlineFlag:
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        old_value = instance.flag

        instance.flag = data.get("flag", instance.flag)
        instance.updated_by = request.user

        instance.full_clean()
        instance.save()

        return self.notify_change(
            request=request,
            instance=instance,
            data_changed=data.get("flag", None) is not None
            and data.get("flag") != old_value,
        )
