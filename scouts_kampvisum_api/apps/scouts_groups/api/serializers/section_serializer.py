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


class ScoutsSectionAPISerializer(serializers.ListSerializer):
    """
    Deserializes a JSON ScoutsSection from the frontend (no serialization).
    """
    
    child = serializers.UUIDField()

    def validate(self, data):
        logger.debug('SECTION DATA: %s', data)
        return data

    def save(self, data):
        logger.debug('SECTION DATA: %s', data)
        #ScoutsSection.objects.filter(uuid_in=uuids)


