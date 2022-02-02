import logging
from rest_framework import serializers

from apps.groups.models import ScoutsSection
from apps.groups.serializers import (
    ScoutsGroupTypeSerializer,
    ScoutsSectionNameSerializer,
)

from scouts_auth.groupadmin.scouts import AgeGroup
from scouts_auth.inuits.models.enums import Gender


logger = logging.getLogger(__name__)


class ScoutsSectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in camp visum views.
    """

    group_type = ScoutsGroupTypeSerializer()
    name = ScoutsSectionNameSerializer()
    hidden = serializers.BooleanField(default=False)

    class Meta:
        model = ScoutsSection
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        if isinstance(data, str):
            instance = ScoutsSection.objects.safe_get(id=data)
            logger.debug("SCOUTS SECTION SERIALIZER TO_INTERNAL_VALUE: %s", instance)

            return instance

        group_type = data.get("group_type", None)
        if group_type:
            data["group_type"] = {"group_type": group_type}

        name = data.get("name", None)
        if name:
            if isinstance(name, dict):
                section_name_name = name.get("name")
                section_name_gender = name.get("gender", Gender.MIXED)
                section_name_age_group = name.get(
                    "age_group", AgeGroup.AGE_GROUP_UNKNOWN
                )
                data["name"] = {
                    "name": section_name_name,
                    "gender": section_name_gender,
                    "age_group": section_name_age_group,
                }
            else:
                data["name"] = {"name": name}

        logger.debug("SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data = super().to_internal_value(data)

        logger.debug("SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

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
