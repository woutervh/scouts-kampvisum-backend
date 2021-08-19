import logging
from rest_framework import serializers

from .models import ScoutsSectionName, ScoutsDefaultSectionName, ScoutsSection
from ..groups.serializers import ScoutsGroupTypeSerializer
from ..groups.serializers import ScoutsGroupSerializer
from apps.groupadmin.api import MemberGender


logger = logging.getLogger(__name__)


class ScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """
    
    name = serializers.CharField(max_length=128)
    gender = serializers.ChoiceField(
        choices = MemberGender, default=MemberGender.MIXED)
    
    class Meta:
        model = ScoutsSectionName
        fields = '__all__'


class ScoutsDefaultSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutDefaultSectionName object
    """
    
    group_type = ScoutsGroupTypeSerializer
    name = ScoutsSectionNameSerializer
    
    class Meta:
        model = ScoutsDefaultSectionName
        fields = '__all__'


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

