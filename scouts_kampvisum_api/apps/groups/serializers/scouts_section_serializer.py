from rest_framework import serializers

from apps.groups.models import ScoutsSection
from apps.groups.serializers import (
    ScoutsGroupTypeSerializer,
    ScoutsSectionNameSerializer,
)

from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in camp visum views.
    """

    # group_type = ScoutsGroupTypeSerializer()
    group = ScoutsGroupSerializer()
    name = ScoutsSectionNameSerializer()
    hidden = serializers.BooleanField(default=False)

    class Meta:
        model = ScoutsSection
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        if isinstance(data, str):
            return ScoutsSection.objects.safe_get(id=data, raise_error=True)

        group = data.get("group", None)
        group_group_admin_id = data.get("group_group_admin_id", None)

        if not group and group_group_admin_id:
            data["group"] = {"group_admin_id": group_group_admin_id}

        data = super().to_internal_value(data)

        # logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

    def validate(self, data: dict) -> ScoutsSection:
        if not data:
            return None

        if isinstance(data, ScoutsSection):
            return data

        id = data.get("id")
        group = data.get("group", None)
        group_admin_id = (
            group.group_admin_id if group else data.get("group_group_admin_id", None)
        )

        if not id:
            if not group_admin_id and data.get("name"):
                raise serializers.ValidationError(
                    "A ScoutsSection can only be identified by either a uuid or the combination of a name and the group's group admin id"
                )

        return data
