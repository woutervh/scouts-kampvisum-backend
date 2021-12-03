import logging
from rest_framework import serializers

from ..models import DefaultSectionName
from ..serializers import (
    GroupTypeSerializer,
    SectionNameSerializer,
)


logger = logging.getLogger(__name__)


class DefaultSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutDefaultSectionName object
    """

    group_type = GroupTypeSerializer
    name = SectionNameSerializer

    class Meta:
        model = DefaultSectionName
        fields = "__all__"
