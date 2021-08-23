import logging
from rest_framework import serializers

from ..models import ScoutsSectionName
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

