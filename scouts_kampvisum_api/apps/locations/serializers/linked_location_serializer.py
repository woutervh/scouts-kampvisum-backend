import logging

from rest_framework import serializers

from apps.locations.models import LinkedLocation
from apps.locations.serializers import CampLocationSerializer


logger = logging.getLogger(__name__)


class LinkedLocationSerializer(serializers.ModelSerializer):

    locations = CampLocationSerializer(many=True)

    class Meta:
        model = LinkedLocation
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("LINKED LOCATION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        id = data.get("id", None)
        if id and len(data.keys()) == 1:
            instance = LinkedLocation.objects.safe_get(id=id)
            if instance:
                return instance

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: LinkedLocation) -> dict:
        data = super().to_representation(obj)

        logger.debug("LINKED LOCATION TO_REPRESENTATION: %s", data)

        return data
