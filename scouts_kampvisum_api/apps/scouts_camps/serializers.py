import logging
from rest_framework import serializers

from .models import ScoutsCamp
from apps.scouts_groups.api.sections.models import ScoutsSection
from apps.scouts_groups.api.sections.serializers import (
    ScoutsSectionSerializer
)


logger = logging.getLogger(__name__)


class ScoutsCampSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsCamp object.
    """
    
    name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    sections = ScoutsSectionSerializer(many=True)
    
    class Meta:
        model = ScoutsCamp
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsCamp:
        return ScoutsCamp(**validated_data)
    
    def update(self, instance, validated_data) -> ScoutsCamp:
        instance.name = validated_data.get(
            'type', instance.type)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date)
        instance.end_date = validated_data.get(
            'end_date', instance.end_date)
        instance.sections = ScoutsSectionSerializer(many=True)
        
        return type


class ScoutsCampAPISerializer(serializers.Serializer):
    """
    Deserializes a JSON ScoutsCamp from the frontend (no serialization).
    """
    
    name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    # List of ScoutsSection uuid's
    sections = serializers.ListField(
        child=serializers.UUIDField()
    )

    class Meta:
        model = ScoutsCamp
        fields = '__all__'
    
    def validate(self, data):
        logger.debug('DATA: %s', data)
        return data
    
    def create(self, validated_data):
        logger.debug('VALIDATED DATA: %s', validated_data)
        uuids = validated_data.get('sections')
        #logger.debug('UUIDS: %s', uuids)
        sections = ScoutsSection.objects.filter(uuid_in=uuids)
        validated_data['sections'] = sections

        return validated_data

