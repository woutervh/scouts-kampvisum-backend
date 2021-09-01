from rest_framework import serializers

from ..models import CategorySet
from ..serializers import (
    CategorySetPrioritySerializer,
    CategorySerializer,
)
from apps.groups.api.serializers import GroupTypeSerializer
from apps.camps.serializers import CampYearSerializer


class CategorySetSerializer(serializers.ModelSerializer):

    priority = CategorySetPrioritySerializer()
    type = GroupTypeSerializer()
    categories = CategorySerializer(many=True)
    camp_year = CampYearSerializer()
    is_default = serializers.BooleanField(default=False)

    class Meta:
        model = CategorySet
        fields = '__all__'
