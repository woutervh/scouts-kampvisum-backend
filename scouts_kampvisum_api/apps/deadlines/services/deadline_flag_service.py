from django.db import transaction

from apps.deadlines.models import Deadline, DefaultDeadlineFlag, DeadlineFlag
from apps.deadlines.services import DefaultDeadlineFlagService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineFlagService:

    default_deadline_flag_service = DefaultDeadlineFlagService()

    @transaction.atomic
    def get_or_create_deadline_flag(
        self, request, deadline: Deadline, default_deadline_flag: DefaultDeadlineFlag
    ) -> DeadlineFlag:
        instance = DeadlineFlag.objects.safe_get(
            parent=default_deadline_flag, deadline=deadline
        )
        if instance:
            return instance

        default_deadline_flag = (
            self.default_deadline_flag_service.get_or_create_default_flag(
                instance=default_deadline_flag,
                **{
                    "name": default_deadline_flag.name,
                    "label": default_deadline_flag.label,
                    "index": default_deadline_flag.index,
                    "flag": default_deadline_flag.flag,
                },
            )
        )

        instance = DeadlineFlag()

        instance.parent = default_deadline_flag
        instance.deadline = deadline
        instance.flag = default_deadline_flag.flag

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update_deadline_flag(
        self, request, instance: DeadlineFlag, **data
    ) -> DeadlineFlag:
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        instance.flag = data.get("flag", instance.flag)
        instance.updated_by = request.user

        instance.full_clean()
        instance.save()

        return instance
