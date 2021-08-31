import logging
from rest_framework import serializers

from ..models import Section
from ..serializers import (
    GroupSerializer,
    SectionNameSerializer,
    SectionNameAPISerializer,
)
from inuits.mixins import FlattenMixin


logger = logging.getLogger(__name__)


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSection object
    """

    group = GroupSerializer()
    name = SectionNameSerializer()
    hidden = serializers.BooleanField()

    class Meta:
        model = Section
        fields = '__all__'


class SectionListSerializer(FlattenMixin, serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in list views.
    """

    class Meta:
        model = Section
        fields = ['name', 'uuid']
        flatten = [('name', SectionNameAPISerializer)]


class SectionCreationAPISerializer(serializers.Serializer):
    """
    Deserializes ScoutSection JSON data into a SectionObject
    """

    name = serializers.JSONField()

    def validate(self, data):
        if data['name'] is None:
            raise serializers.ValidationError("Section name can't be null")

        return data


class SectionAPISerializer(serializers.ListSerializer):
    """
    Deserializes a JSON Section from the frontend (no serialization).
    """

    child = serializers.UUIDField()
