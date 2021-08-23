import logging
from rest_framework import serializers

from ..models import ScoutsDefaultSectionName
from ..serializers import (
    ScoutsGroupTypeSerializer,
    ScoutsSectionNameSerializer,
)


logger = logging.getLogger(__name__)


class ScoutsDefaultSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutDefaultSectionName object
    """
    
    group_type = ScoutsGroupTypeSerializer
    name = ScoutsSectionNameSerializer
    
    class Meta:
        model = ScoutsDefaultSectionName
        fields = '__all__'

