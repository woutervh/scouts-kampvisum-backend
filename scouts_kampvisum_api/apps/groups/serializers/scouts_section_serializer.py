import logging

from rest_framework import serializers

from apps.groups.models import ScoutsSection
from apps.groups.serializers import (
    ScoutsGroupTypeSerializer,
    ScoutsSectionNameSerializer,
)


logger = logging.getLogger(__name__)


class ScoutsSectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in camp visum views.
    """

    # group_type = ScoutsGroupTypeSerializer()
    name = ScoutsSectionNameSerializer()
    hidden = serializers.BooleanField(default=False)

    class Meta:
        model = ScoutsSection
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        if isinstance(data, str):
            return ScoutsSection.objects.safe_get(id=data, raise_error=True)

        data = super().to_internal_value(data)

        # logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

    def validate(self, data: dict) -> ScoutsSection:
        if not data:
            return None

        if isinstance(data, ScoutsSection):
            return data

        if not data.get("id"):
            if not data.get("group_admin_id") and data.get("name"):
                raise serializers.ValidationError(
                    "A ScoutsSection can only be identified by either a uuid or the combination of a name and the group's group admin id"
                )

        return data
