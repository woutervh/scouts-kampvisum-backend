from rest_framework import serializers

from apps.groups.models import ScoutsSection
from apps.groups.serializers import ScoutsGroupTypeSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in camp visum views.
    """

    hidden = serializers.BooleanField(default=False)

    class Meta:
        model = ScoutsSection
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        if isinstance(data, str):
            return ScoutsSection.objects.safe_get(id=data, raise_error=True)

        group_admin_id = data.get("group_group_admin_id", data.get(
            "group", data.get("auth", None)))
        if not group_admin_id:
            raise ValidationError(
                f"[{self.context['request'].user.username}] Invalid group admin id, not found as param or in payload: 'group', 'group_group_admin_id' or 'auth'")
        group = self.context['request'].user.get_scouts_group(
            group_admin_id=group_admin_id, raise_error=True)

        data["group"] = group.group_admin_id
        name = data.get("name", {})
        data["name"] = name.get("name")
        data["gender"] = name.get("gender")
        data["age_group"] = name.get("age_group")

        data = super().to_internal_value(data)

        # logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

    def to_representation(self, obj: ScoutsSection) -> dict:
        section_name = {
            "name": obj.name,
            "gender": obj.gender,
            "age_group": obj.age_group,
        }

        data = super().to_representation(obj)

        data["name"] = section_name

        return data

    def validate(self, data: dict) -> ScoutsSection:
        if not data:
            return None

        if isinstance(data, ScoutsSection):
            return data

        pk = data.get("id")
        group_admin_id = data.get("group_group_admin_id", data.get(
            "group", data.get("auth", None)))

        if group_admin_id:
            self.context['request'].user.get_scouts_group(
                group_admin_id=group_admin_id, raise_error=True)
            data["group"] = group_admin_id

        if not pk and not (group_admin_id and data.get("name")):
            raise serializers.ValidationError(
                "A ScoutsSection can only be identified by either a uuid or the combination of a name and the group's group admin id"
            )

        return ScoutsSection(**data)
