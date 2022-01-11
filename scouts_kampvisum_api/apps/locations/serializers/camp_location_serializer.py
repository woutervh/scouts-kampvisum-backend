import logging

from rest_framework import serializers

from apps.locations.models import CampLocation


logger = logging.getLogger(__name__)


class CampLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampLocation
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("CAMP LOCATION SERIALIZER DATA: %s", data)
        id = data.get("id", None)
        data = super().to_internal_value(data)
        logger.debug("CAMP LOCATION SERIALIZER DATA: %s", data)
        data["id"] = id
        logger.debug("CAMP LOCATION SERIALIZER DATA: %s", data)

        return data
