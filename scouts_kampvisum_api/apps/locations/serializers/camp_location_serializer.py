from rest_framework import serializers

from apps.locations.models import CampLocation


import logging

logger = logging.getLogger(__name__)


class CampLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampLocation
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        id = data.get("id", None)
        data = super().to_internal_value(data)
        data["id"] = id

        return data
