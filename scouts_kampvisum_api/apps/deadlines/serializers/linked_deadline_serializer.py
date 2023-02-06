from rest_framework import serializers

from apps.deadlines.models import LinkedDeadline
from apps.deadlines.serializers import DeadlineSerializer, LinkedDeadlineItemSerializer

from apps.visums.serializers import CampVisumSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineSerializer(serializers.ModelSerializer):

    parent = DeadlineSerializer(required=False)
    visum = CampVisumSerializer(required=False)
    items = LinkedDeadlineItemSerializer(many=True)

    class Meta:
        model = LinkedDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("LINKED DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        parent = data.pop("parent", {})

        data["items"] = []

        # logger.debug("LINKED DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)
        data = super().to_internal_value(data)
        # logger.debug("LINKED DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data["parent"] = parent
        # logger.debug("LINKED DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

    def to_representation(self, obj: LinkedDeadline) -> dict:
        # logger.debug("LINKED DEADLINE SERIALIZER TO_REPRESENTATION: %s", obj)

        visum = obj.visum.id
        group = obj.visum.group
        obj.visum = None

        data = super().to_representation(obj)

        data["visum"] = visum
        data["group"] = group

        return data


class LinkedDeadlineInputSerializer(serializers.Serializer):

    parent = DeadlineSerializer(required=False)
    visum = CampVisumSerializer(required=False)
    items = LinkedDeadlineItemSerializer(many=True)

    class Meta:
        model = LinkedDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data["items"] = []

        data = super().to_internal_value(data)

        return data
