from apps.deadlines.models import LinkedDeadline
from apps.deadlines.serializers import (
    LinkedDeadlineSerializer,
    DeadlineSerializer,
    LinkedDeadlineItemSerializer,
)

from apps.visums.models.enums import CheckState


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class VisumDeadlineSerializer(LinkedDeadlineSerializer):
    def to_representation(self, obj: LinkedDeadline) -> dict:
        data = super().to_representation(obj)

        items = data.get("items", [])

        data["state"] = CheckState.CHECKED
        for item in items:
            if CheckState.is_unchecked(item.get("state", CheckState.UNCHECKED)):
                data["state"] = CheckState.UNCHECKED
                break

        return data
