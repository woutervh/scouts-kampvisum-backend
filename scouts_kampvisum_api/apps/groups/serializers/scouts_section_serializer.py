import logging
from rest_framework import serializers

from apps.groups.models import ScoutsSection
from apps.groups.serializers import (
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

    group = AbstractScoutsGroupSerializerField(source="group_admin_id")
    name = ScoutsSectionNameSerializer()
    hidden = serializers.BooleanField()

    class Meta:
        model = ScoutsSection
        fields = "__all__"


class ScoutsSectionAPISerializer(FlattenSerializerMixin, serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in camp visum views.
    """

    class Meta:
        model = ScoutsSection
        fields = ["uuid"]
        flatten = [("name", ScoutsSectionNameAPISerializer)]


class ScoutsSectionCreationAPISerializer(serializers.Serializer):
    """
    Deserializes ScoutSection JSON data into a SectionObject.
    """

    name = serializers.JSONField()

    def validate(self, data):
        if data["name"] is None:
            raise serializers.ValidationError("Section name can't be null")

        return data
