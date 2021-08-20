import logging
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from .models import ScoutsCamp
from apps.scouts_groups.api.sections.models import ScoutsSection
from apps.scouts_groups.api.sections.serializers import (
    ScoutsSectionSerializer, ScoutsSectionAPISerializer
)
from inuits.serializers import OptionalDateField


logger = logging.getLogger(__name__)


class ScoutsCampSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsCamp object.
    """
    
    name = serializers.CharField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()
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


class ScoutsCampAPISerializer(serializers.ModelSerializer):
    """
    Deserializes a JSON ScoutsCamp from the frontend (no serialization).
    """
    
    name = serializers.CharField()
    #start_date = serializers.DateField(required=False)
    #end_date = serializers.DateField(required=False)
    start_date = OptionalDateField()
    end_date = OptionalDateField()
    # List of ScoutsSection uuid's
    sections = ScoutsSectionAPISerializer()

    class Meta:
        model = ScoutsCamp
        fields = '__all__'
    
    def validate(self, data):
        logger.debug('SCOUTSCAMP API DATA: %s', data)

        if not data.get('name'):
            raise ValidationError(
                "A ScoutsCamp must have a name")
        
        if not data.get('sections'):
            raise ValidationError(
                "A ScoutsCamp must have at least 1 ScoutsSection attached"
            )
        else:
            for section_uuid in data.get('sections'):
                try:
                    ScoutsSection.objects.get(uuid=section_uuid)
                except ObjectDoesNotExist:
                    raise ValidationError(
                        "Invalid UUID. No ScoutsSection with that UUID: " +
                        str(section_uuid)
                    )
        
        # if data.get('start_date') and data.get('start_date') < timezone.now():
        #     raise ValidationError("The camp start date can't be in the past")

        return data

