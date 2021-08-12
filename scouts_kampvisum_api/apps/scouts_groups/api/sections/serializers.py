from rest_framework import serializers
from .models import ScoutsSectionName, DefaultScoutsSectionName, ScoutsSection
from ..groups.serializers import ScoutsGroupTypeSerializer


class ScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """
    
    name = serializers.CharField(max_length=128)
    
    class Meta:
        model = ScoutsSectionName
        fields = '__all__'


class DefaultScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a DefaultScoutSectionName object
    """
    
    name = ScoutsSectionNameSerializer()
    type = ScoutsGroupTypeSerializer()
    
    class Meta:
        model = DefaultScoutsSectionName
        fields = '__all__'


class ScoutsSectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSection object
    """
    
    group = ScoutsSection
    name = serializers.CharField(max_length=128)
    
    class Meta:
        model = ScoutsSection
        fields = '__all__'

