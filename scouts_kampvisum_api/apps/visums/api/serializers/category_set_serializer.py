from rest_framework import serializers

from ..models import CampVisumCategorySet
from ..serializers import (
    CampVisumCategorySetPrioritySerializer,
    CampVisumCategorySerializer,
)
from apps.groups.api.serializers import GroupTypeSerializer
from apps.camps.serializers import CampYearSerializer


class CampVisumCategorySetSerializer(serializers.ModelSerializer):

    priority = CampVisumCategorySetPrioritySerializer()
    type = GroupTypeSerializer()
    categories = CampVisumCategorySerializer(many=True)
    camp_year = CampYearSerializer()
    is_default = serializers.BooleanField(default=False)

    class Meta:
        model = CampVisumCategorySet
        fields = '__all__'
