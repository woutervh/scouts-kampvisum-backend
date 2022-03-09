from rest_framework import serializers

from apps.deadlines.models import Deadline
from apps.deadlines.serializers import DefaultDeadlineSerializer, DeadlineItemSerializer

from apps.visums.serializers import CampVisumSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineSerializer(serializers.ModelSerializer):

    parent = DefaultDeadlineSerializer(required=False)
    visum = CampVisumSerializer(required=False)
    items = DeadlineItemSerializer(many=True)

    class Meta:
        model = Deadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        parent = data.pop("parent", {})

        data["items"] = []

        logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)
        data = super().to_internal_value(data)
        logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data["parent"] = parent
        logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

    def to_representation(self, obj: Deadline) -> dict:
        logger.debug("DEADLINE SERIALIZER TO_REPRESENTATION: %s", obj)

        visum = obj.visum.id
        obj.visum = None

        data = super().to_representation(obj)

        data["visum"] = visum

        return data


class DeadlineInputSerializer(serializers.Serializer):

    parent = DefaultDeadlineSerializer(required=False)
    visum = CampVisumSerializer(required=False)
    items = DeadlineItemSerializer(many=True)

    class Meta:
        model = Deadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data["items"] = []

        data = super().to_internal_value(data)

        return data
