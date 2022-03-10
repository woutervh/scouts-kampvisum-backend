from django.db import transaction
from django.core.exceptions import ValidationError

from apps.deadlines.models import DeadlineItem, DeadlineFlag


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineFlagService:
    @transaction.atomic
    def get_or_create_flag(
        self,
        instance: DeadlineFlag = None,
        deadline_item: DeadlineItem = None,
        **fields
    ) -> DeadlineFlag:
        if instance and isinstance(instance, DeadlineFlag):
            instance = DeadlineFlag.objects.safe_get(id=instance.id)
            if instance:
                return instance

        name = fields.get("name", None)
        if not name:
            raise ValidationError("A deadline flag requires a name, None given")

        instance = DeadlineFlag.objects.safe_get(deadline_item=deadline_item, name=name)
        if instance:
            return self.update_flag(instance=instance, **fields)

        instance = DeadlineFlag()

        instance.name = fields.get("name", "")
        instance.label = fields.get("label", instance.name)
        instance.index = fields.get("index", 0)
        instance.flag = fields.get("flag", False)

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update_flag(self, instance: DeadlineFlag, **fields) -> DeadlineFlag:
        instance.name = fields.get("name", instance.name)
        instance.label = fields.get("label", instance.label)
        instance.index = fields.get("index", instance.index)
        instance.flag = fields.get("flag", instance.flag)

        instance.full_clean()
        instance.save()

        return instance
