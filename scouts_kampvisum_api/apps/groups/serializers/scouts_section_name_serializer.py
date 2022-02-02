import logging

from rest_framework import serializers

from apps.groups.models import ScoutsSectionName


logger = logging.getLogger(__name__)


class ScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """

    class Meta:
        model = ScoutsSectionName
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)
        # logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data = super().to_internal_value(data)
        # logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data
