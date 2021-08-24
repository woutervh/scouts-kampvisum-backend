import logging
from rest_framework import serializers

from ..models import ScoutsSection
from ..serializers import (
    ScoutsGroupSerializer,
    ScoutsSectionNameSerializer,
)
from apps.groupadmin.api import MemberGender


logger = logging.getLogger(__name__)


class ScoutsSectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSection object
    """
    
    group = ScoutsGroupSerializer()
    name = ScoutsSectionNameSerializer()
    hidden = serializers.BooleanField()
    
    class Meta:
        model = ScoutsSection
        fields = '__all__'


class ScoutsSectionCreationAPISerializer(serializers.Serializer):
    """
    Deserializes ScoutSection JSON data into a ScoutsSectionObject
    """
    
    name = serializers.JSONField()
    
    def validate(self, data):
        if data['name'] is None:
            raise serializers.ValidationError("Section name can't be null")

        return data


class ScoutsSectionAPISerializer(serializers.ListSerializer):
    """
    Deserializes a JSON ScoutsSection from the frontend (no serialization).
    """
    
    child = serializers.UUIDField()

