import logging
from rest_framework import serializers

from .models import ScoutsCamp
from apps.scouts_groups.api.sections.serializers import (
    ScoutsSectionSerializer
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

