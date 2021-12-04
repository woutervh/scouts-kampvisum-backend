import logging
from rest_framework import serializers

from apps.groups.models import DefaultScoutsSectionName
from apps.groups.serializers import (
    ScoutsGroupTypeSerializer,
    ScoutsSectionNameSerializer,
)


logger = logging.getLogger(__name__)


class DefaultScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutDefaultSectionName object
    """

    group_type = ScoutsGroupTypeSerializer()
    name = ScoutsSectionNameSerializer()

    class Meta:
        model = DefaultScoutsSectionName
        fields = "__all__"
