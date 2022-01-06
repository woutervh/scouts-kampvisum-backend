import logging, uuid
from rest_framework import serializers

from apps.groups.models import ScoutsSection
from apps.groups.serializers import (
    ScoutsGroupTypeSerializer,
    ScoutsSectionNameSerializer,
    ScoutsSectionNameAPISerializer,
)

from scouts_auth.groupadmin.serializers.fields import AbstractScoutsGroupSerializerField
from scouts_auth.inuits.mixins import FlattenSerializerMixin


logger = logging.getLogger(__name__)


class ScoutsSectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSection object
    """

    # group = AbstractScoutsGroupSerializerField(source="group_admin_id")
    group_type = ScoutsGroupTypeSerializer()
    name = ScoutsSectionNameSerializer()
    hidden = serializers.BooleanField()

    class Meta:
        model = ScoutsSection
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        group_type = data.get("group_type", None)
        if group_type:
            data["group_type"] = {"group_type": group_type}

        name = data.get("name", None)
        if name:
            data["name"] = {"name": name}

        logger.debug("SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data = super().to_internal_value(data)

        logger.debug("SECTION SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data


class ScoutsSectionAPISerializer(FlattenSerializerMixin, serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in camp visum views.
    """

    class Meta:
        model = ScoutsSection
        fields = ["id"]
        flatten = [("name", ScoutsSectionNameAPISerializer)]

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("SERIALIZER DATA: %s (%s)", data, type(data).__name__)

        if isinstance(data, str):
            id = data
            data = {}
            data["id"] = data

        return super().to_internal_value(data)

    def validate(self, data: dict) -> ScoutsSection:
        if not data:
            return None

        if not data.get("id"):
            if not data.get("group_admin_id") and data.get("name"):
                raise serializers.ValidationError(
                    "A ScoutsSection can only be identified by either a uuid or the combination of a name and the groups group admin id"
                )

        return data


class ScoutsSectionCreationAPISerializer(serializers.Serializer):
    """
    Deserializes ScoutSection JSON data into a SectionObject.
    """

    name = serializers.JSONField()

    def validate(self, data):
        if data["name"] is None:
            raise serializers.ValidationError("Section name can't be null")

        return data
