from rest_framework import serializers
from .models import ScoutsSectionName, ScoutsSection
from ..groups.serializers import ScoutsGroupTypeSerializer


class ScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """
    
    name = serializers.CharField(max_length=128)
    
    class Meta:
        model = ScoutsSectionName
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

